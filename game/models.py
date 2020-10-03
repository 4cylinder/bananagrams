from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import TILE_COUNT, getTilesAsList, generateUrlKey

# Create your models here.
class Game(models.Model):
    game_name = models.CharField(default='Bananagrams', max_length=30)
    num_players = models.PositiveIntegerField(validators=[MinValueValidator(2), MaxValueValidator(5)])
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    remaining_tiles = models.CharField(max_length=TILE_COUNT, default=''.join(getTilesAsList()))
    url_key = models.CharField(max_length=100, default=generateUrlKey())
    active = models.BooleanField(default=False)
    def __str__(self):
        return "%d %s (%d)" % (self.pk, self.game_name, self.num_players)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete = models.CASCADE, blank=True)
    active = models.BooleanField(default=False)
    rack = models.CharField(max_length=TILE_COUNT, blank=True)
    grid = models.TextField(blank=True)
    is_host = models.BooleanField(default=False)
    def __str__(self):
        return "%s %s" % (self.user, self.game.game_name)

class EventTypes:
    EVENT_CREATE = 'CREATE'
    EVENT_START = 'START'
    EVENT_JOIN = 'JOIN'
    EVENT_PEEL = 'PEEL'
    EVENT_DUMP = 'DUMP'
    EVENT_BANANAS = 'BANANAS'
    EVENT_WIN = 'WIN'
    EVENT_ROTTEN = 'ROTTEN'
    EVENT_FULL = 'FULL'

class Event(models.Model):
    EVENT_TYPES = (
        (EventTypes.EVENT_CREATE, 'CREATE'),
        (EventTypes.EVENT_START, 'START'),
        (EventTypes.EVENT_JOIN, 'JOIN'),
        (EventTypes.EVENT_PEEL, 'PEEL'),
        (EventTypes.EVENT_DUMP, 'DUMP'),
        (EventTypes.EVENT_BANANAS, 'BANANAS'),
        (EventTypes.EVENT_WIN, 'WIN'),
        (EventTypes.EVENT_ROTTEN, 'ROTTEN'),
        (EventTypes.EVENT_FULL, 'FULL')
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    event_info = models.TextField()
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES, default=EventTypes.EVENT_CREATE)
    event_time = models.TimeField(auto_now_add=True)
