from bot.vkinder import VKinder
from config import token_user, token_group, version



if __name__ == "__main__":
    VKinder(token_group, token_user, version).listen()

