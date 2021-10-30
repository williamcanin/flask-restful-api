from passlib.hash import sha256_crypt as crypt
from main import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    superuser = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def password(self):
        raise AttributeError("password not readable")

    @password.setter
    def password(self, password):
        self.password_hash = crypt.hash(password)

    @password.getter
    def password(self):
        return self.password_hash

    def verify_password(self, password):
        if crypt.verify(password, self.password_hash):
            return True
        return False

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"<User {self.username}>"