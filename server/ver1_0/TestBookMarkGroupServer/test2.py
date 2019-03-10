import mysql.connector

conn = mysql.connector.connect(user='root', password='', host='localhost', db="bookmarkgroup")
cur = conn.cursor()

test_string = '''
    select * from test_sample
    where id > %(id)s;
'''
#cur.execute("select * from test_sample;")
cur.execute(test_string, {'id': 0})

for now in cur.fetchall():
    print(now[0], now[1], now[2])

cur.close
conn.close