"""
    Conifer Discord Bot - kitchen-sink Discord bot for Conifer
    Copyright (C) 2018  ed588

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    """

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s::%(name)s@%(asctime)s λ %(message)s')
logger = logging.getLogger("conifer")

import discord
from discord.ext import commands
bot = commands.Bot(commands.when_mentioned_or("."))

import random, io, requests
from collections import deque

import lxml
from bs4 import BeautifulSoup

INSTA = requests.get("https://i.imgur.com/JYM4cuY.png").content

@bot.event
async def on_ready():
    logger.info("logged in as {0.user} ({0.user.id})".format(bot))

@bot.command()
async def ping(ctx):
    """Sends pong back

    Useful for testing that the bot is alive, and not much else
    """
    logger.info("pinged by {}".format(ctx.author))
    await ctx.send("pong")

@bot.command()
async def links(ctx):
    """Gives some links for the region

    Sends a message containing links to various useful resources related to the region.
    """
    logger.info("{} requested region links".format(ctx.author))
    emb = discord.Embed(title="Conifer")
    emb.set_thumbnail(url="https://www.nationstates.net/images/flags/uploads/rflags/conifer__839453.png")
    emb.colour = 0x6aff55
    emb.add_field(name="Link", value="https://www.nationstates.net/region=conifer")
    emb.add_field(name="Offsite Website", value="https://conifer.ed588.me/")
    emb.add_field(name="First Charter", value="https://conifer.ed588.me/legislation/firstcharter.pdf")
    emb.add_field(name="Voting Site", value="https://conifer.ed588.me/vote/")
    await ctx.send(embed=emb)

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command()
async def quote(ctx, who: discord.Member):
    """Gets a quote from someone

    This works by searching through the pinned messages in the Main category.
    It takes a while, please be patient.
    """
    logger.info("{} requested quote from {}".format(ctx.author, who))
    msgs = []
    files = []
    async with ctx.typing():
        cat = discord.utils.get(ctx.guild.categories, id=421881187775152128)
        catr = discord.utils.get(ctx.guild.categories, id=442440761481363457)
        chs = []
        chs.extend(cat.channels)
        chs.extend(catr.channels)
        chs.append(discord.utils.get(ctx.guild.text_channels, id=429621752897732608))
        for ch in chs:
            for pin in await ch.pins():
                if pin.author == who:
                    msgs.append(pin)
        if len(msgs) == 0:
            await ctx.send("Could not find any quotes for {}. <:mb:453992890423574559>".format(who))
        else:
            ts = random.choice(msgs)
            for att in ts.attachments:
                tf = io.BytesIO()
                await att.save(tf)
                df = discord.File(tf, att.filename)
                files.append(df)
            await ctx.send(ts.content, files=files)
    for df in files:
        df.close()

@commands.cooldown(3, 20, commands.BucketType.channel)
@bot.command()
async def apab(ctx):
    """Apabeossie Simulator

    Pretends to be our lord and saviour, Apabeossie (aka Agnatoli, aka Grenet)
    """
    logger.info("{} did apab command".format(ctx.author))
    srcs = ["i can't see messages", ":(", ":)", ":/", "...", "SHUT UP", "?", "???", "////", '\\\\\\\\', "*", ".", "!", ":|"]
    al = []
    for i in range(random.randint(2, 5)):
        dsts = []
        count = random.randint(6, 18)
        for i in range(count):
            dsts.append(random.choice(srcs))
        al.append(" ".join(dsts))
    await ctx.send("\n".join(al))

@commands.cooldown(20, 30)
@bot.command(enabled=False)
async def region(ctx):
    """Conifer regional statistics

    Gives you some nicely-formatted stats for the region.
    """
    pass

