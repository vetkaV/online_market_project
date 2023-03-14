class User():
    def __init__(self, login, email, phone):
        self.login = login
        self.email = email
        self.phone = phone
        self.name = None
        self.surname = None
        self.address = None
    
    def set_info_user(self, name, surname, address):
        self.name = name
        self.surname = surname
        self.address = address