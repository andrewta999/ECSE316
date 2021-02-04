import struct 
import random

QType = {
    'A': 1, 
    'NS': 2, 
    'MX': 15,
    'CNAME': 5
}

class DnsPacket():
    '''
    A class that builds a dns packet and
    analyze the response packet 
    '''
    def __init__(self):
        self.id = None # packet id
        self.client_packet = b'' # dns packet
        self.format = '' # packet format

    def build_packet(self, address, query_type):
        '''Build a DNS package given address and question type

        Parameters
        ----------
        address : str
            address string
        query_type : str
            question type

        Returns
        -------
        dns : bytes
            bytes object represents a dns packet 
        '''

        # contruct the packet's header 
        self.id = random.getrandbits(16)
        dns = struct.pack('>HHHHHH', self.id, 256, 1, 0, 0, 0)
        self.format += '>HHHHHH' 

        # construct the packet's body
        # split address by '.' character
        url_list = address.split('.')
        # loop through each sub url and add it to dns
        for url in url_list:
            # add the length of this url
            dns += struct.pack('B', len(url))
            self.format += 'B'
            # add the url
            for c in url:
                # add an encoded character in url
                dns += struct.pack('c', c.encode('utf-8'))
                self.format += 'c'
        
        # add end of data 
        dns += struct.pack('B', 0)
        self.format += 'B'

        # add query type and query class 
        dns += struct.pack('>HH', QType[query_type], 1)
        self.format += 'HH'

        # store dns
        self.client_packet = dns 

        # return the packet
        return dns 


    def unpack_packet(self, response):
        '''
        Decode a dns response packet

        Parameters
        ----------
        response : bytes
            bytes object represents a dns response packet

        Returns
        -------
        dict
        '''
        result = {} # dictionary to store data
        
        # unpack response header and question
        response_hq = struct.unpack_from(self.format, response)

        # header flags
        flag = response_hq[1]

        # unpack question
        i = 6
        num = response_hq[i]
        question = []
        while num != 0:
            question.append(b''.join(response_hq[i+1:i+num+1:]).decode())
            i = i + num + 1
            num = response_hq[i]

        # unpack qtype and qclass 
        qtype, qclass = response_hq[-2], response_hq[-1]

        # unpack answer section

        # unpack authoritive section

        # unpack additionals section

        result = {
            "id": response_hq[0],
            "qr": (flag & 0x8000) >> 15,
            "opcode": (flag & 0x7800) >> 11,
            "aa": (flag & 0x0400),
            "tc": (flag & 0x200),
            "rd": (flag & 0x100) >> 8,
            "ra": (flag & 0x80) >> 7,
            "z": (flag & 0x70) >> 4,
            "rcode": flag & 0xF,
            "qdcount": response_hq[2], 
            "ancount": response_hq[3],
            "nscount": response_hq[4],
            "arcount": response_hq[5],
            "question": '.'.join(question),
            "qtype": qtype, 
            "qclass": qclass,
            "answer": "",
            "authority": "",
            "additional": ""
        }

        # return result
        return result 

