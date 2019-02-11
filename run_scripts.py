from wrappers.handle_price_data import get_price_data
import time
import psycopg2
import sshtunnel

# Import list of traded pairs form get_timeframe_data file
from inputs import ALLpairs

# sshtunnel.SSH_TIMEOUT = 5.0
# sshtunnel.TUNNEL_TIMEOUT = 5.0

#with sshtunnel.SSHTunnelForwarder(
#    ('ssh.pythonanywhere.com'),
#    ssh_username='martendo',
#    ssh_password='martendo85',
#    remote_bind_address=('martendo-824.postgres.pythonanywhere-services.com', 10824)
#) as tunnel:

#    params = {
#        "dbname": 'llweb',
#        "user": 'super',
#        "password": 'postgres85',
#        "host": 'localhost',
#        "port": tunnel.local_bind_port,
#    }

# Use local Postgres
params = {
        "dbname": 'llweb',
        "user": 'postgres',
        "password": 'martendo85',
        "host": 'localhost',
        "port": '5432'
    }

conn = psycopg2.connect(**params)
cur = conn.cursor()

# Make price data query for all pairs

# Load 5m timeframe
for pair in ALLpairs:
    get_price_data(pair, '5m', cur,  hist=False)

# Load 15m timeframe
i = 0
while i == 0:
    time = time.gmtime()
    if time[4] % 15 == 1:
        for pair in ALLpairs:
            get_price_data(pair, '15m', cur,  hist=False)
            i += 1
    else: time.sleep(5)

# Load 1h timeframe
i = 0
while i == 0:
    time = time.gmtime()
    if time[4] % 60 == 2:
        for pair in ALLpairs:
            get_price_data(pair, '1h', cur,  hist=False)
            i += 1
    else: time.sleep(5)

# Load 6h timeframe
i = 0
while i == 0:
    time = time.gmtime()
    if time[4] % 60 == 3 and (time[3] - 1) % 6 == 0:
        for pair in ALLpairs:
            get_price_data(pair, '6h', cur,  hist=False)
            i += 1
    else: time.sleep(5)

# Load 1D timeframe
i = 0
while i == 0:
    time = time.gmtime()
    if time[4] % 60 == 4 and (time[3] - 1) % 24 == 0:
        for pair in ALLpairs:
            get_price_data(pair, '1D', cur,  hist=False)
            i += 1
    else: time.sleep(5)

conn.commit()
conn.close()
