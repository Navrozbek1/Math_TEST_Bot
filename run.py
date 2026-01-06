import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 🔑 Bot token (o'zingiznikiga almashtiring)
TOKEN = "8492051752:AAF6zW7N_Djda1SJQTUdWWGhjw7L0N8R3_E"

# 👑 Admin ID (o'zingizning ID'ingiz)
ADMIN_ID = 6189981072

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchi ma'lumotlari (RAMda saqlanadi)
user_data = {}

# Matnli masalalar shablonlari (yosh bolalar uchun qiziqarliroq qilindi)
text_templates = {
    "+": [
        "{a} ta olma bor edi, yana {b} ta oldi. Jami nechta olma bo‘ldi?",
        "Do‘stim menga {a} ta konfet berdi, keyin {b} ta qo‘shdim. Hammasi nechta?",
        "Sinfda {a} ta o‘quvchi bor edi, bugun {b} ta yangi bola keldi. Jami nechta?"
    ],
    "-": [
        "{a} ta shokolad bor edi, {b} tasini yedim. Qancha shokolad qoldi?",
        "Ota-onam {a} ming so‘m berdi, {b} ming so‘m xarajat qildim. Qancha qoldi?",
        "{a} ta qalam bor edi, {b} tasini sinfdoshlarimga berdim. Nechta qoldi?"
    ],
    "*": [
        "{a} ta stol bor, har bir stol ustida {b} ta kitob. Jami nechta kitob?",
        "Har bir kunda {a} ta soat o‘qiyman, {b} kun davomida nechta soat bo‘ladi?",
        "{a} ta guruhda, har bir guruhda {b} ta bola. Hammasi nechta bola?"
    ],
    "/": [
        "{a} ta konfetni {b} ta do‘stga teng taqsimladik. Har biriga nechta?",
        "{a} ta olma {b} ta bolaga bo‘linganda, har bir bola nechta oladi?",
        "{a} metr mato {b} ta bir xil ko‘ylakka yetadi. Har bir ko‘ylakka nechta metr?"
    ]
}

def generate_questions():
    questions = []
    operations = ["+", "-", "*", "/"]

    # 12 ta OSON (1-120 oralig‘ida, oddiy sonlar)
    for _ in range(12):
        op = random.choice(operations)
        if op == "+":
            a = random.randint(5, 80)
            b = random.randint(3, 100 - a)
            ans = a + b
        elif op == "-":
            a = random.randint(10, 100)
            b = random.randint(2, a - 2)
            ans = a - b
        elif op == "*":
            a = random.randint(2, 10)
            b = random.randint(2, 8)
            ans = a * b
        else:  # "/"
            b = random.randint(2, 6)
            ans = random.randint(3, 12)
            a = ans * b

        wrongs = set()
        while len(wrongs) < 3:
            offset = random.randint(-6, 6)
            if offset != 0 and ans + offset > 0:
                wrongs.add(ans + offset)
        wrongs = list(wrongs)
        options = [ans] + wrongs
        random.shuffle(options)

        if random.random() > 0.35:
            q_text = random.choice(text_templates[op]).format(a=a, b=b)
        else:
            q_text = f"{a} {op} {b} = ?"

        questions.append({
            "q": q_text,
            "options": [str(o) for o in options],
            "answer": options.index(ans),
            "level": "Oson"
        })

    # 18 ta O‘RTACHA (30-400 oralig‘ida)
    for _ in range(18):
        op = random.choice(operations)
        if op == "+":
            a = random.randint(30, 300)
            b = random.randint(10, 350 - a)
            ans = a + b
        elif op == "-":
            a = random.randint(50, 350)
            b = random.randint(10, a - 5)
            ans = a - b
        elif op == "*":
            a = random.randint(6, 20)
            b = random.randint(4, 12)
            ans = a * b
        else:  # "/"
            b = random.randint(4, 10)
            ans = random.randint(6, 25)
            a = ans * b

        wrongs = set()
        while len(wrongs) < 3:
            offset = random.randint(-15, 15)
            if offset != 0 and ans + offset > 0:
                wrongs.add(ans + offset)
        wrongs = list(wrongs)
        options = [ans] + wrongs
        random.shuffle(options)

        if random.random() > 0.3:
            q_text = random.choice(text_templates[op]).format(a=a, b=b)
        else:
            q_text = f"{a} {op} {b} = ?"

        questions.append({
            "q": q_text,
            "options": [str(o) for o in options],
            "answer": options.index(ans),
            "level": "O‘rtacha"
        })

    # 15 ta QIYIN (150-1200 oralig‘ida)
    for _ in range(15):
        op = random.choice(operations)
        if op == "+":
            a = random.randint(150, 900)
            b = random.randint(50, 1000 - a)
            ans = a + b
        elif op == "-":
            a = random.randint(200, 1000)
            b = random.randint(50, a - 20)
            ans = a - b
        elif op == "*":
            a = random.randint(12, 35)
            b = random.randint(8, 20)
            ans = a * b
        else:  # "/"
            b = random.randint(8, 15)
            ans = random.randint(12, 50)
            a = ans * b

        wrongs = set()
        while len(wrongs) < 3:
            offset = random.randint(-40, 40)
            if offset != 0 and ans + offset > 0:
                wrongs.add(ans + offset)
        wrongs = list(wrongs)
        options = [ans] + wrongs
        random.shuffle(options)

        if random.random() > 0.25:
            q_text = random.choice(text_templates[op]).format(a=a, b=b)
        else:
            q_text = f"{a} {op} {b} = ?"

        questions.append({
            "q": q_text,
            "options": [str(o) for o in options],
            "answer": options.index(ans),
            "level": "Qiyin"
        })

    random.shuffle(questions)
    return questions  # 45 ta savol bo‘ladi

def get_keyboard(q_index: int, questions):
    opts = questions[q_index]["options"]
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=opts[0], callback_data=f"{q_index}:0"),
            InlineKeyboardButton(text=opts[1], callback_data=f"{q_index}:1")
        ],
        [
            InlineKeyboardButton(text=opts[2], callback_data=f"{q_index}:2"),
            InlineKeyboardButton(text=opts[3], callback_data=f"{q_index}:3")
        ]
    ])

