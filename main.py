import os

TOKEN = os.getenv("MTQ1NjI3NDQzMzY0MjU5NDQ4Mg.GeOI7R.-J1b5izwu10HqJmUNNXj3Fnfy3JDhs86CsbPh0")
OWNER_ID = int(os.getenv(1390832712193019975))

import discord
from discord.ext import commands, tasks
import json
import random
import os

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

# Bot prefix
bot = commands.Bot(command_prefix=".", intents=intents)

# Owner ID
OWNER_ID = int(os.getenv("1390832712193019975"))

# Load balances
def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("{}")
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

balances_file = "balances.json"
bank_file = "bank.json"
ltc_file = "user_ltc.json"

# Helper functions
def get_balance(user_id):
    balances = load_json(balances_file)
    return balances.get(str(user_id), 0)

def add_balance(user_id, amount):
    balances = load_json(balances_file)
    balances[str(user_id)] = balances.get(str(user_id), 0) + amount
    save_json(balances_file, balances)

def remove_balance(user_id, amount):
    balances = load_json(balances_file)
    balances[str(user_id)] = balances.get(str(user_id), 0) - amount
    save_json(balances_file, balances)

# READY
@bot.event
async def on_ready():
    print(f"{bot.user} is online")

# ----------------- ECONOMY COMMANDS -----------------

@bot.command()
async def balance(ctx):
    bal = get_balance(ctx.author.id)
    await ctx.send(f"{ctx.author.mention} Balance: {bal} coins")

@bot.command()
async def daily(ctx):
    bal = get_balance(ctx.author.id)
    add_balance(ctx.author.id, 100)
    await ctx.send(f"{ctx.author.mention} You received your daily 100 coins! New balance: {bal+100}")

# ----------------- ADMIN COMMANDS -----------------

def is_owner(ctx):
    return ctx.author.id == OWNER_ID

@bot.command()
async def addbalance(ctx, member: discord.Member, amount: int):
    if not is_owner(ctx):
        await ctx.send("You cannot use this command!")
        return
    add_balance(member.id, amount)
    await ctx.send(f"{amount} coins added to {member.mention}")

@bot.command()
async def removebalance(ctx, member: discord.Member, amount: int):
    if not is_owner(ctx):
        await ctx.send("You cannot use this command!")
        return
    remove_balance(member.id, amount)
    await ctx.send(f"{amount} coins removed from {member.mention}")

@bot.command()
async def setbalance(ctx, member: discord.Member, amount: int):
    if not is_owner(ctx):
        await ctx.send("You cannot use this command!")
        return
    balances = load_json(balances_file)
    balances[str(member.id)] = amount
    save_json(balances_file, balances)
    await ctx.send(f"{member.mention} balance set to {amount} coins")

# ----------------- CASINO COMMANDS -----------------

# Coinflip
@bot.command()
async def coinflip(ctx, choice: str, amount: int):
    bal = get_balance(ctx.author.id)
    if amount > bal:
        await ctx.send("You don't have enough coins!")
        return
    flip = random.choice(["heads", "tails"])
    if choice.lower() == flip:
        add_balance(ctx.author.id, amount)
        await ctx.send(f"You won! It was {flip}. +{amount} coins")
    else:
        remove_balance(ctx.author.id, amount)
        await ctx.send(f"You lost! It was {flip}. -{amount} coins")

# Slots
@bot.command()
async def slots(ctx, amount: int):
    bal = get_balance(ctx.author.id)
    if amount > bal:
        await ctx.send("You don't have enough coins!")
        return
    remove_balance(ctx.author.id, amount)
    emojis = ["🍒", "🍋", "🍉", "⭐", "💎"]
    result = [random.choice(emojis) for _ in range(3)]
    await ctx.send(" | ".join(result))
    if len(set(result)) == 1:
        reward = amount * 5
        add_balance(ctx.author.id, reward)
        await ctx.send(f"Jackpot! You won {reward} coins")
    elif len(set(result)) == 2:
        reward = amount * 2
        add_balance(ctx.author.id, reward)
        await ctx.send(f"You won {reward} coins")
    else:
        await ctx.send("You lost!")

