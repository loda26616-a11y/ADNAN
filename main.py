from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler, ChatMemberHandler
from telegram.constants import ChatMemberStatus
from telegram.error import NetworkError, TimedOut, RetryAfter
import json
import os
import sys
import asyncio
import requests
from io import BytesIO
from datetime import datetime

# Force unbuffered output so logs show instantly
sys.stdout.reconfigure(line_buffering=True)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
APK_URL = os.environ.get("APK_URL")

USERS_FILE = "users.json"
APK_CACHE = None

def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return []

def save_users(users):
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
    except IOError as e:
        print(f"Error saving users: {e}")

def add_user(user, users):
    if not any(u["id"] == user.id for u in users):
        users.append({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "joined_at": datetime.now().isoformat()
        })
        save_users(users)
    return users

def fetch_apk_at_startup():
    global APK_CACHE
    if not APK_URL:
        print("WARNING: APK_URL not set — APK will not be sent.")
        return
    try:
        print(f"Downloading APK from GitHub...")
        response = requests.get(APK_URL, timeout=120)
        response.raise_for_status()
        APK_CACHE = response.content
        print(f"APK cached successfully ({len(APK_CACHE)} bytes)")
    except Exception as e:
        print(f"Failed to download APK: {e}")
        APK_CACHE = None

# --- New Leave Handler ---
async def leave_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    # Check if the user left or was removed
    if result.new_chat_member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
        user = result.from_user
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text=(
                    f"👋 Hello {user.first_name},\n\n"
                    "Aapne humara channel leave kar diya hai. 😟\n"
                    "Agar koi problem thi ya aap help chahte ho, toh humse contact karein: @ADNAN_HACK_MANAGER\n\n"
                    "Wapas join karne ke liye link ka use karein! https://t.me/+25K-yX2HWtBiZTk1 🔥"
                )
            )
            print(f"Leave message sent to: {user.id}")
        except Exception as e:
            print(f"Could not send leave message to {user.id}: {e}")

async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    for attempt in range(3):
        try:
            users = load_users()
            add_user(user, users)

            await context.bot.send_message(
                chat_id=user.id,
                text="🚀🔥 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 ADNAN 𝗧𝗥𝗔𝗗𝗘𝗥𝗦 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧 🔥"
            )

            if APK_CACHE:
                apk_file = BytesIO(APK_CACHE)
                apk_file.name = "𝐀𝐃𝐍𝐀𝐍_𝐈𝐍𝐉𝐄𝐂𝐓𝐎𝐑_𝐇𝐀𝐂𝐊_1_0_jaiwin (1).apk"
                await context.bot.send_document(
                    chat_id=user.id,
                    document=apk_file,
                    filename="𝐀𝐃𝐍𝐀𝐍_𝐈𝐍𝐉𝐄𝐂𝐓𝐎𝐑_𝐇𝐀𝐂𝐊_1_0_jaiwin (1).apk",
                    caption=(
                        "✅ 100% NUMBER HACK 💥\n\n"
                        "( ONLY FOR PREMIUM USERS ⚡️ )\n"
                        "( 100% LOSS RECOVER GUARANTEE ⚡️ )\n\n"
                        "𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 𝐇𝐀𝐂𝐊 :- https://t.me/HOW_TO_USE_ADNAN_HACK/41559\n"
                        "FOR HELP @ADNAN_HACK_MANAGER"
                    )
                )
                print(f"APK sent to: {user.id} (@{user.username})")
            else:
                print(f"APK cache empty, not sent to: {user.id}")
            break
        except RetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except (NetworkError, TimedOut) as e:
            if attempt < 2: await asyncio.sleep(5)
        except Exception as e:
            print(f"Error for {user.id}: {e}")
            break

def main():
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN not set")
        return

    print(f"[{datetime.now()}] Starting bot...")
    fetch_apk_at_startup()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(ChatJoinRequestHandler(join_request))
    app.add_handler(ChatMemberHandler(leave_handler, ChatMemberHandler.CHAT_MEMBER))

    print(f"[{datetime.now()}] Bot running...")

    # Added "chat_member" to allowed_updates
    app.run_polling(
        drop_pending_updates=True, 
        allowed_updates=["chat_join_request", "chat_member"]
    )

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Crashed: {e}")
            import time
            time.sleep(10)
            
