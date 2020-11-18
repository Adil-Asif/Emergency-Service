import random


class Account:
    _name = None
    _email = None
    _phone = None
    _cnic = None 
    _ids = None
    _password = None
    
    
        
    
    def signup(self):
        self._name = input("Enter your Name: ")
        self._email = input("Enter your Email Address: ")
        self._cninc = input("Enter your Cnic Number: ")
        self._phone = input("Enter your Phone Number: ")
        self._password = input("Enter your Password: ")
        re_password = input("Enter your Password: ")
        while ((re_password != self._password)):
            self._password = input("Enter your Password: ")
            re_password = input("Enter your Password: ")
        self._ids = random.random() * self._cnic + self._phone 

    def signin(self):
        email = input("Enter your email address: ")
        ids = input("Enter your assigned id: ")

        if((self._email == email) and (self._ids == ids)):
            print("successfully logged in")
        else:
            print("login failed")

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()