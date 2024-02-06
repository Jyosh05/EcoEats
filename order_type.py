class DineIn:
    def __init__(self, time, pax):
        self.__time = time
        self.__pax = pax


    def get_time(self):
        return self.__time

    def get_pax(self):
        return self.__pax


    def set_time(self, time):
        self.__time = time

    def set_pax(self, pax):
        self.__pax = pax


class Delivery:
    def __init__(self, street, block, unit_no, postal_code):
        self.__street = street
        self.__block = block
        self.__unit_no = unit_no
        self.__postal_code = postal_code


    def get_street(self):
        return self.__street

    def get_block(self):
        return self.__block

    def get_unit_no(self):
        return self.__unit_no

    def get_postal_code(self):
        return self.__postal_code


    def set_street(self, street):
        self.__street = street

    def set_block(self, block):
        self.__block = block

    def set_unit_no(self, unit_no):
        self.__unit_no = unit_no

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code