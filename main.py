from random import randrange
import requests
# https://oauth.vk.com/authorize?client_id=8041748&display=page&scope=stats,photos,offline&response_type=token&v=5.131
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import token_group, token_user, version

vk_bot = vk_api.VkApi(token=token_group)
vk_user = vk_api.VkApi(token=token_user)
api_bot = vk_bot.get_api()
api_user = vk_user.get_api()
longpoll = VkLongPoll(vk_bot)

url = 'https://api.vk.com/method/'
params_bot = {
            'access_token': token_group,
            'v': version,
        }
params_user = {
            'access_token': token_user,
            'v': version,
        }



def get_user_data(user_id):
    get_user_data_params = {
        'user_ids': user_id,
        'fields': 'city, sex, relation, bdate'
    }
    user_data = api_user.users.get(user_ids=user_id, afields='city, sex, relation, bdate')
    # data_get_url = url + 'users.get'
    # user_data = requests.get(data_get_url, params={**params_bot, **get_user_data_params}).json()
    return user_data
    # user_sex = user_data['response'][0].get('sex')


def search_users(user_data):
    AGE_FROM = 30
    AGE_TO = 40
    CITY = user_data['response'][0]['city']['id']
    offset = 0
    count = 1000
    users_ids = []

    rs = api_user.users.search(city=CITY, age_from=AGE_FROM, age_to=AGE_TO, fields='domain')
    users_ids = [user['id'] for user in rs['items']]
    print(users_ids)
# 27944409 - я
# Настя Пигасова - 141040434
user_data = get_user_data('27944409')

search_users(user_data)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#
#         if event.to_me:
#             request = event.text
#
#             if request == "привет":
#                 write_msg(event.user_id, f"Хай, {event.user_id}")
#             elif request == "пока":
#                 write_msg(event.user_id, "Пока((")
#             else:
#                 write_msg(event.user_id, "Не поняла вашего ответа...")