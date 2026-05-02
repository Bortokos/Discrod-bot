discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# -------------------------
# INTENTS
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------
# TABLE CHANNEL ID
TABLE_CHANNEL_ID = 1500186859832086729
import
# DATA
data = {}
table_message = None

# ------------------------
@bot.event
async def on_ready():
global table_message
print("BOT ONLINE:", bot.user)

channel = bot.get_channel(TABLE_CHANNEL_ID)
if channel:
table_message = await channel.send("📊 TABLE LOADING...")
wait refresh_table()

# ------------------------
# 📊 TABLE UPDATE
async def refresh_table():
global table_message

if not table_message:
return

if not data:
text = "📊 PARTS TABLE\n\nNo data"
else:
text = "📊 PARTS TABLE\n\n"
name, quantity data.items():
text += f"{name} - {quantity} parts\n"

wait for table_message.edit(content=text)

# ------------------------
# ➕ ADD
@bot.command()
@commands.has_permissions(administrator=True)
async def add(ctx, member: discord.Member, quantity: int):
name = member.display_name
data[name] = data.get(name, 0) + quantity
wait refresh_table()

# ------------------------
# ❌ 1 PERSON FULL DELETE
@bot.command()
@commands.has_permissions(administrator=True)
async def remove(ctx, tag: discord.Member):
name = tag.display_name
if name in data:
del data[name]
wait refresh_table()

# ------------------------
# 🧹 RESET ALL
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
if name in data:
data[name] = 0
wait refresh_table()

# ------------------------
# ❌ ERROR HANDLING
@add.error
@remove.error
@clear.error
async def error_handler(ctx, error):
if isinstance(error, commands.MissingPermissions):
await ctx.send("❌ Only admin can use it!")

# ------------------------
# 🔹 Keep-alive Flask (for free hosts)
app = Flask("")

@app.route("/")
def home():
return "Bot is running"

def run():
app.run(host="0.0.0.0", port=3000)

Thread(target=run).start()
