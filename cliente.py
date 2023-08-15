from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address)
conn.send('hola crayola')
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()