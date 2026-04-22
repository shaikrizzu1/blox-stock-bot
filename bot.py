import discord
from discord import app_commands

TOKEN = "MTQ5NjQzMzg1ODg5ODI5Njg3Mg.GHAILU.E3Ccl7eEV3UAKssGJrNEk9Ae-fpBSy_CKlYDOU"
CHANNEL_ID = 1496130761932144740
ROLE_ID = None  # put role id if you want ping

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# =========================
# 📦 STOCK
# =========================
current_stock = []
stock_message = None

# =========================
# 🎨 PRO EMBED
# =========================
def create_embed():
    embed = discord.Embed(
        title="🟢 BLOX FRUITS DEALER STOCK",
        description="**Live Dealer Stock • Updates Automatically**",
        color=0x00ff88
    )

    if not current_stock:
        embed.description += "\n\n_No stock available_"
        return embed

    for item in current_stock:
        status = "🟢 AVAILABLE" if item["stock"] else "🔴 OUT OF STOCK"

        embed.add_field(
            name=f"{item['name']}",
            value=f"💰 **{item['price']}**\n📦 {status}",
            inline=True
        )

    embed.set_footer(text="⏳ Next Update: When dealer refreshes")
    return embed

# =========================
# 🤖 READY
# =========================
@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {client.user}")

# =========================
# 📜 SET STOCK (PRO FORMAT)
# =========================
@tree.command(name="setstock", description="Update full stock")
async def setstock(interaction: discord.Interaction, data: str):
    global current_stock, stock_message

    # format:
    # dragon,3500000,true; dough,2800000,false

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

    # 🔥 ALERT SYSTEM
    for item in current_stock:
        if item["stock"]:
            if "Dragon" in item["name"]:
                await channel.send("🐉🔥 **DRAGON IN STOCK — BUY FAST!** 🔥🐉")
            if "Leopard" in item["name"]:
                await channel.send("🐆⚡ **LEOPARD AVAILABLE NOW!** ⚡🐆")
            if "Dough" in item["name"]:
                await channel.send("🍩✨ **DOUGH IN STOCK!** ✨🍩")

    await interaction.response.send_message("✅ Stock updated (PRO STYLE)", ephemeral=True)

# =========================
# 📜 VIEW STOCK
# =========================
@tree.command(name="stock", description="View stock")
async def stock(interaction: discord.Interaction):
    embed = create_embed()
    await interaction.response.send_message(embed=embed)

# =========================
# ▶️ RUN
# =========================
client.run(TOKEN)