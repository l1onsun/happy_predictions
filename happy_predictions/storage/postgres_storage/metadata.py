from sqlalchemy import Column, Integer, MetaData, String, Table

metadata = MetaData()

user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)
