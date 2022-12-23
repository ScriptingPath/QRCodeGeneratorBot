import os
import traceback
import sys

try:
    import qrcode
except ImportError:
    question = input(
        "Библиотека qrcode не установлена. Установить её? (y/n): ")
    if (question == "y"):
        if os.system("pip install qrcode") == 0:
            print("Библиотека qrcode успешно установлена.")
            try:
                import qrcode
            except ImportError:
                print(
                    "Не удалось загрузить библиотеку qrcode. Попробуйте перезапустить бота.")
                input("Нажмите на любую клавишу для выхода...")
        else:
            print("Не удалось установить библиотеку qrcode. Попробуйте сделать это вручную, после чего перезапустите бота.")
            input("Нажмите на любую клавишу для выхода...")
    else:
        print("Без установки библиотеки qrcode невозможно запустить бота.")
        input("Нажмите на любую клавишу для выхода...")
        sys.exit()


from io import BytesIO

try:
    from colorama import Fore, init
except ImportError:
    question = input(
        "Библиотека colorama не установлена. Установить её? (y/n): ")
    if (question == "y"):
        if os.system("pip install colorama") == 0:
            print("Библиотека colorama успешно установлена.")
            try:
                from colorama import Fore, init
            except ImportError:
                print(
                    "Не удалось загрузить библиотеку colorama. Попробуйте перезапустить бота.")
                input("Нажмите на любую клавишу для выхода...")
        else:
            print("Не удалось установить библиотеку colorama. Попробуйте сделать это вручную, после чего перезапустите бота.")
            input("Нажмите на любую клавишу для выхода...")
    else:
        print("Без установки библиотеки colorama невозможно запустить бота.")
        input("Нажмите на любую клавишу для выхода...")
        sys.exit()

try:
    from aiogram import Bot, Dispatcher, executor, types
    from aiogram.utils import executor
    from aiogram.types import ReplyKeyboardMarkup
except ImportError:
    question = input(
        "Библиотека aiogram не установлена. Установить её? (y/n): ")
    if (question == "y"):
        if os.system("pip install aiogram") == 0:
            print("Библиотека aiogram успешно установлена.")
            try:
                from aiogram import Bot, Dispatcher, executor, types
                from aiogram.utils import executor
            except ImportError:
                print(
                    "Не удалось загрузить библиотеку aiogram. Попробуйте перезапустить бота.")
                input("Нажмите на любую клавишу для выхода...")
        else:
            print("Не удалось установить библиотеку aiogram. Попробуйте сделать это вручную, после чего перезапустите бота.")
            input("Нажмите на любую клавишу для выхода...")
    else:
        print("Без установки библиотеки aiogram невозможно запустить бота.")
        input("Нажмите на любую клавишу для выхода...")
        sys.exit()

init(autoreset=True)
token = os.getenv("TOKEN")

if token is None:
    token = input("Введите токен бота (можно получить в боте @BotFather): ")

bot = Bot(token=token)
dp = Dispatcher(bot)

count = 0
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add("💿 Информация")


async def on_startup(_):
    print(Fore.LIGHTWHITE_EX + "Бот запущен и готов к работе")


@dp.message_handler(commands=["start", "help"])
async def start_command(msg: types.Message):
    await msg.reply("*👋 Привет, этот бот позволяет делать QR-коды из любого текста или ссылки. Просто отправь в чат с ботом ссылку на сайт.*", parse_mode="markdown", reply_markup=start_keyboard, reply=False)

@dp.message_handler()
async def on_message(msg: types.Message):
    if (msg.text == "💿 Информация"):
        await msg.reply("*♦ Этот бот позволяет создавать QR-коды. Просто отправь в чат с этим ботом текст или ссылку.*", parse_mode="markdown", reply=False)
    else:
        # если пользователь решил создать qr-код
        global count
        count += 1
        if len(msg.text) < 500:
            print(Fore.LIGHTBLUE_EX +
                f"\n\n[{count}] – Начинаю генерацию QR-кода для пользователя {msg.from_user.full_name} (ID: {msg.from_user.id}, количество символов: {len(msg.text)})")
            status = await msg.reply("⚙ Генерирую QR-код...", reply=False)

            try:
                print(Fore.LIGHTBLUE_EX +
                    f"""[{count}] – Генерация QR-кода "{msg.text}"..""")
                img = qrcode.make(msg.text)

                print(Fore.LIGHTBLUE_EX +
                    f"[{count}] – Сохраняю QR-код в память..")
                bio = BytesIO()
                bio.name = 'qr.jpeg'
                img.save(bio, "jpeg")
                bio.seek(0)

                print(Fore.LIGHTBLUE_EX +
                    f"[{count}] – Отправляю QR-код пользователю {msg.from_user.full_name} (ID: {msg.from_user.id})")
                await msg.reply_photo(photo=bio, reply=False)
                await status.edit_text("*✅ QR-код успешно сгенерирован!*", parse_mode="markdown")

                print(Fore.LIGHTBLUE_EX +
                    f"[{count}] – Удаляю переменные из памяти..")
                
                del bio
                del img
                del status

                print(Fore.LIGHTWHITE_EX +
                    f"[{count}] – QR-код от пользователя {msg.from_user.full_name} (ID: {msg.from_user.id}) успешно обработан")
                return
            except Exception as ex:
                print(Fore.LIGHTRED_EX +
                    f"Ошибка при генерации QR-кода для пользователя {msg.from_user.full_name} (ID: {msg.from_user.id}):\n{traceback.format_exc().strip()}\n Информация о сообщении: {msg}")
                await status.edit_text("*❌ Произошла неизвестная ошибка при генерации QR-кода. Повторите попытку позже.*", parse_mode="markdown")
        else:
            print(Fore.LIGHTCYAN_EX +
                f"\n[{count}] Не удалось обработать QR-код пользователя {msg.from_user.full_name} (ID: {msg.from_user.id}) из-за превышения допустимого лимита значения (> 500)")
            await msg.reply("*❌ Слишком большое сообщение для обработки. Максимальное количество символов: 500*", parse_mode="markdown")

while True:
    while True:
        try:
            executor.start_polling(
                dp, skip_updates=False, on_startup=on_startup)
        except Exception as ex:
            print(traceback.format_exc())
