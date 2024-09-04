import os

import asyncio
import disnake
from disnake.ext import commands

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"Bot {bot.user} in connected!")
    print(f"In {len(bot.guilds)} guilds")
    print(f"Disnake Version: {disnake.__version__}")
    print("-----------------------------")


@bot.slash_command(name="report", description="Отправляет жалобу на участника")
async def report(inter: disnake.AppCmdInter, member: disnake.Member, text: str):
    await inter.channel.purge(limit=1)

    report_channel = bot.get_channel(1082126615368175717)  # id канала для репортов заменить на свой

    author = inter.author

    embed = disnake.Embed(
        title="** Жалоба на пользователя! **",
        description=f"**Жалоба от:** {author.mention}\n**Жалоба на:** {member.mention}\n\n**Описание жалобы:** \n" + text,
        colour=disnake.Colour.from_rgb(255, 0, 0))

    await report_channel.send(embed=embed)

    await inter.send("Жалоба успешно отправлена!", ephemeral=True)
    await asyncio.sleep(1)


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run('MTI4MDkyNzM2MDAzMTUyMjg5MA.GbQX2C.MvI3ufjtJpP--ObvaR-AOQUIz_7oVlaY-XGrPs')