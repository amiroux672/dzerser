import logging
import requests
import telebot
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import aiohttp
import asyncio

# ضبط إعدادات تسجيل الدخول
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO
)
logger = logging.getLogger()

# روابط الـ API مع معرّف اللاعب (UID)
api_url = "https://free-ff-api.onrender.com/api/v1/account?region=me&uid={}"

# عدد الطلبات التي تريد إرسالها

# قائمة لتخزين أيديات المجموعات المسموح بها
allowed_chats = [-1002199181721]  #

# إنشاء بوت تيلجرام
bot = telebot.TeleBot("6480987684:AAGSp2l0_xXZiJp9l8C0NXuwjRmu3C2-KVE")

# دالة البداية للبوت
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, ' \nارسل  الأيدي لمعرفت حالة لحساب \n\nلجلب معلومات\n/a id\nلي لارسال زوار\n/visit id\nلمعرفت الإحصائيات لاعب\n--id')

# دالة للتحقق من إذن المجموعة
def is_allowed_chat(chat_id):
    return chat_id in allowed_chats



# وظيفة لجلب معلومات اللاعب
def get_player_info(uid):
    response = requests.get(api_url.format(uid))
    if response.status_code == 200:
        return response.json()
    else:
        return None

# دالة للتعامل مع جلب معلومات اللاعب
@bot.message_handler(commands=['a'])
def player_info(message):
    chat_id = message.chat.id
    args = message.text.split()
    
    if is_allowed_chat(chat_id):
        if len(args) > 1:
            uid = args[1]
            data = get_player_info(uid)
            if data:
                basic_info = data.get('basicInfo', {})
                captain_info = data.get('captainBasicInfo', {})
                clan_info = data.get('clanBasicInfo', {})
                credit_info = data.get('creditScoreInfo', {})
                pet_info = data.get('petInfo', {})
                profile_info = data.get('profileInfo', {})
                social_info = data.get('socialInfo', {})

                info = (
                    f"┌ 📋 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗵𝗶𝘀𝘁𝗼𝗿𝘆  [×] \n"
                    f"├─ Last Login : {basic_info.get('lastLoginAt', 'N/A')}\n"
                    f"└─ Created At : {basic_info.get('createAt', 'N/A')}\n\n"

                    f"┌ 👤 𝗔𝗰𝗰𝗼𝘂𝗻𝘁 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝘁𝗶𝗼𝗻 \n"
                    f"├─ Account ID : {basic_info.get('accountId', 'N/A')}\n"
                    f"├─ Nickname : {basic_info.get('nickname', 'N/A')}\n"
                    f"├─ Level : {basic_info.get('level', 'N/A')}\n"
                    f"├─ Likes : {basic_info.get('liked', 'N/A')}\n"
                    f"├─ Experience : {basic_info.get('exp', 'N/A')}\n"
                    f"├─ Avatar : {profile_info.get('avatarId', 'N/A')}\n"
                    f"├─ Banner : {basic_info.get('title', 'N/A')}\n"
                    f"├─ Rank : {basic_info.get('rank', 'N/A')}\n"
                    f"├─ Ranking Points : {basic_info.get('rankingPoints', 'N/A')}\n"
                    f"├─ Badge Count : {basic_info.get('badgeCnt', 'N/A')}\n"
                    f"├─ Booyah Pass : {basic_info.get('hasElitePass', 'N/A')}\n"
                    f"├─ CS Rank : {basic_info.get('csRank', 'N/A')}\n"
                    f"├─ CS Ranking Points : {basic_info.get('csRankingPoints', 'N/A')}\n"
                    f"└─ Bio : {social_info.get('signature', 'N/A')}\n\n"

                    f"┌ 🛡️ 𝗚𝗨𝗜𝗟𝗗 𝗜𝗡𝗙𝗢 \n"
                    f"├─ Clan ID : {clan_info.get('clanId', 'N/A')}\n"
                    f"├─ Clan Name : {clan_info.get('clanName', 'N/A')}\n"
                    f"├─ Level : {clan_info.get('clanLevel', 'N/A')}\n"
                    f"├─ Capacity : {clan_info.get('capacity', 'N/A')}\n"
                    f"├─ Member Num : {clan_info.get('memberNum', 'N/A')}\n"
                    f"└─ Captain Name : {captain_info.get('nickname', 'N/A')}\n\n"

                    f"┌ ♻️ 𝗚𝗨𝗜𝗟𝗗 𝗟𝗘𝗔𝗗𝗘𝗥 𝗜𝗡𝗙𝗢 \n"
                    f"├─ Nickname : {captain_info.get('nickname', 'N/A')}\n"
                    f"├─ Level : {captain_info.get('level', 'N/A')}\n"
                    f"├─ Exp : {captain_info.get('exp', 'N/A')}\n"
                    f"├─ Rank : {captain_info.get('rank', 'N/A')}\n"
                    f"├─ Ranking Points : {captain_info.get('rankingPoints', 'N/A')}\n"
                    f"├─ Badge Count : {captain_info.get('badgeCnt', 'N/A')}\n"
                    f"├─ Likes : {captain_info.get('liked', 'N/A')}\n"
                    f"├─ CS Rank : {captain_info.get('csRank', 'N/A')}\n"
                    f"├─ CS Ranking Points : {captain_info.get('csRankingPoints', 'N/A')}\n"
                    f"├─ Last Login At : {captain_info.get('lastLoginAt', 'N/A')}\n"
                    f"└─ Created At : {captain_info.get('createAt','N/A')}\n\n"

                    f"┌ 🐾 𝗣𝗘𝗧 𝗜𝗡𝗙𝗢 \n"
                    f"├─ Pet ID : {pet_info.get('id', 'N/A')}\n"
                    f"├─ Pet Name : {pet_info.get('name', 'N/A')}\n"
                    f"├─ Pet Level : {pet_info.get('level', 'N/A')}\n"
                    f"├─ Pet Experience : {pet_info.get('exp', 'N/A')}\n"
                    f"└─ Selected Skill : {pet_info.get('selectedSkillId', 'N/A')}\n\n"


                    f"┌  🚧 𝗠𝗬 𝗔𝗖𝗖𝗢𝗨𝗡𝗧𝗦 \n@nkmok"
                  
                )
                bot.reply_to(message, info)
            else:
                bot.reply_to(message, "لم أتمكن من جلب المعلومات.")
        else:
            bot.reply_to(message, 'يرجى توفير UID بعد الأمر ')
    else:
        bot.reply_to(message, 'هذه المجموعة غير مسموح لها باستخدام هذا الأمر.')
 
 
 
 
