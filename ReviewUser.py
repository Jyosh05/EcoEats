class UserReview():
    count_id = 0
    def __init__(self, first_name, last_name, feedback):
        UserReview.count_id += 1
        self.__user_id = UserReview.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__feedback = feedback

    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_feedback(self):
        return self.__feedback

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_feedback(self, feedback):
        self.__feedback = feedback