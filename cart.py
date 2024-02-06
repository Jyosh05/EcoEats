class CartItem:
    def __init__(self, product_name, product_price, product_image, quantity):
        self.__name = product_name
        self.__price = product_price
        self.__image = product_image
        self.__quantity = quantity


    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_image(self):
        return self.__image

    def get_quantity(self):
        return self.__quantity



    def set_name(self, product_name):
        self.__name = product_name

    def set_price(self, product_price):
        self.__price = product_price

    def set_image(self, product_image):
        self.__image = product_image
    def set_quantity(self, quantity):
        self.__quantity = quantity

