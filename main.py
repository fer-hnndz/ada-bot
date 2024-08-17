import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
from cogs.verification import Verification

load_dotenv()

flags = commands.CommandSyncFlags.default()
intents = disnake.Intents.all()
client = commands.Bot(
    command_prefix="$",
    test_guilds=[1274077543833665610, 1243747892477431880],
    command_sync_flags=flags,
    intents=intents,
)


@client.event
async def on_ready():
    print("Bot is running!")
    await client.change_presence(
        status=disnake.Status.online,
        activity=disnake.Activity(
            type=disnake.ActivityType.playing, name="Vigilando Sistemáticos"
        ),
    )


@client.command()
@commands.is_owner()
async def verify_embed(ctx: commands.Context):
    verify_embed = disnake.Embed(
        title="Verificación",
        description=f"Para poder verificarse como sistemático, envía una foto de tu carnet o un video donde se muestre tu info en registo a {client.owner.mention}",
        color=disnake.Color.red(),
    )

    if not ctx.guild:
        return

    verify_embed.set_thumbnail(
        url=(ctx.guild.icon.url if ctx.guild.icon else ctx.author.display_avatar.url)
    )

    await ctx.send(embed=verify_embed)


# ================ Cog Management ================


@client.command()
@commands.is_owner()
async def load(ctx, extension: str):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} cog")


@client.command()
@commands.is_owner()
async def unload(ctx, extension: str):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension} cog")


@client.command()
@commands.is_owner()
async def reload(ctx, extension: str):
    client.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension} cog")


cogs = [
    f"cogs.{extension[:-3]}"
    for extension in os.listdir("cogs")
    if extension.endswith(".py")
]
for cog in cogs:
    client.load_extension(cog)

client.run(os.environ.get("TOKEN", ""))
