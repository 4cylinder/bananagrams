from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import *

# Create your models here.

class Game(models.Model):
    game_name = models.CharField(default='Bananagrams', max_length=20)
    num_players = models.PositiveIntegerField(validators=[MinValueValidator(2), MaxValueValidator(5)])
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True)
    remaining_tiles = models.CharField(max_length=TILE_COUNT, default=''.join(getTilesAsList()))
    url_key = models.CharField(max_length=20, default=generateUrlKey())
    active = models.BooleanField(default=False)
    def __str__(self):
        return "%d %s %d" % (self.pk, self.game_name, self.start_time)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete = models.CASCADE, blank=True)
    active = models.BooleanField(default=False)
    rack = models.CharField(max_length=TILE_COUNT, blank=True)
    grid = models.TextField(blank=True)
    is_host = models.BooleanField(default=False)
    def __str__(self):
        return "%s %s" % (self.user, self.game.game_name)

class Event(models.Model):
    player = models.ForeignKey(Player, on_delete = models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    event_info = models.TextField()
    event_time = models.TimeField(auto_now_add=True)
