import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 🔑 Bot token
TOKEN = "8492051752:AAF6zW7N_Djda1SJQTUdWWGhjw7L0N8R3_E"
# 👑 Admin ID
ADMIN_ID = 6189981072

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchi ma'lumotlari
user_data = {}

# Matnli masalalar shablonlari
text_templates = {
    "+": [
        "{a} ta olma bor edi, yana {b} ta oldi. Jami nechta?",
        "{a} ta kitob oldi, do'sti {b} ta berdi. Umumiy nechta?",
        "Sinfda {a} ta o'g'il bola, {b} ta qiz bola. Jami nechta bola?"
    ],
    "-": [
        "{a} ta shokolad bor edi, {b} tasini yedi. Qancha qoldi?",
        "{a} ta mashina bor edi, {b} tasi sotildi. Qancha qoldi?",
        "{a} ta qalam bor edi, {b} tasini yo'qotdi. Nechtasi qoldi?"
    ],
    "*": [
        "{a} ta guruhda, har birida {b} ta bola. Jami nechta bola?",
        "{a} ta quti, har birida {b} ta shirinlik. Jami nechta?",
        "{a} kunlik ish, har kuni {b} soat. Jami nechta soat?"
    ],
    "/": [
        "{a} ta olma {b} ta bolaga taqsimlandi. Har biriga nechta?",
        "{a} ta konfet {b} ta do'stga bo'lingan. Har biriga nechta?",
        "{a} ta metr mato {b} ta kiyimga. Har biriga nechta metr?"
    ]
}


# Savol generatori (100 ta savol, turli darajalar)
def generate_questions():
    questions = []
    operations = ["+", "-", "*", "/"]

    # 40 ta oson (1-200)
    for _ in range(40):
        op = random.choice(operations)
        if op == "+":
            a = random.randint(5, 200)
            b = random.randint(2, 200 - a if a < 200 else 50)
            ans = a + b
        elif op == "-":
            a = random.randint(5, 200)
            b = random.randint(2, a - 1)
            ans = a - b
        elif op == "*":
            a = random.randint(2, 20)
            b = random.randint(2, 10)
            ans = a * b
        else:  # "/"
            b = random.randint(2, 10)
            ans = random.randint(2, 20)
            a = ans * b

        wrongs = set()
        while len(wrongs) < 3:
            offset = random.randint(-10, 10)
            if offset != 0 and ans + offset > 0:
                wrongs.add(ans + offset)
        wrongs = list(wrongs)
        options = [ans] + wrongs
        random.shuffle(options)

        q_text = f"{a} {op} {b} = ?" if random.random() > 0.2 else random.choice(text_templates[op]).format(a=a, b=b)
        questions.append(
            {"q": q_text, "options": [str(o) for o in options], "answer": options.index(ans), "level": "Oson"})

    # 30 ta o'rtacha (1-600)
    for _ in range(30):
        op = random.choice(operations)
        if op == "+":
            a = random.randint(50, 600)
            b = random.randint(10, 600 - a if a < 600 else 100)
            ans = a + b
        elif op == "-":
            a = random.randint(50, 600)
            b = random.randint(10, a - 1)
            ans = a - b
        elif op == "*":
            a = random.randint(10, 30)
            b = random.randint(5, 20)
            ans = a * b
        else:  # "/"
            b = random.randint(5, 20)
            ans = random.randint(5, 30)
            a = ans * b

        wrongs = set()
        while len(wrongs) < 3:
            offset = random.randint(-20, 20)
            if offset != 0 and ans + offset > 0:
                wrongs.add(ans + offset)
        wrongs = list(wrongs)
        options = [ans] + wrongs
        random.shuffle(options)

        q_text = f"{a} {op} {b} = ?" if random.random() > 0.2 else random.choice(text_templates[op]).format(a=a, b=b)
        questions.append(
            {"q": q_text, "options": [str(o) for o in options], "answer": options.index(ans), "level": "O'rtacha"})

    # 20 ta qiyin (1-1000)
    for _ in range(20):
        op = random.choice(operations)
        if op == "+":
            a = random.randint(100, 1000)
            b = random.randint(50, 1000 - a if a < 1000 else 200)
            ans = a + b
        elif op == "-":
            a = random.randint(100, 1000)
            b = random.randint(50, a - 1)
            ans = a - b
        elif op == "*":
            a = random.randint(20, 50)
            b = random.randint(10, 20)
            ans = a * b
        else:  # "/"
            b = random.randint(10, 20)
            ans = random.randint(10, 50)
            a = ans * b

        wrongs = set()
        while len(wrongs) < 3:
            offset = random.randint(-50, 50)
            if offset != 0 and ans + offset > 0:
                wrongs.add(ans + offset)
        wrongs = list(wrongs)
        options = [ans] + wrongs
        random.shuffle(options)

        q_text = f"{a} {op} {b} = ?" if random.random() > 0.2 else random.choice(text_templates[op]).format(a=a, b=b)
        questions.append(
            {"q": q_text, "options": [str(o) for o in options], "answer": options.index(ans), "level": "Qiyin"})

    # 10 ta juda qiyin (1-5000)
    for _ in range(10):
        op = random.choice(operations)
        if op == "+":
            a = random.randint(500, 5000)
            b = random.randint(100, 5000 - a if a < 5000 else 500)
            ans = a + b
        elif op == "-":
            a = random.randint(500, 5000)
            b = random.randint(100, a - 1)
            ans = a - b
        elif op == "*":
            a = random.randint(50, 100)
            b = random.randint(20, 50)
            ans = a * b
        else:  # "/"
            b = random.randint(20, 50)
            ans = random.randint(20, 100)
            a = ans * b

        wrongs = set()
        while len(wrongs) < 3:
            offset = random.randint(-100, 100)
            if offset != 0 and ans + offset > 0:
                wrongs.add(ans + offset)
        wrongs = list(wrongs)
        options = [ans] + wrongs
        random.shuffle(options)

        q_text = f"{a} {op} {b} = ?" if random.random() > 0.2 else random.choice(text_templates[op]).format(a=a, b=b)
        questions.append(
            {"q": q_text, "options": [str(o) for o in options], "answer": options.index(ans), "level": "Juda qiyin"})

    random.shuffle(questions)
    return questions


