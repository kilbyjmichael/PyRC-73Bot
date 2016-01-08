from pydblite import Base
from datetime import datetime

from lastseen import LastSeen
ls = LastSeen()

USER = 'sageinventor'
CHANNEL = '#akakdnd'
JOINTIME = "2016-01-07 18:55:24.606482"
QUITTIME = str(datetime.now())
database = Base('test.pdl')

ls.store_joined(USER,CHANNEL)
#time.sleep(5)
ls.store_quit(USER,CHANNEL)
if database.exists():
    database.open()
    record = database(user=USER)
    for item in record:
        quittime = item['quittime']
        jointime = item['jointime']
    is_on = ls.calculate_last_seen(jointime, quittime)
    print is_on
