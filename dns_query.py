import socket 
import time 

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

        self.retry = 0

    
    def send_query(self):
        # initialize the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)

        # build a dns packet
        dns = DnsPacket()
        query_packet = dns.build_packet(self.name, self.query_type)

        # send and receive
        start = time.time()
        server_packet = self.send(sock, query_packet)
        end = time.time()

        # decode and print response
        self. print_response(dns, server_packet, end - start)

    
    def send(self, sock, query_packet, retry=0):
        self.retry = retry 
        if retry > self.max_retries:
            return None 
        try:
            # send the packet
            sock.sendto(query_packet, (self.address, self.port))
            # get the response
            server_packet = sock.recv(4096)
        except socket.timeout:
            return self.send(sock, query_packet, retry + 1)
        
        return server_packet


    def print_error(self, error_code):
        if error_code == 1:
            print(f"Maximum number of retries {self.max_retires} exceeded")

    
    def print_response(self, dns, response, interval):
        print(f"DnsClient sending request for {self.name}")
        print(f"Server: {self.address}")
        print(f"Request type: {self.query_type}\n")

        if response != None:
            # decode packet
            response = dns.unpack_packet(response)
            print(f"Response received after {interval} seconds ({self.retry} retries)")
            
            ancount = response['header']['ancount']
            nscount = response['header']['nscount']
            arcount = response['header']['arcount']

            if response['header']['aa'] == 0:
                auth = "noauth"
            else:
                auth = "auth"

            # print each section
            self.print_section(ancount, response['answer'], "Answer", auth)
            #self.print_section(ancount, response['answer'], "Authority", auth)
            #self.print_section(ancount, response['answer'], "Additional", auth)


    def print_section(self, count, section, section_name, auth):
        if count > 0:
            print(f"***{section_name} Section ({count} records)***")
                
            for ans in section:
                if ans["TYPE"] == 1:
                    print(f"IP\t{ans['RDATA']}\t{ans['TTL']}\t{auth}")
                elif ans["TYPE"] == 5:
                    print(f"CNAME\t{ans['RDATA']}\t{ans['TTL']}\t{auth}")
                elif ans["TYPE"] == 15:
                    print(f"MX\t{ans['RDATA']['exchange']}\t{ans['RDATA']['preference']}\t{ans['TTL']}\t{auth}")
                else: 
                    print(f"NS\t{ans['RDATA']}\t{ans['TTL']}\t{auth}")