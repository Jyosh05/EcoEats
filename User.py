class User:
    id = 0 # this is the id_count
    def __init__(self,username, password):
        User.id += 1
        # self.__user_id = User.count_id
        self.__username = username
        self.__password = password
        self.__first_name = None
        self.__last_name = None
        self.__gender = None
        self.__membership = None
        self.__remarks = None

    def get_userCount(self):
        return User.id
    def get_user_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_membership(self):
        return self.__membership

    def get_remarks(self):
        return self.__remarks

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_membership(self, membership):
        self.__membership = membership

    def set_remarks(self, remarks):
        self.__remarks = remarks

print("Hello")
print('cb')