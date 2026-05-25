# Roblox Birthday Bot

Simple Discord bot na nag-change ng Roblox birthday to June 5, 2014 using `/change` command.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get your Discord token from [Discord Developer Portal](https://discord.com/developers/applications)

3. Update `.env` file with your token:
```
DISCORD_TOKEN=your_token_here
```

4. Run the bot:
```bash
python bot.py
```

## Usage

In Discord:
```
/change <roblox_cookie> <roblox_password>
```

The bot will:
- Verify your Roblox cookie
- Change birthday to June 5, 2014
- Send success/error message

## Deployment on Render

1. Push to GitHub
2. Create new Web Service on Render
3. Connect your repo
4. Set environment variables in Render dashboard
5. Deploy!

## Notes

- Cookie is hidden from other users (ephemeral response)
- Make sure your Roblox account allows birthday changes
- Some accounts may have restrictions