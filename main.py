from keep_alive import keep_alive

keep_alive()  # запускаем веб-сервер для поддержания активности

import os
import webbrowser
import time
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)
from datetime import datetime, timedelta

token = os.getenv("TELEGRAM_TOKEN")  # Replit сам подставит токен из Secrets


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # данные пользователя
    user = update.effective_user
    username = user.username
    name = user.first_name
    surname = user.last_name
    partID = user.id

    # если ботом начал пользоваться я
    if username == "andrewbody":
        await update.message.reply_text(f"Инициализация: {name} {surname}")
        time.sleep(1)
        await update.message.reply_text(
            "Меню:", reply_markup=InlineKeyboardMarkup(menuButtons)
        )
        # ...

    # если ботом начал пользоваться любой другой пользователь
    else:
        await update.message.reply_text(f"Инициализация: {name} {surname}")
        # ...

    # добавление новых пользователей в список участников чата
    part = [partID, username, name, surname]
    if part not in partList:
        partList.append(part)


async def button_clicked(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # отправляем запроc
    query = update.callback_query
    # получаем ответ
    await query.answer()

    global meetStr

    # обработка кнопки "участники чата"
    if query.data == "people":
        partStr = "Список участников чата:\n"
        for part in partList:
            partStr += (
                str(part[0])
                + " | "
                + str(part[1])
                + " | "
                + str(part[2])
                + " "
                + str(part[3])
                + "\n"
            )
        await query.edit_message_text(
            text=partStr, reply_markup=InlineKeyboardMarkup(back)
        )

    # обработка кнопки "назначить встречу"
    elif query.data == "meet":
        await query.edit_message_text(
            text="Формат встречи:", reply_markup=InlineKeyboardMarkup(format)
        )

    # обработка кнопок "общение, совещание, корпоратив"
    elif (
        query.data == "communication"
        or query.data == "conference"
        or query.data == "corporative"
    ):
        await query.edit_message_text(
            text="Место встречи:", reply_markup=InlineKeyboardMarkup(place)
        )
        if query.data == "communication":
            meetStr += "      Формат: Общение\n"
        elif query.data == "conference":
            meetStr += "      Формат: Совещание\n"
        else:
            meetStr += "      Формат: Корпоратив\n"

    # обработка кнопки "отмена"
    elif query.data == "cancel":
        await query.edit_message_text(
            text="Меню:", reply_markup=InlineKeyboardMarkup(menuButtons)
        )
        meetStr = "   Новая встреча:\n"

    # обработка кнопок "кафе, офис, природа"
    elif query.data == "cafe" or query.data == "office" or query.data == "nature":
        date = [
            [
                InlineKeyboardButton(
                    datetime.now().strftime("%d.%m"),
                    callback_data=datetime.now().strftime("%d.%m"),
                ),
                InlineKeyboardButton(
                    (datetime.now() + timedelta(days=1)).strftime("%d.%m"),
                    callback_data=(datetime.now() + timedelta(days=1)).strftime(
                        "%d.%m"
                    ),
                ),
                InlineKeyboardButton(
                    (datetime.now() + timedelta(days=2)).strftime("%d.%m"),
                    callback_data=(datetime.now() + timedelta(days=2)).strftime(
                        "%d.%m"
                    ),
                ),
                InlineKeyboardButton(
                    (datetime.now() + timedelta(days=3)).strftime("%d.%m"),
                    callback_data=(datetime.now() + timedelta(days=3)).strftime(
                        "%d.%m"
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    (datetime.now() + timedelta(days=4)).strftime("%d.%m"),
                    callback_data=(datetime.now() + timedelta(days=4)).strftime(
                        "%d.%m"
                    ),
                ),
                InlineKeyboardButton(
                    (datetime.now() + timedelta(days=5)).strftime("%d.%m"),
                    callback_data=(datetime.now() + timedelta(days=5)).strftime(
                        "%d.%m"
                    ),
                ),
                InlineKeyboardButton(
                    (datetime.now() + timedelta(days=6)).strftime("%d.%m"),
                    callback_data=(datetime.now() + timedelta(days=6)).strftime(
                        "%d.%m"
                    ),
                ),
                InlineKeyboardButton(
                    (datetime.now() + timedelta(days=7)).strftime("%d.%m"),
                    callback_data=(datetime.now() + timedelta(days=7)).strftime(
                        "%d.%m"
                    ),
                ),
            ],
            [InlineKeyboardButton("Отмена", callback_data="cancel")],
        ]
        await query.edit_message_text(
            "Дата встречи:", reply_markup=InlineKeyboardMarkup(date)
        )
        if query.data == "cafe":
            meetStr += "      Место: Кафе\n"
        elif query.data == "office":
            meetStr += "      Место: Офис\n"
        else:
            meetStr += "      Место: Природа\n"

    elif query.data[2] == ".":
        timing = [
            [
                InlineKeyboardButton("09:00", callback_data="09:00"),
                InlineKeyboardButton("10:00", callback_data="10:00"),
                InlineKeyboardButton("11:00", callback_data="11:00"),
                InlineKeyboardButton("12:00", callback_data="12:00"),
            ],
            [
                InlineKeyboardButton("13:00", callback_data="13:00"),
                InlineKeyboardButton("14:00", callback_data="14:00"),
                InlineKeyboardButton("15:00", callback_data="15:00"),
                InlineKeyboardButton("16:00", callback_data="16:00"),
            ],
            [
                InlineKeyboardButton("17:00", callback_data="17:00"),
                InlineKeyboardButton("18:00", callback_data="18:00"),
                InlineKeyboardButton("19:00", callback_data="19:00"),
                InlineKeyboardButton("20:00", callback_data="20:00"),
            ],
            [InlineKeyboardButton("Отмена", callback_data="cancel")],
        ]
        await query.edit_message_text(
            text="Время встречи:", reply_markup=InlineKeyboardMarkup(timing)
        )
        meetStr += "      Дата встречи: " + query.data + "\n"

    elif query.data[2] == ":":
        meetStr += "      Время встречи: " + query.data + "\n"
        sending = [
            [InlineKeyboardButton("Отправить сотрудникам", callback_data="sending")],
            [InlineKeyboardButton("Отмена", callback_data="cancel")],
        ]
        await query.edit_message_text(
            text=f"Проверка информации:\n{meetStr}",
            reply_markup=InlineKeyboardMarkup(sending),
        )

    elif query.data == "sending":
        await query.edit_message_text(text="Ожидание отправки...")
        meetString = f"{meetStr[-33:-28]} - {meetStr[-6:-1]}"

        if meetString in meets:
            await query.edit_message_text(
                text="На данное время встреча уже запланирована!"
            )
        else:
            for part in partList:
                if part[0] != 1181155172:
                    partStr = f"accept:{meetString}:{part[1]}"
                    # проверяем размер строки (д.б. менее 64 байт)
                    print(len(partStr.encode("utf-8")))
                    okey = [[InlineKeyboardButton("Принять", callback_data=partStr)]]
                    await context.bot.send_message(
                        chat_id=part[0],
                        text=meetStr,
                        reply_markup=InlineKeyboardMarkup(okey),
                    )
            await query.edit_message_text(
                text="Приглашения отправлены всем сотрудникам!"
            )
            meets[meetString] = []
            meetList.append(meetStr)
        meetStr = "   Новая встреча:\n"
        time.sleep(2)
        await query.edit_message_text(
            text="Меню:", reply_markup=InlineKeyboardMarkup(menuButtons)
        )

    elif query.data.startswith("accept:"):
        meet = query.data[7:20]
        meets[meet].append(query.data[21:])
        stringMeetVtor = ""
        for meetString in meetList:
            if meet[:5] in meetString and meet[8:12] in meetString:
                stringMeetVtor += meetString[18:]
                break
        await query.edit_message_text(text=f"Вы приняли встречу:\n{stringMeetVtor}")

    elif query.data == "planningMeets":
        string = f"Список запланированных встреч:"
        meetButtons = []
        for meet in meets:
            print(meet)
            meetButtons.append([InlineKeyboardButton(meet, callback_data=f"-{meet}")])
        meetButtons.append(
            [InlineKeyboardButton("Обновить список", callback_data="updateMeetList")]
        )
        meetButtons.append([InlineKeyboardButton("Назад", callback_data="cancel")])
        await query.edit_message_text(
            text=string, reply_markup=InlineKeyboardMarkup(meetButtons)
        )

    elif query.data == "updateMeetList":
        pass

    elif " - " in query.data and query.data[0] == "-":
        for meet in meets:
            if meet == query.data[1:]:
                for meetL in meetList:
                    if meetL[-33:-28] == meet[:5] and meetL[-6:-1] == meet[8:]:
                        stringMeets = str(meets[query.data[1:]])
                        await query.edit_message_text(
                            text=f"{meetL}{stringMeets[2:-2]} - ПОДТВЕРЖДЕНО",
                            reply_markup=InlineKeyboardMarkup(back),
                        )


def main():
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_clicked))
    app.run_polling(poll_interval=1)


if __name__ == "__main__":
    partList = []
    menuButtons = [
        [InlineKeyboardButton("Участники чата", callback_data="people")],
        [InlineKeyboardButton("Назначить встречу", callback_data="meet")],
        [
            InlineKeyboardButton(
                "Запланированные встречи", callback_data="planningMeets"
            )
        ],
    ]
    format = [
        [
            InlineKeyboardButton("Общение", callback_data="communication"),
            InlineKeyboardButton("Совещание", callback_data="conference"),
        ],
        [InlineKeyboardButton("Корпоратив", callback_data="corporative")],
        [InlineKeyboardButton("Отмена", callback_data="cancel")],
    ]
    place = [
        [
            InlineKeyboardButton("Кафе", callback_data="cafe"),
            InlineKeyboardButton("Офис", callback_data="office"),
        ],
        [
            InlineKeyboardButton("Природа", callback_data="nature"),
        ],
        [InlineKeyboardButton("Отмена", callback_data="cancel")],
    ]
    back = [[InlineKeyboardButton("Назад", callback_data="cancel")]]
    meetStr = "   Новая встреча:\n"
    meets = {}
    meetList = []
    main()