def get_player_stats(uid):
    url = f"https://free-ff-api.onrender.com/api/v1/playerstats?region=ME&uid={uid}"
    response = requests.get(url)
    
    if response.status_code == 200:
        player_stats = response.json()
        return player_stats
    else:
        return f"فشل في جلب البيانات. رمز الحالة: {response.status_code}"

# دالة لتنسيق إحصائيات اللاعب
def format_player_stats(player_stats):
    if isinstance(player_stats, dict):
        result = "\nإحصائيات اللاعب:\n\n"
        
        solo_stats = player_stats.get('soloStats', {})
        duo_stats = player_stats.get('duoStats', {})
        quad_stats = player_stats.get('quadStats', {})

        result += "\nإحصائيات الفردي (Solo Stats):\n"
        result += f"رقم الحساب: {solo_stats.get('accountId')}\n"
        result += f"الألعاب الملعوبة: {solo_stats.get('gamesPlayed')}\n"
        result += f"القتلات: {solo_stats.get('kills')}\n"
        detailed_solo = solo_stats.get('detailedStats', {})
        result += f"  الوفيات: {detailed_solo.get('deaths')}\n"
        result += f"  المسافة المقطوعة: {detailed_solo.get('distanceTravelled')}\n"
        result += f"  وقت البقاء: {detailed_solo.get('survivalTime')}\n"
        result += f"  أعلى عدد من القتلات: {detailed_solo.get('highestKills')}\n"
        result += f"  الضرر: {detailed_solo.get('damage')}\n"
        result += f"  الرؤوس الحمراء: {detailed_solo.get('headshots')}\n"
        result += f"  قتلات بالرأس: {detailed_solo.get('headshotKills')}\n"
        result += f"  الحصول على الأدوات: {detailed_solo.get('pickUps')}\n"

        result += "\nإحصائيات الثنائي (Duo Stats):\n"
        result += f"رقم الحساب: {duo_stats.get('accountId')}\n"
        result += f"الألعاب الملعوبة: {duo_stats.get('gamesPlayed')}\n"
        result += f"الانتصارات: {duo_stats.get('wins')}\n"
        result += f"القتلات: {duo_stats.get('kills')}\n"
        detailed_duo = duo_stats.get('detailedStats', {})
        result += f"  الوفيات: {detailed_duo.get('deaths')}\n"
        result += f"  عدد مرات الوصول لأعلى: {detailed_duo.get('topNTimes')}\n"
        result += f"  المسافة المقطوعة: {detailed_duo.get('distanceTravelled')}\n"
        result += f"  وقت البقاء: {detailed_duo.get('survivalTime')}\n"
        result += f"  أعلى عدد من القتلات: {detailed_duo.get('highestKills')}\n"
        result += f"  الضرر: {detailed_duo.get('damage')}\n"
        result += f"  الرؤوس الحمراء: {detailed_duo.get('headshots')}\n"
        result += f"  قتلات بالرأس: {detailed_duo.get('headshotKills')}\n"
        result += f"  عدد الضربات التي أسقطتهم: {detailed_duo.get('knockDown')}\n"
        result += f"  الحصول على الأدوات: {detailed_duo.get('pickUps')}\n"

        result += "\nإحصائيات الرباعي (Quad Stats):\n"
        result += f"رقم الحساب: {quad_stats.get('accountId')}\n"
        result += f"الألعاب الملعوبة: {quad_stats.get('gamesPlayed')}\n"
        result += f"الانتصارات: {quad_stats.get('wins')}\n"
        result += f"القتلات: {quad_stats.get('kills')}\n"
        detailed_quad = quad_stats.get('detailedStats', {})
        result += f"  الوفيات: {detailed_quad.get('deaths')}\n"
        result += f"  عدد مرات الوصول لأعلى: {detailed_quad.get('topNTimes')}\n"
        result += f"  المسافة المقطوعة: {detailed_quad.get('distanceTravelled')}\n"
        result += f"  وقت البقاء: {detailed_quad.get('survivalTime')}\n"
        result += f"  عدد الإحياء: {detailed_quad.get('revives')}\n"
        result += f"  أعلى عدد من القتلات: {detailed_quad.get('highestKills')}\n"
        result += f"  الضرر: {detailed_quad.get('damage')}\n"
        result += f"  الرؤوس الحمراء: {detailed_quad.get('headshots')}\n"
        result += f"  قتلات بالرأس: {detailed_quad.get('headshotKills')}\n"
        result += f"  عدد الضربات التي أسقطتهم: {detailed_quad.get('knockDown')}\n"
        result += f"  الحصول على الأدوات: {detailed_quad.get('pickUps')}\n"
        return result
    else:
        return player_stats

