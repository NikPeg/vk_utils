import vk
from tenacity import retry, wait_exponential, stop_after_attempt

import constants
import time


class GroupHandler:
    def __init__(self):
        self.vk_api = vk.API(access_token=constants.TOKEN, v=constants.VK_VERSION)

    def get_all_users(self, group_id):
        try:
            group = self.vk_api.groups.getMembers(group_id=group_id,
                                                  v=5.131, fields='sex', access_token=constants.TOKEN,
                                                  offset=0, count=10)
        except Exception as e:
            print(e)
            return []
        step = 1000
        res = []
        for i in range(0, group['count'], step):
            group = self.vk_api.groups.getMembers(group_id=group_id,
                                                  v=5.131, fields='sex', access_token=constants.TOKEN,
                                                  offset=i // step, count=step)
            res.extend([str(elem['id']) for elem in group['items']])
            time.sleep(0.3)
        return res

    def get_members_count(self, group_name):
        try:
            group = self.vk_api.groups.getMembers(group_id=group_name,
                                                  v=5.131, fields='sex', access_token=constants.TOKEN,
                                                  offset=1, count=1)
        except Exception as e:
            print(e)
            return -1
        return group['count']

    def groups_in_interval(self, group_ids, min_members=0, max_members=1000):
        res = []
        print("groups_in_interval")
        for i in range(len(group_ids)):
            print(f"{i}/{len(group_ids)}")
            group_id = group_ids[i]
            if min_members <= self.get_members_count(group_id) <= max_members:
                res.append(group_id)
            time.sleep(0.03)
        return res

    @retry(wait=wait_exponential(max=10), stop=stop_after_attempt(10))
    def get_name(self, group_id):
        try:
            group = self.vk_api.groups.getById(group_id=group_id,
                                               v=5.131, fields='name', access_token=constants.TOKEN)
        except Exception as e:
            print(e)
            return ""
        return group[0]["name"]

    def groups_to_csv(self, group_ids, filename="groups"):
        print("groups_to_csv")
        with open(f"{filename}.csv", "w") as file:
            file.write(f"name;link\n")
            for i in range(len(group_ids)):
                print(f"{i}/{len(group_ids)}")
                group_id = group_ids[i]
                name = self.get_name(group_id)
                time.sleep(0.03)
                try:
                    file.write(f"{name};https://vk.com/public{group_id}\n")
                except UnicodeEncodeError:
                    file.write(f"None;https://vk.com/public{group_id}\n")
                except Exception as e:
                    print(e)

    def groups_statistics_to_csv(self, groups, filename="groups"):
        print("groups_statistics_to_csv")
        with open(f"{filename}.csv", "w") as file:
            file.write(f"link;subscribers count\n")
            for group_id, group_info in groups.items():
                file_line = f"https://vk.com/public{group_id};{group_info}\n"
                try:
                    file.write(file_line)
                except Exception as e:
                    print(e)
