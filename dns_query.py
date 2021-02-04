import socket 

from dns_packet import DnsPacket

class DnsClient():
    ''' 
    A class that establishes a UDP socket connection to 
    a DNS server and send a query to that socket

    Attributes
    ----------
    timeout : int
        socket timeout
    max_retires : int
        maximum number of retries
    port : int
        port number
    query_type : string
        query type
    server : string
        ip address of the DNS server
    name : string
        domain name
    '''
    def __init__(self, params):
        self.timeout = params.timeout
        self.max_retries = params.max_retries
        self.port = params.port
        self.address = params.address[1::]
        self.name = params.name
        
        self.query_type = "A"
        if params.NS:
            self.query_type = "NS"
        if params.MX:
            self.query_type = "MX"


    
    def send_query(self):
        # initialize the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)

        # build a dns packet
        dns = DnsPacket()
        query_packet = dns.build_packet(self.name, self.query_type)

        # send the packet
        sock.sendto(query_packet, (self.address, self.port))

        # get the response
        server_packet = sock.recv(4096)
        print(server_packet)

        # decode the response
        response = dns.unpack_packet(server_packet)
        print(response)
