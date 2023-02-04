import dotenv
import os
from functools import wraps


dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


def UserLogger(username):
    dotenv.set_key(dotenv_file, "USER_LOGGED_IN", "True")
    dotenv.set_key(dotenv_file, "USERNAME", username)
    if eval(os.getenv("USER_LOGGED_IN")):
        return 'Login Done', 201
    else:
        return 'Login Failed From Auth', 401


def UserLogout(username):
    dotenv.set_key(dotenv_file, "USER_LOGGED_IN", "False")
    dotenv.set_key(dotenv_file, "USERNAME", None)
    if not eval(os.getenv("USER_LOGGED_IN")):
        return 'Logout Done', 201
    else:
        return 'Logout Failed From Auth', 401


def user_login_verify(func):
    """Code will only run if Env variable for USER_LOGGED_IN is equal to True, checks for .env file"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        is_logged_in = eval(os.getenv("USER_LOGGED_IN"))
        print(is_logged_in, type(is_logged_in))
        if is_logged_in:
            print('Triggered')
            return func(*args, **kwargs)
        else:
            raise Exception('Access denied: User not logged in')

    return wrapper

# @logged_in_only
# def my_function():
#     # This code will only run if USER_LOGGED_IN is True
#     print('Hello, world!')