def get_keyboard(q_index: int, questions):
    buttons = []
    opts = questions[q_index]["options"]
    buttons.append([
        InlineKeyboardButton(text=opts[0], callback_data=f"{q_index}:0"),
        InlineKeyboardButton(text=opts[1], callback_data=f"{q_index}:1")
    ])
    buttons.append([
        InlineKeyboardButton(text=opts[2], callback_data=f"{q_index}:2"),
        InlineKeyboardButton(text=opts[3], callback_data=f"{q_index}:3")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Vaqtni boshqarish uchun
async def question_timer(user_id, q_index, questions, message):
    await asyncio.sleep(60)  # 1 daqiqa kutish
    if user_id in user_data and user_data[user_id]["current"] == q_index:
        data = user_data[user_id]
        data["current"] += 1
        next_q = data["current"]

        await message.answer("⏰ Vaqt tugadi! Bu savol xato deb hisoblanadi.")

        if next_q < len(questions):
            q = questions[next_q]
            new_message = await message.answer(
                f"Savol {next_q + 1}/{len(questions)} ({q['level']}):\n{q['q']}",
                reply_markup=get_keyboard(next_q, questions)
            )
            asyncio.create_task(question_timer(user_id, next_q, questions, new_message))
        else:
            await finish_test(user_id, message)


async def finish_test(user_id, message):
    data = user_data[user_id]
    score = data["score"]
    total = len(data["questions"])
    percent = round((score / total) * 100)

    if percent >= 80:
        status = "✅ Siz testdan o‘tdingiz!"
    else:
        status = "❌ Siz testdan o‘tolmadingiz! Yana urinib ko'ring."

    await message.answer(
        f"📊 Test tugadi!\n"
        f"To‘g‘ri javoblar: {score}/{total}\n"
        f"Foiz: {percent}%\n\n"
        f"{status}"
    )

    # Adminni ogohlantirish
    fullname = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"
    await bot.send_message(
        ADMIN_ID,
        f"📊 {fullname} (ID: {user_id}, {username}) testni tugatdi.\n"
        f"✅ To‘g‘ri: {score}/{total}\n"
        f"📈 Foiz: {percent}%\n"
        f"{status}"
    )

    user_data.pop(user_id)


# /start komandasi
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    fullname = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"
    await message.answer(
        "👋 Salom! Men Matematika Test Botiman. 4-sinf bolalari uchun mo'ljallangan.\n"
        "Testni boshlash uchun /test yozing.\n"
        "Qo‘shimcha yordam uchun /help buyrug‘ini bering."
    )
    await bot.send_message(
        ADMIN_ID,
        f"📥 Yangi foydalanuvchi start bosdi!\n\n"
        f"👤 Fullname: {fullname}\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"🔗 Username: {username}"
    )


# /help komandasi
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ Botdan foydalanish yo‘riqnomasi:\n\n"
        "/start – Botni ishga tushirish\n"
        "/help – Yordam\n"
        "/test – 100 ta savollik matematika testini boshlash (4-sinf darajasida)\n\n"
        "⏰ Har bir savol uchun 1 daqiqa vaqt beriladi.\n"
        "✅ Test tugagach, natijangiz foiz hisobida chiqadi. 80% va undan yuqori bo'lsa, o'tdingiz!"
    )


# /test komandasi
@dp.message(Command("test"))
async def cmd_test(message: types.Message):
    user_id = message.from_user.id
    questions = generate_questions()

    user_data[user_id] = {"score": 0, "current": 0, "questions": questions}

    q = questions[0]
    new_message = await message.answer(
        f"Savol 1/{len(questions)} ({q['level']}):\n{q['q']}",
        reply_markup=get_keyboard(0, questions)
    )

    # Adminni ogohlantirish
    fullname = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"
    await bot.send_message(
        ADMIN_ID,
        f"📝 {fullname} (ID: {user_id}, {username}) testni boshladi."
    )

    # Timer start
    asyncio.create_task(question_timer(user_id, 0, questions, new_message))


# Javoblarni qayta ishlash
@dp.callback_query(F.data)
async def process_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_data:
        await callback.answer("Avval /test buyrug‘ini bering.", show_alert=True)
        return

    data = user_data[user_id]
    q_index, opt_index = map(int, callback.data.split(":"))
    if q_index != data["current"]:
        await callback.answer("Bu savol allaqachon o'tib ketdi!", show_alert=True)
        return

    questions = data["questions"]
    correct = questions[q_index]["answer"]

    if opt_index == correct:
        data["score"] += 1
        await callback.answer("✅ To‘g‘ri!")
    else:
        correct_text = questions[q_index]["options"][correct]
        await callback.answer(f"❌ Noto‘g‘ri! To‘g‘ri javob: {correct_text}")

    data["current"] += 1
    next_q = data["current"]

    if next_q < len(questions):
        q = questions[next_q]
        new_message = await callback.message.answer(
            f"Savol {next_q + 1}/{len(questions)} ({q['level']}):\n{q['q']}",
            reply_markup=get_keyboard(next_q, questions)
        )
        asyncio.create_task(question_timer(user_id, next_q, questions, new_message))
    else:
        await finish_test(user_id, callback.message)

    await callback.message.delete()


async def main():
    print(f"Bot ishga tushdi...✅")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

    
