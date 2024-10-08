from peewee import OperationalError
from pyrogram import Client, filters
from pyrogram.types import Message,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,CallbackQuery
from pyrogram.handlers import MessageHandler
import asyncio, logging, random, time, datetime, json
from pytz import timezone
from MySQLDatabase import db, User, create_table, table_exists
from MySQLDatabase import Message as db_Message
logging.basicConfig(level=logging.DEBUG)
with open('config.json', 'r') as file:
    config = json.load(file)

bot_id = config['bot_id']
api_id = config['api_id']
api_hash = config['api_hash']
bot_token = config['bot_token']
if table_exists():
    print("Table  exists.")
else:
    print("Table does not exist.")
    db.close()
    create_table()
# Close the database connection
db.close()

proxy = {
     "scheme": "http",
     "hostname": "127.0.0.1",
     "port": 2081
 }
app = Client("my_botn", api_id=int(api_id), api_hash=api_hash,bot_token=bot_token)
async def check_db(username, id, link):
    print("Checking db")
    try:
        db.connect()
        print("connecting to db")
        user_exists = User.select().where(User.username == username).exists()
        if user_exists :
            print("user exist")
        else:
            print("id saved :",id)
            db_message = User.create(
                username=username,
                id=int(id),
                link=link,
                joined_date=datetime.datetime.now(timezone('Asia/Tehran')).strftime('%Y:%m:%d %H:%M:%S %Z') )
    except OperationalError:
        print("connecting to db by operational error")
        user_exists = User.select().where(User.username == username).exists()
        if user_exists :
            print("user exist")
        else:
            print("id saved :",id)
            db_message = User.create(
                username=username,
                id=int(id),
                link=link,
                joined_date=datetime.datetime.now(timezone('Asia/Tehran')).strftime('%Y:%m:%d %H:%M:%S %Z') )
    finally:    
        db.close()
        print("connection closed")

user_states = {}
user_recieve_states = {}
def link_creator(id:int):
    random.seed(id)
    user_str="".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",k=10))
    user_link=f"https://t.me/{bot_id}?start={user_str}"
    return user_link,user_str
#keyboard = ReplyKeyboardMarkup([key1])

key3 = InlineKeyboardButton("hi",callback_data="/command1")
key4 = InlineKeyboardButton("اتصال به ناشناس",callback_data="/command1")
key1 = InlineKeyboardButton("لینک ناشناس من",callback_data="/mylink")
key2 = InlineKeyboardButton("پروفایل ناشناس من",callback_data="/command2")
key5 = InlineKeyboardButton(" بازگشت به منوی اصلی",callback_data="/backtostart")


@app.on_message(filters.regex("^/start$"))
async def start(client, message):
    welcome_text = f"""سلام {message.from_user.first_name}
    به ربات چت ناشناس من خوش آمدید
    چه کاری میتوانم برایتان انجام دهم؟
    """
    print(message)
    user_str = link_creator(message.from_user.id)[1]
    await check_db(message.from_user.username, message.from_user.id, user_str)
    user_link = link_creator(message.from_user.id)[0]
    print(user_link)
    keyboard = InlineKeyboardMarkup([[key1,key2],[key3,key4]])
    await message.reply(text=welcome_text, reply_markup = keyboard)
    print("hi")

@app.on_message(filters.regex("^/start[=\s]\w{10}$"))
async def start(client, message):
    user_str = link_creator(message.from_user.id)[1]
    print("hi\nIam here\n\n you know what you are doing")
    #await check_db(message.from_user.username, message.from_user.id, message.text.split(" ")[1])
    await check_db(message.from_user.username, message.from_user.id, user_str)
    print(message)
    print("inja")
    user_to_send = User.get(User.link == f'{message.text.split(" ")[1]}')
    user_states[message.from_user.id] = ["waiting_for_reply",{"to":user_to_send.id}]
    text=f"در حال ارسال پیام ناشناس به {user_to_send.username} هستی.\nهر انتقاد یا حرفی که داری رو میتونی بهش بگی چون پیامت به صورت ناشناس به دستش میرسه!"
    await message.reply(text=text)
    
