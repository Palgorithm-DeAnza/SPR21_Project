import discord
from discord.ext import commands
import wolframalpha
import googletrans
from dotenv import load_dotenv
import os
import ed
import asyncio
load_dotenv()


client = discord.Client()
client = commands.Bot(command_prefix="i")
client.remove_command("help")

@client.event
async def on_ready():
    print("Im on.")

@client.command()
async def mup(ctx):
    await ctx.send("Im ready.")

@client.command()
async def math(ctx, *, question):

            #initialized wolframalpha client with api token from .env file
    math = wolframalpha.Client(os.environ.get('Wolframaplha_API'))
    try:
            #query question from api and put it in resQ
        resQ = math.query(str(question))

                #find the actual answer in text
        answer = next(resQ.results).text
        # print(dir(ctx))
                #image for logo
        # print((next(resQ.results)))
        image_addy= "https://www.iconsdb.com/icons/preview/red/wolfram-alpha-xxl.png"
                #embedding to send
        e = discord.Embed(color=0xe74c3c, description = f"{answer}")
        e.set_footer(text= f'Requested by {ctx.author}' , icon_url=image_addy)
                #Say typing and wait 2 second then send the embedding
        await ctx.trigger_typing()
        await asyncio.sleep(2)
        await ctx.send(embed = e)
                #catch exception if we didn't find an answer
    except StopIteration:
        await ctx.send("I have no answers for you. :( ")






@client.command(aliases = ["tran"])
async def translate(ctx,lang_to,*,argument):


            #language tp translate to needs to be lowercase to find it in the google trans language dictionary
    lang_to = lang_to.lower()

            # Chinese has 2different languges(simplified and traditional) so doesn't recognize just chinese so to make the simplified default
    if lang_to == "chinese":
        lang_to = "zh-cn"

    # print(googletrans.LANGUAGES)

            #Check if the languge we are translating too is found in the list
    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
        raise commands.BadArgument("Can't find the languages you are trying to translate to.")

            # initialize google translator
    translator = googletrans.Translator()

            # translate given argument into given languge
    transed = translator.translate(argument, dest=lang_to)
    # print(dir(transed))
    # print(transed.extra_data["definitions"][0][1][0])
    # for direct in dir(transed):
    # example = transed.extra_data["definitions"][0][1][0][2]


            #If it has no pronunciation or the same as argument
    if transed.pronunciation == None or transed.pronunciation == argument:
        pronunciation = "---"
            #if it has a pronunciation then get it
    else:
        pronunciation = transed.pronunciation

            #embed the information in a box to send it
    e = discord.Embed(color=0xe74c3c, title=f"{transed.text} \nPronounced '{pronunciation}'")
    imageAdd = "https://cdn3.iconfinder.com/data/icons/google-suits-1/32/18_google_translate_text_language_translation-512.png"
    e.set_footer(text="Google translate", icon_url=imageAdd)

    await ctx.trigger_typing()
    await asyncio.sleep(2)
            #send it on discord
    await ctx.send(embed = e)

@client.event
async def on_message(message):
    await client.process_commands(message)
            #check if author is bot
    if client.user == message.author:
        return
            #check if PalBot is @ed
    if "<@!840905807717335040>" in message.content:
        content = message.content
        content = content.replace("<@!840905807717335040>", " ")
        math = wolframalpha.Client(os.environ.get('Wolframaplha_API'))
        resQ = math.query(str(content))
        # print((next(resQ.results)))

        try:
            # answer = next(resQ.results).text
                #obtain image answer
            Answer_image = next(resQ.results)["subpod"]["img"]["@src"]
            image_addy = "https://www.iconsdb.com/icons/preview/red/wolfram-alpha-xxl.png"
            e = discord.Embed(color=0xe74c3c)
            e.set_image(url=Answer_image)
            e.set_footer(text=f'Requested by {message.author}', icon_url=image_addy)
            # print(dir(message.channel))
            await message.channel.trigger_typing()
            await asyncio.sleep(2)
            await message.channel.send(embed=e)
        except StopIteration:
            await message.channel.send("I have no answers for you. :( ")

@client.command()
async def help(ctx):
    # descript= "imath - to get a copyable answer from wolframAlpha \n@PalBot 'question'- to get an image answer. \
    # nitran 'language to translate to' 'What to translate?' - to translate anything."
    embedding = discord.Embed(color=0xe74c3c, title="PalBot")
    image_addy = "https://www.iconsdb.com/icons/preview/red/wolfram-alpha-xxl.png"
    embedding.set_footer(text="© 2021 Palgorithm", icon_url=image_addy)
    # embedding.set_image(url=image_addy)
    embedding.add_field(name="itran 'language to translate to' 'What to translate?'", value= "To translate anything using google translate.",inline=False)
    embedding.add_field(name="imath 'question'", value='To get a copyable answer from wolframAlpha', inline=False)
    embedding.add_field(name="@PalBot 'question'", value="- To get an image answer from wolframAlpha.", inline=False)
    embedding.set_thumbnail(url=image_addy)
    await ctx.send(embed= embedding)

client.run(os.environ.get('Bot_Token'))