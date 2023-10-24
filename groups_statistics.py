from GroupHandler import GroupHandler
from UserHandler import UserHandler
from random import choice


gh = GroupHandler()
users = gh.get_all_users('jupiter_plane')

uh = UserHandler()
for user in users:
    print(uh.get_all_groups(user))
