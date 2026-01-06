import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8492051752:AAF6zW7N_Djda1SJQTUdWWGhjw7L0N8R3_E"
ADMIN_ID = 6189981072

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

text_templates = {
    "+": ["{a} + {b} = ?"],
    "-": ["{a} - {b} = ?"],
    "*": ["{a} × {b} = ?"],
    "/": ["{a} ÷ {b} = ?"]
}

# ================== SAVOL GENERATOR ==================

def make_question(level):
    op = random.choice(["+", "-", "*", "/"])

    if level == "Oson":        # 5x qiyin
        if op == "+":
            a, b = random.randint(200, 500), random.randint(200, 500)
            ans = a + b
        elif op == "-":
            a, b = random.randint(300, 600), random.randint(100, 300)
            ans = a - b
        elif op == "*":
            a, b = random.randint(12, 25), random.randint(10, 20)
            ans = a * b
        else:
            b = random.randint(6, 15)
            ans = random.randint(10, 30)
            a = ans * b

    elif level == "O‘rtacha":  # 10x qiyin
        if op == "+":
            a, b = random.randint(800, 2000), random.randint(500, 1500)
            ans = a + b
        elif op == "-":
            a, b = random.randint(1000, 2500), random.randint(300, 900)
            ans = a - b
        elif op == "*":
            a, b = random.randint(20, 50), random.randint(15, 35)
            ans = a * b
        else:
            b = random.randint(8, 20)
            ans = random.randint(20, 60)
            a = ans * b

    else:                     # QIYIN – 20x
        if op == "+":
            a, b = random.randint(3000, 9000), random.randint(2000, 7000)
            ans = a + b
        elif op == "-":
            a, b = random.randint(5000, 12000), random.randint(2000, 5000)
            ans = a - b
        elif op == "*":
            a, b = random.randint(40, 90), random.randint(25, 60)
            ans = a * b
        else:
            b = random.randint(15, 30)
            ans = random.randint(30, 100)
            a = ans * b

    wrongs = set()
    while len(wrongs) < 3:
        x = ans + random.randint(-ans//4, ans//4)
        if x != ans and x > 0:
            wrongs.add(x)

    options = [ans] + list(wrongs)
    random.shuffle(options)

    return {
        "q": random.choice(text_templates[op]).format(a=a, b=b),
        "options": [str(i) for i in options],
        "answer": options.index(ans),
        "level": level
    }

def generate_questions():
    q = []
    q += [make_question("Oson") for _ in range(15)]
    q += [make_question("O‘rtacha") for _ in range(15)]
    q += [make_question("Qiyin") for _ in range(10)]
    random.shuffle(q)
    return q

# ================== KEYBOARD ==================

def keyboard(qi, qs):
    o = qs[qi]["options"]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=o[0], callback_data=f"{qi}:0"),
         InlineKeyboardButton(text=o[1], callback_data=f"{qi}:1")],
        [InlineKeyboardButton(text=o[2], callback_data=f"{qi}:2"),
         InlineKeyboardButton(text=o[3], callback_data=f"{qi}:3")]
    ])

# ================== TIMER (REAL COUNTDOWN) ==================

async def timer(uid, qi, msg):
    for sec in range(60, 0, -1):
        await asyncio.sleep(1)
        if uid not in user_data or user_data[uid]["current"] != qi:
            return
        try:
            await msg.edit_text(
                user_data[uid]["text"] + f"\n\n⏳ Qolgan vaqt: {sec} s",
                reply_markup=msg.reply_markup
            )
        except:
            pass

    if uid in user_data and user_data[uid]["current"] == qi:
        user_data[uid]["current"] += 1
        await msg.answer("⏰ Vaqt tugadi!")
        await next_question(uid, msg)

# ================== NEXT ==================

async def next_question(uid, msg):
    data = user_data[uid]
    qi = data["current"]

    if qi >= len(data["questions"]):
        await finish(uid, msg)
        return

    q = data["questions"][qi]
    text = f"Savol {qi+1}/40 ({q['level']}):\n{q['q']}"
    data["text"] = text
    m = await msg.answer(text, reply_markup=keyboard(qi, data["questions"]))
    asyncio.create_task(timer(uid, qi, m))

# ================== FINISH ==================

async def finish(uid, msg):
    d = user_data[uid]
    s = d["score"]
    p = round(s / 40 * 100, 1)
    await msg.answer(f"🏁 Test tugadi!\n✅ {s}/40\n📊 {p}%")
    user_data.pop(uid)

# ================== HANDLERLAR ==================

@dp.message(Command("test"))
async def start_test(msg: types.Message):
    uid = msg.from_user.id
    if uid in user_data:
        return await msg.answer("Test allaqachon boshlangan!")

    qs = generate_questions()
    user_data[uid] = {"questions": qs, "current": 0, "score": 0}
    await next_question(uid, msg)

@dp.callback_query(F.data)
async def answer(cb: types.CallbackQuery):
    uid = cb.from_user.id
    if uid not in user_data:
        return

    qi, oi = map(int, cb.data.split(":"))
    d = user_data[uid]

    if qi != d["current"]:
        return

    if oi == d["questions"][qi]["answer"]:
        d["score"] += 1

    d["current"] += 1
    await cb.message.delete()
    await next_question(uid, cb.message)

async def main():
    print("BOT ISHLAYAPTI 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
