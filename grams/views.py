from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import Player, Game
from django.shortcuts import render
from .utils import *

def index(request):
    activePlayer = Player.objects.get(user=request.user, active=True)
    if activePlayer:
        activeGame = activePlayer.game
        context = {
            'player': activePlayer,
            'game': activeGame
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')

def createNewGame(request, numPlayers, gameName='Bananagrams'):
    newGame = Game(game_name=gameName, num_players=numPlayers, active=True)
    newGame.save()
    host = Player(user=request.user, game=newGame, active=True, is_host=True)
    host.save()
    context = {
        'player': host,
        'game': newGame
    }
    return render(request, 'index.html', context)

def checkGameAvailability(request, urlKey):
    game = Game.objects.get(url_key=url_key, active=True)
    if game:
        presentPlayers = Player.objects.all().filter(game=game, active=True)
        if len(presentPlayers) == game.num_players:
            return HttpResponse("GAME IS FULL")
        elif len(presentPlayers) < game.num_players:
            return HttpResponse("CAN JOIN GAME")
    else:
        return HttpResponse("GAME DOES NOT EXIST")

def joinGame(request, urlKey):
    game = Game.objects.get(url_key=url_key, active=True)
    guest = Player(user=request.user, game=game, active=True, is_host=False)
    guest.save()
    context = {
        'player': guest,
        'game': game
    }
    return render(request, 'index.html', context)

def startGame(request, gameId):
    game = Game.objects.get(pk=gameId)
    # check that there are enough players
    players = Player.objects.all().filter(game=game, active=True)
    if (len(players) != game.num_players):
        return HttpResponse("NOT ENOUGH PLAYERS")

    startTileCount = getStartTileCount(game.num_players)
    distributeTiles(startTileCount, game)

    return HttpResponse("GAME STARTED")

def distributeTiles(numTiles, game):
    players = Player.objects.select_for_update().all().filter(game=game, active=True)
    tiles = list(game.remaining_tiles)

    for player in players:
        player.rack += ''.join(tiles[:numTiles])
        tiles = tiles[numTiles:]
        player.save()
    game.remaining_tiles = ''.join(tiles)
    game.save()

# Player has finished their grid and clicks PEEL
# When a player peels, ALL players must take one tile
def peel(request, gameId):
    game = Game.objects.select_for_update().get(pk=gameId)
    peeler = Player.objects.select_for_update().get(user=request.user, game=game)
    newGrid = request.POST['grid']
    if validatePeel(peeler.grid, peeler.rack, newGrid):
        peeler.grid = newGrid
        peeler.rack = ""
    else:
        return HttpResponse("Invalid Move")
    
    distributeTiles(1, game)

# When a player dumps, they put one tile back and take 3 more (if available)
def dump(request, gameId, toDump):
    game = Game.objects.select_for_update().get(pk=gameId)
    tiles = list(game.remaining_tiles)
    if len(tiles) == 0:
        return HttpResponse('Cannot dump')
    dumper = Player.objects.select_for_update().get(user=request.user, game=game)
    rack = list(dumper.rack)
    rack.remove(toDump)
    
    for i in range(min(3, len(tiles))):
        rack.append(tiles.pop(0))
    tiles.append(toDump)
    game.remaining_tiles = tiles
    game.save()
    dumper.rack = rack
    dumper.save()
    return HttpResponse('Dumped')

# Front end polls this to ensure that peel/dumps properly update everyone
def updateGameInfo(request, gameId):
    game = Game.objects.select_for_update().get(pk=gameId)
    player = Player.objects.select_for_update().get(user=request.user, game=game)
    return JsonResponse({
        'rack': player.rack,
        'grid': player.grid,
        'tilesLeft': len(game.remaining_tiles)
    })

# No more tiles to distribute, and one player finishing up = Bananas
def bananas(request, gameId):
    game = Game.objects.select_for_update().get(pk=gameId)
    caller = Player.objects.select_for_update().get(user=request.user, game=game)
    newGrid = request.POST['grid']
    if validateBananas(newGrid):
        return HttpResponse("You win!")
    else:
        return HttpResponse("Rotten Banana")
