from lastseen import LastSeen
ls = LastSeen()

USER = 'sageinventor'
CHANNEL = '#akakdnd'

ls.store_active(USER, CHANNEL)
time, channel = ls.last_seen(USER)

date = time[:10]
time = time[11:]

print time
print date
print channel

time, channel = ls.last_seen('localhost')

date = time[:10]
time = time[11:]

print time
print date
print channel