@app.on_message(filters.text)
async def handle_reply(client, message: Message):
    user_id = message.from_user.id
    msg_id=message.msg_id
    if user_id in user_states and user_states[user_id][0] == "waiting_for_reply":
        print(user_states[user_id])
        user_response = message.text
        if user_states[user_id][1]["to"] in user_recieve_states[user_states[user_id][1]["to"]] :
            user_recieve_states[user_states[user_id][1]["to"]][1]["messages"].append(msg_id)
            user_recieve_states[user_states[user_id][1]["to"]][1]["messages"].append(user_response)
        else:
            user_recieve_states[user_states[user_id][1]["to"]]=["have_message",{"from":user_id,"messages":[msg_id,user_response]}]
        await message.reply(f"پیام شما دریافت و ارسال شد:\n {user_response}")
        key6 = InlineKeyboardButton("خواندن پیام",callback_data=f"/read_message `` {msg_id}")
        await client.send_message(user_states[user_id][1]["to"],text=f"یک پیام ناشناس جدید داری ",reply_markup = InlineKeyboardMarkup([[key6]]))
        print(user_states)
        print(user_states[user_id])
        del user_states[user_id]
        print(user_states)

@app.on_callback_query(filters.regex("read_message"))
async def link(client, cbq:CallbackQuery):
    user_id = cbq.from_user.id
    msg_id = cbq.data.split(" `` ")[1]#this comes from the bottom and must delete a msg that its id is msg_id
    msg_index=user_recieve_states[user_id][1]["messages"].index(msg_id)
    response=user_recieve_states[user_id][1]["messages"][msg_index+1]
    user_link=link_creator(user_states[user_id][1]["from"])[0]
    await client.send_message(user_states[user_id][1]["from"],text=f"{cbq.from_user.first_name}پیام شما را خواند")
    key7 = InlineKeyboardButton("  ار سال پاسخ ",url=user_link)
    await cbq.edit_message_text(text=f"{response} \n")
    await client.send_message(user_id,text=f" در صورتی که میخواهید پاسخی ارسال کنید بر روی دکمه زیر کلیک کنید:\n ",reply_markup = InlineKeyboardMarkup([[key7]]))
    if msg_index==0:
        del user_recieve_states[user_id]
    else:
        del user_recieve_states[user_id][1]["messages"][msg_index:msg_index+2]


@app.on_callback_query(filters.regex("mylink"))
async def link(client, cbq:CallbackQuery):
    chat_id=cbq.from_user.id
    print(f"this is command5{chat_id}")
    user_link=link_creator(chat_id)[0]
    chat_name=cbq.from_user.first_name
    keyboard = InlineKeyboardMarkup([[key1,key2],[key3,key4]])
    invite_text=f""" سلام {chat_name} هستم \nلینک زیر رو لمس کن و هر حرفی که تو دلت هست یا هر انتقادی که نسبت به من داری رو با خیال راحت بنویس و بفرست. بدون اینکه از اسمت باخبر بشم پیامت به من می‌رسه. خودتم می‌تونی امتحان کنی و از بقیه بخوای راحت و ناشناس بهت پیام بفرستن، حرفای خیلی جالبی می‌شنوی! 😉\n\n {user_link}"""
    await cbq.edit_message_text(text=invite_text,reply_markup = keyboard)

@app.on_callback_query(filters.regex("backtostart"))
async def hi(client, cbq:CallbackQuery):
    print(f"this is command5{cbq.from_user.id}")
    chat_id=cbq.from_user.id
    #await cbq.answer("عملیات با موفقیت انجام شد", show_alert=True)   
    # You can also edit the message to provide feedback
    keyboard = InlineKeyboardMarkup([[key1,key2],[key3,key4]])
    await cbq.edit_message_text("شما به منوی اصلی بازگشتید\nچه کاری میتوانم برایتان انجام دهم؟",reply_markup = keyboard)



logging.info("debug loging:")
app.run()


