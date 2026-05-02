import discord
from discord.ext import commands

# INTENTS
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# TÁBLA CSATORNA ID
TABLA_CSATORNA_ID = 1500186859832086729

# ADATOK
adatok = {}
tabla_uzenet = None


@bot.event
async def on_ready():
    global tabla_uzenet

    print("BOT ONLINE:", bot.user)

    channel = bot.get_channel(TABLA_CSATORNA_ID)

    if channel:
        tabla_uzenet = await channel.send("📊 TÁBLA BETÖLTÉS...")
        await frissit_tabla()


# 📊 TÁBLA FRISSÍTÉS
async def frissit_tabla():
    global tabla_uzenet

    if not tabla_uzenet:
        return

    if not adatok:
        szoveg = "📊 ALKATRÉSZ TÁBLA\n\nNincs adat"
    else:
        szoveg = "📊 ALKATRÉSZ TÁBLA\n\n"
        for nev, menny in adatok.items():
            szoveg += f"{nev} - {menny} alkatrész\n"

    await tabla_uzenet.edit(content=szoveg)


# ➕ HOZZÁADÁS
@bot.command()
@commands.has_permissions(administrator=True)
async def add(ctx, member: discord.Member, mennyiseg: int):
    nev = member.display_name

    adatok[nev] = adatok.get(nev, 0) + mennyiseg

    await frissit_tabla()


# ❌ 1 EMBER TELJES TÖRLÉSE A TÁBLÁBÓL
@bot.command()
@commands.has_permissions(administrator=True)
async def remove(ctx, member: discord.Member):
    nev = member.display_name

    if nev in adatok:
        del adatok[nev]

    await frissit_tabla()


# 🧹 MINDEN NULLÁZÁSA (NEVEK MARADNAK)
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
    for nev in adatok:
        adatok[nev] = 0

    await frissit_tabla()


# ❌ HIBA KEZELÉS
@add.error
@remove.error
@clear.error
async def error_handler(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ csak admin használhatja!")



bot.run ("MTUwMDE4MjQ5NDAyMjk5MTg4Mg.GrSy8t.sGVVJ4K2IYmrtYf_QUN7L1MNFtcWf697QQxTVI")