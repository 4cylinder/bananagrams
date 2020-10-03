from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import Event, EventTypes

event_signal = Signal(providing_args=["user", "game", "eventType"])

EVENT_MESSAGES = {
    EventTypes.EVENT_CREATE: "%s created a lobby",
    EventTypes.EVENT_START: "%s started the game",
    EventTypes.EVENT_JOIN: "%s joined the game",
    EventTypes.EVENT_PEEL: "%s says PEEL!",
    EventTypes.EVENT_DUMP: "%s says DUMP!",
    EventTypes.EVENT_BANANAS: "%s called BANANAS!",
    EventTypes.EVENT_WIN: "%s won the game",
    EventTypes.EVENT_FULL: "%s's game can start"
}

@receiver(event_signal)
def eventLogger(sender, **kwargs):
    user = kwargs['user']
    game = kwargs['game']
    eventType = kwargs['eventType']

    eventInfo = EVENT_MESSAGES[eventType] % user.username
    event = Event(game=game, event_type=eventType, event_info=eventInfo)
    event.save()