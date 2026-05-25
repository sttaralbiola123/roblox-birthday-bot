import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Roblox API endpoints
ROBLOX_BIRTHDATE_API = "https://users.roblox.com/v1/user/birthdate"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Synced {await bot.tree.sync()} command(s)')

# Slash Command: Change Birthday
@bot.tree.command(name="change", description="Change Roblox birthday to June 5, 2014")
@app_commands.describe(
    cookie="Your Roblox .ROBLOSECURITY cookie",
    password="Your Roblox account password"
)
async def change_birthday(interaction: discord.Interaction, cookie: str, password: str):
    """
    Changes Roblox birthday to June 5, 2014
    """
    try:
        await interaction.response.defer(ephemeral=True)
        
        if not cookie or not password:
            await interaction.followup.send("❌ Cookie and password are required!", ephemeral=True)
            return

        # Verify Roblox cookie
        headers = {
            'Cookie': f'.ROBLOSECURITY={cookie}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }

        # Get current user info
        verify_response = requests.get(
            "https://users.roblox.com/v1/user",
            headers=headers,
            timeout=10
        )

        if verify_response.status_code != 200:
            await interaction.followup.send("❌ Invalid Roblox cookie! Authentication failed.", ephemeral=True)
            return

        user_data = verify_response.json()
        username = user_data.get('name')

        # Change birthday to June 5, 2014
        birthdate_payload = {
            'birthMonth': 6,
            'birthDay': 5,
            'birthYear': 2014
        }

        birthdate_response = requests.post(
            ROBLOX_BIRTHDATE_API,
            json=birthdate_payload,
            headers=headers,
            timeout=10
        )

        if birthdate_response.status_code == 200:
            embed = discord.Embed(
                title="✅ Success!",
                description=f"Birthday changed to **June 5, 2014**",
                color=discord.Color.green()
            )
            embed.add_field(name="Username", value=username, inline=True)
            await interaction.followup.send(embed=embed, ephemeral=True)
        
        elif birthdate_response.status_code == 401:
            await interaction.followup.send("❌ Authentication failed. Cookie may be expired.", ephemeral=True)
        
        elif birthdate_response.status_code == 400:
            await interaction.followup.send("❌ Cannot change birthday - Account restrictions or already set.", ephemeral=True)
        
        else:
            await interaction.followup.send(f"❌ Error: {birthdate_response.status_code}", ephemeral=True)

    except requests.exceptions.Timeout:
        await interaction.followup.send("❌ Request timeout. Try again later.", ephemeral=True)
    except requests.exceptions.RequestException as e:
        await interaction.followup.send(f"❌ Network error: {str(e)}", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)

# Run bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("ERROR: DISCORD_TOKEN not found in .env file")
    else:
        bot.run(token)