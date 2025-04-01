from telethon.sync import TelegramClient
import pandas as pd
import re
import os
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("TELEGRAM_PHONE_NUMBER")
target_group_name = os.getenv("TELEGRAM_TARGET_GROUP")

# Create the client session
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=phone_number)

    print("Fetching chats...")
    dialogs = await client.get_dialogs()
    group = next((d.entity for d in dialogs if d.name == target_group_name), None)

    if not group:
        print(f"Group '{target_group_name}' not found.")
        return

    print(f"Found group: {group.title}. Fetching participants...")
    participants = await client.get_participants(group)

    data = []
    for user in participants:
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        username = f"@{user.username}" if user.username else ""
        data.append({
            "Display Name": full_name,
            "Username": username
        })

    # Make the filename safe
    safe_group_name = re.sub(r'[\\/*?:"<>|]', "_", group.title)
    filename = f"{safe_group_name}_members.xlsx"
    filepath = os.path.joi
