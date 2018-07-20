from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from model_utils.models import TimeStampedModel
from .constants import Postion, Vote_result
from haru141 import settings


class Player(TimeStampedModel):
    name = models.CharField(max_length=200, blank=False)
    number = models.CharField(max_length=2, blank=False)
    player_position = models.SmallIntegerField(
        choices=Postion.get_choices(), 
        blank=True)

    def __str__(self):
        return self.name


class Game(TimeStampedModel):
    title = models.CharField(max_length=200, null=True)
    game_start_date = models.DateTimeField(auto_now_add=False)
    first_scorer = models.ForeignKey(Player, on_delete=models.DO_NOTHING, null=True, related_name='first_scorer', blank=True)
    member = models.ManyToManyField(Player, blank=True, related_name='member')

    def __str__(self):
        return str(self.title)

    def was_vote_closed(self):
        now = timezone.now()
        return self.game_start_date < now


class Vote(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    vote_result = models.SmallIntegerField(
        choices=Vote_result.get_vote_result(), 
        null=True)
