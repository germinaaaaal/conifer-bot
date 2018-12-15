import discord

import random
import re
diceroll = re.compile(r"\b((\d+)?d(\d+))\b")
client = discord.Client()

@client.event
async def on_ready():
    print("Logged in")

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    matches = diceroll.findall(msg.content)
    if matches:
        resp = []
        for match in matches:
            full, count, sides = match
            count = 1 if count == '' else int(count)
            sides = int(sides)
            if count > 9999 or sides > 9999:
                result = "*one or more numbers are too large for me :(*"
            else:
                result = 0
                for i in range(count):
                    result += random.randint(1, sides)
            resp.append( "`{}`: **{}**".format(full, result) )
            
        await msg.channel.send("\n".join(resp))

if __name__ == "__main__":
    from os import getenv
    tok = getenv("DICEBOT_TOKEN", None)
    if tok is None:
        print("Set the envvar DICEBOT_TOKEN to your token")
    else:
        client.run(tok.strip())
