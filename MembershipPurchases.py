class MembershipPoints:
    points = 0
    def __init__(self, totalEarned, currentBalance, newBalance):
        self.__totalEarned = totalEarned
        self.__currentBalance = currentBalance
        self.__newBalance = newBalance


    def get_totalEarned(self):
        return self.__totalEarned
    def set_totalEarned(self, totalEarned):
        self.__totalEarned = totalEarned

    def get_currentBalance(self):
        return self.__currentBalance
    def set_currentBalance(self, currentBalance):
        self.__currentBalance = currentBalance

    #adding points to make new balance
    def newBalance(self, payment):
        self.__newBalance = self.__currentBalance + payment

    def get_newBalance(self):
        return self.__newBalance
    def set_newBalance(self, newBalance):
        self.__newBalance = newBalance

    def membershipStatus(self, totalEarned):

        if totalEarned > 300:
            self.__membershipStatus = 'Bloom'
        elif totalEarned < 100:
            self.__membershipStatus = 'Seed'
        else:
            self.__membershipStatus = 'Sprout'
