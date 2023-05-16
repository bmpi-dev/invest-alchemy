# execute this code when needs
import sys, os

sys.path.append(os.getcwd())

from storage import get_premium_user_list

users = get_premium_user_list()

print('user list size is: ', len(users))