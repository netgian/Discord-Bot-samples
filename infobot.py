import discord
from discord.ext import commands

# Make sure to turn on your discord bot intents on the discord developer page
intents = discord.Intents.default()
intents.members = True
intents.presences = True


TOKEN = "YOUR_BOT_TOKEN"
PREFIX = "!"

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print("Ready")

@bot.command(name='userinfo')
async def userinfo(ctx, member: discord.Member = discord.User):
    if member == discord.user.User:
        member = ctx.author

    roles = [role for role in member.roles]
    roles.pop(0)
    rolesMention = " ".join([role.mention for role in roles]) if roles != [] else "No roles"

    permisos = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
    if "Administrator" in permisos:
        permisos = "Administrator"

    embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
    embed.set_author(name=f"»▬«User Info»▬«  ▶  {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Asked for:  {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID: ", value=member.id, inline=False)
    embed.add_field(name="Account created at: ", value=member.created_at.strftime("%#d/%m/%Y, %I:%M %p"), inline=False)
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%#d/%m/%Y, %I:%M %p"), inline=False)
    embed.add_field(name=f"Roles ({len(roles)}): ", value=rolesMention, inline=False)
    embed.add_field(name="Permissions:", value=f"||{permisos}||", inline=False)

    embed.add_field(name='Status: ', value=estado, inline=False)
    await ctx.send(embed=embed)


@bot.command(name="serverinfo")
async def serverinfo(ctx):
    guild = ctx.author.guild
    textC = len(guild.text_channels)
    voiceC = len(guild.voice_channels)

    bots = []
    [bots.append(user) if user.bot else False for user in guild.members]
    bots = len(bots)
    usuarios = len(guild.members) - bots

    embed = discord.Embed(colour=discord.Color.blurple())
    embed.set_author(name=f"»▬«Server Info»▬«   ▶   {guild.name}")
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(text=f"Server name: {guild.name} | ID: {guild.id}")

    embed.add_field(name="Owner:", value=guild.owner.mention, inline=True)
    embed.add_field(name="Boosting Level:", value=f"[{guild.premium_tier}]", inline=True)
    embed.add_field(name="Created at:", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Roles:", value=str(len(guild.roles)), inline=True)
    embed.add_field(name="Members:", value=f"{usuarios} usuarios\n{bots} bots", inline=True)
    embed.add_field(name="Channels:", value=f"{textC} de Texto\n{voiceC} de Voz", inline=True)
    embed.add_field(name="Verification:", value=guild.verification_level, inline=True)
    embed.add_field(name="Emojis:", value=str(len(guild.emojis)), inline=True)
    embed.add_field(name="Region:", value=guild.region, inline=True)

    await ctx.send(embed=embed)

@bot.command(name='roleinfo')
async def roleinfo(ctx, role: discord.Role = discord.Role):
    if role == discord.role.Role:
        await ctx.send("Etiqueta un rol para mostrar su información :)")
    else:
        guild = ctx.author.guild
        perm = ', '.join([str(p[0]).replace("_", " ").title() for p in role.permissions if p[1]])
        perm = "Administrator" if "Administrator" in perm else perm
        embed = discord.Embed(colour=discord.Color.blurple(), timestamp=ctx.message.created_at)

        embed.add_field(name="Nombre:", value=f"{role.mention}", inline=False)
        embed.add_field(name="ID:", value=f"{role.id}", inline=False)
        embed.add_field(
            name="Creado el ",
            value=role.created_at.strftime("%#d/%m/%Y, %I:%M %p"),
            inline=False)
        embed.add_field(name="Permisos:", value=f"{perm}", inline=False)

        embed.set_author(name="»▬«Role info»▬«")
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Solicitado por:  {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

@bot.command(name='botinfo')
async def _bot(ctx):
    em = discord.Embed(colour=discord.Color.blurple(), title='»▬«Bot info»▬«', timestamp=ctx.message.created_at)
    em.add_field(name="Servers", value=len(ctx.bot.guilds))
    em.add_field(name='Users', value=len(ctx.bot.users))
    em.add_field(name='Channels', value=f"{sum(1 for g in ctx.bot.guilds for _ in g.channels)}")
    em.add_field(name="Latency", value=f"{ctx.bot.ws.latency * 1000:.0f} ms")
    em.set_footer(text=f'Asked for:  {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)

bot.run(TOKEN)
