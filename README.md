# Чат-бот знакомств VKinder
## Возможности бота
1. Выполняет поиск по пользователям сети VKontakte на основе информации со страницы пользователя, написавшего в чат запрос "Найди пару". Поиск выполняется по городу (город должен быть обязательно указан в профиле), полу, возрасту и семейному положению.
Бот всегда дополнительно запрашивает максимльно допустимую разницу в возрасте. Если на странице запрашивающего пользователя не указана (или указана не полностью) дата рождения, бот также запрашивает дополнительно возраст пользователя. Найденные пользователи записываются в базу данных.
2. На запрос "Покажи, кто есть" отправляет пользователю сообщения со ссылками на профили пользователей и 3 самыми популярными фотографиями из их профилей. Популярность фотографий определяется по поличеству лайков и комментариев. Сортировка пользователей выполняется по разнице в возрасте и по количеству общих друзей.
3. Можно добавлять в чёрный список или избранное. Для этого необходимо написать в чат соответственно "Добавь в чёрный список:" или "Добавь в избранное: " и после двоеточия через запятую написать имена и фамилии добавляемых пользователей. Люди, занесённые в чёрный список, больше не будут отправляться пользователю.
4. На запрос "Покажи избранных" отправляет ссылки фотографии и ссылки на профили только пользователей, добавленных в избранный список.
## Настройки
### Настройка группы и получение токена сообщества
Создать группу в VK
1. Создать группу в VK
2. Зайти в Управление -> Работа с API. Создать ключ
![Получение токена](https://downloader.disk.yandex.ru/preview/210efbd3aad9153c3c1265650cf3792834e60979222c0aca38d0e3b7670f995b/61ec659a/xTJu7CXGT7uCiIbtt3ceY8dOTrRPQMF3lbac3PlUJAWsNKb2Gs2qzzvv29bgm-QaqQ2UvGY2wIRD2Sqd9X79sA%3D%3D?uid=0&filename=VKinder_group_token_1.JPG&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048)
3. Включить возможность писать сообщения в группу. Управление -> Сообщения -> Сообщения сообщества: включить.
4. Настройки бота. Возможности бота: Включены
![Настройки группы для бота](https://downloader.disk.yandex.ru/preview/aa21153ae724c5e54be13340044729ecea16cae840a2caaaaa1a3cc8248ba650/61ec6736/8Ax2InMx0FaT0KN6IefTtBm2WXbL8928tvBvup2fuJ6lKcHGxVqNZPmATpC8aNLH2UzkFCXqLW1iY3JBjLY24A%3D%3D?uid=0&filename=VKinder_group_settings.JPG&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048)
### Получение токена пользователя
1. Для создания приложения перейти по ссылке https://vk.com/editapp?act=create
2. Выбрать Standalone-приложение
![Создание приложения](https://downloader.disk.yandex.ru/preview/37e8cf7c054b10f2e2ad3fb7dd16e9a147f1d426e05ea3ca4ecb73cc28501487/61ed3da8/_RpJweSoGG3hG5QZTpaoZicoCghlNljH_cHLHB2gBQgOCurgX57YLzaEP8scyXyuJMzKdcdWxVzzbJClhRRPAA%3D%3D?uid=0&filename=Create_application_1.JPG&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048)

3. Перейти в настройки, влючить Open Api
4. В поле *адрес сайта* ввести http://localhost
5. В поле базовый домен ввести localhost
![Настройки приложения](https://downloader.disk.yandex.ru/preview/92fecfb119038d8595085201eab5ca3572870c0223ef9db1bf637b212f70b01f/61ed45fc/3uf50F-aGzGJ_7jXR2cNiradiKMJrD7bMXWRjUm0ScjxXEF1NnBZaBEseS_X3XceGNXSA8XJlyQYUE7AAOikLQ%3D%3D?uid=0&filename=Application_settings.JPG&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048)
6. Сохранить изменения
7. Скопировать id приложения в ссылку
https://oauth.vk.com/authorize?client_id=1&display=page&scope=stats,offline&response_type=token&v=5.131 вместо 1 вставить id **вашего** приложения. Не забудьте указать scope: https://vk.com/dev/permissions
8. Нажать разрешить
9. Сохранить токен
![Сохрание токена](https://downloader.disk.yandex.ru/preview/67d1480d28f249d69253909325561403f02ad9b5bc887755c3503931cf0940bf/61ed489f/Ndem7qusIrQWIP9oHRpI14SiXAxg48KZzq__sm2EaQStTeXnkNUtKBiks6ZdA2rSxb5qaOnT0UfPniki7iUSdw%3D%3D?uid=0&filename=2022-01-23_11-20-39.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=1872x940)
### Редактирование файла config.py
Перейти в папку settings проекта и вписать в файл config.py токены сообщества и пользователя в поля token_group и token_user соответственно, а также id пользователя VK в поле user_id.
![Настройка config.py](https://user-images.githubusercontent.com/87200878/150670754-ac24e664-e7ee-4944-858b-0c12a9f01cc5.png)
