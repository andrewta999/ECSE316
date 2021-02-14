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
        ''' Creates a socket instance and send a DNS packet through it
        '''
        # initialize the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)

        # build a dns packet
        dns = DnsPacket()
        query_packet = dns.build_packet(self.name, self.query_type)

        # send and receive
        start = time.time()
        server_packet, error_code = self.send(sock, query_packet)
        end = time.time()

        # decode and print response
        self.print_response(dns, server_packet, end - start, error_code)

    
    def send(self, sock, query_packet, retry=0):
        ''' Send a packet through a socket intance
        Retry a certain number of times if faillure occur

        Parameters
        ----------
        sock : socket
            a socket instance
        query_packet : bytes
            packet in bytes
        retry : int
            the number of current retry cycle
        
        Returns
        -------
        server_packet : bytes
            packet received in bytes
        '''
        # update self.retry
        self.retry = retry 

        # if retry more than expected
        # return None
        if retry > self.max_retries:
            return None, 1
        try:
            # send the packet
            sock.sendto(query_packet, (self.address, self.port))
            # get the response
            server_packet = sock.recv(4096)
        except socket.timeout:
            # retry if socket timeout
            return self.send(sock, query_packet, retry + 1)
        
        # return the response 
        return server_packet, 0


    def print_error(self, error_code):
        ''' Print error according to error code

        Parameters
        ----------
        error_code : int
            error code
        '''
        if error_code == 1:
            print(f"Error: Maximum number of retries {self.max_retries} exceeded")

    
    def print_response(self, dns, response, interval, error_code):
        ''' Format the response and print it to stdout

        Parameters
        ----------
        dns : DnsClient
            a DnsClient instance
        response : dict
            a dictionary that store the response
        interval : float
            timelapse from sending to receiving
        error_code : int
            error code
        '''
        print(f"DnsClient sending request for {self.name}")
        print(f"Server: {self.address}")
        print(f"Request type: {self.query_type}\n")

        if error_code == 0:
            # decode packet
            response = dns.unpack_packet(response)
            print(f"Response received after {interval} seconds ({self.retry} retries)")
            
            # get number of records in answer, authority, and additional sections
            ancount = response['header']['ancount']
            nscount = response['header']['nscount']
            arcount = response['header']['arcount']

            # auth boolean
            if response['header']['aa'] == 0:
                auth = "noauth"
            else:
                auth = "auth"

            # print answer section
            self.print_section(ancount, response['answer'], "Answer", auth)
            
            # print authority section
            self.print_section(nscount, response['authority'], "Authority", auth)
            
            # print additional section
            self.print_section(arcount, response['additional'], "Additional", auth)
        else:
            self.print_error(error_code)


    def print_section(self, count, section, section_name, auth):
        ''' Print the records in a section

        Parameters
        ----------
        count : int
            number of records
        section : dict
            dictionary of records
        section_name : dict
            name of the section
        auth : boolean
            auth or not
        '''
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
        
        if section_name == "Answer" and count == 0:
            print("NOT FOUND")