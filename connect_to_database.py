from psycopg2 import connect

import os
import dotenv
import hashlib
from  psycopg2.errors import UniqueViolation

dotenv.load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_PASS = os.environ.get("DB_PASS")

conn = connect(
    database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
)

cursor = conn.cursor()

cursor.execute("select * from users ;")
result = cursor.fetchone()
if result is not None:
    print(result[0])
    print(type(result[0]))


class User:
    def __init__(
        self,
        username: str,
        passwrod: str,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> None:
        self.id :int|None=None
        self.is_logedin = False
        self.username: str = username
        self.password: str = self.hash_password(passwrod)
        self.first_name: str | None = first_name
        self.last_name: str | None = last_name

    def hash_password(self, password: str) -> str:
        m = hashlib.sha256()
        m.update(password.encode("utf-8"))
        hash_password = str(m.hexdigest())
        return hash_password

    def update_password(self,password):
        self.password = self.hash_password(password)

    def __str__(self) -> str:
        return f"User(id={self.id}, username={self.username},first_name={self.first_name},last_name={self.last_name})"

    def login(self, password):
        if self.id is None:
            raise ValueError("user does not have any id")
        if self.password != self.hash_password(password):
            raise ValueError("wrong password")
        else:
            self.is_logedin=True

    def save(self):
        conn = connect(
            database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )

        cursor = conn.cursor()
        if self.id is not None:
            cursor.execute("update users set username=%s, password=%s, first_name=%s,last_name=%s where id=%s;",(self.username,self.password,self.first_name,self.last_name,self.id))
        else:
            try:
                cursor.execute(f"insert into users (username,password,first_name, last_name) values ('{self.username}','{self.password}','{self.first_name}','{self.last_name}') RETURNING id;")
                self.id =  cursor.fetchone()[0]
            except UniqueViolation:
                raise ValueError("user name exists!")
        conn.commit()
        conn.close()

    @classmethod
    def load(cls, username):
        conn = connect(
            database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )

        cursor = conn.cursor()
        cursor.execute(f"select * from users where username='{username}';")
        user_data = cursor.fetchone()
        if user_data is None:
            raise ValueError("user does not exist.")
        
        id,username,first_name,last_name,password = user_data
        user = User(username=username,passwrod=password,first_name=first_name,last_name=last_name)
        user.id = id
        conn.close()
        return user


# s = User(username="mohammadnpak2", passwrod="321",first_name="mohammad2",last_name="nozari2")
# s.save()

# s.first_name = "alireza"
# s.save()

# m = User.load(username="mohammad")

user = User.load("mohammadnpak")
user.update_password("1234")
user.save()

# user.login("123")
# print(user.is_logedin)


# user = User(username="mohammadnpak", passwrod="232342",first_name="saddsgf",last_name="sfsdfas")
# user.save()