class Product:
    count_id = 0

    # initializer method
    def __init__(self, name, price, category, image, description, ingredients_info, is_recommended, idproducts=None):
        Product.count_id += 1
        self.__product_id = idproducts if idproducts is not None else Product.count_id
        self.__name = name
        self.__price = price
        self.__category = category
        self.__image = image
        self.__description = description
        self.__ingredients_info = ingredients_info
        self.__is_recommended = is_recommended


    # accessor methods
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_category(self):
        return self.__category

    def get_image(self):
        return self.__image

    def get_description(self):
        return self.__description

    def get_ingredients_info(self):
        return self.__ingredients_info

    def get_is_recommended(self):
        return self.__is_recommended



    # mutator methods
    def set_product_id(self, id):
        self.__product_id = id

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_category(self, category):
        self.__category = category

    def set_image(self, image):
        self.__image = image

    def set_description(self, description):
        self.__description = description

    def set_ingredients_info(self, ingredients_info):
        self.__ingredients_info = ingredients_info
        
    def set_is_recommended(self, is_recommended):
        self.__is_recommended = is_recommended


        