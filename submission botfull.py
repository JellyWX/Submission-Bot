
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
    #Question setup
    if message.content.startswith('%setup'):
        global questions
        questions = []
        for n in range(1,4):
            su1 = discord.Embed(description='Please enter question:' + str(n), colour=0xff5050)
            await client.send_message(message.channel, embed=su1)
            question1 = await client.wait_for_message(author=message.author,channel=message.channel)
            questions.append(question1.content)
        open('QuestionOptions','w').close()
        with open('QuestionOptions', 'a') as f:
            for file in questions:
                f.write(file + ',')

    #Submission log viewing       
    if message.content.startswith('%view'):
        with open('Submission', 'r') as f:
            finalSubmission = f.read()
        viewEmbed = discord.Embed(description=finalSubmission, colour=0xff5050)
        await client.send_message(message.channel, embed=viewEmbed)

    #Submission log clearing
    elif message.content.startswith('%clear'):
        open('Submission','w').close()
        await client.send_message(message.channel, '**The submission log has been cleared**')

    #Introduction/instructions
    elif message.content.startswith('%submit'):
        em = discord.Embed(title='---------------NEW-SUBMISSION---------------', description='''Please fill out the questiions in this form to submit a bot-request.
Please start all your answers with the prefex "%".
Type "%start" to start your submission.''', colour=0xff5050)
        await client.send_message(message.channel, embed=em)
        
    #Question asking and answer recieving
    if message.content.startswith('%start'):
        global answerList
        answerList = []
        with open('QuestionOptions', 'r') as f:
            file_questions = f.read()
        for mainQuestion in file_questions.split(','):
            if not mainQuestion:
                continue
            em2 = discord.Embed(description=mainQuestion, colour=0xff5050)
            await client.send_message(message.channel, embed=em2)
            ans1 = await client.wait_for_message(author=message.author,channel=message.channel)
            answerList.append(ans1.content)
        
        #Final submission
        emFinal = discord.Embed(description='Are you sure you wish to Submit? ("%yes" / "%no")', colour=0xff5050)
        await client.send_message(message.channel, embed=emFinal)
        mesFinal = await client.wait_for_message(author=message.author,channel=message.channel)
        if mesFinal.content == '%yes':
            with open('Submission', 'a') as f:
                f.write('----------NEW-SUBMISSION---------- \r\n' + '\r\n'.join(answerList) + 2*'\r\n')
            await client.send_message(message.channel, '**Your application has been submitted**')
        elif mesFinal.content =='%no':
            await client.send_message(message.channel, '**Your application has not been submitted**')
        else:
            await client.send_message(message.channel, 'Error')

#Token
client.run('MzU4NjQwODA4NzQ1ODkzODg4.DJ7Zyw.3L8Lkny7YGkCT1cTQUMTFLHqXdc')
