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
guild receptionist commands:
\u001b[0;36m/commands - lists all services\u001b[0;0m
\u001b[0;36m/register - registers the adventurer as a guild member\u001b[0;0m
\u001b[0;36m/create - creates a new quest\u001b[0;0m
\u001b[0;36m/quests - displays the member's quest board\u001b[0;0m
\u001b[0;36m/info - displays the guild member's card\u001b[0;0m
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
        self.add_item(discord.ui.InputText(label="Due Date (ex:2024-01-31)"))
        self.add_item(discord.ui.InputText(label="Difficulty"))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.children[0].value,
            description=self.children[1].value,
            color=discord.Colour.darker_grey(),
        )
        embed.set_footer(
            text="Quest issued on {date}".format(date=datetime.date.today())
        )
        embed.set_author(name="Quest Notice")
        embed.add_field(name="Due Date", value=self.children[2].value)
        embed.add_field(name="Difficulty", value=self.children[3].value)

        valid_quest = True
        try:
            date = datetime.datetime.strptime(self.children[2].value, "%Y-%m-%d")
            print(date)
        except:
            print("invalid date")

        bd.create_task(
            interaction.user.id,
            (
                self.children[0].value,
                self.children[1].value,
                self.children[2].value,
                self.children[3].value,
            ),
        )
        await interaction.response.send_message(embeds=[embed])


@bot.command(name="create", description="create a new task")
async def create_quest(ctx: discord.ApplicationContext):
    await ctx.send_modal(QuestForm(title="Quest Form"))


class MyView(discord.ui.View):
    def __init__(self, user_id, quest_id):
        super().__init__()
        self._user_id = user_id
        self._quest_id = quest_id

    @discord.ui.button(label="Turn in quest", style=discord.ButtonStyle.success)
    async def button_callback(self, button, interaction):
        bd.complete_task(self._user_id, self._quest_id)
        await interaction.response.send_message("quest finished!")


@bot.command(name="quests", description="pulls up the quest board")
async def quests(ctx):
    vals = bd.active_tasks(ctx.author.id)
    if vals:
        for i in vals:
            quest_embed = discord.Embed(
                title=i[1],
                description=i[2],
                color=discord.Colour.darker_grey(),
            )
            quest_embed.set_footer(text="Quest issued on {date}".format(date=i[3]))
            quest_embed.set_author(name="Quest Notice")
            quest_embed.add_field(name="Due Date", value=i[4])
            quest_embed.add_field(name="Difficulty", value=i[5])

            await ctx.respond(embed=quest_embed, view=MyView(ctx.author.id, i[0]))
    else:
        await ctx.respond(
            """```ansi
\u001b[1;31mno quests available...\u001b[0;0m
```"""
        )


bot.run(TOKEN)
