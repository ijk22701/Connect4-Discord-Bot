from email.policy import default
from re import purge
from turtle import delay
import discord
from discord.ext import commands

purgeCount = int(3)
boardBackgroundEmoji = '▫️'
boardLength = 7
boardHeight = 6

async def connect4Main(ctx, bot):
    global purgeCount
    global boardBackgroundEmoji
    global boardLength
    global boardHeight
    board = [[boardBackgroundEmoji for a in range(boardLength)] for b in range(boardHeight)]
    currentPlayer = 1
    player1 = await getUserCharacter(ctx, bot, currentPlayer)
    player2 = await getUserCharacter(ctx, bot, currentPlayer + 1)
 
    while player1 == player2:
        await ctx.send("Please select a different emoji than player 1.")
        player2 = await getUserCharacter(ctx, bot, currentPlayer + 1)
        purgeCount += int(2)
    #await ctx.channel.purge(limit=int(purgeCount))
    print(f'purged {purgeCount}')
    await ctx.send(f"Player 1 chose {player1}\nPlayer 2 chose {player2}")
    turnCounter = 0
    winCondition = False
    while not winCondition:
        userChoice = await getUserChoice(ctx, board, bot)
        print(userChoice)
        xCoordinate = await decodeUserChoice(userChoice)
        yCoordinate = await getPlacementCoordinates(xCoordinate, board)
        print(f'{xCoordinate}, {yCoordinate}')
        #await ctx.channel.purge(limit=int(2))
        if turnCounter % 2 == 0:
            board = await modifyBoard(board, yCoordinate, xCoordinate, player1)
            winCondition = await checkForWin(ctx, board, player1)
            if not winCondition:
                await ctx.send(f"Player {player2}'s turn\n\n") #Displays for next turn, backwards from above
        else:
            board = await modifyBoard(board, yCoordinate, xCoordinate, player2)
            winCondition = await checkForWin(ctx, board, player2)
            if not winCondition:
                await ctx.send(f"Player {player1}'s turn\n\n") #Displays for next turn, backwards from above
        
        turnCounter += 1


#Modifed from ExceedCoding on Youtube https://www.youtube.com/watch?v=JdVAx7bSQfw&t=536s
async def getUserCharacter(ctx, bot, currentPlayer):

    def checkReactions(reaction, user):
        return user!= bot.user

    validEmoji = False

    while not validEmoji:
        global boardBackgroundEmoji
        await ctx.send(f"Player {str(currentPlayer)}: pick your character by reacting with an Emoji ")
        reaction, user = await bot.wait_for("reaction_add", timeout=30, check=checkReactions)
        if reaction.emoji == '▫️':
            await ctx.send(f"Cannot choose \"{boardBackgroundEmoji}\", please choose another emoji.")
            global purgeCount
            #purgeCount += int(2)
        else:
            validEmoji = True

    return str(reaction.emoji)

async def getUserChoice(ctx, board, bot):
    global boardBackgroundEmoji


    msg = await ctx.send(await generateBoardString(board))

    for i in range(len(board[0])): 
        if board[0][i] == boardBackgroundEmoji:
            await msg.add_reaction(await decodeNumberEmoji(i + 1))

    def checkReactions(reaction, user):
        return user!= bot.user

    reaction, user = await bot.wait_for("reaction_add", check=checkReactions)

    return reaction.emoji

async def generateBoardString(board):
    board
    boardString = ""
    for row in board:
        for tile in row:
            boardString += tile
        boardString += "\n"

    for i in range(0, len(board[0])):
        if board[0][i] == boardBackgroundEmoji:
            boardString += await decodeNumberEmoji(i + 1)
        else:
            boardString += '❌'
    
    return boardString


async def modifyBoard(board, newY, newX, emoji):
    global boardLength
    global boardHeight
    newBoard = [['' for a in range(boardLength)] for b in range(boardHeight)]
    y = 0
    for row in board:
        x = 0
        for tile in row:
            if x != newX or y != newY:
                newBoard[y][x] += board[y][x]
            else:
                newBoard[y][x] += emoji
            x += 1
        y += 1
    return newBoard

async def getPlacementCoordinates(column, board):
    global boardBackgroundEmoji
    yCoordinate = 0
    if board[len(board) - 1][column] == boardBackgroundEmoji:
        return len(board) - 1 
    for row in board:
        if board[yCoordinate + 1][column] != boardBackgroundEmoji:
            return yCoordinate
        else:
            yCoordinate += 1
    return "error; empty spot not found"

async def decodeNumberEmoji(number):
    match number:
        case 1:
            return '1️⃣'
        case 2:
            return '2️⃣'
        case 3:
            return '3️⃣'               
        case 4:
            return '4️⃣'
        case 5:
            return '5️⃣'
        case 6:
            return '6️⃣'
        case 7:
            return '7️⃣'

async def decodeUserChoice(userChoiceEmoji):
    match userChoiceEmoji:
        case '1️⃣':
            return 0
        case '2️⃣':
            return 1            
        case '3️⃣':
            return 2
        case '4️⃣':
            return 3
        case '5️⃣':
            return 4
        case '6️⃣':
            return 5    
        case '7️⃣':
            return 6    

async def checkForWin(ctx, board, player):
    global boardBackgroundEmoji
    
    #Vertical
    for i in range(len(board) - 3): #height
        for j in range(len(board[i])): #width
                if board[i][j] != boardBackgroundEmoji and board[i][j] == board[i + 1][j] and board[i][j] == board[i + 2][j] and board[i][j] == board[i + 3][j]:
                    await ctx.send(f"Player {player} has won!")
                    print(f"vertical win {i}, {j} to {i + 3}, {j}")
                    await ctx.send(await generateBoardString(board))
                    return True

    #Horizontal
    for i in range(len(board)): #height
        for j in range(len(board[i]) - 3): #width
                if board[i][j] != boardBackgroundEmoji and board[i][j] == board[i][j + 1] and board[i][j] == board[i][j + 2] and board[i][j] == board[i][j + 3]:
                    await ctx.send(f"Player {player} has won!")
                    print(f"horizontal win {i}, {j} to {i}, {j + 3}")
                    await ctx.send(await generateBoardString(board))
                    return True

    #Acending diagonal
    for i in range(3, len(board)): #height
        for j in range(len(board[i]) - 3): #width
            if board[i][j] != boardBackgroundEmoji and board[i][j] == board[i - 1][j + 1] and board[i][j] == board[i - 2][j + 2] and board[i][j] == board[i - 3][j + 3]:
                await ctx.send(f"Player {player} has won!")
                print(f"diagonal ascending win {i}, {j} to {i - 3}, {j + 3}")
                await ctx.send(await generateBoardString(board))
                return True

    #Descending diagonal
    for i in range(len(board) - 3): #height
        for j in range(len(board[i]) -3): #width
            if board[i][j] != boardBackgroundEmoji and board[i][j] == board[i + 1][j + 1] and board[i][j] == board[i + 2][j + 2] and board[i][j] == board[i + 3][j + 3]:
                await ctx.send(f"Player {player} has won!")
                print(f"diagonal descending {i}, {j} to {i + 3}, {j + 3}")
                await ctx.send(await generateBoardString(board))
                return True

    #blackout (all squares used)
    defaultSquareExists = False
    for i in range(len(board) - 3): #height
        for j in range(len(board[i]) -3): #width
            if board[i][j] == boardBackgroundEmoji:
                defaultSquareExists = True
    if not defaultSquareExists:
        await ctx.send("Game ends in a tie")
        return True #game ends