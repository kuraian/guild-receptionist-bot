import discord
import os
from dotenv import load_dotenv
import backend as bd
import datetime

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.command(name="hello", description="Say hello to the bot")
async def say_hello(ctx):
    await ctx.respond("hewwo :3")


@bot.command(name="commands", description="lists sidekick's commands")
async def commands(ctx):
    await ctx.respond(
        """```ansi
cà phê bot commands:
\u001b[0;36m/commands - displays all commands\u001b[0;0m
\u001b[0;36m/register - creates a user and accompanying db\u001b[0;0m
\u001b[0;36m/create - creates a new quest\u001b[0;0m
\u001b[0;36m/quests - displays the quest board\u001b[0;0m
```"""
    )


@bot.command(name="register", description="start here!")
async def register(ctx):
    if bd.create_user(ctx.author.id):
        await ctx.respond(
            """```ansi
\u001b[1;36mwelcome...\u001b[0;0m
```"""
        )
    else:
        await ctx.respond(
            """```ansi
\u001b[1;31muser already exists...\u001b[0;0m
```"""
        )


class QuestForm(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Quest Title"))
        self.add_item(
            discord.ui.InputText(
                label="Quest Description", style=discord.InputTextStyle.long
            )
        )
        self.add_item(discord.ui.InputText(label="Due Date (Year-Month-Day)"))
        self.add_item(discord.ui.InputText(label="Difficulty"))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.children[0].value,
            description=self.children[1].value,
            color=discord.Colour.darker_grey(),
        )
        embed.set_footer(
            text="Quest issued on {date}.".format(date=datetime.date.today())
        )
        embed.set_author(name="Quest Notice")
        embed.add_field(name="Due Date", value=self.children[2].value)
        embed.add_field(name="Difficulty", value=self.children[3].value)

        bd.create_task(
            (
                self.children[0].value,
                self.children[1].value,
                self.children[2].value,
                self.children[3].value,
            )
        )
        await interaction.response.send_message(embeds=[embed])


@bot.command(name="create", description="create a new task")
async def create_quest(ctx: discord.ApplicationContext):
    await ctx.send_modal(QuestForm(title="Quest Form"))


@bot.command(name="quests", description="pulls up the quest board")
async def quests(ctx):
    vals = bd.active_tasks(ctx.author.id)
    await ctx.respond(vals)


bot.run(TOKEN)