# Blackjack
@bot.command()
async def blackjack(ctx, amount: int):
    bal = get_balance(ctx.author.id)
    if amount > bal:
        await ctx.send("You don't have enough coins!")
        return
    remove_balance(ctx.author.id, amount)
    # Simple blackjack: random 17-21 wins
    player = random.randint(15, 21)
    dealer = random.randint(16, 21)
    if player > dealer:
        reward = amount * 2
        add_balance(ctx.author.id, reward)
        await ctx.send(f"You won! Your {player} vs Dealer {dealer}. +{reward} coins")
    elif player < dealer:
        await ctx.send(f"You lost! Your {player} vs Dealer {dealer}. -{amount} coins")
    else:
        add_balance(ctx.author.id, amount)
        await ctx.send(f"Draw! Your {player} vs Dealer {dealer}. Coins returned")

# Mines
@bot.command()
async def mines(ctx, amount: int):
    bal = get_balance(ctx.author.id)
    if amount > bal:
        await ctx.send("You don't have enough coins!")
        return
    remove_balance(ctx.author.id, amount)
    chance = random.randint(1, 3)
    if chance == 1:
        reward = amount * 2
        add_balance(ctx.author.id, reward)
        await ctx.send(f"You avoided mines! Won {reward} coins")
    else:
        await ctx.send(f"You hit a mine! Lost {amount} coins")

# Limbo
@bot.command()
async def limbo(ctx, multiplier: float, amount: int):
    bal = get_balance(ctx.author.id)
    if amount > bal:
        await ctx.send("You don't have enough coins!")
        return
    remove_balance(ctx.author.id, amount)
    chance = random.random()
    if chance < 0.5:
        await ctx.send(f"You lost {amount} coins")
    else:
        reward = int(amount * multiplier)
        add_balance(ctx.author.id, reward)
        await ctx.send(f"You won {reward} coins!")

# Keno
@bot.command()
async def keno(ctx, amount: int):
    bal = get_balance(ctx.author.id)
    if amount > bal:
        await ctx.send("You don't have enough coins!")
        return
    remove_balance(ctx.author.id, amount)
    hits = random.randint(0, 10)
    reward = hits * amount
    if reward > 0:
        add_balance(ctx.author.id, reward)
        await ctx.send(f"You hit {hits} numbers! Won {reward} coins")
    else:
        await ctx.send(f"No hits! Lost {amount} coins")

# Rain
@bot.command()
async def rain(ctx, amount: int):
    members = [m for m in ctx.guild.members if not m.bot]
    if not members:
        await ctx.send("No members to rain on")
        return
    per_user = amount // len(members)
    for member in members:
        add_balance(member.id, per_user)
    await ctx.send(f"Rained {per_user} coins on {len(members)} users!")

# ----------------- LTC COMMANDS -----------------

@bot.command()
async def setltc(ctx, address: str):
    data = load_json(ltc_file)
    data[str(ctx.author.id)] = address
    save_json(ltc_file, data)
    await ctx.send(f"LTC address saved for {ctx.author.mention}")

@bot.command()
async def myltc(ctx):
    data = load_json(ltc_file)
    address = data.get(str(ctx.author.id), None)
    if address:
        await ctx.author.send(f"Your LTC address: {address}")
        await ctx.send("Your LTC address has been sent to your DM!")
    else:
        await ctx.send("No LTC address set. Use `.setltc <address>`")

# ----------------- RUN BOT -----------------
TOKEN = os.getenv("MTQ1NjI3NDQzMzY0MjU5NDQ4Mg.GeOI7R.-J1b5izwu10HqJmUNNXj3Fnfy3JDhs86CsbPh0")
bot.run(MTQ1NjI3NDQzMzY0MjU5NDQ4Mg.GeOI7R.-J1b5izwu10HqJmUNNXj3Fnfy3JDhs86CsbPh0)
