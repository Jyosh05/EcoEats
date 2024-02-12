import User


class Membership(User.User):
    def __init__(self, date_joined, birthdate, phone_number, newsletter):
        self.__membership = 'Seed'  # default is base tier
        self.__phone_number = phone_number
        self.__date_joined = date_joined
        self.__birthdate = birthdate
        self.__newsletter = newsletter

        # self.__Buyrewards = ''  # default you haven't bought any rewards
        # self.__totalBalance = 0  # default is 0
        # self.__currentBalance = 0  # default is 0
        # does the defaults affect only when a new membership is created, or every time it is retrieved?***

    # accessor methods
    # def get_membership_id(self):
    #     return self.__customer_id

    def get_phone_number(self):
        return self.__phone_number

    def get_date_joined(self):
        return self.__date_joined

    def get_birthdate(self):
        return self.__birthdate
    def get_newsletter(self):
        return self.__newsletter

    # def get_Buyrewards(self):
    #     return self.__Buyrewards
    #
    # def get_totalPoints(self):
    #     return self.__totalPoints
    #
    # def get_currentBalance(self):
    #     return self.__currentBalance

    # mutator methods
    # def set_membership_id(self, membership_id):
    #     self.__membership_id = membership_id

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def set_newsletter(self, newsletter):
        self.__newsletter = newsletter

    # def set_rewards(self, Buyrewards):
    #     self.__Buyrewards = Buyrewards
    #
    # def set_totalPoints(self, totalPoints):
    #     self.__totalPoints = totalPoints
    #
    # def set_currentBalance(self, currentBalance):
    #     self.__currentBalance = currentBalance