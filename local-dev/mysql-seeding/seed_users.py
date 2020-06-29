import time
import random

from sqlalchemy import (
    engine,
    create_engine,
    Table,
    Column,
    Integer,
    String,
    Boolean,
    MetaData,
    text,
    dialects,
)
from sqlalchemy.dialects import mysql
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.exc import InterfaceError
from sqlalchemy.schema import DropTable

from faker import Faker

states = ["IT", "EN"]
faker = Faker("en")


class MySqlSeeder:
    def __init__(self):
        config = {
            "drivername": "mysql+mysqlconnector",
            "username": "root",
            "password": "root",
            "host": "mysql" if script_runs_in_container() else "localhost",
            "port": "3306",
            "database": "database",
        }
        while not hasattr(self, "connection"):
            try:
                self.engine = create_engine(engine.url.URL(**config))
                self.connection = self.engine.connect()
                self.meta = MetaData()
            except InterfaceError:
                print("MySQL not up yet, sleep and retry...")
                time.sleep(1)

    def seed(self):
        print("Clearing old data...")
        self.drop_user_table()
        print("Start seeding...")
        self.create_user_table()
        self.insert_users()

        self.connection.close()
        print("Done!")

    def create_user_table(self):
        self.Users = Table(
            "users",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
            Column("email", String(250)),
            Column("state", String(50)),
            Column("birthday", TIMESTAMP),
            Column("notes", String(250)),
            Column("is_adult", Boolean, default=False),
            extend_existing=True
        )
        self.meta.create_all(self.engine)

    def insert_users(self):
        users = []
        for _ in range(500):
            user = {
                "name": faker.name(),
                "email": faker.ascii_free_email(),
                "state": faker.random.choice(states),
                "birthday": faker.date_time(),
                "notes": faker.sentence(nb_words=5),
                "is_adult": faker.boolean(chance_of_getting_true=50),
            }
            users.append(user)

        self.connection.execute(self.Users.insert(), users)

    def drop_user_table(self):
        if self.engine.has_table("users"):
            print("Dropping users table...")
            t = Table('users', self.meta)
            self.connection.execute(DropTable(t))


def script_runs_in_container():
    # Check if docker is running
    with open("/proc/1/cgroup", "r") as cgroup_file:
        return "docker" in cgroup_file.read()


if __name__ == "__main__":
    MySqlSeeder().seed()
