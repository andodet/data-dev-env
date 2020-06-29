import time
from utils import constants

from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import (
    create_engine,
    engine,
    MetaData,
    Table,
    Column,
    Boolean,
    Integer,
    String,
)
from sqlalchemy.exc import InterfaceError
from sqlalchemy.types import TIMESTAMP, DECIMAL
from sqlalchemy.schema import DropTable

from seed_users import script_runs_in_container

from faker import Faker

faker = Faker("en")


class MyTxSeeder:
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
                self.meta = MetaData(bind=self.engine)
            except InterfaceError:
                print("MySQL not up yet, sleep and retry...")
                time.sleep(1)

        self.session = Session(self.engine)

        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)

        self.Users = self.Base.classes.users

    def seed(self):
        print("Clearng old data...")
        self.drop_tx_table()
        print("Start seeding...")
        self.create_tx_table()
        self.insert_transactions()

        print("Done!")
        self.connection.close()

    def get_users(self):
        users = self.session.query(self.Users).all()
        uids = [user.id for user in users]
        return uids

    def create_tx_table(self):
        self.Transactions = Table(
            "transactions",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("order_id", Integer),
            Column("user_id", Integer),
            Column("ts", TIMESTAMP),
            Column("amount", DECIMAL(19, 4)),
            Column("currency_code", String(3)),
            Column("item", String(100)),
            Column("is_premium", Boolean, default=False),
            extend_existing=True
        )
        self.meta.create_all(self.engine)

    def insert_transactions(self):
        uids = self.get_users()
        transactions = []
        for _ in range(2000):
            transaction = {
                "order_id": faker.pyint(min_value=1, max_value=9999, step=1),
                "user_id": faker.random.choice(uids),
                "ts": faker.date_time(),
                "amount": faker.pydecimal(
                    left_digits=4, right_digits=2, min_value=1
                ),
                "currency_code": faker.currency_code(),
                "item": faker.random.choice(constants['products']),
                "is_premium": faker.boolean(chance_of_getting_true=50)
            }
            transactions.append(transaction)
        self.connection.execute(self.Transactions.insert(), transactions)

    def drop_tx_table(self):
        if self.engine.has_table("transactions"):
            print("Dropping transaction table...")
            t = Table('transactions', self.meta)
            self.connection.execute(DropTable(t))


if __name__ == "__main__":
    MyTxSeeder().seed()

