import discord
import asyncio
import subprocess
import pickle
from mcstatus import MinecraftServer

commands = ["help", "ip", "version", "info", "badCommand", "Messages","server"]
totalHidden = 3;

curVersion = 0.1

MineServer = MinecraftServer.lookup("127.0.0.1:25565")


class person:
    name = ""
    commandsNum = []
    hiddenFound = 0
    version = 0
    def __init__(self):
        self.commandsNum = [0, 0, 0, 0, 0, 0,0]
        self.hiddenFound = 0
        self.version = curVersion


client = discord.Client()

people = []
cashedIp = ""

def updatePerson(pos):
    global people
    if people[pos].version == curVersion:
        return
    while len(people[pos].commandsNum) < len(commands):
        people[pos].commandsNum.append(0)
    people[pos].version = curVersion

def checkIfInGame(author):
    count = -1
    global people
    for persons in people:
        count += 1
        if persons.name == author:
            updatePerson(count)
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

        messageCase = message.content.lower()
    
        playerPos = checkIfInGame(message.author.name)
        if playerPos == -1:
            playerPos = addNewPlayer(message.author.name)
            print("Added new player : " + people[playerPos].name)

        if messageCase.startswith('!ip'):
            # await client.send_message(message.channel, 'Currenttly Ip dont work')

            # bash = "curl ipecho.net/plain"

            output = result = subprocess.run(['curl', 'ipecho.net/plain'], stdout=subprocess.PIPE)
            Ip = output.stdout.decode('utf-8')

            if cashedIp != Ip and cashedIp != "":
                print('IP CHANGED')
            await client.send_message(message.channel, 'Current Ip ' + Ip)

            people[playerPos].commandsNum[1] += 1

        elif messageCase.startswith('!info'):
            pp = people[playerPos]
            string = "Player : " + pp.name
            string += " \n !help : " + str(pp.commandsNum[0])
            string += " \n !ip : " + str(pp.commandsNum[1])
            string += " \n !version : " + str(pp.commandsNum[2])
            string += " \n !info : " + str(pp.commandsNum[3])
            string += " \n !badCommand : " + str(pp.commandsNum[4])
            string += " \n General Chat : " + str(pp.commandsNum[5])
            string += " \n !server : " + str(pp.commandsNum[6])
            string += " \n hidden Commands used : " + str(pp.hiddenFound) + " / " + str(totalHidden)
            string += " \n Bot Version : " + str(curVersion)

            await client.send_message(message.channel, string)
            people[playerPos].commandsNum[3] += 1

        elif messageCase.startswith('!help'):
            await client.send_message(message.channel, 'Current Commands : \n !version \n !ip \n !info')
            people[playerPos].commandsNum[0] += 1

        elif messageCase.startswith('!server'):
            serverCommand = messageCase.split()
            string = ""
            
            
            
            if len(serverCommand) == 1:
                string = "Needs a sub command :"
                string += " \n ```<players>``` to see number of players online"
                string += " \n ```<playerNames>``` to see the name of players online"
                string += " \n ```<online>``` to see if the server is online"
            elif serverCommand[1] == "players":
                try:
                    status = MineServer.status()
                    string = "The server has {0} players online".format(status.players.online)
                except Exception:
                    string = "Server not online"
            elif serverCommand[1] == "online":
                try:
                    ping = MineServer.ping()
                    string = "The server has {0} ms ping to bot so prob online".format(ping)
                except Exception:
                    string = "Server not online"
            elif serverCommand[1] == "playernames":
                try:
                    query = MineServer.query()
                    string = "The server has the following players online: ``` {0}".format(", ".join(query.players.names)) + " ```"
                except Exception:
                    string = "Server not online"
            else:
                string = "Incorrect Sub Command do !server to see all valid"
                    
            people[playerPos].commandsNum[6] += 1
            await client.send_message(message.channel,string)
        elif messageCase.startswith('!version'):
            version = 'Server is Currently Running ```FTB DireWolf 1.10 - Minecraft V 1.7.0``` just get a legit minecraft account'
            await client.send_message(message.channel, version)
            people[playerPos].commandsNum[2] += 1
        elif messageCase.startswith('!'):
            await client.send_message(message.channel, "Command '" + message.content + "' is not a command dum dum, see !help")
            people[playerPos].commandsNum[4] += 1

        if messageCase.startswith('!'):
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