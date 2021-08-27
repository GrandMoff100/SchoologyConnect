from db import DB


class UserCache:
    USERS = []
    MAX_LEN = 500

    @staticmethod
    def add(user):
        UserCache.USERS.append(user)
        if len(UserCache.USERS) > UserCache.MAX_LEN:
            user = UserCache.USERS[0]
            UserCache.USERS.pop(0)
            DB.save(user)

    @staticmethod
    def get(oauth_token):
        for auth in UserCache.USERS[::-1]:
            if auth.oauth_token == oauth_token:
                return auth
