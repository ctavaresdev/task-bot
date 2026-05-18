import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

# -------------------------
# Configuração do bot
# -------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

ARQUIVO = "dados_estudos.json"


# -------------------------
# Funções de banco JSON
# -------------------------
def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return {
            "tarefas": [],
            "provas": [],
            "materias": []
        }

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# -------------------------
# Evento inicial
# -------------------------
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")


# -------------------------
# Comando de ajuda
# -------------------------
@bot.command()
async def comandos(ctx):
    mensagem = """
🤖 **TASK BOT - Comandos Disponíveis**

📌 **Tarefas**
!tarefa [descrição] → Adiciona tarefa
!tarefas → Lista tarefas
!remover_tarefa [número] → Remove tarefa

📚 **Matérias**
!materia [nome] → Adiciona matéria
!materias → Lista matérias
!remover_materia [número] → Remove matéria

🗓️ **Provas**
!prova [matéria] [data] → Agenda prova
!provas → Lista provas
!remover_prova [número] → Remove prova

ℹ️ **Ajuda**
!comandos → Mostra todos os comandos
"""
    await ctx.send(mensagem)


# -------------------------
# Adicionar tarefa
# -------------------------
@bot.command()
async def tarefa(ctx, *, descricao):
    dados = carregar_dados()
    dados["tarefas"].append(descricao)
    salvar_dados(dados)

    await ctx.send(f"📌 Tarefa adicionada: {descricao}")


# -------------------------
# Listar tarefas
# -------------------------
@bot.command()
async def tarefas(ctx):
    dados = carregar_dados()

    if not dados["tarefas"]:
        await ctx.send("✅ Nenhuma tarefa cadastrada.")
        return

    lista = "\n".join(
        [f"{i+1}. {t}" for i, t in enumerate(dados["tarefas"])]
    )

    await ctx.send(f"📚 Suas tarefas:\n{lista}")


# -------------------------
# Remover tarefa
# -------------------------
@bot.command()
async def remover_tarefa(ctx, numero: int):
    dados = carregar_dados()

    if not dados["tarefas"]:
        await ctx.send("📭 Não há tarefas para remover.")
        return

    if numero < 1 or numero > len(dados["tarefas"]):
        await ctx.send("❌ Número de tarefa inválido.")
        return

    tarefa_removida = dados["tarefas"].pop(numero - 1)
    salvar_dados(dados)

    await ctx.send(f"🗑️ Tarefa removida: {tarefa_removida}")


# -------------------------
# Adicionar matéria
# -------------------------
@bot.command()
async def materia(ctx, *, nome):
    dados = carregar_dados()
    dados["materias"].append(nome)
    salvar_dados(dados)

    await ctx.send(f"📖 Matéria adicionada: {nome}")


# -------------------------
# Listar matérias
# -------------------------
@bot.command()
async def materias(ctx):
    dados = carregar_dados()

    if not dados["materias"]:
        await ctx.send("📭 Nenhuma matéria cadastrada.")
        return

    lista = "\n".join(
        [f"{i+1}. {m}" for i, m in enumerate(dados["materias"])]
    )

    await ctx.send(f"📝 Matérias:\n{lista}")


# -------------------------
# Remover matéria
# -------------------------
@bot.command()
async def remover_materia(ctx, numero: int):
    dados = carregar_dados()

    if not dados["materias"]:
        await ctx.send("📭 Não há matérias para remover.")
        return

    if numero < 1 or numero > len(dados["materias"]):
        await ctx.send("❌ Número de matéria inválido.")
        return

    materia_removida = dados["materias"].pop(numero - 1)
    salvar_dados(dados)

    await ctx.send(f"🗑️ Matéria removida: {materia_removida}")


# -------------------------
# Adicionar prova
# -------------------------
@bot.command()
async def prova(ctx, materia, data):
    dados = carregar_dados()

    dados["provas"].append({
        "materia": materia,
        "data": data
    })

    salvar_dados(dados)

    await ctx.send(f"🗓️ Prova de {materia} marcada para {data}")


# -------------------------
# Listar provas
# -------------------------
@bot.command()
async def provas(ctx):
    dados = carregar_dados()

    if not dados["provas"]:
        await ctx.send("🎉 Nenhuma prova agendada.")
        return

    lista = "\n".join(
        [
            f"{i+1}. {p['materia']} - {p['data']}"
            for i, p in enumerate(dados["provas"])
        ]
    )

    await ctx.send(f"📅 Provas agendadas:\n{lista}")


# -------------------------
# Remover prova
# -------------------------
@bot.command()
async def remover_prova(ctx, numero: int):
    dados = carregar_dados()

    if not dados["provas"]:
        await ctx.send("📭 Não há provas para remover.")
        return

    if numero < 1 or numero > len(dados["provas"]):
        await ctx.send("❌ Número de prova inválido.")
        return

    prova_removida = dados["provas"].pop(numero - 1)
    salvar_dados(dados)

    await ctx.send(
        f"🗑️ Prova removida: {prova_removida['materia']} - {prova_removida['data']}"
    )


# -------------------------
# Rodar bot
# -------------------------


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)
