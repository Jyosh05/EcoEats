import User


class Membership(User.User):
    count_id = 0
    store_rewards = ['Loyalty Treat: Customer-For-1-Year Receive S$5 Off Your Purchase',
                     'Holiday Treat: Enjoy 1-For-1 Treat On December Exclusive Drinks']

    def __init__(self, first_name, last_name, gender, membership, remarks, email, date_joined, address, Buyrewards,
                 totalPoints, currentBalance):
        super().__init__(first_name, last_name, gender, remarks)
        membership.count_id += 1
        self.__membership_id = Membership.count_id
        self.__store_rewards = Membership.store_rewards
        self.__membership = 'Seed'  # default is base tier
        self.__email = email
        self.__date_joined = date_joined
        self.__address = address
        self.__Buyrewards = ''  # default you haven't bought any rewards
        self.__totalPoints = 0  # default is 0
        self.__currentBalance = 0  # default is 0
        # does the defaults affect only when a new membership is created, or every time it is retrieved?***

    # accessor methods
    def get_membership_id(self):
        return self.__customer_id

    def get_store_reward(self):
        return self.__store_rewards

    def get_email(self):
        return self.__email

    def get_date_joined(self):
        return self.__date_joined

    def get_address(self):
        return self.__address

    def get_membership(self):
        return self.__membership

    def get_Buyrewards(self):
        return self.__Buyrewards

    def get_totalPoints(self):
        return self.__totalPoints

    def get_currentBalance(self):
        return self.__currentBalance

    # mutator methods
    def set_membership_id(self, membership_id):
        self.__membership_id = membership_id

    def set_store_rewards(self, store_rewards):
        self.__store_rewards = store_rewards

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def set_membership(self, membership):
        self.__membership = membership

    def set_rewards(self, Buyrewards):
        self.__Buyrewards = Buyrewards

    def set_totalPoints(self, totalPoints):
        self.__totalPoints = totalPoints

    def set_currentBalance(self, currentBalance):
        self.__currentBalance = currentBalance