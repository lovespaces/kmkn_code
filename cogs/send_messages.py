import discord
from discord.ext import commands

channel = [] #ここにチャンネルのIDを貼り付け！

class SendMessages(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        elif message.channel.id in channel:
            org_msg = message
            counter = 0
            for i in channel:
                q_ch = message.guild.get_channel(i)
                if q_ch.type == discord.ChannelType.forum:
                    for j in q_ch.threads:
                        async for message in j.history(limit=200):
                            if message.author == org_msg.author:
                                counter += 1
                else:
                    async for message in q_ch.history(limit=200):
                        if message.author == org_msg.author:
                            counter += 1
            embed = discord.Embed(
                title="質問する前に確認して！",
                description="**これはコマ研サーバーで直近で質問チャンネルで質問をしたことがない人向けに送られています。**\n" + 
                            "### 回答者があなたの望む答えを出せるように質問文で以下の内容が含まれているか確認してください。\n" +
                            "- **`どんなコマンドを打ったのか（コマンドを打ったが実行されない！という質問のみ）`**\n" +
                            "- **`データパック/チャット/コマブロのどれでコマンドを実行したか（コマンドを打ったが実行されない！という質問のみ）`**\n" +
                            "- **`何をしたいのか（一番重要）`**\n \n" +
                            "**思考を文字なしで共有しているわけでもないしこのサーバーにいるみんながあなたと同じ考えをしているわけありません。**\n"+
                            "**困ったときはお互い様です。どうしたらなにができないか、きちんと書いてください。**",
                color=0xe06e64
            )
            embed.set_footer(text="もしこのメッセージが誤送信/既にメッセージの通りに質問を書いた場合は下の「🗑️」からメッセージを削除してください。\n" +
                             "ボタンは返信元のユーザーにしか実行されません"
                             ) # メッセージはお前らで考えてもらってもええんやで
            view = discord.ui.View()
            view.add_item(discord.ui.Button(emoji="🗑️", custom_id="DELETE." + str(org_msg.author.id), style=discord.ButtonStyle.gray))
            if counter == 1:
                await org_msg.reply(embed = embed, view = view)

async def setup(bot):
    await bot.add_cog(SendMessages(bot))
