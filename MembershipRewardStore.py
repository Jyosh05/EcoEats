from MembershipPurchases import *

class Rewards(MembershipPoints):
    reward1 = 30
    reward2 = 60
    reward3 = 90
    reward4 = 120

    def __init__(self, currentBalance, chosen_reward):
        super().__init__(currentBalance)
        self.__chosen_reward = chosen_reward

    def get_chosen_reward(self):
        return self.__chosen_reward
    def set_chosen_reward(self, chosen_reward):
        self.__chosen_reward = chosen_reward

    def rewardRedemption(self, currentBalance, chosen_reward):
        if currentBalance >= chosen_reward:
            aftDeduction = currentBalance - chosen_reward
            MembershipPoints.set_newBalance(aftDeduction)

#figure out how to link pressing the separate rewards to their individual
#points they cost