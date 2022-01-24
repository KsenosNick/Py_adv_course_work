
from random import randrange
import vk_api
from sqlalchemy import desc, or_, text
from vk_api import VkTools
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime
import time

from database.db_classes import Session, Base, engine, VKUser, Photo


class VKinder:
    url = 'https://api.vk.com/method/'

    def __init__(self, token_group, token_user, version):

        self.vk_bot = vk_api.VkApi(token=token_group)
        self.vk_user = vk_api.VkApi(token=token_user)
        self.api_bot = self.vk_bot.get_api()
        self.api_user = self.vk_user.get_api()
        self.longpoll = VkLongPoll(self.vk_bot)
        self.city = ''

        self.params_bot = {
            'access_token': token_group,
            'v': version,
        }

        self.params_user = {
            'access_token': token_user,
            'v': version,
        }

    get_user_data_params = {
        'fields': 'city, sex, relation, bdate, common_count, is_no_index',
    }

    search_users_data_params = {
        'method': 'users.search',
        'max_count': 100,
        'values': {
            'city': '',
            'age_from': 0,
            'age_to': 0,
            'fields': 'city, sex, relation, bdate',
        },
    }

    get_photos_params = {
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1
    }

    def write_msg(self, user_id, message):
        self.vk_bot.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})

    def longpoll_request(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    return request

    def get_age_from_birth_date(self, birth_date):
        try:
            bdate_obj = datetime.strptime(birth_date, '%d.%m.%Y')
            date_current = datetime.now()
            age = int((date_current - bdate_obj).days / 365.2425)
        except Exception:
            age = 0
        return age

    def get_user_data(self, user_id):
        user_data = self.api_user.users.get(user_id=user_id, **self.get_user_data_params)
        if not user_data[0].get('relation'):
            user_data[0]['relation'] = 0
        if not user_data[0].get('bdate'):
            user_data[0]['bdate'] = ''
        return user_data

    def search_users(self, user_data):
        if not user_data[0].get('city'):
            self.write_msg(user_data[0]['user_id'], "Необходимо указать город в профиле. "
                                                    "Выберите город и повторите запрос")
        age = self.get_age_from_birth_date(user_data[0]['bdate'])
        if age != 0:
            user_data[0]['age'] = age
        else:
            self.write_msg(user_data[0]['user_id'], f"Укажите возраст: ")
            age = int(self.longpoll_request())
            user_data[0]['age'] = age
        self.write_msg(user_data[0]['id'], 'Сколько лет допустима разница в возрасте (числом)? ')
        age_difference = int(self.longpoll_request())

        self.search_users_data_params['values']['city'] = user_data[0]['city']['id']
        self.search_users_data_params['values']['age_from'] = user_data[0]['age'] - age_difference
        self.search_users_data_params['values']['age_to'] = user_data[0]['age'] + age_difference
        if user_data[0]['sex'] == 1:
            self.search_users_data_params['values']['sex'] = 2
        elif user_data[0]['sex'] == 2:
            self.search_users_data_params['values']['sex'] = 1

        users_data = VkTools(self.api_user).get_all(**self.search_users_data_params)

        return users_data

    def get_photos(self, user_id):
        data_photo = self.api_user.photos.get(owner_id=user_id, **self.get_photos_params)
        return data_photo

    def vkuser_db_filling(self, user_id, people):
        session = Session()
        Base.metadata.create_all(engine)
        users_list = []
        user_age = self.get_age_from_birth_date(self.get_user_data(user_id)[0]['bdate'])
        for item in people['items']:
            item = self.get_user_data(item['id'])
            if not item[0].get('city'):
                item[0]['city'] = {}
                item[0]['city']['id'] = 0
            age = self.get_age_from_birth_date(item[0]['bdate'])
            if age != 0:
                db_user = VKUser(
                    user_id=item[0]['id'],
                    first_name=item[0]['first_name'],
                    last_name=item[0]['last_name'],
                    age=age,
                    age_difference=abs(user_age - age),
                    city=item[0]['city']['id'],
                    sex=item[0]['sex'],
                    relation=item[0]['relation'],
                    common_count=item[0]['common_count'],
                    black_list=False,
                )
                user_exists = session.query(VKUser).filter_by(user_id=item[0]['id']).count()
                if user_exists == 0:
                    users_list.append(db_user)
        session.add_all(users_list)
        session.commit()

    def photo_db_filling(self):
        session = Session()
        Base.metadata.create_all(engine)
        users = session.query(VKUser)
        photos_list = []
        for user in users:
            try:
                photos = self.get_photos(user.user_id)
                for photo_item in photos['items']:
                    db_photo = Photo(
                        user_id=user.id,
                        photo_id=photo_item['id'],
                        url=f"https://vk.com/id{user.user_id}?z=photo{user.user_id}_{photo_item['id']}",
                        likes_count=photo_item['likes']['count'],
                        comments_count=photo_item['comments']['count']
                    )
                    photo_exists = session.query(Photo).filter_by(id=photo_item['id']).count()
                    if photo_exists == 0:
                        photos_list.append(db_photo)
                time.sleep(0.5)
            except Exception:
                pass
        session.add_all(photos_list)
        session.commit()

    def add_to_black_list(self, users):
        session = Session()
        users = users.split(', ')
        for user in users:
            user = user.split(' ')
            session.query(VKUser).filter(VKUser.first_name == user[0], VKUser.last_name == user[1]).update(
                {"black_list": True})

        session.commit()

    def add_to_favorites(self, users):
        session = Session()
        users = users.split(', ')
        for user in users:
            user = user.split(' ')
            session.query(VKUser).filter(VKUser.first_name == user[0], VKUser.last_name == user[1]).update(
                {"favorites_list": True})
        session.commit()

    def show_pairs(self, user_id):
        session = Session()
        Base.metadata.create_all(engine)
        pairs = session.query(VKUser).filter(
            or_(VKUser.relation == 1, VKUser.relation == 6), VKUser.black_list != True).order_by(
            VKUser.age_difference, desc(VKUser.common_count))
        for user in pairs:
            photos = session.query(Photo).filter(
                Photo.user_id == user.id).order_by(text("comments_count + likes_count desc")).limit(3)
            print(photos)
            message = f"{user.first_name} {user.last_name} {'https://vk.com/id' + str(user.user_id)}"
            self.write_msg(user_id, message)
            for photo in photos:
                self.write_msg(user_id, photo.url)

    def show_favorites(self, user_id):
        session = Session()
        Base.metadata.create_all(engine)
        favorites = session.query(VKUser).filter(VKUser.favorites_list == True).order_by(
            VKUser.age_difference, desc(VKUser.common_count))
        for favorite in favorites:
            photos = session.query(Photo).filter(
                Photo.user_id == favorite.id).order_by(desc(Photo.likes_count), desc(Photo.comments_count)).limit(3)
            message = f"{favorite.first_name} {favorite.last_name} {'https://vk.com/id' + str(favorite.user_id)}"
            self.write_msg(user_id, message)
            for photo in photos:
                self.write_msg(user_id, photo.url)

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text

                    if request == 'Привет':
                        user_data = self.get_user_data(event.user_id)
                        self.write_msg(event.user_id, f"Привет, {user_data[0]['first_name']}!\n"
                                                      f"Я Vkinder и я могу помочь с поиском пары\n"
                                                      )
                    elif request == 'Найди пару':
                        user_data = self.get_user_data(event.user_id)
                        possible_pairs = self.search_users(user_data)
                        self.write_msg(event.user_id, f"Поиск окончен. Пополняю базу")
                        self.vkuser_db_filling(event.user_id, possible_pairs)
                        self.photo_db_filling()
                        self.write_msg(event.user_id, f"База пополнена")
                        self.show_pairs(event.user_id)

                    elif request == 'Покажи, кто есть':
                        self.show_pairs(event.user_id)

                    elif request == 'Покажи избранных':
                        self.show_favorites(event.user_id)

                    elif 'Добавь в избранное: ' in request:
                        favorites = request.replace('Добавь в избранное: ', '')
                        self.add_to_favorites(favorites)

                    elif 'Добавь в черный список: ' in request:
                        black_list = request.replace('Добавь в черный список: ', '')
                        self.add_to_black_list(black_list)

                    elif request == "Пока":
                        self.write_msg(event.user_id, "Пока((")
                    else:
                        self.write_msg(event.user_id, "Я не понимаю, что вы сказали...")