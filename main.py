from re import match
import nextcord
from nextcord.ext import commands
import requests
import json
import aiohttp
import os
from keepAlive import keep_alive

token = os.environ['token']

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents,help_command=None)

async def logsend(embed):
  async with aiohttp.ClientSession() as session:
    webhook = nextcord.Webhook.from_url(roblox['webhook'], session=session)
    await webhook.send(embed=embed)

class Spam(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("สเเปมเว็ปฮุก")  
        self.webhook = nextcord.ui.TextInput(
            label="ลิ้งค์",
            required=True
        )
        self.add_item(self.webhook)
        self.msg = nextcord.ui.TextInput(
            label="ข้อความ",
            required=True
        )
        self.add_item(self.msg)
        self.amount = nextcord.ui.TextInput(
            label="จำนวน",
            required=True
        )
        self.add_item(self.amount)

    async def callback(self, interaction: nextcord.Interaction):
        response = requests.get(self.webhook.value)
        if not match(r"https:\/\/discord\.com\/api\/webhooks\/[0-9]{18,19}\/[a-zA-Z0-9_-]{68,69}", self.webhook.value):
            return await interaction.send("ลิงค์เว็ปฮุคไม่ถูกต้อง", ephemeral=True)

        try:
            amount_value = int(self.amount.value)
        except ValueError:
            return await interaction.send("จำนวนต้องเป็นตัวเลข", ephemeral=True)

        if response.status_code == 200:
            await interaction.send(f"**กำลังสเเปมไปที่** `{self.webhook.value}`", ephemeral=True)
            for i in range(amount_value):
                requests.post(self.webhook.value, json={'content': self.msg.value})  
        else:
            await interaction.send("**สแปมเว็ปฮุคไม่สําเร็จ หรือ เว็ปฮุคถูกลบไปแล้ว**", ephemeral=True)


class Delete(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("ลบเว็ปฮุค")  
        self.webhook = nextcord.ui.TextInput(
            label="ลิ้งค์เว็บฮุก",
            required=True
        )
        self.add_item(self.webhook)
    async def callback(self, interaction: nextcord.Interaction):
        if not match(r"https:\/\/discord\.com\/api\/webhooks\/[0-9]{18,19}\/[a-zA-Z0-9_-]{68,69}" ,self.webhook.value):
          return await interaction.send("ลิงค์เว็ปฮุคไม่ถูกต้อง",ephemeral=True)
        if requests.delete(self.webhook.value).status_code == 204:
          await interaction.send(f"**ลบเว็ปฮุคสําเร็จ** `{self.webhook.value}`",ephemeral=True)
        else:
          await interaction.send("**ลบเว็ปฮุคไม่สําเร็จ หรือ เว็ปฮุคถูกลบไปแล้ว**",ephemeral=True)

class Check(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("เช็คเว็ปฮุก")  
        self.webhook = nextcord.ui.TextInput(
            label="ลิ้งค์เว็บฮุก",
            required=True
        )
        self.add_item(self.webhook)
    async def callback(self, interaction: nextcord.Interaction):
        response = requests.get(self.webhook.value)
        if not match(r"https:\/\/discord\.com\/api\/webhooks\/[0-9]{18,19}\/[a-zA-Z0-9_-]{68,69}" ,self.webhook.value):
          return await interaction.send("ลิ้งค์เว็ปฮุกไม่ถูกต้อง",ephemeral=True)
        if response.status_code == 200:
          i = response.json()
          if i['avatar'] == None:
            embed = nextcord.Embed(description=f"**TYPE** : `{i['type']}`\n**ไอดี** : `{i['id']}`\n**ชื่อ** : `{i['name']}`\n**ไอดีช่อง** : `{i['channel_id']}`\n**ไอดีเซิฟ** : `{i['guild_id']}`\n**ไอดีแอป** : `{i['application_id']}`\n**โทเคนเว็ปฮุก** : `{i['token']}`")
            await interaction.send(embed=embed,ephemeral=True)
          else:
            embed = nextcord.Embed(description=f"**TYPE** : `{i['type']}`\n**ไอดี** : `{i['id']}`\n**ชื่อ** : `{i['name']}`\n**ไอดีช่อง** : `{i['channel_id']}`\n**ไอดีเซิฟ** : `{i['guild_id']}`\n**ไอดีแอป** : `{i['application_id']}`\n**โทเคนเว็ปฮุก** : `{i['token']}`")
            embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{i['id']}/{i['avatar']}.png")
            await interaction.send(embed=embed,ephemeral=True)
        else:
          await interaction.send("**ไม่สำเร็จ อาจจะถูกลบไปเเล้วนะ+**",ephemeral=True)

class Button(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="เช็คเว็ปฮุก", style=nextcord.ButtonStyle.green, emoji="🔍",custom_id="เช็ค webhook")
    async def check(self, button: nextcord.Button , interaction: nextcord.Interaction):
                await interaction.response.send_modal(Check())

    @nextcord.ui.button(label="สแปมเว็บฮุก", style=nextcord.ButtonStyle.blurple, emoji="🔫",custom_id="ยิง webhook")
    async def spam(self, button: nextcord.Button , interaction: nextcord.Interaction):
                await interaction.response.send_modal(Spam())

    @nextcord.ui.button(label="ลบเว็บฮุก", style=nextcord.ButtonStyle.red, emoji="👾",custom_id="ลบ webhook")
    async def delete(self, button: nextcord.Button , interaction: nextcord.Interaction):
                await interaction.response.send_modal(Delete())


@bot.event
async def on_ready():
    bot.add_view(Button())
    print(f"BOT NAME : {bot.user}")
    await bot.change_presence(activity=nextcord.Game(name="《 Fake Link Webhook 》"))

@bot.command(pass_context=True)
async def setup(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.message.delete()
        embed = nextcord.Embed(title="WEBHOOK SPAMMER",description="```สแปม webhook ```",color=0xFFFFFF)
        embed.set_image(url="https://media.discordapp.net/attachments/1183420745544646716/1190862499193565236/w.gif?ex=65a35820&is=6590e320&hm=20f851fcbebfbf66b0972f0241874dbcf7cdbcea5d7797701616e91c0d722af2&=")
        await ctx.send(embed=embed, view=Button())
    else:
        await ctx.reply('ไม่น่ารักเลยนะค่ะ!')

keep_alive()
bot.run(process.env.token);
