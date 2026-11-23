
import discord
import json
import aiohttp
import os

# CONFIGURATION
BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
WEBHOOK_URL = "PUT_YOUR_NEW_WEBHOOK_URL_HERE"

MILESTONE = 30
COUNT_FILE = "member_count.json"

# Load saved count
if os.path.exists(COUNT_FILE):
    with open(COUNT_FILE, "r") as f:
        data = json.load(f)
        count = data.get("count", 0)
else:
    count = 0

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


def save_count():
    with open(COUNT_FILE, "w") as f:
        json.dump({"count": count}, f)


async def send_application():
    message = {
        "embeds": [{
            "title": "🛡️ Moderator Applications",
            "description": (
                "We're looking for new moderators!\n\n"
                "Interested in joining the staff team?\n\n"
                "**Moderator Application**\n"
                "1. Discord username:\n"
                "2. Age:\n"
                "3. Timezone:\n"
                "4. Previous moderation experience:\n"
                "5. Why should we choose you?\n"
                "6. How active are you?\n\n"
                "Contact the server administration to apply."
            ),
            "color": 5793266,
            "footer": {
                "text": "Community Staff Recruitment"
            }
        }]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            WEBHOOK_URL,
            json=message
        ) as response:
            print("Webhook status:", response.status)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"Current join count: {count}")


@client.event
async def on_member_join(member):
    global count

    count += 1
    save_count()

    print(f"{member} joined. Total: {count}")

    if count % MILESTONE == 0:
        await send_application()
        print("Moderator application announcement sent!")


client.run(BOT_TOKEN)
