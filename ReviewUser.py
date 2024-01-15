import User

class UserReview(User.User):
    count_id = 0
    def __init__(self, name, email, experience,feedback):
        UserReview.count_id += 1
        UserReview.__experience = None
        self.__user_id = UserReview.count_id
        self.__name = name
        self.__email = email
        self.__feedback = feedback

    def get_experience(self):
        return self.__experience

    def set_experience(self, experience):
        self.__experience = experience

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_feedback(self):
        return self.__feedback

    def set_feedback(self, feedback):
        self.__feedback = feedback

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, user_id):
        self.__user_id = user_id

