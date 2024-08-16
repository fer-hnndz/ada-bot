import disnake
from disnake.ext import commands
from typing import Literal

flags = commands.CommandSyncFlags.default()
client = commands.Bot(
    command_prefix="$", test_guilds=[1274077543833665610], command_sync_flags=flags
)


@client.slash_command(name="embed", description="Send an embed from the list")
async def embeds(
    inter: disnake.ApplicationCommandInteraction,
    embed: str = commands.Param(choices=["verify", "test"]),
):
    if inter.author.id != client.owner.id:
        return await inter.response.send_message(
            "You are not allowed to use this command!", ephemeral=True
        )

    verify_embed = disnake.Embed(
        title="Verificación",
        description=f"Para poder verificarse como sistemático, envía una foto de tu carnet a {client.owner.mention}",
        color=disnake.Color.red(),
    )

    verify_embed.set_thumbnail(
        url=(
            inter.guild.icon.url
            if inter.guild.icon
            else inter.author.display_avatar.url
        )
    )

    await inter.send(embed=verify_embed)


@client.slash_command(
    name="verificar", description="Le agrega el rol de verificado a un usuario"
)
async def verificar(inter: disnake.ApplicationCommandInteraction, user: disnake.Member):
    await inter.response.defer(ephemeral=True)

    if not "admin" in [role.name.lower() for role in inter.author.roles]:
        await inter.send("No tienes permisos para usar este comando", ephemeral=True)
        return

    if "verificado" in [role.name.lower() for role in user.roles]:
        await inter.send("Este usuario ya está verificado", ephemeral=True)
        return

    role: disnake.Role = disnake.utils.get(inter.guild.roles, name="Verificado")  # type: ignore
    unverified_role: disnake.Role = disnake.utils.get(inter.guild.roles, name="No Verificado")  # type: ignore

    await user.remove_roles(unverified_role)
    await user.add_roles(role)

    try:
        await user.send(f"Has sido verificado en **{inter.guild.name}**!")

    except Exception:
        print(
            f"No se pudo enviar el mensaje al usuario {user.mention} tratandolo de verificar."
        )

    await inter.edit_original_response(
        content=f"El usuario {user.mention} ha sido verificado."
    )


print("Bot is running!")
client.run("MTI3NDA3NDgyMTI2MDYwNzUyOA.GlJkeh.rTEoGuBcAGg9jw7IHx5rmKhge5qtZ-fP2iI8B8")
