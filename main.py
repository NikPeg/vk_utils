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

if exists('ok_groups.pickle'):
    with open('ok_groups.pickle', 'rb') as f:
        ok_groups = pickle.load(f)
else:
    ok_groups = gh.groups_in_interval(groups, 100, 300)
    with open('ok _groups.pickle', 'wb') as f:
        pickle.dump(ok_groups, f)

gh.groups_to_csv(ok_groups)
