import os
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

users = set()

APK_CAPTION = """
✅ 100% NUMBER HACK 💥

( ONLY FOR PREMIUM USERS ⚡️ )
( 100% LOSS RECOVER GUARANTEE ⚡️ )

𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 𝐇𝐀𝐂𝐊 :- https://t.me/HOW_TO_USE_ADNAN_HACK/41551

FOR HELP @ADNAN_HACK_MANAGER
"""


# Join Request Auto Approve
async def approve_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.chat_join_request.from_user
    chat_id = update.chat_join_request.chat.id

    # approve join request
    await context.bot.approve_chat_join_request(chat_id, user.id)

    users.add(user.id)

    # welcome message
    await context.bot.send_message(
        chat_id=user.id,
        text="✨ WELCOME TO ADNAN PREMIUM BOT ✨\n\nAccess Granted 🚀"
    )

    # send APK
    try:
        with open("𝐀𝐃𝐍𝐀𝐍_𝐈𝐍𝐉𝐄𝐂𝐓𝐎𝐑_𝐇𝐀𝐂𝐊 (2).apk", "rb") as apk:
            await context.bot.send_document(
                chat_id=user.id,
                document=apk,
                caption=APK_CAPTION
            )
    except Exception as e:
        print(e)


# Broadcast message
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    for user_id in users:
        try:
            await context.bot.copy_message(
                chat_id=user_id,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.id
            )
        except:
            pass


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(approve_request))
    app.add_handler(MessageHandler(filters.ALL, broadcast))

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
