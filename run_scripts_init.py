from wrappers.handle_price_data import get_price_data
import psycopg2
import sshtunnel

# Import list of traded pairs form get_timeframe_data file
from inputs import ALLpairs

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

with sshtunnel.SSHTunnelForwarder(
   ('ssh.pythonanywhere.com'),
   ssh_username='martendo',
   ssh_password='martendo85',
   remote_bind_address=('martendo-824.postgres.pythonanywhere-services.com', 10824)
) as tunnel:

    params = {
       "dbname": 'llweb',
       "user": 'super',
       "password": 'postgres85',
       "host": 'localhost',
       "port": tunnel.local_bind_port,
    }

# # Use local Postgres
# params = {
#         "dbname": 'llweb',
#         "user": 'postgres',
#         "password": 'martendo85',
#         "host": 'localhost',
#         "port": '5432'
#     }

    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    # Load timeframe
    for pair in ALLpairs:
        get_price_data(pair, '1D', cur,  hist=False)

    conn.commit()
    conn.close()

