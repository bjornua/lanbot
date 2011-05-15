# -*- coding: utf-8 -*-
import app.lib.command

from datetime import datetime

from pytz import timezone

tz_utc = timezone("UTC")

timezones = (
    ("Danmark", timezone("Europe/Copenhagen")),
    ("Korea", timezone("Asia/Seoul")),
    ("Pacific Daylight Time (USA)", timezone("America/Los_Angeles")),
)

class Command(app.lib.command.BaseCommand):
    name = "now"
    
    def exists(self):
        return True
    
    def __call__(self):
        utc = datetime.utcnow().replace(tzinfo = tz_utc)
        

        self.msg.reply(" | ".join(
            label + ": " + utc.astimezone(tz).strftime("%d/%m-%Y kl. %H:%M:%S")
            for (label, tz) in timezones
        ))
