from GroupHandler import GroupHandler
from UserHandler import UserHandler
from random import choice


gh = GroupHandler()
users = gh.get_all_users('jupiter_plane')
winner = choice(users)

uh = UserHandler()
winner_name = uh.get_full_name(winner)
print(winner_name)
