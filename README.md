# s07

A simple Python-based user management system with PostgreSQL integration. This project demonstrates user creation, password hashing, authentication, and persistent storage using `psycopg2`.

## 📝 Description

This project is designed to:

- Connect to a PostgreSQL database using credentials from a `.env` file.
- Store user information (username, password, first name, last name).
- Hash passwords using SHA-256 for secure storage.
- Provide features to save, load, update, and authenticate users.
- Use object-oriented programming principles to model users.

---

## 📦 Dependencies

Ensure the following Python packages are installed:

```toml
dotenv>=0.9.9
ipython>=9.5.0
mypy>=1.17.1
psycopg2-binary>=2.9.10
types-psycopg2>=2.9.21.20250809
```


### 📦 Installing Dependencies

Before running the project, make sure to install all required dependencies.

#### 1. Clone the repository (if applicable)

```bash
git clone https://github.com/yourusername/s07.git
cd s07
python -m venv venv
```


here is my uer code in python

```python

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


```
