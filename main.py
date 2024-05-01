import discord
from discord.ext import commands, tasks
import mysql.connector
import datetime
import pytz
import time
import requests
import asyncio
import os

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

#conn = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#    database="passionrp"
#)

async def update_presence():
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="Passion RP FA",
        state="Staff"
    )
    await bot.change_presence(activity=activity)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')
    await bot.change_presence(activity=discord.Game(name="Passion RP FA", type=discord.ActivityType.playing))
#    check_updates.start()
    await bot.tree.sync()
    await update_presence()

#@tasks.loop(minutes=0.2) 
#async def check_updates():
#    cursor = conn.cursor()
#    cursor.execute("SELECT * FROM contact WHERE est_mise_a_jour = 0")
#    new_updates = cursor.fetchall()
#    print('MAJ SERVER')
#    if new_updates:
#        for update in new_updates:
#            embed = discord.Embed(title=f"Message de {update[4]}", color=0x808080)
#            embed.add_field(name=f"Sujet : {update[5]}", value=f"{update[1]}, \nEMAIL : {update[6]}", inline=False)
#           tz = pytz.timezone('Europe/Paris')
#            heure_actuelle = datetime.datetime.now(tz)
#            formatted_time = heure_actuelle.strftime("le %d/%m à %H:%M:%S")
#            embed.set_footer(text=formatted_time)
#            embed.set_author(name="Passion RP FA", icon_url="https://cdn.discordapp.com/avatars/1161596570261798934/50d2afec0afdac59fef300291a75f892?size=1024")
#            embed.add_field(name="Supprimer", value="Cliquez sur 🔴 pour Effacer.")
#            embed.add_field(name="Valider", value="Cliquez sur 🟢 pour Confirmer.")
#            embed.add_field(name="En cours", value="Cliquez sur 🟠 pour : En cours.")
#            embed.add_field(name="À faire", value="Cliquez sur ⚪ pour : À faire.")
#            channel = bot.get_channel(1129024097846829177)
#            message1 = await channel.send(embed=embed)
#            await message1.add_reaction('🔴')
#            await message1.add_reaction('🟢') 
#            await message1.add_reaction('🟠') 
#            await message1.add_reaction('⚪') 
#        cursor.execute("UPDATE contact SET est_mise_a_jour = 1 WHERE est_mise_a_jour = 0")
#    conn.commit()


#@bot.event
#async def on_reaction_add(reaction, user):
#    if reaction.emoji == '🔴' and not user.bot:
#        await reaction.message.delete()
#    elif reaction.emoji == '⚪' and not user.bot: 
#        embed = reaction.message.embeds[0]
#        if "À faire" not in embed.title and "En cours" not in embed.title and "Terminé" not in embed.title:
#            embed.title = f"À faire: {embed.title}" 
#        elif "En cours" in embed.title:
#            embed.title = embed.title.replace("En cours", "À faire")
#        elif "Terminé" in embed.title:
#            embed.title = embed.title.replace("Terminé", "À faire")
#        embed.color = 0x808080
#        await reaction.message.edit(embed=embed)
#    elif reaction.emoji == '🟢' and not user.bot: 
#        embed = reaction.message.embeds[0]
#        if "Terminé" not in embed.title and "En cours" not in embed.title and "À faire" not in embed.title:
#            embed.title = f"Terminé: {embed.title}" 
#         elif "En cours" in embed.title:
#        embed.title = embed.title.replace("En cours", "Terminé")
#        elif "À faire" in embed.title:
#            embed.title = embed.title.replace("À faire", "Terminé")
#        embed.color = 0x00FF00 
#        await reaction.message.edit(embed=embed)
#    elif reaction.emoji == '🟠' and not user.bot:
#        embed = reaction.message.embeds[0] 
#        if "En cours" not in embed.title and "Terminé" not in embed.title and "À faire" not in embed.title:
#            embed.title = f"En cours: {embed.title}"
#        elif "Terminé" in embed.title:
#            embed.title = embed.title.replace("Terminé", "En cours") 
#        elif "À faire" in embed.title:
#            embed.title = embed.title.replace("À faire", "En cours")
#        embed.color = 0xFFA500
#        await reaction.message.edit(embed=embed)

@bot.tree.command(name="players",description="Affiche le nombre de joueurs en ligne.")
async def slash_command(ctx: discord.interactions.Interaction):
    response = requests.get("http://213.199.55.142:30120/dynamic.json")
    if response.status_code == 200:
        embed = discord.Embed(color=0xFFFFFF)
        embed.add_field(name="Joueurs", value=f"{response.json()['clients']}/{response.json()['sv_maxclients']}", inline=False)
        await ctx.response.send_message(embed=embed)
    else:
        await ctx.response.send_message("Impossible d'obtenir les données du serveur.")

@bot.tree.command(name="playersliste", description="Affiche la liste de tous les joueurs en ligne.")
async def slash_command(ctx: discord.interactions.Interaction):
    response = requests.get("http://213.199.55.142:30120/players.json")
    if response.status_code == 200:
        embed = discord.Embed(title="Liste des joueurs en ligne", color=0xFFFFFF) 
        noms = []
        ids = []
        discordids = []
        fivemids = []
        for element in response.json():
            noms.append(element["name"])
            ids.append(element["id"])
            for identifier in element["identifiers"]:
                if "discord" in identifier:
                    discordids.append(identifier.split(":")[1]) 
                if "fivem" in identifier:
                    fivemids.append(identifier.split(":")[1]) 
        for nom, identifiant, discordid, fivemid in zip(noms, ids, discordids, fivemids):
            embed.add_field(name=nom, value=f"ID : {identifiant}, Discord : <@{discordid}> ({discordid}), FiveM : {fivemid}", inline=False)
        await ctx.response.send_message(embed=embed) 
    else:
        await ctx.response.send_message("Impossible d'obtenir les données du serveur.")

@bot.tree.command(name="invite", description="Le lien d'invitation.")
async def slash_command(ctx: discord.interactions.Interaction):
    await ctx.response.send_message("Passion RP FA, c'est tout simplement de l'amour: https://discord.gg/passionrp") 


#@bot.event
#async def on_disconnect():
#    conn.close()


bot.run(os.environ.get(TOKEN))
