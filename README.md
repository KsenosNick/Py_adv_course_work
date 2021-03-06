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
![image](https://user-images.githubusercontent.com/87200878/150820401-8d9aa784-d644-41f6-a550-f7149f2814e0.png)
3. Включить возможность писать сообщения в группу. Управление -> Сообщения -> Сообщения сообщества: включить.
4. Настройки бота. Возможности бота: Включены
![image](https://user-images.githubusercontent.com/87200878/150820200-3a39b0d7-7421-4864-bf03-72fe0379af3d.png)
### Получение токена пользователя
1. Для создания приложения перейти по ссылке https://vk.com/editapp?act=create
2. Выбрать Standalone-приложение
![image](https://user-images.githubusercontent.com/87200878/150819996-25af974b-1369-49c9-a8ee-fef0c26a7450.png)


3. Перейти в настройки, влючить Open Api
4. В поле *адрес сайта* ввести http://localhost
5. В поле базовый домен ввести localhost
![image](https://user-images.githubusercontent.com/87200878/150832620-841c0086-bf5e-415c-a9f6-d74b894db1e2.png)
6. Сохранить изменения
7. Скопировать id приложения в ссылку
https://oauth.vk.com/authorize?client_id=1&display=page&scope=stats,offline&response_type=token&v=5.131 вместо 1 вставить id **вашего** приложения. Не забудьте указать scope: https://vk.com/dev/permissions
8. Нажать разрешить
9. Сохранить токен
![image](https://user-images.githubusercontent.com/87200878/150832954-bdfb249e-594e-4230-8410-baaaf7bdc8cc.png)
### Редактирование файла config.py
Перейти в папку settings проекта и вписать в файл config.py токены сообщества и пользователя в поля token_group и token_user соответственно, а также id пользователя VK в поле user_id.
![Настройка config.py](https://user-images.githubusercontent.com/87200878/150670754-ac24e664-e7ee-4944-858b-0c12a9f01cc5.png)
