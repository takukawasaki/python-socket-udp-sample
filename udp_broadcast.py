from socket import *
import argparse


BUFSIZ = 65535

def server(interface, port):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
    sock.bind((interface, port))

    print("Listening datagram at {}".format(sock.getsockname()))

    while True:
        data , address = sock.recvfrom(BUFSIZ)
        text = data.decode('utf-8')
        print("The client at {} says: {!r}".format(address, text))

def client(network, port):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    text = 'Broadcast datagram'
    sock.sendto(text.encode('utf-8'), (network,port))


if __name__ == '__main__':
    choices = {'client': client , 'server' : server}

    parser = argparse.ArgumentParser(description = 'send receive udp broadcast.')
    parser.add_argument('role', choices = choices, help = 'which role to play?')
    parser.add_argument('host', help='interface the server listen at;')
    parser.add_argument('-p', metavar= 'PORT',type=int, default= 8888,
                        help = 'UDP port default (8888)')
    args = parser.parse_args()

    func = choices[args.role]
    func(args.host, args.p)

    # use single quote
    # usage server: python3 udp_broadcast.py server ''
    #       client: python3 udp_broadcast.py client ''    
    
