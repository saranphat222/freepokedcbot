import sys
import os
import requests
import discord
from discord.ext import commands
from keep_alive import keep_alive

class Colors:
    white = "\033[37m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    cyan = "\033[36m"

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print(f"\n{Colors.white}[{Colors.red}ERROR{Colors.white}] {Colors.red}Token not found in environment variables!")
    sys.exit(1)

url = "https://discord.com/api/v10/users/@me"
headers = {
    "Authorization": f"Bot {TOKEN}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(f"\n{Colors.white} [{Colors.green}!{Colors.white}] {Colors.green}Token is valid.\n")
else:
    print(f"\n{Colors.white} [{Colors.red}!{Colors.white}] {Colors.red}Invalid token. Please check your token and try again.\n{Colors.white}")
    sys.exit(1)

print(f"{Colors.green}✅ Token is valid! บอทกำลังเริ่มต้น...")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"{Colors.cyan}บอทออนไลน์แล้ว! {bot.user} พร้อมให้บริการ!")

@bot.command()
async def poke(ctx, member: discord.Member, *, message: str = "ว่างมั้ย?"):
    avatar_url = member.display_avatar.url if member.display_avatar else ""
    embed = discord.Embed(
        title=f"{ctx.author.display_name} pokes you!",
        description=message,
        color=discord.Color.yellow()
    )
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_footer(text="Poke", icon_url=ctx.bot.user.display_avatar.url)

    try:
        await member.send(embed=embed)
        await ctx.send(embed=discord.Embed(
            description=f"✅ Poked {member.mention} successfully!",
            color=discord.Color.green()
        ), ephemeral=True)
    except discord.Forbidden:
        await ctx.send(embed=discord.Embed(
            description=f"❌ ไม่สามารถส่งข้อความไปยัง {member.mention} ได้ (DM ถูกปิด)",
            color=discord.Color.red()
        ), ephemeral=True)

keep_alive()

bot.run(TOKEN)

