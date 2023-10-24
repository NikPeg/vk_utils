import collections
import time

from GroupHandler import GroupHandler
from UserHandler import UserHandler


gh = GroupHandler()
users = gh.get_all_users('jupiter_plane')
groups_statistics = collections.defaultdict(int)

uh = UserHandler()
print("Get users groups...")
i = 0
for user in users:
    print(f"{i}/{len(users)}")
    groups = uh.get_all_groups(user)
    time.sleep(0.2)
    for group in groups:
        groups_statistics[group] += 1
    i += 1

print("Saving statistics...")
gh.groups_statistics_to_csv(groups_statistics)
