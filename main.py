from random import randrange
import requests
# https://oauth.vk.com/authorize?client_id=8041748&display=page&scope=stats,photos,offline&response_type=token&v=5.131
import vk_api
from vk_api import VkTools
from vk_api.longpoll import VkLongPoll, VkEventType

from config import token_group, token_user, version

vk_bot = vk_api.VkApi(token=token_group)
vk_user = vk_api.VkApi(token=token_user)
api_bot = vk_bot.get_api()
api_user = vk_user.get_api()
longpoll = VkLongPoll(vk_bot)
city = ''

url = 'https://api.vk.com/method/'
params_bot = {
            'access_token': token_group,
            'v': version,
        }
params_user = {
            'access_token': token_user,
            'v': version,
        }
get_user_data_params = {
        'fields': 'city, sex, relation, bdate'
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


def get_user_data(user_id, params):
    user_data = api_user.users.get(user_id=user_id, **params)
    return user_data


def search_users(user_data, params):
    params['values']['city'] = user_data[0]['city']['id']
    # params['values']['city'] = 2
    params['values']['age_from'] = 30
    params['values']['age_to'] = 40

    users_data = VkTools(api_user).get_all_iter(**params)

    return users_data


# 27944409 - я
# Настя Пигасова - 141040434
user_data = get_user_data('27944409', get_user_data_params)
users_data = search_users(user_data, search_users_data_params)


def users_iterator(users_data):
    next_element_exist = True
    user_list = []
    while next_element_exist:
        i = 0
        try:
            user = next(users_data)
        except StopIteration:
            next_element_exist = False
        else:
            user_list.append(user)
    print(len(user_list))


def write_msg(user_id, message):
    vk_bot.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text.lower()

                if request == "привет":
                    user_data = get_user_data(event.user_id, get_user_data_params)
                    write_msg(event.user_id, f"Привет, {user_data[0]['first_name']}!")
                    received_users_data = search_users(user_data, search_users_data_params)
                    write_msg(event.user_id, f"'Вот кого я нашёл:'")
                    for user in received_users_data['items']:
                        if user.get('sex') == 1:
                            sex = 'женский',
                        elif user.get('sex') == 1:
                            sex = 'мужской'
                        else:
                            sex = 'не указан'
                        if user.get('city'):
                            city = user['city']['title']
                        else:
                            city = 'город не указан'





                elif request == "пока":
                    write_msg(event.user_id, "Пока((")
                else:
                    write_msg(event.user_id, "Не поняла вашего ответа...")


# if __name__ == "__main__":
#     main()