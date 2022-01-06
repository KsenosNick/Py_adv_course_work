
from random import randrange

import vk_api
from vk_api import VkTools
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import datetime

from config import token_group, token_user, version


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
        'fields': 'city, sex, relation, bdate, common_count',
    }

    search_users_data_params = {
        'method': 'users.search',
        'max_count': 1000,
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
        self.vk_bot.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

    def longpoll_request(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text
                    return request

    def get_user_data(self, user_id):
        user_data = self.api_user.users.get(user_id=user_id, **self.get_user_data_params)

        if not user_data[0].get('city'):
            self.write_msg(user_id, "Необходимо указать город в профиле. Выберите город и повторите запрос")
        try:
            datetime.strptime(user_data[0]['bdate'], '%d.%m.%Y')
        except Exception:
            self.write_msg('27944409', f"Укажите возраст: ")
            age = int(self.longpoll_request())
            user_data[0]['age'] = age

        else:
            bdate_obj = datetime.strptime(user_data[0]['bdate'], '%d.%m.%Y')
            date_current = datetime.now()
            age = int((date_current - bdate_obj).days / 365.2425)
            user_data[0]['age'] = age
        return user_data

    def search_users(self, user_data):
        self.search_users_data_params['values']['city'] = user_data[0]['city']['id']
        self.search_users_data_params['values']['age_from'] = user_data[0]['age']
        self.search_users_data_params['values']['age_to'] = user_data[0]['age']

        users_data = VkTools(self.api_user).get_all(**self.search_users_data_params)

        return users_data

    def get_photos(self, user_id):

        data_photo = self.api_user.photos.get(owner_id=user_id, **self.get_photos_params)
        # photo_url = data_photo['items'][8]['sizes'][0]['url']
        return data_photo


# 27944409 - я
# 12126259"- Марина
# Настя Пигасова - 141040434
photos_data = VKinder(token_group, token_user, version).get_photos('27944409')

user_data = VKinder(token_group, token_user, version).get_user_data('27944409')

users_data = VKinder(token_group, token_user, version).search_users(user_data)
