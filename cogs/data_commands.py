import discord
from discord import app_commands
from discord.ext import commands
import pandas as pd
import logging

logger = logging.getLogger('System')

class DataCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.file_path = "vehicules_cIara_2025.csv"

    @app_commands.command(name="stats", description="Affiche le nombre total de véhicules dans la base de données.")
    async def stats_command(self, interaction: discord.Interaction):
        try:
            df = pd.read_csv(self.file_path)
            total_vehicules = len(df)
            
            response = (
                f"J'ai trouvé **{total_vehicules}** véhicules enregistrés dans le fichier "
                f"`{self.file_path}`.\n"
                f"Les colonnes disponibles sont : `{', '.join(df.columns)}`."
            )
            
        except FileNotFoundError:
            response = f"Erreur : Le fichier `{self.file_path}` est introuvable. Assurez-vous qu'il est à côté de `main.py`."
            logger.error(f"Fichier CSV non trouvé à l'emplacement: {self.file_path}")
        except Exception as e:
            response = f"Erreur lors de la lecture du fichier : Une erreur s'est produite."
            logger.error(f"Erreur de lecture CSV: {e}")

        await interaction.response.send_message(response, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(DataCommands(bot))