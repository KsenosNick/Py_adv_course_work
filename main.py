
from vk_api.longpoll import VkEventType

from bot.vkinder import VKinder

def users_iterator(users_data):
    next_element_exist = True
    user_list = []
    while next_element_exist:
        try:
            user = next(users_data)
        except StopIteration:
            next_element_exist = False
        else:
            user_list.append(user)
    print(len(user_list))


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

#
# if __name__ == "__main__":
#     main()