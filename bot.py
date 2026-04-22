import discord
from discord import app_commands
import os

TOKEN = os.getenv("MTQ5NjQzMzg1ODg5ODI5Njg3Mg.G2BOE0.TggUkCe2HBlUGiBhe1RB5Mu9DiDJ0HDYiGY_8Y")  # ✅ Railway variable
CHANNEL_ID = 1496130761932144740
ROLE_ID = None  # optional role ping

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# =========================
# 📦 STOCK DATA
# =========================
current_stock = []
stock_message = None

# =========================
# 🎨 EMBED DESIGN (PRO)
# =========================
def create_embed():
    embed = discord.Embed(
        title="🟢 BLOX FRUITS DEALER STOCK",
        description="**Live Dealer Stock • Updated Manually**",
        color=0x00ff88
    )

    if not current_stock:
        embed.description += "\n\n_No stock available_"
        return embed

    for item in current_stock:
        status = "🟢 AVAILABLE" if item["stock"] else "🔴 OUT OF STOCK"

        embed.add_field(
            name=item["name"],
            value=f"💰 **{item['price']}**\n📦 {status}",
            inline=True
        )

    embed.set_footer(text="⏳ Updates when dealer refreshes")
    return embed

# =========================
# 🤖 READY EVENT
# =========================
@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {client.user}")

# =========================
# 📜 SET STOCK (FIXED)
# =========================
@tree.command(name="setstock", description="Update full stock")
async def setstock(interaction: discord.Interaction, data: str):
    await interaction.response.defer(ephemeral=True)  # ✅ FIX

    global current_stock, stock_message

    items = data.split(";")
    new_stock = []

    for item in items:
        try:
            name, price, available = item.split(",")

            name = name.strip().title()
            price = price.strip()
            available = available.strip().lower() == "true"

            emoji = "🍎"
            if "dragon" in name.lower():
                emoji = "🐉"
            elif "dough" in name.lower():
                emoji = "🍩"
            elif "leopard" in name.lower():
                emoji = "🐆"
            elif "venom" in name.lower():
                emoji = "☠️"

            new_stock.append({
                "name": f"{emoji} {name}",
                "price": price,
                "stock": available
            })

        except:
            continue

    current_stock = new_stock

    embed = create_embed()

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        channel = await client.fetch_channel(CHANNEL_ID)

    # 🔥 SINGLE MESSAGE SYSTEM
    if stock_message is None:
        if ROLE_ID:
            stock_message = await channel.send(f"<@&{ROLE_ID}>", embed=embed)
        else:
            stock_message = await channel.send(embed=embed)
    else:
        await stock_message.edit(embed=embed)

    # 🔥 ALERTS
    for item in current_stock:
        if item["stock"]:
            if "Dragon" in item["name"]:
                await channel.send("🐉🔥 **DRAGON IN STOCK — BUY FAST!** 🔥🐉")
            if "Leopard" in item["name"]:
                await channel.send("🐆⚡ **LEOPARD AVAILABLE NOW!** ⚡🐆")
            if "Dough" in item["name"]:
                await channel.send("🍩✨ **DOUGH IN STOCK!** ✨🍩")

    await interaction.followup.send("✅ Stock updated!", ephemeral=True)

# =========================
# 📜 VIEW STOCK (FIXED)
# =========================
@tree.command(name="stock", description="View stock")
async def stock(interaction: discord.Interaction):
    await interaction.response.defer()  # ✅ FIX

    embed = create_embed()

    await interaction.followup.send(embed=embed)

# =========================
# ▶️ RUN
# =========================
client.run(TOKEN)
