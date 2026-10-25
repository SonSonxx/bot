"""
Mig's Discord Bot — interactive catalog.
Shows the catalog's original loader text as Lua snippets; this bot does not execute them.
"""
import io
import logging
import os
import random
import zipfile
from pathlib import Path

import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("mig_bot")

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não definido. Configure a variável de ambiente no painel de hospedagem.")

def read_authorized_user_id():
    value = os.getenv("AUTHORIZED_USER_ID", "").strip()
    if not value:
        return None
    if not value.isdecimal() or int(value) <= 0:
        raise RuntimeError("AUTHORIZED_USER_ID precisa ser um ID numérico positivo.")
    return int(value)

AUTHORIZED_USER_ID = read_authorized_user_id()

CATALOG = {
    "MM2": [
        {
            "name": "SP HUB",
            "url": "https://raw.githubusercontent.com/as6cd0/SP_Hub/refs/heads/main/Loader",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/as6cd0/SP_Hub/refs/heads/main/Loader"))()',
        },
        {
            "name": "YARHM",
            "url": "https://raw.githubusercontent.com/Joystickplays/psychic-octo-invention/main/yarhm.lua",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/Joystickplays/psychic-octo-invention/main/yarhm.lua", false))()',
        },
        {
            "name": "Less Menu",
            "url": "https://raw.githubusercontent.com/ness-script/mm2/main/hub",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/ness-script/mm2/main/hub"))()',
        },
        {
            "name": "Metan Hub",
            "url": "https://raw.githubusercontent.com/Youdfff/MetanHub/refs/heads/main/moonveil.lua",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/Youdfff/MetanHub/refs/heads/main/moonveil.lua"))()',
        },
        {
            "name": "MONO HUB",
            "url": "https://raw.githubusercontent.com/Main-Scripts-Ready-V9/Mono-Hub/refs/heads/main/Murder-Mystery-Hub.lua",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/Main-Scripts-Ready-V9/Mono-Hub/refs/heads/main/Murder-Mystery-Hub.lua"))()',
        },
    ],
    "Steal a Brainrot": [
        {
            "name": "Printed Duel",
            "url": "https://api.luarmor.net/files/v4/loaders/25c9a4fc1c1b2908fcb859d49c1a355b.lua",
            "loader": 'loadstring(game:HttpGet("https://api.luarmor.net/files/v4/loaders/25c9a4fc1c1b2908fcb859d49c1a355b.lua"))()',
        },
        {
            "name": "Sofka Hub Anti Lag",
            "url": "https://raw.githubusercontent.com/6ixhub/ANTI-LAG/refs/heads/main/SOFKA",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/6ixhub/ANTI-LAG/refs/heads/main/SOFKA"))()',
        },
        {
            "name": "CHIRAQ HUB",
            "url": "https://api.luarmor.net/files/v4/loaders/1883fe82b9d8cca5ea890c9d6edfc19e.lua",
            "loader": 'loadstring(game:HttpGet("https://api.luarmor.net/files/v4/loaders/1883fe82b9d8cca5ea890c9d6edfc19e.lua"))()',
        },
        {
            "name": "Irish Hub Free 1 Day Desync",
            "url": "https://raw.githubusercontent.com/irishhub-scriptzzz/Desync-Bypass-Free-1-Day/refs/heads/main/Irish%20Hub%20Desynx%20Free%201%20Day.lua",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/irishhub-scriptzzz/Desync-Bypass-Free-1-Day/refs/heads/main/Irish%20Hub%20Desynx%20Free%201%20Day.lua"))()',
        },
        {
            "name": "Koby Finder",
            "url": "https://api.getpolsec.com/scripts/hosted/ba906ffb795c03853572622ca4d0e157983dfe3763d49bc84b27521c4b228302.lua",
            "loader": 'script_key = "trial"\nloadstring(game:HttpGet("https://api.getpolsec.com/scripts/hosted/ba906ffb795c03853572622ca4d0e157983dfe3763d49bc84b27521c4b228302.lua"))()',
        },
    ],
    "Steal a Egg": [
        {
            "name": "Stalalika Hub",
            "url": "https://flowauth.net/v1/loaders/fd88218fedb3d91bca7d234a32a42e0b.lua",
            "loader": 'loadstring(game:HttpGet("https://flowauth.net/v1/loaders/fd88218fedb3d91bca7d234a32a42e0b.lua"))()',
        },
        {
            "name": "Venyx Hub",
            "url": "https://raw.githubusercontent.com/tienkhanh1/Venyx/main/VenyxHub",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/tienkhanh1/Venyx/main/VenyxHub"))()',
        },
        {
            "name": "Cebo Script",
            "url": "https://raw.githubusercontent.com/apiluarmor-hub/CeboScripts-Egg/refs/heads/main/teleports-eggs",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/apiluarmor-hub/CeboScripts-Egg/refs/heads/main/teleports-eggs"))()',
        },
        {
            "name": "Miranda Hub - New Update",
            "url": "https://raw.githubusercontent.com/miirandahub/loader/refs/heads/main/afkk",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/miirandahub/loader/refs/heads/main/afkk"))()',
        },
        {
            "name": "Pulse Hub",
            "url": "https://raw.githubusercontent.com/PulseZax/Loader/refs/heads/main/.lua",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/PulseZax/Loader/refs/heads/main/.lua"))()',
        },
        {
            "name": "New Bee Hub",
            "url": "https://flowauth.net/v1/loaders/026c52c6ec62cd086277f45a113a680a.lua",
            "loader": 'loadstring(game:HttpGet("https://flowauth.net/v1/loaders/026c52c6ec62cd086277f45a113a680a.lua"))()',
        },
        {
            "name": "Lennon Hub Steal an Egg",
            "url": "https://raw.githubusercontent.com/lennonxscripts/lennonfarmv2/refs/heads/main/stealanegg",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/lennonxscripts/lennonfarmv2/refs/heads/main/stealanegg"))()',
        },
        {
            "name": "Admin Visual",
            "url": "https://raw.githubusercontent.com/Dayvinksthik/Script/refs/heads/main/Games/JoshBNS-Crack.lua",
            "loader": 'loadstring(game:HttpGet("https://raw.githubusercontent.com/Dayvinksthik/Script/refs/heads/main/Games/JoshBNS-Crack.lua"))()',
        },
    ],
}

