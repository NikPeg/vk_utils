import vk
from vk_api import VkApiError

import constants
import time
import collections
from tenacity import retry, wait_exponential, wait_fixed, stop_after_attempt


class UserHandler:
    def __init__(self):
        self.vk_api = vk.API(access_token=constants.TOKEN, v=constants.VK_VERSION)

    def get_full_name(self, user_id):
        try:
            user = self.vk_api.users.get(user_id=user_id, v=5.131, access_token=constants.TOKEN)[0]
        except Exception as e:
            print(e)
            return []
        return f"""{user["first_name"]} {user["last_name"]}"""

    @retry(wait=wait_exponential(max=10), stop=stop_after_attempt(10))
    def get_all_groups(self, user_id):
        try:
            user = self.vk_api.users.getSubscriptions(user_id=user_id,
                                                      v=5.131, fields='id', access_token=constants.TOKEN)
        except VkApiError as e:
            if e.code == 6:
                print(e)
                print("Retrying...")
                raise e
            print(e)
            return []
        except Exception as e:
            print(e)
            return []
        return user['groups']['items']

    def bulk_get_all_groups(self, user_ids):
        print("bulk_get_all_groups")
        res = []
        for i in range(len(user_ids)):
            print(f"{i}/{len(user_ids)}")
            user_id = user_ids[i]
            res.extend(self.get_all_groups(user_id))
            time.sleep(0.3)
        return res

    def bulk_get_groups_statistics(self, user_ids):
        print("bulk_get_groups_statistics")
        res = collections.defaultdict(int)
        for i in range(len(user_ids)):
            print(f"{i}/{len(user_ids)}")
            user_id = user_ids[i]
            for group in self.get_all_groups(user_id):
                res[group] += 1
            time.sleep(0.3)
        return res