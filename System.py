import socket, ssl
import MySQLdb
from utils import bin_to_int, int_to_bin

bindsocket = socket.socket()
bindsocket.bind(('', 10023))
bindsocket.listen(5)

db = MySQLdb.connect("localhost", "root", "root", "system_users")


def uncapsulate(data):
    data_vector = data.split(',')

    binary_vector = []
    binary_id = []
    for k in data_vector[:-1]:
        binary_vector = int_to_bin(int(k))
        binary_id.append(binary_vector[0])

    value = float(data_vector[-1])
    id = bin_to_int(binary_id)

    return id, value


def verify(connstream, data):
    id, value = uncapsulate(data)

    cursor = db.cursor()
    sql = "SELECT * FROM customers WHERE id = %s" % id
    cursor.execute(sql)
    data = cursor.fetchone()
    print "DAAAAATAAA: ", data

    if value <= data[-1]:
        sql = "UPDATE customers SET balance = balance - %f WHERE id = %s" % (value, id)
        cursor.execute(sql)

        sql = "SELECT * FROM customers WHERE id = %s" % id
        cursor.execute(sql)
        data = cursor.fetchone()
        print "DAAAAATAAA: ", data

        ok = 'BIRL,' + str(data[-1])
        connstream.write(ok)
    else:
        connstream.write('NOPE')

    return False


def deal_with_client(connstream):
    data = connstream.read()
    while data:
        if not verify(connstream, data):
            break
        data = connstream.read()


def wait_connection():
    while True:
        newsocket, fromaddr = bindsocket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                     server_side=True,
                                     certfile="./SSLcertificate/sistema/server.crt",
                                     keyfile="./SSLcertificate/sistema/server.key")
        try:
            deal_with_client(connstream)
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()

if __name__ == "__main__":

    wait_connection()
    db.close()
