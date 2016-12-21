import sys
import socket, ssl
import MySQLdb
from random import randint
from utils import int_to_bin, bin_to_int

# conexao ssl entre cliente e site
# cert_key = {'ca': '/etc/mysql/ca.pem', 'cert': '/etc/mysql/client-cert.pem',
#             'key': '/etc/mysql/client-key.pem'}
cert_key = {'ca': './SSLcertificate/dbSite/ca.pem', 'cert': './SSLcertificate/dbSite/client-cert.pem',
            'key': './SSLcertificate/dbSite/client-key.pem'}
db = MySQLdb.connect(host="localhost", user="cliente", passwd="senha",
                     db="storedb", ssl=cert_key)


def connection(send_string):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ssl_sock = ssl.wrap_socket(s,
                               ca_certs="./SSLcertificate/sistema/server.crt",
                               cert_reqs=ssl.CERT_REQUIRED)

    ssl_sock.connect(('localhost', 10023))

    print "\nToken: ", "["+send_string+"]"
    ssl_sock.write(send_string)

    data = ssl_sock.read()
    answer = data.split(',')
    if answer[0] == 'BIRL':
        print "\nTransacao autorizada!\nSeu saldo e: %f" % float(answer[1])
    else:
        print "\nTransacao recusada!"

    ssl_sock.close()


def encapsulate(id, value):
    int_vector = []
    binary_vector = int_to_bin(id)
    for i in range(8):
        binary_vector_rand = []
        binary_vector_rand.insert(0, binary_vector[i])
        for j in range(1, 16):
            binary_vector_rand.append(randint(0, 1))
        int_vector.append(bin_to_int(binary_vector_rand))
    int_vector.append(value)

    send_string = ','.join(str(e) for e in int_vector)
    return send_string


def user_login(username, password):
    cursor = db.cursor()
    sql = "SELECT * FROM customers WHERE username = " \
          "'%s' AND password = '%s'" % (username, password)
    cursor.execute(sql)
    data = cursor.fetchone()

    if data is None:
        print "\nErro: nome de usuario ou senha incorretos!"
        return None
    elif username == data[0] and password == data[1]:
        return data[2]


def hello():
    prods = [500.0, 150.0, 300.50, 200.0, 345.99]

    print "\nLOJA EXEMPLO:"
    print "\nCod.\t\tProdutos\t\tPreco"
    print "  0\t\tproduto A\t\t500,00\n" \
          "  1\t\tproduto B\t\t150,00\n" \
          "  2\t\tproduto C\t\t300,50\n" \
          "  3\t\tproduto D\t\t200,00\n" \
          "  4\t\tproduto E\t\t345,99\n"

    print "\nPara comprar digite o codigo do produto e a quantidade\n" \
          "Digite 'end' para terminar.\n"

    cod, qtt, sum = 0, 0, 0
    while True:
        string = raw_input("Insira: ")
        if string == 'end':
            break
        l = string.split(' ')
        cod = int(l[0])
        qtt = float(l[1])
        sum += prods[cod] * qtt

    return sum


if __name__ == "__main__":

    if (len(sys.argv) != 3):
        print("\nModo de uso: python Client.py <usuario> <senha>\n")
        sys.exit(-1)

    username, password = sys.argv[1], sys.argv[2]
    id = user_login(username, password)
    if id is not None:
        value = hello()
        if value != 0:
            send_string = encapsulate(id, value)
            connection(send_string)
        else:
            sys.exit(-1)

    db.close()
