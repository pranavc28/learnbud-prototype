import pymysql
from flask_login import UserMixin
from learning.db import get_conn

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
        user_obj = cur.fetchone()
        if not user_obj:
            return None
        user = User(
            id_=user_obj[0], name=user_obj[1], email=user_obj[2], profile_pic=user_obj[3]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Users (id, name, email, profile_pic) "
            "VALUES (%s, %s, %s, %s)",
            (id_, name, email, profile_pic),
        )
        conn.commit()
