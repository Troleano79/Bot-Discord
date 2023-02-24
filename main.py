import nextcord
from nextcord.ext import commands
import datetime
from classic import ClassicPrice
from data import GetData

class CreateTicket(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Vender Oro", style=nextcord.ButtonStyle.blurple, custom_id="create_ticket")
    async def create_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        msg = await interaction.response.send_message("Ticket is being created...", ephemeral=True)
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            interaction.guild.get_role(1078726191298646056): nextcord.PermissionOverwrite(read_messages=True)
        }

        channel = await interaction.guild.create_text_channel(f'{interaction.user.name}-ticket', overwrites=overwrites)
        await msg.edit(f'Nuevo canal creado! {channel.mention}')
        embed = nextcord.Embed(title='Ticket Creado', description='Escribe el server y la cantidad de oro que deseas vender!')
        await channel.send(embed=embed, view=TicketSettings())

class TicketSettings(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Cerrar Ticket", style=nextcord.ButtonStyle.blurple, custom_id='crear_ticket:blurple')
    async def close_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message('Ticket Closed', ephemeral=True)
        await interaction.channel.delete()
        await interaction.user.send('Close')


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False
    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(CreateTicket())
            self.persistent_views_added = True
            print('Persistent views added')
        
        print(f'Bot is up and ready | Logged in as {self.user}')

servers = {
    'Arugal': ['Horde'],
    "Atiesh": ['Alliance'],
    "Benediction": ['Alliance'],
    "Eranikus": ['Horde', 'Alliance'],
    "Faerlina": ['Horde'],
    "Grobbulus": ['Horde', 'Alliance'],
    "Maladath": ['Horde', 'Alliance'],
    "Mankrik": ['Horde'],
    "Old": ['Horde', 'Alliance'],
    "Pagle": ['Alliance'],
    "Skyfury": ['Horde', 'Alliance'],
    "Sulfuras": ['Horde', 'Alliance'],
    "Westfall": ['Alliance'],
    "Whitemane": ['Horde'],
    "Yojamba": ['Horde']
    }

bot = Bot(command_prefix="!", intents=nextcord.Intents.all())

# @bot.event
# async def on_ready():
#     print(f'conectado como: {bot.user}')

@bot.command()
async def classic(ctx):
    url = 'https://sls.g2g.com/offer/search?service_id=lgc_service_1&brand_id=lgc_game_29076&region_id=dfced32f-2f0a-4df5-a218-1e068cfadffa&sort=lowest_price&filter_attr=lgc_29076_platform:lgc_29076_platform_41146,lgc_29076_platform_41149,lgc_29076_platform_41161,lgc_29076_platform_46450,lgc_29076_platform_46451,lgc_29076_platform_41207,lgc_29076_platform_41222,lgc_29076_platform_41224,lgc_29076_platform_46321,lgc_29076_platform_46322,lgc_29076_platform_41249,lgc_29076_platform_41258,lgc_29076_platform_41259,lgc_29076_platform_41261,lgc_29076_platform_46319,lgc_29076_platform_46320,lgc_29076_platform_41286,lgc_29076_platform_41287,lgc_29076_platform_41298,lgc_29076_platform_41303,lgc_29076_platform_41311&page_size=48&currency=USD&country=NI'
    GetData(url, 'ethernal_classic_US.csv').write_csv()
    classic_us = ClassicPrice('ethernal_classic_US.csv', rate=.83).filtered_data()
    embed = nextcord.Embed(title="Lista de Precio", 
                          description="Precios Actualizados",
                          color=nextcord.Color.blue())
    embed.add_field(name="Server", value=classic_us['server'].to_string(index=False), inline=True)
    embed.add_field(name='Horda', value=classic_us['Horda'].to_string(index=False))
    embed.add_field(name='Alianza', value=classic_us['Alianza'].to_string(index=False))
    embed.timestamp = datetime.datetime.now()
    await ctx.send(embed=embed, )

@bot.command()
@commands.has_permissions(manage_guild=True)
async def setup_ticket(ctx: commands.Context):
    embed = nextcord.Embed(title='Crear Ticket', description='Para vender oro presiona el boton crear ticket, pronto nos comunicaremos contigo')
    await ctx.send(embed=embed, view=CreateTicket())



bot.run('MTA2NzIyODI0NzY4OTAyMzUyOA.Gu6aNN.P2_BFUVLdaiYbZdDgMxf8wJhR9FtuHqQE7IGII')