# دالة لإرسال رسالة طويلة بشكل مقسم
def send_long_message(chat_id, text, bot, chunk_size=4096):
    for i in range(0, len(text), chunk_size):
        bot.send_message(chat_id, text[i:i+chunk_size])



# استقبال الرسائل التي تبدأ بـ '++'
@bot.message_handler(func=lambda message: message.text.startswith('--'))
def send_player_stats(message):
    uid = message.text[2:]  # إزالة '++' من البداية
    player_stats = get_player_stats(uid)
    formatted_stats = format_player_stats(player_stats)
    send_long_message(message.chat.id, formatted_stats, bot)


async def send_visit(session, url, counter):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            counter[0] += 1
            if counter[0] % 100 == 0:
                print(f"Visited {counter[0]} times successfully.")
    except aiohttp.ClientError as e:
        pass

async def send_visits(uid, num_visits=100):
    region = "ME"
    url = f"https://free-ff-api.onrender.com/api/v1/account?region=me&uid={uid}"
    counter = [0]

    async with aiohttp.ClientSession() as session:
        tasks = [send_visit(session, url, counter) for _ in range(num_visits)]
        await asyncio.gather(*tasks)

        # إذا وصلنا هنا، فقد قمنا بإرسال الزيارات بنجاح
        print(f"Successfully sent {num_visits} visits to {uid}")

