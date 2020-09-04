import pytest


@pytest.fixture
def db_conn():
    from sqlalchemy import create_engine, engine
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.exc import InterfaceError

    config = {
        "drivername": "mysql+mysqlconnector",
        "username": "root",
        "password": "root",
        "host": "mysql",
        "port": "3306",
        "database": "database",
    }

    Base = automap_base()

    try:
        engine = create_engine(engine.url.URL(**config))
    except InterfaceError:
        print("Something went wrong while connecting to MySQL db")

    Base.prepare(engine, reflect=True)
    yield engine
    print("Disposing engine")
    engine.dispose()


def test_user_table_exists(db_conn):
    assert db_conn.has_table("users") == True


def test_users_exist(db_conn):
    results = db_conn.execute("select * from users limit 1")
    users = [user for user in results]
    assert len(users) > 0, "Empty list, no users found"


def test_tx_table_exists(db_conn):
    assert db_conn.has_table("transactions") == True


def test_transactions_exist(db_conn):
    results = db_conn.execute("select * from transactions limit 1")
    transactions = [tx for tx in results]
    assert len(transactions) > 0, "Empty list, no transactions found"
