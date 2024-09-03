from peewee import MySQLDatabase, OperationalError
from peewee import Model, CharField, IntegerField, AutoField, BigIntegerField, TextField, BooleanField, DateTimeField, SQL
from datetime import datetime
from pyrogram.types import Message

db_name = 'mybot_db'
db_user = 'mohammad'
db_pass = 'Mr.mrn1041378'
db_host_ip = 'mysql'
db = MySQLDatabase(
    database = db_name ,  # Replace with your database name
    user = db_user,
    password = db_pass,
    host=db_host_ip,
    port=3306   
)
   

class User(Model):
    username = CharField(unique=True,max_length=32)
    id = BigIntegerField(unique=True)
    link =CharField(unique=True)
    joined_date =CharField()       
    class Meta:
        database = db  # This model uses the "db" database.
        table_name = 'Users'  # Optional: Specify the table name
class Message(Model):
    id = AutoField()  # شناسه یکتا
    user_id = BigIntegerField()  # شناسه کاربر
    username = CharField(max_length=255, null=True)  # نام کاربری
    chat_id = BigIntegerField()  # شناسه چت
    message_id = BigIntegerField()  # شناسه پیام
    message_text = TextField(null=True)  # متن پیام
    message_date = DateTimeField()  # تاریخ و زمان دریافت پیام
    message_type = CharField(max_length=50, null=True)  # نوع پیام
    is_command = BooleanField(default=False)  # آیا پیام یک دستور است یا خیر
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    image_id=BigIntegerField()
    class Meta:
        database = db  # This model uses the "db" database.
        table_name = 'Messages'  # Optional: Specify the table name
def create_table():
    try:
        db.connect()
        # Perform a simple query to check if the database connection is working
        #db.execute_sql("SELECT 1;")
        print("Database exists")
        db.create_tables([User, Message])
        tables = db.get_tables()
        user_exists = User.select().where(User.username == "mr_anonymousq").exists()
        print(user_exists)
    # Print the list of tables
        print("Existing tables in the database:", tables)
    except OperationalError as e:
        print("Database does not exist or an error occurred:", e)
    finally:
        db.close()
        print("end")
def table_exists():
    db.connect()
    return db.table_exists(User._meta.table_name)


