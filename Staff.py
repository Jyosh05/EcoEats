# User class
class Staff:

    # initializer method
    def __init__(self,id, first_name, last_name, gender, role, email):
        self.__user_id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__role = role
        self.__email = email

    # accessor methods
    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_role(self):
        return self.__role

    def get_email(self):
        return self.__email

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_role(self, role):
        self.__role = role

    def set_email(self, email):
        self.__email = email
