from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class Customer:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __str__(self):
        return f"Customer: {self.name}, Email: {self.email}\n"
