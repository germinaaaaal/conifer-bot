# Conifer bot

A kitchen-sink bot that does various things, useful and otherwise, for [Conifer](https://nationstates.net/region=conifer)'s discord server.

## Features:
- Useful region info commands (poll, links etc)
- Quote any person by scanning their pinned messsages
- Quotes vyutsk whenever somebody says "no"
- State-of-the-art apabeossie simulator
- Mr Bean on error
- COMMUNISM
- and much more besides

# Disclaimer
This bot was made as a private bot for a fairly small discord server. It's not meant to
be customiseable, and furthermore the code quality is kinda bad.

Use at your own risk...

# Usage
1. Get the source: `git clone https://github.com/ed588/conifer-bot.git`
2. (Optional) Make a venv: `python3 -m venv venv`, and activate it: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Make token file: `echo YOUR_TOKEN > token` (in other words, make a file called `token` and put your token in it)
5. Run: `python3 bot.py`

# License
AGPL-3; see LICENSE file for details

# Also included: keith the dice bot
Set the `DICEBOT_TOKEN` envvar to your bot token, then run `keith.py`.
## Features
Responds to any message he can see that contains a request for a D&D-style dice roll. For instance if
a message contains "2d20" then keith will roll two d20s and add them together for you.
