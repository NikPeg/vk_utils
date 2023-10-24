import vk
import constants


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

    def get_all_groups(self, user_id):
        try:
            user = self.vk_api.users.getSubscriptions(user_id=user_id,
                                                      v=5.131, fields='id', access_token=constants.TOKEN)
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
        return res