import os
import logging
import discord
from discord import app_commands
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('System')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

activity = discord.Activity(
    type=discord.ActivityType.listening,
    name="Test activity"
)

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
    
    async def on_ready(self):
        """Se déclenche une fois le bot connecté."""
 
        await self.change_presence(
            status=discord.Status.dnd,
            activity=activity
        )
        
        logger.info(f'------------------------------------')
        logger.info(f'Bot connecté avec succès : {self.user}')
        logger.info(f'ID : {self.user.id}')
        logger.info(f'Statut défini sur DND, Activité : {activity.name}')
        logger.info(f'Prêt à recevoir des commandes Slash.')
        logger.info(f'------------------------------------')

if __name__ == "__main__":
    if not TOKEN:
        logger.critical("Erreur: Le token est introuvable dans le fichier .env")
        exit()

    client = Client()
    
    try:
        client.run(TOKEN)
    except Exception as e:
        logger.critical(f"Impossible de démarrer le bot : {e}")