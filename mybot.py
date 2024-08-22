
from pyrogram import Client, filters
from pyrogram.types import Message,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,CallbackQuery
from pyrogram.handlers import MessageHandler
import asyncio, logging, random, datetime
from pytz import timezone
from MySQLDatabase import db, User
from MySQLDatabase import Message as db_Message
logging.basicConfig(level=logging.DEBUG)
api_id = 27561080
api_hash = "f3eaaf759cbabd85281cf299669110e0"
bot_token = "7493225528:AAHm1ttLQdiKaHtozifsD88qiW6wGAQKQVM"

async def check_db(username, id, link):
    db.connect()
    user_exists = User.select().where(User.username == username).exists()
    if user_exists :
        pass
    else:
        db_message = User.create(
            username=username,
            id=id,
            link=link,
            joined_date=datetime.datetime.now(timezone('Asia/Tehran')).strftime('%Y:%m:%d %H:%M:%S %Z') )    
    db.close()

app = Client("my_botn", api_id=int(api_id), api_hash=api_hash,bot_token=bot_token)
#key1 = [KeyboardButton("hi")]
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
    random.seed(message.from_user.id)
    user_id="".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",k=10))
    user_link=f"https://t.me/myanonychatbot?start={user_id}"
    print(user_link)
    keyboard = InlineKeyboardMarkup([[key1,key2],[key3,key4]])
    await message.reply(text=welcome_text, reply_markup = keyboard)
    print("hi")

@app.on_message(filters.regex("^/start\s\w{10}$"))
async def start(client, message):
    print("hi\nIam here\n\n you know what you are doing")
    await check_db(message.from_user.username, message.from_user.id, message.text.split(" ")[1])
    print("inja")
    user = User.get(User.link == f'{message.text.split(" ")[1]}')
    text=f"در حال ارسال پیام ناشناس به {user} هستی.\nهر انتقاد یا حرفی که داری رو میتونی بهش بگی چون پیامت به صورت ناشناس به دستش میرسه!"
    await message.reply(text=text)
    


@app.on_callback_query(filters.regex("mylink"))
async def link(client, cbq:CallbackQuery):
    print(f"this is command5{cbq.from_user.id}")
    chat_id=cbq.from_user.first_name
    random.seed(chat_id)
    user_id="".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",k=10))
    user_link=f"https://t.me/myfchatbot?start={user_id}"
    keyboard = InlineKeyboardMarkup([[key1,key2],[key3,key4]])
    invite_text=f""" سلام {chat_id} هستم \nلینک زیر رو لمس کن و هر حرفی که تو دلت هست یا هر انتقادی که نسبت به من داری رو با خیال راحت بنویس و بفرست. بدون اینکه از اسمت باخبر بشم پیامت به من می‌رسه. خودتم می‌تونی امتحان کنی و از بقیه بخوای راحت و ناشناس بهت پیام بفرستن، حرفای خیلی جالبی می‌شنوی! 😉\n\n {user_link}"""
    await cbq.edit_message_text(text=invite_text,reply_markup = keyboard)

@app.on_callback_query(filters.regex("backtostart"))
async def hi(client, cbq:CallbackQuery):
    print(f"this is command5{cbq.from_user.id}")
    chat_id=cbq.from_user.id
    #await cbq.answer("عملیات با موفقیت انجام شد", show_alert=True)   
    # You can also edit the message to provide feedback
    keyboard = InlineKeyboardMarkup([[key1,key2],[key3,key4]])
    await cbq.edit_message_text("شما به منوی اصلی بازگشتید\nچه کاری میتوانم برایتان انجام دهم؟",reply_markup = keyboard)



logging.info("debug logiing:")
app.run()

