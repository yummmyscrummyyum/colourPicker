import discord
import asyncio
import webcolors
from discord.ext import commands

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

class ColorRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_color_from_input(self, color_input: str):
        color_input = color_input.lower().strip()

        if color_input.startswith("#"):
            clean_hex = color_input[1:]
        else:
            clean_hex = color_input

        if len(clean_hex) == 6:
            try:
                value = int(clean_hex, 16)
                return discord.Color(value)
            except ValueError:
                pass 

        try:
            rgb = webcolors.name_to_rgb(color_input)
            return discord.Color.from_rgb(rgb.red, rgb.green, rgb.blue)
        except ValueError:
            pass

        try:
            method = getattr(discord.Color, color_input)
            if callable(method):
                return method()
        except AttributeError:
            pass

        return None

    @commands.command()
    async def color(self, ctx, *, color_input: str):
        color_value = self.get_color_from_input(color_input)

        if color_value is None:
            await ctx.send(f"I don't know the color **{color_input}**. Can you give me the Hex code instead? (e.g. `#FF0000`)")
            return

        role_name = f"{ctx.author.name}'s Color"
        existing_role = discord.utils.get(ctx.guild.roles, name=role_name)

        if existing_role:
            try:
                await existing_role.delete()
            except discord.Forbidden:
                await ctx.send("I cannot delete your old role. Check my permissions.")
                return

        try:
            new_role = await ctx.guild.create_role(name=role_name, color=color_value)
            
            await asyncio.sleep(0.7) 

            bot_top_role = ctx.guild.me.top_role
            target_pos = max(1, bot_top_role.position - 1)

            try:
                await ctx.guild.edit_role_positions({new_role: target_pos})
            except discord.HTTPException:
                await ctx.send("Warning: Created the role, but I couldn't move it up. Make sure my role is high enough!")

            await ctx.author.add_roles(new_role)
            
            embed = discord.Embed(
                description=f"**Role Created!** You are now **{color_input.title()}**.",
                color=color_value
            )
            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(ColorRole(bot))