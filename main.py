from random import randrange
import requests

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import token, version

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

url = 'https://api.vk.com/method/'
params = {
            'access_token': token,
            'v': version,
        }


def get_user_data(user_id):
    get_user_data_params = {
        'user_ids': user_id,
        'fields': 'city, sex, relation, bdate'
    }
    data_get_url = url + 'users.get'
    user_data = requests.get(data_get_url, params={**params, **get_user_data_params}).json()
    return user_data
    # user_sex = user_data['response'][0].get('sex')


get_user_data('141040434')

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request == "привет":
                write_msg(event.user_id, f"Хай, {event.user_id}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")