import os
import logging
import discord
from discord.ext import commands
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

class BotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='', intents=discord.Intents.default())

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.data_commands")
        logger.info("Extension 'cogs.data_commands' chargée.")
        
        try:
            synced_commands = await self.tree.sync() 
            logger.info(f"Synchronisation de {len(synced_commands)} commandes Slash effectuée.")
        except Exception as e:
            logger.error(f"Erreur lors de la synchronisation des commandes: {e}")

    async def on_ready(self):
        await self.change_presence(
            status=discord.Status.dnd,
            activity=activity 
        )
        
        logger.info(f'------------------------------------')
        logger.info(f'Bot connecté avec succès : {self.user}')
        logger.info(f'Statut défini sur DND, Activité : {activity.name}')
        logger.info(f'Prêt à recevoir des commandes Slash.')
        logger.info(f'------------------------------------')

if __name__ == "__main__":
    if not TOKEN:
        logger.critical("Erreur: Le token est introuvable dans le fichier .env")
        exit()

    client = BotClient()
    
    try:
        client.run(TOKEN)
    except Exception as e:
        logger.critical(f"Impossible de démarrer le bot : {e}")