import time

import GroupHandler
import UserHandler
import pickle
from os.path import exists


gh = GroupHandler.GroupHandler()
uh = UserHandler.UserHandler()

if exists('users.pickle'):
    with open('users.pickle', 'rb') as f:
        users = pickle.load(f)
else:
    users = gh.get_all_users('jupiter_plane')
    with open('users.pickle', 'wb') as f:
        pickle.dump(users, f)

if exists('groups.pickle'):
    with open('groups.pickle', 'rb') as f:
        groups = pickle.load(f)
else:
    groups = uh.bulk_get_all_groups(users)
    with open('groups.pickle', 'wb') as f:
        pickle.dump(groups, f)

if exists('stat.pickle'):
    with open('stat.pickle', 'rb') as f:
        stat = pickle.load(f)
else:
    stat = uh.bulk_get_groups_statistics(users)
    with open('stat.pickle', 'wb') as f:
        pickle.dump(stat, f)

lst = [(v, k) for k, v in stat.items() if v > 5]
for v, k in sorted(lst)[::-1]:
    print(gh.get_name(k), v, f"https://vk.com/public{k}")
    time.sleep(0.3)