async def question_timer(user_id, q_index, questions, message: types.Message):
    await asyncio.sleep(60)  # 60 sekund = 1 daqiqa
    if user_id in user_data and user_data[user_id].get("current") == q_index:
        data = user_data[user_id]
        data["current"] += 1
        next_q = data["current"]
        await message.answer("⏰ Vaqt tugadi! Bu savol xato hisoblanadi.")
        if next_q < len(questions):
            q = questions[next_q]
            new_msg = await message.answer(
                f"Savol {next_q + 1}/45 ({q['level']}):\n{q['q']}",
                reply_markup=get_keyboard(next_q, questions)
            )
            asyncio.create_task(question_timer(user_id, next_q, questions, new_msg))
        else:
            await finish_test(user_id, message)

async def finish_test(user_id, message: types.Message):
    if user_id not in user_data:
        return
    data = user_data[user_id]
    score = data["score"]
    total = len(data["questions"])  # 45
    percent = round((score / total) * 100, 1)

    status = "✅ Ajoyib! Testdan o‘tdingiz!" if percent >= 80 else "❌ Yana biroz mashq qilish kerak. Yana urinib ko‘ring!"

    await message.answer(
        f"🎉 Test yakunlandi!\n"
        f"To‘g‘ri javoblar: {score}/{total}\n"
        f"Foiz: {percent}%\n\n"
        f"{status}"
    )

    # Admin xabari
    fullname = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"
    await bot.send_message(
        ADMIN_ID,
        f"📊 {fullname} (ID: {user_id}, {username}) testni tugatdi\n"
        f"To‘g‘ri: {score}/{total}  |  {percent}%  |  {status}"
    )

    user_data.pop(user_id, None)

# ==================== HANDLERLAR ====================

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Salom! Men 4-sinf o‘quvchilari uchun Matematika Test Botiman.\n\n"
        "Testni boshlash: /test\n"
        "Yordam: /help"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ Qo‘llanma:\n\n"
        "/start — salomlashish\n"
        "/help — bu xabar\n"
        "/test — 45 ta savoldan iborat test boshlash\n\n"
        "⏱ Har bir savolga 1 daqiqa vaqt beriladi.\n"
        "80% va undan yuqori — testdan o‘tdingiz!"
    )

@dp.message(Command("test"))
async def cmd_test(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_data:
        await message.answer("Sizda allaqachon faol test bor. Avval uni tugating yoki /start bilan boshlang.")
        return

    questions = generate_questions()  # 45 ta savol
    user_data[user_id] = {"score": 0, "current": 0, "questions": questions}

    q = questions[0]
    msg = await message.answer(
        f"Savol 1/45 ({q['level']}):\n{q['q']}",
        reply_markup=get_keyboard(0, questions)
    )

    # Admin ogohlantirish
    fullname = message.from_user.full_name
    username = f"@{message.from_user.username}" if message.from_user.username else "yo‘q"
    await bot.send_message(ADMIN_ID, f"📝 {fullname} (ID: {user_id}, {username}) test boshladi.")

    asyncio.create_task(question_timer(user_id, 0, questions, msg))

@dp.callback_query(F.data)
async def process_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_data:
        await callback.answer("Avval /test buyrug‘ini bering.", show_alert=True)
        return

    data = user_data[user_id]
    try:
        q_index, opt_index = map(int, callback.data.split(":"))
    except:
        await callback.answer("Xato!", show_alert=True)
        return

    if q_index != data["current"]:
        await callback.answer("Bu savol allaqachon o‘tib ketgan.", show_alert=True)
        return

    questions = data["questions"]
    correct_idx = questions[q_index]["answer"]

    if opt_index == correct_idx:
        data["score"] += 1
        await callback.answer("✅ To‘g‘ri!")
    else:
        correct = questions[q_index]["options"][correct_idx]
        await callback.answer(f"❌ Xato! To‘g‘ri: {correct}")

    data["current"] += 1
    next_q = data["current"]

    await callback.message.delete()

    if next_q < len(questions):
        q = questions[next_q]
        new_msg = await callback.message.answer(
            f"Savol {next_q + 1}/45 ({q['level']}):\n{q['q']}",
            reply_markup=get_keyboard(next_q, questions)
        )
        asyncio.create_task(question_timer(user_id, next_q, questions, new_msg))
    else:
        await finish_test(user_id, callback.message)

async def main():
    print("Bot ishga tushdi... 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
