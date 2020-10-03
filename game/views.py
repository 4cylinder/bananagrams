from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import Player, Game, Event, EventTypes
from django.shortcuts import render
from .utils import *
from .forms import CreateGameForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .signals import event_signal

def home(request):
    if request.user.is_authenticated:
        return redirect('game:index')
    else:
        return render(request, 'index.html')

@login_required()
def index(request):
    try:
        activePlayer = Player.objects.get(user=request.user, active=True)
        activeGame = activePlayer.game
        context = {
            'player': activePlayer,
            'game': activeGame
        }
        return render(request, 'index.html', context)
    except Exception as e:
        print(e)
        return render(request, 'index.html', {'create_game_form': CreateGameForm()})

@login_required
def createNewGame(request):
    gameName = request.POST['game_name']
    numPlayers = request.POST['player_count']
    newGame = Game(game_name=gameName, num_players=numPlayers, active=True)
    newGame.save()
    host = Player(user=request.user, game=newGame, active=True, is_host=True)
    host.save()
    event_signal.send(sender=None, user=request.user, game=newGame, eventType=EventTypes.EVENT_CREATE)
    return redirect('game:index')

@login_required
def checkGameAvailabilityByUrl(request, urlKey):
    game = Game.objects.get(url_key=url_key, active=True)
    if game:
        return HttpResponse("CAN JOIN GAME" if numPlayersInGame(game) < game.num_players else "GAME IS FULL")
    else:
        return HttpResponse("GAME DOES NOT EXIST")

def numPlayersInGame(game):
    presentPlayers = Player.objects.all().filter(game=game, active=True)
    return len(presentPlayers)

@login_required
def joinGame(request, urlKey):
    game = Game.objects.get(url_key=urlKey, active=True)
    existingPlayers = numPlayersInGame(game)
    if existingPlayers < game.num_players:
        guest, created = Player.objects.get_or_create(user=request.user, game=game, active=True, is_host=False)
        if created: guest.save()
        event_signal.send(sender=None, user=request.user, game=game, eventType=EventTypes.EVENT_JOIN)
        if existingPlayers == game.num_players - 1:
            event_signal.send(sender=None, user=request.user, game=game, eventType=EventTypes.EVENT_FULL)
        return redirect('game:index')
    else:
        return HttpResponse("GAME IS FULL")

@login_required
def startGame(request, gameId):
    game = Game.objects.get(pk=gameId)
    # check that there are enough players
    players = Player.objects.all().filter(game=game, active=True)
    if (len(players) != game.num_players):
        return HttpResponse("NOT ENOUGH PLAYERS")

    startTileCount = getStartTileCount(game.num_players)
    distributeTiles(startTileCount, game)

    event_signal.send(sender=None, user=request.user, game=game, eventType=EventTypes.EVENT_START)
    return HttpResponse("STARTED")

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
@login_required
def peel(request, gameId):
    game = Game.objects.select_for_update().get(pk=gameId)
    peeler = Player.objects.select_for_update().get(user=request.user, game=game)
    newGrid = request.POST['grid']
    if validatePeel(peeler.grid, peeler.rack, newGrid):
        peeler.grid = newGrid
        peeler.rack = ""
        peeler.save()
        distributeTiles(1, game)
        event_signal.send(sender=None, user=request.user, game=game, eventType=EventTypes.EVENT_PEEL)
    else:
        return HttpResponse("Invalid Move")

# When a player dumps, they put one tile back and take 3 more (if available)
@login_required
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
    dumper.rack = ''.join(rack)
    dumper.save()

    event_signal.send(sender=None, user=request.user, game=game, eventType=EventTypes.EVENT_DUMP)
    return HttpResponse('Dumped')

# poll for game events
@login_required
def getGameEvents(request, gameId):
    game = Game.objects.get(pk=gameId)
    event = Event.objects.all().filter(game=game).order_by('-event_time')[0]

    return JsonResponse({
        'tilesLeft': len(game.remaining_tiles),
        'event': {
            'time': event.event_time,
            'info': event.event_info,
            'event_type': event.event_type
        }
    })

# update player state if an event requires it (peel, bananas, dump)
@login_required
def updatePlayerState(request, gameId):
    game = Game.objects.get(pk=gameId)
    player = Player.objects.get(user=request.user, game=game)
    return JsonResponse({
        'rack': player.rack,
        'active': player.active
    })

# No more tiles to distribute, and one player finishing up = Bananas
@login_required
def bananas(request, gameId):
    game = Game.objects.select_for_update().get(pk=gameId)
    caller = Player.objects.select_for_update().get(user=request.user, game=game)
    newGrid = request.POST['grid']
    event_signal.send(sender=None, user=request.user, game=game, eventType=EventTypes.EVENT_BANANAS)

    if validateBananas(newGrid):
        game.end_time = datetime.now()
        game.save()
        event_signal.send(sender=None, user=request.user, game=game, eventType=EventTypes.EVENT_WIN)
        return HttpResponse("You win!")
    else:
        return HttpResponse("Rotten Banana")
