import disnake
from disnake.ext import commands


class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_cog_load(self):
        print("Verification cog has been loaded.")

    @commands.Cog.listener()
    async def on_cog_unload(self):
        print("Verification cog has been unloaded.")

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        unverifed_role = disnake.utils.get(member.guild.roles, name="No Verificado")

        if unverifed_role is None:
            await self.bot.owner.send(
                f"Error while attempting to add No Verificado role to user {member.mention}"
            )
            return

        await member.add_roles(unverifed_role)

    @commands.slash_command(
        name="verificar", description="Le agrega el rol de verificado a un usuario"
    )
    async def verificar(
        inter: disnake.ApplicationCommandInteraction, user: disnake.Member
    ):

        # TODO: linkear account id a numero de cuenta y nombre
        # Defer to allow bot to take a while to respond
        await inter.response.defer(ephemeral=True)

        if not "admin" in [role.name.lower() for role in inter.author.roles]:
            await inter.send(
                "No tienes permisos para usar este comando", ephemeral=True
            )
            return

        if "verificado" in [role.name.lower() for role in user.roles]:
            await inter.send("Este usuario ya está verificado", ephemeral=True)
            return

        verified_role: disnake.Role = disnake.utils.get(inter.guild.roles, name="Verificado")  # type: ignore
        unverified_role: disnake.Role = disnake.utils.get(inter.guild.roles, name="No Verificado")  # type: ignore

        await user.remove_roles(unverified_role)
        await user.add_roles(verified_role)

        try:
            await user.send(f"Has sido verificado en **{inter.guild.name}**!")

        except Exception:
            print(
                f"No se pudo enviar el mensaje al usuario {user.mention} tratandolo de verificar."
            )

        await inter.edit_original_response(
            content=f"El usuario {user.mention} ha sido verificado."
        )


def setup(client: commands.Bot):
    client.add_cog(Verification(client))
