import datetime
from bson.objectid import ObjectId
from apps.main.models import BaseDocument, Event, register


@register
class EventLog(BaseDocument):
    __collection__ = 'event_log'
    structure = {
      'event': Event,
      'user': ObjectId,
      'action': int,
      'context': unicode,
      'comment': unicode,
    }

    # we're not using autorefs here because then we don't have to cascade
    # deletes
    use_autorefs = False

    @staticmethod
    def get_eventlogs_by_event(event):
        """return a cursor for all the eventlogs related to this parameter
        event.

        The reason why this is a static method here and not part of the
        apps.main.models.Event class is because I don't want to clutter the main
        app with something like the eventlog which is much less important."""
        return event.db.EventLog.find({'event':event})

    @property
    def user(self):
        return self.db.User.find_one({'_id': self['user']})