EMOJIS = {"MM2": "🔪", "Steal a Brainrot": "🧠", "Steal a Egg": "🥚"}
HELP_TEXT = (
    "**📜 Comandos disponíveis**\n\n"
    "`/script` — abre o catálogo interativo por jogo\n"
    "`/help` — mostra esta ajuda\n"
    "`.help` — mostra esta ajuda por mensagem\n"
    "`/source` — envia o ZIP do código-fonte ao ID autorizado\n\n"
    "Escolha um jogo e use **Outro script** para alternar entre entradas."
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

def make_source_zip():
    root = Path(__file__).resolve().parent
    names = ("bot.py", "requirements.txt", "README.md", ".env.example", "sillydev.conf")
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            path = root / name
            if path.is_file():
                archive.write(path, arcname=name)
    output.seek(0)
    return output

def make_embed(game, entry, index):
    entries = CATALOG[game]
    embed = discord.Embed(
        title=f"{EMOJIS[game]} {entry['name']}",
        description=(
            f"**Jogo:** {game}\n"
            f"**Entrada {index + 1} de {len(entries)}**\n\n"
            f"**Loader Lua (copie o bloco):**\n```lua\n{entry['loader']}\n```"
        ),
        color=0x5865F2,
    )
    embed.add_field(name="Fonte original", value=f"[Abrir fonte]({entry['url']})", inline=False)
    embed.set_footer(text="O bot exibe o texto do loader; não executa código externo.")
    return embed

class GameSelectView(discord.ui.View):
    def __init__(self, owner_id):
        super().__init__(timeout=180)
        self.owner_id = owner_id

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Este menu pertence a outra pessoa. Use `/script` para abrir o seu.",
                ephemeral=True,
            )
            return False
        return True

    @discord.ui.select(
        placeholder="Escolha um jogo…",
        options=[
            discord.SelectOption(label="MM2", emoji="🔪", value="MM2"),
            discord.SelectOption(label="Steal a Brainrot", emoji="🧠", value="Steal a Brainrot"),
            discord.SelectOption(label="Steal a Egg", emoji="🥚", value="Steal a Egg"),
        ],
    )
    async def choose_game(self, interaction: discord.Interaction, select: discord.ui.Select):
        game = select.values[0]
        index = random.randrange(len(CATALOG[game]))
        await interaction.response.edit_message(
            content=None,
            embed=make_embed(game, CATALOG[game][index], index),
            view=ScriptView(game, index, self.owner_id),
        )

class ScriptView(discord.ui.View):
    def __init__(self, game, current_index, owner_id):
        super().__init__(timeout=180)
        self.game = game
        self.current_index = current_index
        self.owner_id = owner_id

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Este menu pertence a outra pessoa. Use `/script` para abrir o seu.",
                ephemeral=True,
            )
            return False
        return True

    @discord.ui.button(label="Outro script", style=discord.ButtonStyle.secondary, emoji="🔀")
    async def next_entry(self, interaction: discord.Interaction, button: discord.ui.Button):
        entries = CATALOG[self.game]
        next_index = random.choice([i for i in range(len(entries)) if i != self.current_index])
        self.current_index = next_index
        await interaction.response.edit_message(
            embed=make_embed(self.game, entries[next_index], next_index),
            view=self,
        )

    @discord.ui.button(label="Voltar ao menu", style=discord.ButtonStyle.primary, emoji="🔙")
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            content="**Escolha um jogo:**",
            embed=None,
            view=GameSelectView(self.owner_id),
        )

@bot.tree.command(name="script", description="Menu interativo do catálogo por jogo")
async def script_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**Escolha um jogo:**",
        view=GameSelectView(interaction.user.id),
        ephemeral=False,
    )

@bot.tree.command(name="help", description="Mostra os comandos disponíveis")
async def slash_help(interaction: discord.Interaction):
    await interaction.response.send_message(HELP_TEXT, ephemeral=True)

@bot.tree.command(name="source", description="Recebe o ZIP do código-fonte (apenas autorizado)")
async def source_command(interaction: discord.Interaction):
    if AUTHORIZED_USER_ID is None or interaction.user.id != AUTHORIZED_USER_ID:
        await interaction.response.send_message(
            "❌ Você não tem permissão para usar este comando.", ephemeral=True
        )
        return
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(
        "📦 Aqui estão os arquivos-fonte atualizados:",
        file=discord.File(make_source_zip(), filename="bot_source.zip"),
        ephemeral=True,
    )

@bot.command(name="help")
async def prefix_help(ctx):
    await ctx.send(HELP_TEXT)

@bot.event
async def setup_hook():
    synced = await bot.tree.sync()
    logger.info("Comandos slash sincronizados: %d", len(synced))

@bot.event
async def on_ready():
    logger.info("Bot online como %s (ID: %s)", bot.user, bot.user.id if bot.user else "?")
    if AUTHORIZED_USER_ID is None:
        logger.warning("AUTHORIZED_USER_ID não definido; /source bloqueado para todos.")

if __name__ == "__main__":
    bot.run(TOKEN)