@bot.message_handler(commands=['v'])
def handle_visit(message):
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "هناك خطأ في الايدي أو ربما لم تضع الايدي.")
        else:
            uid = parts[1].strip()
            if not uid.isdigit():
                bot.reply_to(message, "هذا الايدي غير صالح.")
            else:
                num_visits = int(parts[2].strip()) if len(parts) > 2 else 100
                if num_visits > 100:  # التحقق من الحد الأقصى لعدد المشاهدات
                    num_visits = 100
                bot.reply_to(message, "A visit will be sent  ")
                asyncio.run(send_visits(uid, num_visits))
                bot.reply_to(message, f"💎 Successfully sent {num_visits} visits to {uid}💎")


cookies = {
    'source': 'mb',
    '_gid': 'GA1.2.1236421304.1706295770',
    '_gat_gtag_UA_137597827_4': '1',
    'session_key': 'hnl4y8xtfe918iiz2go67z85nsrvwqdn',
    '_ga': 'GA1.2.1006342705.1706295770',
    'datadome': '3AmY3lp~TL1WEuDKCnlwro_WZ1C6J66V1Y0TJ4ITf1Hvo4833Fh4LF3gHrPCKFJDPUPoXh2dXQHJ_uw0ifD8jmCaDltzE5T3zzRDbXOKH9rPNrTFs29DykfP3cfo7QGy',
    '_ga_R04L19G92K': 'GS1.1.1706295769.1.1.1706295794.0.0.0',
}

headers = {
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Origin': 'https://shop.garena.sg',
    'Referer': 'https://shop.garena.sg/app/100067/idlogin',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'accept': 'application/json',
    'content-type': 'application/json',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'x-datadome-clientid': 'DLm2W1ajJwdv~F~a_1d_1PyWnW6ns7GY5ChVcZY3HJ9r6D29661473aQaL2~3Nfh~Vf3m7rie7ObIb1_3eRN7J0G6uFZhMq5pM2jA828fE1dS7rZ7H3MWGQ5vGraAQWd',
}

def get_data(UID):
    json_data = {
        'app_id': 100067,
        'login_id': UID,
        'app_server_id': 0,
    }
    
    response = requests.post('https://shop.garena.sg/api/auth/player_id_login', cookies=cookies, headers=headers, json=json_data)
    return response.json()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! يرجى إرسال معرف اللاعب.")

@bot.message_handler(func=lambda message: True)
def show_player_info(message):
    try:
        UID = message.text
        player_info = get_data(UID)
        
        if 'region' in player_info and 'nickname' in player_info:
            nickname = player_info['nickname']
            region = player_info['region']
            status = player_info.get('status', 'ME')         
            developer = player_info.get('developer', 'A    I    Z      E      N')
            level =player_info.get('level', 'level')
            
            reply_text = (
                "┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                "┃🧾 PLAYER INFO \n"
                "┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                f"┃🔰 ID : {UID}\n"
                "┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                f"┃👤 NAME : {nickname}\n"
                "┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                f"┃🌐 REGION : {region}\n"
                "┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                f"┃👾 STATUS : {status}\n"
                "┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
            )
            reply_text = (
                "┏ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                "┃🧾 معلومات الاعب \n"
                "┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                f"┃🔰 ايدي : {UID}\n"
                "┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                f"┃👤 الاسم : {nickname}\n"
                "┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                f"┃🌐 سيرفر : {region}\n"
                "┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                f"┃👾 حالة الاعب  : غير مبند\n"
                "┣ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━ ━\n"
                        )
            
            bot.reply_to(message, reply_text)
        else:
            bot.reply_to(message, "")
    except Exception as e:
        bot.reply_to(message, "An error occurred: " + str(e))
# بدء البوت
bot.polling()