class UserReview():
    count_id = 0

    def __init__(self, name, email, stars, feedback):
        UserReview.count_id += 1
        self.__user_id = UserReview.count_id
        self.__name = name
        self.__email = email
        self.__stars = stars
        self.__feedback = feedback

    def get_stars(self):
        return self.__stars

    def set_stars(self, stars):
        self.__stars = stars

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
