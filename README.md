# Colour Picker Cog

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776ab?logo=python&logocolour=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/library-discord.py-5865f2?logo=discord&logocolour=white)](https://github.com/Rapptz/discord.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This is a Discord bot cog that lets users set a **custom colour for their username** by creating a personal colour role. Users can provide a colour as a hex code, a CSS colour name, or a built-in discord.py colour name — the bot handles the rest automatically.

---

## How It Works

### Setting a colour
Users run the prefix command:
```
!color <color>
```
The bot accepts three input formats:
- **Hex code** — `#FF0000` or `FF0000`
- **CSS colour name** — `red`, `cornflowerblue`, `hotpink`, etc. (resolved via `webcolours`)
- **discord.py colour name** — `blurple`, `dark_gold`, `teal`, etc.

If the input doesn't match any of these, the bot prompts the user to provide a hex code instead.

### Role Management
Each user gets one personal role named `<username>'s colour`. When the command is run:

1. Any existing colour role for that user is deleted.
2. A new role is created with the chosen colour.
3. The role is moved just below the bot's highest role so it takes effect on the username.
4. The role is assigned to the user.

The bot then sends an embed coloured in the chosen colour confirming the change.

---

## Setup

1. Install dependencies:
   ```
   pip install discord.py webcolours
   ```
2. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications) and enable the **Message Content Intent**
3. Ensure the bot's role is **above** any colour roles in the server's role list — otherwise the colour won't display on usernames
4. Load the cog in your bot's main file:
   ```python
   await bot.load_extension("main")  # or wherever the file is located
   ```
5. Run your bot.

---

## Things to consider / change

### Clean Up Roles When a User Leaves
colour roles will persist even if a user leaves the server. Add a listener to auto-delete them:
```python
@commands.Cog.listener()
async def on_member_remove(self, member):
    role_name = f"{member.name}'s colour"
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role:
        await role.delete()
```

### Add a Command to Remove Your colour
Let users opt out of their colour role without setting a new one:
```python
@commands.command()
async def removecolour(self, ctx):
    role_name = f"{ctx.author.name}'s colour"
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await role.delete()
        await ctx.send("Your colour role has been removed.")
    else:
        await ctx.send("You don't have a colour role.")
```

### Restrict the Command to Specific Roles
Limit who can use `!colour` by adding a role check:
```python
@commands.has_any_role("Member", "Subscriber")
@commands.command()
async def colour(self, ctx, *, colour_input: str):
    ...
```

### Add a Slash Command Version
Convert the command to a slash command for a cleaner UX:
```python
@app_commands.command(name="colour", description="Set your username colour")
async def slash_colour(self, interaction: discord.Interaction, colour: str):
    ...
```

### Add a Cooldown to Prevent Spam
Stop users from rapidly creating and deleting roles:
```python
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.command()
async def colour(self, ctx, *, colour_input: str):
    ...
```

---

## Further info
- The bot requires **Manage Roles** permission and its role must be positioned above any user colour roles for them to visually take effect.
- The small `asyncio.sleep(0.7)` delay after role creation is intentional — it gives Discord's API time to register the role before repositioning it.
- Servers have a **250 role limit**. In large or active servers, consider periodically auditing and removing orphaned colour roles.