@commands.cooldown(20, 30)
@bot.command()
async def poll(ctx):
    """Current Poll

    Gives you information about the current poll going on in conifer, if there is one
    """
    logger.info("{} requested poll".format(ctx.author))
    await ctx.trigger_typing()
    req = requests.get("https://www.nationstates.net/cgi-bin/api.cgi?region=conifer&q=poll&v=9", headers={"User-Agent": "Conifer Bot (by Honk Donk)"}).text
    soup = BeautifulSoup(req, "xml")
    root = soup.REGION
    if len(root.contents) < 2:
        # no poll
        await ctx.send("Currently, there is no poll in Conifer. <:mb:453992890423574559>")
    else:
        poll = root.POLL
        emb = discord.Embed()
        emb.colour = 0xf02020
        emb.title = poll.TITLE.text
        emb.url = "https://www.nationstates.net/page=poll/p=" + poll['id']
        emb.description = poll.TEXT.text
        for opt in poll.OPTIONS("OPTION"):
            emb.add_field(name=opt.OPTIONTEXT.text, value="{} vote{} so far".format(opt.VOTES.text, "s" if int(opt.VOTES.text) != 1 else ""))
        await ctx.send(embed=emb)


poland_deque = deque(maxlen=20)
@commands.cooldown(1, 20, commands.BucketType.channel)
@bot.command()
async def poland(ctx):
    """Polandball

    Gives you a Polandball comic from r/polandball
    """
    logger.info("{} requested poland".format(ctx.author))
    await ctx.trigger_typing()
    res = requests.get("https://api.reddit.com/r/polandball/hot", headers={"User-Agent":"server:me.ed588.coniferbot:v0.1 (by /u/ed588)"}).json()
    for item in res['data']['children']:
        if item['data']['name'] not in poland_deque:
            poland_deque.append(item['data']['name'])
            to_send = item
            break
    else:
        await ctx.send("I couldn't find any Polandballs that I haven't already sent. Try again later. <:mb:453992890423574559>")
        return
    emb = discord.Embed()
    emb.title = to_send['data']['title']
    emb.url = "https://reddit.com" + to_send['data']['permalink']
    emb.set_footer(text="From /r/polandball ⁃ By /u/{}".format(to_send['data']['author']))
    emb.set_image(url=to_send['data']['url'])
    await ctx.send(embed=emb)

@commands.is_owner()
@bot.command()
async def shutdown(ctx):
    await ctx.send("bye")
    raise KeyboardInterrupt()

@bot.command(aliases=["<:commie:468389309163241472>"])
async def commie(ctx):
    await ctx.send("""**Soiuz nerushimyj respublik svobodnykh
Splotila naveki Velikaia Rus.
Da zdravstvuet sozdannyj volej narodov
Edinyj, moguchij Sovetskij Soiuz!

Slavsia, Otechestvo nashe svobodnoe,
Druzhby, narodov nadezhnyj oplot!
Znamia sovetskoe, znamia narodnoe
Pust ot pobedy, k pobede vedet!**
""")

@bot.command()
async def коммунист(ctx):
    await ctx.send("""**Союз нерушимый республик свободных
Сплотила навеки Великая Русь!
Да здравствует созданный волей народов
Единый, могучий Советский Союз!

Славься, Отечество наше свободное,
Дружбы народов надёжный оплот!
Знамя Советское, знамя народное
Пусть от победы к победе ведёт!**
""")


general_channel_id = 421880721523605506
@bot.event
async def on_member_remove(member):
    general = bot.get_channel(general_channel_id)
    msg = "Bye, **{0.name}#{0.discriminator}**! It was nice to have you here!".format(member)
    await general.send(msg)

@bot.event
async def on_member_join(member):
    general = bot.get_channel(general_channel_id)
    msg = "Hello and welcome to Conifer's Discord server, **{0.mention}**! Please state your nation name and the region in which you reside, and then make yourself at home here!".format(member)
    await general.send(msg)

@bot.event
async def on_message(msg):
    if msg.content.lower() == "good bot":
        await msg.channel.send("Thanks!")
    elif msg.content.lower() == "bad bot":
        await msg.channel.send("shut")
    elif msg.content.lower() == "no":
        await msg.channel.send(file=discord.File(io.BytesIO(INSTA), "no.png"))
    elif msg.content.lower().startswith("*cries in "):
        await msg.channel.send("*laughs in binary*")
    elif msg.content.lower() == "yee":
        await msg.channel.send("https://www.youtube.com/watch?v=q6EoRBvdVPQ")
    await bot.process_commands(msg)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("The {0.invoked_with} command has a cooldown set. Please wait another {1} seconds before retrying. <:mb:453992890423574559>".format(ctx, round(error.retry_after)))
    else:
        await ctx.send("{}. <:mb:453992890423574559>".format(str(error)))

token = open("token", "r").read().rstrip()
bot.run(token)
