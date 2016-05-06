import socket as s
import argparse
from datetime  import datetime

MAX_BYTES = 65535

def server(port):
    sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))

    print("listening at {} ".format(sock.getsockname()))
    
    while True:
        data , address = sock.recvfrom(MAX_BYTES)
        text = data.decode('utf-8')
        print("The client at {} says {!r} ".format(address, text))

        text = "Your data was {} bytes long.".format(len(data))
        data = text.encode('utf-8')
        sock.sendto(data, address)

        
def client(port):
    sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
    text = 'The time is {}'.format(datetime.now())
    data = text.encode('utf-8')
    sock.sendto(data,('127.0.0.1', port))
    print("OS assigned me the address {}".format(sock.getsockname()))
    
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('utf-8')
    
    print("The server {} replied {!r}".format(address, text))

    
    
if __name__ == '__main__':
    choice = {'server': server, 'client' : client}

    parser = argparse.ArgumentParser(description='Send and receive udp locally')
    parser.add_argument('role',choices = choice,help = 'which role to play')
    parser.add_argument('-p', metavar = 'PORT',type=int,default= 1060,
                       help = 'UDP port (default 1060)')
    args = parser.parse_args()
    function = choice[args.role]
    function(args.p)

    
    
        

    
