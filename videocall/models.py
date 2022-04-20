from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
status_list = {
    0: 'Contacting',
    1: 'Not available',
    2: 'Accepted',
    3: 'Rejected',
    4: 'Busy',
    5: 'Processing',
    6: 'Ended',
}

class VideoCall(models.Model):
    caller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caller_user')
    callee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='callee_user')
    status = models.IntegerField(default=0)
    date_started = models.DateTimeField(default=datetime.now)
    date_ended = models.DateTimeField(default=datetime.now)
    date_created = models.DateTimeField(default=datetime.now)

    @property
    def status_name(self):
        return status_list[self.status]

    @property
    def duration(self):
        return self.date_ended - self.date_started
