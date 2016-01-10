from lastseen import LastSeen
ls = LastSeen("America/Chicago")

from datetime import datetime
import time

USER = 'sageinventor'
CHANNEL = '#akakdnd'

ls.store_active(USER, CHANNEL)
timeu, channel = ls.last_seen(USER)
print timeu

date = timeu[:10]
timeu = timeu[11:]
#timeu = datetime.strptime(timeu[11:], "%H:%M:%S")
#timeu = timeu.strftime("%I:%M %p")

print timeu
print date
print channel
'''
timeu, channel = ls.last_seen('localhost')

date = timeu[:10]
timeu = timeu[11:]


print timeu
print date
print channel
'''
