import discord
from discord.ext import commands

class Buttons(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener('on_interaction')
    async def detect(self, inter: discord.Interaction):
        try:
            if inter.data['component_type'] == 2:
                await button(inter)
        except KeyError:
            pass

async def button(inter: discord.Interaction):
    custom_id = inter.data['custom_id']
    if "DELETE" in custom_id:
        await inter.response.defer(thinking = True, ephemeral = True)
        split = custom_id.split(".")
        member = inter.guild.get_member(int(split[1]))
        if member == None:
            await inter.followup.send("削除したよ\n送り主が既にサーバーにいなかったから誰でも消せるようになってるよ")
            await inter.message.delete()
        elif int(split[1]) != inter.user.id: # ❓
            await inter.followup.send("❓")
        elif int(split[1]) == inter.user.id:
            await inter.followup.send("削除したよ")
            await inter.message.delete()

async def setup(bot):
    await bot.add_cog(Buttons(bot))
