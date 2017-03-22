import discord
import asyncio
import subprocess
import pickle

commands = ["help", "ip", "version", "info", "badCommand","Messages"]

totalHidden = 3;


class person:
    name = ""
    commandsNum = []
    hiddenFound = 0

    def __init__(self):
        self.commandsNum = [0,0,0,0,0,0]
        self.hiddenFound = 0



client = discord.Client()


people = []
cashedIp = ""


def checkIfInGame(author):
    count = -1
    global people
    for persons in people:
        count += 1
        if persons.name == author:
            return count

    return -1

def addNewPlayer(author):
    global people
    player = person()
    player.name = author
    people.append(player)
    return checkIfInGame(author)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    try:
        with open('peopleSaveFile', 'rb') as fp:
            global people
            people = pickle.load(fp)
    except IOError as e:
        global people
        people = []
        print(str(e))

global playerPos

@client.event
async def on_message(message):
    global people
    try:

        playerPos = checkIfInGame(message.author.name)
        if playerPos == -1:
            playerPos = addNewPlayer(message.author.name)
            print("Added new player : " + people[playerPos].name)


        if message.content.startswith('!ip'):
            # await client.send_message(message.channel, 'Currenttly Ip dont work')

            # bash = "curl ipecho.net/plain"

            output = result = subprocess.run(['curl', 'ipecho.net/plain'], stdout=subprocess.PIPE)
            Ip = output.stdout.decode('utf-8')

            if cashedIp != Ip and cashedIp != "":
                print('IP CHANGED')
            await client.send_message(message.channel, 'Current Ip ' + Ip)

            people[playerPos].commandsNum[1] += 1

        elif message.content.startswith('!info'):
            pp = people[playerPos]
            string = "Player : " + pp.name
            string += " \n !help : " + str(pp.commandsNum[0])
            string += " \n !ip : " + str(pp.commandsNum[1])
            string += " \n !version : " + str(pp.commandsNum[2])
            string += " \n !info : " + str(pp.commandsNum[3])
            string += " \n !badCommand : " + str(pp.commandsNum[4])
            string += " \n General Chat : " + str(pp.commandsNum[5])
            string += " \n hidden Commands used : " + str(pp.hiddenFound) + " / " + str(totalHidden)

            await client.send_message(message.channel, string)
            people[playerPos].commandsNum[3] += 1

        elif message.content.startswith('!help'):
            await client.send_message(message.channel, 'Current Commands : \n !version \n !ip \n !info')
            people[playerPos].commandsNum[0] += 1

        elif message.content.startswith('!version'):
            version = 'Server is Currently Running DireWolf20 1.8.1 '
            version += 'Make sure to update'
            await client.send_message(message.channel, version)
            people[playerPos].commandsNum[2] += 1
        elif message.content.startswith('!'):
            await client.send_message(message.channel, "Command '" + message.content + "' is not a command dum dum, see !help")
            people[playerPos].commandsNum[4] += 1

        if message.content.startswith('!'):
            pass
            with open('peopleSaveFile', 'wb') as fp:
                pickle.dump(people, fp)

        people[playerPos].commandsNum[5] += 1

    except Exception as e:
        print('Error! ' + str(e))
        # await client.send_message(message.channel, 'ERROR')
        print('Generated from : ' + message.content)


		
tokenFile = open("token", "r") 
client.run(tokenFile.read())