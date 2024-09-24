import discord
from discord.ext import commands
import random

# Configuración de los intents del bot
intents = discord.Intents.default()
intents.message_content = True

# Inicialización del bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Lista de preguntas con niveles de dificultad
trivia_questions = [
    {"question": "¿Cuál es el nombre del protagonista de la serie The Legend of Zelda?", "answer": "Link", "difficulty": "fácil"},
    {"question": "¿En qué año se lanzó el primer juego de la serie Super Mario Bros?", "answer": "1985", "difficulty": "fácil"},
    {"question": "¿Cuál es el nombre del planeta natal de Samus Aran en la serie Metroid?", "answer": "Zebes", "difficulty": "medio"},
    {"question": "¿Cuál es el título del primer juego de la serie Final Fantasy?", "answer": "Final Fantasy", "difficulty": "medio"},
    {"question": "¿Cuál es el nombre de la franquicia de videojuegos más vendida de todos los tiempos?", "answer": "Mario", "difficulty": "difícil"},
    {"question": "¿Cuál es el nombre del primer Pokémon en la Pokédex?", "answer": "Bulbasaur", "difficulty": "fácil"},
    {"question": "¿En qué juego aparece el famoso 'It's-a me, Mario!' por primera vez?", "answer": "Super Mario 64", "difficulty": "medio"},
    {"question": "¿Cómo se llama el arma principal del protagonista en Doom?", "answer": "BFG 9000", "difficulty": "difícil"},
    {"question": "¿Cuál es el nombre de la ciudad donde se desarrolla Grand Theft Auto: San Andreas?", "answer": "Los Santos", "difficulty": "medio"},
    {"question": "¿En qué juego de Nintendo puedes encontrar a un personaje llamado 'Tom Nook'?", "answer": "Animal Crossing", "difficulty": "fácil"},
    {"question": "¿Cuál es el nombre del villano principal en la serie de juegos 'Resident Evil'?", "answer": "Albert Wesker", "difficulty": "difícil"},
    {"question": "¿Qué juego popular de Valve presenta una guerra entre terroristas y antiterroristas?", "answer": "Counter-Strike", "difficulty": "medio"},
    {"question": "¿En qué año fue lanzado el primer juego de la serie Halo?", "answer": "2001", "difficulty": "difícil"},
    {"question": "¿Cómo se llama la protagonista del juego 'Tomb Raider'?", "answer": "Lara Croft", "difficulty": "medio"},
    {"question": "¿Qué desarrolladora es responsable del juego 'The Witcher 3: Wild Hunt'?", "answer": "CD Projekt Red", "difficulty": "difícil"},
    {"question": "¿Cuál es el nombre del dragón principal en la serie de juegos Spyro?", "answer": "Spyro", "difficulty": "medio"},
    {"question": "¿En qué juego de PlayStation se hizo famoso el personaje Solid Snake?", "answer": "Metal Gear Solid", "difficulty": "difícil"},
    {"question": "¿Qué juego popular de construcción en bloques fue adquirido por Microsoft en 2014?", "answer": "Minecraft", "difficulty": "fácil"},
    {"question": "¿Cuál es el nombre del asesino protagonista en la serie de juegos Assassin's Creed?", "answer": "Ezio Auditore", "difficulty": "medio"},
    {"question": "¿Cómo se llama la princesa que Mario siempre intenta rescatar?", "answer": "Peach", "difficulty": "fácil"},
    {"question": "¿Cuál es el nombre del mundo en el que se desarrolla la serie de juegos The Elder Scrolls?", "answer": "Tamriel", "difficulty": "difícil"},
    {"question": "¿Qué compañía desarrolló la serie de juegos Call of Duty?", "answer": "Activision", "difficulty": "medio"},
    {"question": "¿Cuál es el nombre del héroe en la serie de juegos Halo?", "answer": "Master Chief", "difficulty": "difícil"},
    {"question": "¿Qué juego tiene como protagonista a un bandicoot mutante llamado Crash?", "answer": "Crash Bandicoot", "difficulty": "fácil"},
    {"question": "¿Cuál es el nombre del modo de juego en Fortnite donde los jugadores compiten para ser el último en pie?", "answer": "Battle Royale", "difficulty": "medio"},
    {"question": "¿En qué año fue lanzado el primer juego de la serie The Legend of Zelda?", "answer": "1986", "difficulty": "difícil"},
    {"question": "¿Cuál es el nombre del creador de la serie de juegos 'Super Mario'?", "answer": "Shigeru Miyamoto", "difficulty": "medio"},
    {"question": "¿Qué juego de lucha de Nintendo reúne personajes de varias franquicias?", "answer": "Super Smash Bros.", "difficulty": "fácil"},
    {"question": "¿Cómo se llama la enfermedad que afecta a los ciudadanos de Raccoon City en Resident Evil?", "answer": "T-Virus", "difficulty": "difícil"},
    {"question": "¿Cuál es el nombre del zorro protagonista de la serie de juegos Star Fox?", "answer": "Fox McCloud", "difficulty": "medio"},
]

# Diccionario para almacenar puntuaciones de jugadores
player_scores = {}

# Diccionario para almacenar preguntas ya usadas por jugador
used_questions = {}

# Evento que se activa cuando el bot está listo
@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} se ha conectado a Discord!')

# Comando de trivia
@bot.command(name='trivia')
async def trivia(ctx, difficulty: str = 'fácil'):
    valid_difficulties = ['fácil', 'medio', 'difícil']
    
    if difficulty not in valid_difficulties:
        await ctx.send(f'Nivel de dificultad inválido. Elige entre: {", ".join(valid_difficulties)}.')
        return

    # Filtrar preguntas por nivel de dificultad
    filtered_questions = [q for q in trivia_questions if q["difficulty"] == difficulty]
    
    if not filtered_questions:
        await ctx.send('No hay preguntas disponibles para este nivel de dificultad.')
        return

    # Filtrar preguntas que no han sido usadas
    user_id = ctx.author.id
    if user_id not in used_questions:
        used_questions[user_id] = set()

    available_questions = [q for q in filtered_questions if q["question"] not in used_questions[user_id]]
    
    if not available_questions:
        await ctx.send('Ya has respondido todas las preguntas disponibles para este nivel de dificultad.')
        return

    # Elegir una pregunta al azar
    question = random.choice(available_questions)
    used_questions[user_id].add(question["question"])  # Marcar la pregunta como usada
    await ctx.send(question["question"])

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        response = await bot.wait_for('message', check=check, timeout=15.0)
        if response.content.lower() == question["answer"].lower():
            score = {'fácil': 1, 'medio': 2, 'difícil': 3}
            if ctx.author.id not in player_scores:
                player_scores[ctx.author.id] = 0
            player_scores[ctx.author.id] += score[difficulty]
            await ctx.send(f'¡Correcto! Has ganado {score[difficulty]} punto(s). Tu puntuación actual es {player_scores[ctx.author.id]} puntos.')
        else:
            await ctx.send(f'Incorrecto. La respuesta correcta era: {question["answer"]}')
    except:
        await ctx.send('Se acabó el tiempo!')

# Comando para ver la puntuación de un jugador
@bot.command(name='puntuación')
async def puntuación(ctx):
    if ctx.author.id in player_scores:
        await ctx.send(f'Tu puntuación actual es {player_scores[ctx.author.id]} puntos.')
    else:
        await ctx.send('No tienes puntuaciones registradas. Juega una trivia para empezar a acumular puntos.')

# Corre el bot
#bot.run('#tu bot token')
