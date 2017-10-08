import os
import discord
import asyncio
import time

client = discord.Client()
global messageDisplayTime
messageDisplayTime = 20
global prefix
prefix = '%'

#Defining premium users
def get_patrons(level='Premium!'):
    p_server = client.get_server('366542432671760396')
    p_role = discord.utils.get(p_server.roles,name=level)
    premiums = [user for user in p_server.members if p_role in user.roles]
    return premiums

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):

    #Per server based directories
    try:
        os.mkdir(message.server.id)
    except FileExistsError:
        pass
    
    #Setup options
    global prefix
    if message.content.startswith(prefix + 'setup'):
        if message.author.server_permissions.administrator:
            print('Admin Role')
            setupSettings = discord.Embed(description='Welcome to setup, please select an option (by typing its corrosponding number): \r\n**1.** Question Setup\r\n**2.** Message Display Time\r\n**3.** Prefix Setup\r\n**4.** Help\r\n**5.** About', colour=0xff5050)
            await client.send_message(message.channel, embed=setupSettings)
            setupSettingsOption = await client.wait_for_message(author=message.author,channel=message.channel)
            
            #Question setup
            if setupSettingsOption.content.startswith('1'):
                numQuestions = 4
                if message.author in get_patrons(level='Premium!'):
                    while True:
                        pQsetup = discord.Embed(description='Please type how many questions you would like', colour=0xff5050)
                        await client.send_message(message.channel, embed=pQsetup)
                        tempQuestions = await client.wait_for_message(author=message.author,channel=message.channel)
                        try:
                            numQuestions = int(tempQuestions.content)
                            break
                        except ValueError:
                            pQsetupError = discord.Embed(description='Please only input an integer', colour=0xff5050)
                            await client.send_message(message.channel, embed=pQsetupError)
                    numQuestions = numQuestions + 1
                        
                global questions
                questions = []
                su0 = discord.Embed(description='Welcome to Question Setup. Type "' + prefix + 'cancel" to cancel setup.', colour=0xff5050)
                await client.send_message(message.channel, embed=su0)
                time.sleep(3)
                for n in range(1,numQuestions):
                    su1 = discord.Embed(description='Please enter question ' + str(n), colour=0xff5050)
                    await client.send_message(message.channel, embed=su1)
                    question1 = await client.wait_for_message(author=message.author,channel=message.channel)
                    if question1.content.startswith(prefix + 'cancel'):
                        await client.send_message(message.channel, '**Question Setup Canceled**')
                        return
                    questions.append(question1.content)
                open(message.server.id + '\QuestionOptions','w').close()
                with open(message.server.id + '\QuestionOptions', 'a') as f:
                    for file in questions:
                        f.write(file + ',')

            #message display time setup
            elif setupSettingsOption.content.startswith('2'):
                mdt1 = discord.Embed(description='**Please enter a value for the amount of seconds you wish for the Submission Log to be displayed for(seconds):**', colour=0xff5050)
                await client.send_message(message.channel, embed=mdt1)
                mdtans = await client.wait_for_message(author=message.author,channel=message.channel)
                mdt = mdtans.content
                global messageDisplayTime
                messageDisplayTime = int(mdt)
                mdt2 = discord.Embed(description='**The message display time has been set to **' + str(messageDisplayTime) + '** seconds**', colour=0xff5050)
                await client.send_message(message.channel, embed=mdt2)
                open(message.server.id + '\MessageDisplay','w').close()
                with open(message.server.id + '\MessageDisplay', 'a') as f:
                    f.write(str(messageDisplayTime))

            #Prefix setup
            elif setupSettingsOption.content.startswith('3'):
                pre1 = discord.Embed(description='**Please enter the prefix you would like to use (please ingnore common prefixes like "!") :', colour=0xff5050)
                pre2 = await client.send_message(message.channel, embed=pre1)
                preChoice = await client.wait_for_message(author=message.author,channel=message.channel)
                prefix = preChoice.content
                pre3 = discord.Embed(description='**Your prefix has been set to: **' + prefix, colour=0xff5050)
                await client.send_message(message.channel, embed=pre3)
                open(message.server.id + '\Prefix','w').close()
                with open(message.server.id + '\Prefix', 'a') as f:
                    f.write(str(prefix))

            #Help
            elif setupSettingsOption.content.startswith('4'):

            #About
            elif setupSettingsOption.content.startswith('5'):
                
        else:
            needAdmin = discord.Embed(description='**You must have Administrator permission in order to use this feature**', colour=0xff5050)
            await client.send_message(message.channel, embed=needAdmin)
            
    #Submission log viewing       
    if message.content.startswith(prefix + 'view'):
        with open(message.server.id + '\Submission', 'r') as f:
            finalSubmission = f.read()
        if not finalSubmission:
            v2 = await client.send_message(message.channel, '**There has been no new submissions**')
            time.sleep(10)
            await client.delete_message(v2)
            return
        viewEmbed = discord.Embed(description=finalSubmission + '\r\n \r\n **To clear the submission log, type "' + prefix + 'clear"**\r\n *This message will automatically close. To change the time this message is displayed for, please change it in setup.*', colour=0xff5050)
        global v1
        v1 = await client.send_message(message.channel, embed=viewEmbed)
        #CHANGE THIS
        time.sleep(messageDisplayTime)
        await client.delete_message(v1)

    #Submission log clearing
    elif message.content.startswith(prefix + 'clear'):
        open(message.server.id + '\Submission','w').close()
        await client.send_message(message.channel, '**The submission log has been cleared**')

    #Introduction/instructions
    elif message.content.startswith(prefix + 'submit'):
        em = discord.Embed(title='---------------NEW-SUBMISSION---------------', description='''Please fill out the questiions in this form to submit a bot-request.
Please start all your answers with the prefex "''' + prefix + '''".
Type "''' + prefix + '''start" to start your submission.
Type "''' + prefix + '''cancel" to cancel your submission.''', colour=0xff5050)
        await client.send_message(message.channel, embed=em)
        startAns = await client.wait_for_message(author=message.author,channel=message.channel)
        if startAns.content.startswith(prefix + 'cancel'):
            await client.send_message(message.channel, '**Submission Canceled**')
            return
        
        
    #Question asking and answer recieving
    if message.content.startswith(prefix + 'start'):
        global answerList
        answerList = []
        try:
            with open(message.server.id + '\QuestionOptions', 'r') as f:
                file_questions = f.read()
            for mainQuestion in file_questions.split(','):
                if not mainQuestion:
                    continue
                em2 = discord.Embed(description=mainQuestion, colour=0xff5050)
                q = await client.send_message(message.channel, embed=em2)
                ans1 = await client.wait_for_message(author=message.author,channel=message.channel)
                if ans1.content.startswith(prefix + 'cancel'):
                    await client.send_message(message.channel, '**Submission Canceled**')
                    return
                answerList.append(ans1.content)
                time.sleep(0.5)
                await client.delete_message(q)
                await client.delete_message(ans1)
        except:
            excepterror = discord.Embed(description='**Please ask your server administrator to set up the questions**', colour=0xff5050)
            eemessage = await client.send_message(message.channel, embed=excepterror)
        
        #Final submission
        emFinal = discord.Embed(description='Are you sure you wish to Submit? ("yes" / "no")', colour=0xff5050)
        await client.send_message(message.channel, embed=emFinal)
        mesFinal = await client.wait_for_message(author=message.author,channel=message.channel)
        if mesFinal.content == 'yes':
            with open(message.server.id + '\Submission', 'a') as f:
                f.write('----------NEW-SUBMISSION---------- \r\n' + '\r\n'.join(answerList) + 2*'\r\n')
            q2 = await client.send_message(message.channel, '**Your application has been submitted**')
            time.sleep(5)
            await client.delete_message(q2)
        elif mesFinal.content =='no':
            q3 = await client.send_message(message.channel, '**Your application has not been submitted**')
            time.sleep(5)
            await client.delete_message(q3)
        else:
            await client.send_message(message.channel, '**Error! Please contact your server admin if you think this is wrong**')

#Token
client.run('MzU4NjQwODA4NzQ1ODkzODg4.DJ7Zyw.3L8Lkny7YGkCT1cTQUMTFLHqXdc')
