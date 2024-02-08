import mysql.connector

mydb= mysql.connector.connect(
    host='localhost',
    user='root',
    password='JYOSHNA2006!',
    port='3306',
    database='ecoeatsusers'
)

mycursor = mydb.cursor()
class User:
    id = 0 # this is the id_count
    def __init__(self,username, password, email=None, gender=None,postal_code = 0,profilePic=None, accountStatus='Active'):
        User.id += 1
        # self.__user_id = User.count_id
        self.__username = username
        self.__password = password
        self.__first_name = None
        self.__last_name = None
        self.__gender = None
        self.__membership = None
        self.__remarks = None
        self.__email = email
        self.__gender = gender
        self.__postal_code = postal_code
        self.__profilePic = profilePic
        self.__accountStatus = accountStatus

    def set_email(self,email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_gender(self,gender):
        self.__gender = gender

    def get_gender(self):
        return self.__gender

    def set_postal_code(self,postal_code):
        self.__postal_code = postal_code

    def get_postal_code(self):
        return self.__postal_code

    def set_profilePic(self,profilePic):
        self.__profilePic = profilePic

    def get_profilePic(self):
        return self.__profilePic

    def set_accountStatus(self,accountStatus):
        self.__accountStatus = accountStatus

    def get_accountStatus(self):
        return self.__accountStatus

    def get_userCount(self):
        return User.id
    def get_user_id(self):
        return self.__user_id

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_membership(self):
        return self.__membership

    def get_remarks(self):
        return self.__remarks

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_membership(self, membership):
        self.__membership = membership

    def set_remarks(self, remarks):
        self.__remarks = remarks

    @staticmethod
    def get_username_by_id(user_id):
        # Implement the logic to retrieve the username from your database

            select= ("SELECT username FROM users WHERE id = %s")
            mycursor.execute(select, (user_id,))
            result = mycursor.fetchone()[0]
            return result
        #     if result:
        #         result[0]
        #     else:
        #         return None
        # except Exception as e:
        #     print("Error:", e)
        #     return None  # Handle the exception as needed

        # Example: return User.query.get(user_id).get_username()


print("Hello")
print('cb')