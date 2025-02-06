class User:
    def __init__(self, name=None, email=None):
        if not name or not email:
            raise NoDataProvidedError("Name and email are required.")

        self.name = name
        self.email = email

    def update(self, name=None, email=None):
        if not name and not email:
            raise NoDataProvidedError("At least one field must be provided.")

        if name:
            self.name = name

        if email:
            self.email = email

    @classmethod
    def from_repository(cls, user_db):
        return cls(user_db.name, user_db.email)


class NoDataProvidedError(Exception):
    pass
