import sys
import socket as s
import argparse
import random

MAX_BYTES = 65535

def server(interface, port):
    sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
    sock.bind((interface, port))

    print("Listening at {}".format(sock.getsockname()))

    while True:
        data, address = sock.recvfrom(MAX_BYTES)

        if random.random() < 0.5:
            print("pretending drop packet from {}".format(address))
            continue

        text = data.decode('utf-8')
        print("Client says {} {!r} ".format(address, text))

        message = "Your data was {} bytes long".format(len(data))
        sock.sendto(message.encode('utf-8'), address)


def client(hostname, port):
    sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
    hostname =sys.argv[2]
    sock.connect((hostname, port))
    print("Client socket name is {}".format(sock.getsockname()))

    delay = 0.1
    text = "This is another message!"
    data = text.encode('utf-8')

    while True:
        sock.send(data)
        print("Waiting up to {} seconds to reply.".format(delay))
        sock.settimeout(delay)

        try:
            data = sock.recv(MAX_BYTES)
        except s.timeout:
            delay *= 2
            if delay > 2.0:
                raise RuntimeError('It seems server down...')
            else:
                break

    print("server says {!r} ".format(data.decode('utf-8')))

if __name__ == '__main__':
    choices = {'client' : client , 'server' : server}
    parser = argparse.ArgumentParser(description='send and receive udp, pretending packets are often dropped')
    parser.add_argument('role',choices = choices,help= 'which role to play')
    parser.add_argument('host', help ='interface the server listen at'
                        'host the client send to')
    parser.add_argument('-p', metavar = 'PORT',type=int, default = 1060 , help='UDP port default (1060)')
    args = parser.parse_args()
    func = choices[args.role]
    func(args.host, args.p)

    

                
            
        
        
