class Rewards():
    def __init__(self, reward_name, reward_value, reward_type):
        self.__reward_name = reward_name
        self.__reward_value = reward_value
        self.__reward_type = reward_type


    def get_reward_name(self):
        return self.__reward_name

    def set_reward_name(self, reward_name):
        self.__reward_name = reward_name

    def get_reward_value(self):
        return self.__reward_value

    def set_reward_value(self, reward_value):
        self.__reward_value = reward_value

    def get_reward_type(self):
        return self.__reward_type

    def set_reward_type(self, reward_type):
        self.__reward_type = reward_type