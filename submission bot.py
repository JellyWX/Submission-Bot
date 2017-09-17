
import discord
import asyncio

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('%submit'):
        em = discord.Embed(title='---------------NEW-SUBMISSION---------------', description='''Please fill out the questiions in this form to submit a bot-request.
Please start all your answers with the prefex "%".
Type "%start" to start your submission.''', colour=0xff5050)
        await client.send_message(message.channel, embed=em)
    #first question
    if message.content.startswith('%start'):
        em2 = discord.Embed(description='What is your discord name?', colour=0xff5050)
        await client.send_message(message.channel, embed=em2)
        ans1 = await client.wait_for_message(author=message.author,channel=message.channel)
        em3 = discord.Embed(description='Thank You, Could you please describe what your bot does in detail?', colour=0xff5050)
        await client.send_message(message.channel, embed=em3)
        ans2 = await client.wait_for_message(author=message.author,channel=message.channel)
        
        



        emFinal = discord.Embed(description='Are you sure you wish to Submit? ("%yes" / "%no")', colour=0xff5050)
        await client.send_message(message.channel, embed=emFinal)
        mesFinal = await client.wait_for_message(author=message.author,channel=message.channel)
        if mesFinal.content == '%yes':
            with open('Submission', 'a') as f:
                f.write(ans1.content + '\r\n -----------QUESTION2----------- \r\n' + ans2.content)
        elif mesFinal.content =='%no':
            await client.send_message(message.channel, 'Well... What a fucking waste of time that was!')
        else:
            await client.send_message(message.channel, 'Error')
        
        
        
    
                                                        
client.run('MzU4NjQwODA4NzQ1ODkzODg4.DJ7Zyw.3L8Lkny7YGkCT1cTQUMTFLHqXdc')
