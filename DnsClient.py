import argparse

from dns_query import DnsClient

def parse_input():
    '''
    Parse input from cli entry

    Returns
    -------
    dict : 
        dictionary of parameters and their values
    '''
    # create a parser
    parser = argparse.ArgumentParser()

    # timeout, max_retires, and port number
    parser.add_argument('-t', action='store', dest='timeout', help='socket timeout', type=int, default=5)
    parser.add_argument('-r', action='store', dest='max_retries', help='maximum number of retries', type=int, default=3)
    parser.add_argument('-p', action='store', dest='port', help='socket port', type=int, default=53)

    # either mx of ns is selected, not both
    qtype = parser.add_mutually_exclusive_group(required=False)
    qtype.add_argument('-ns', action="store_true", default=False, dest='NS', help="NS type")
    qtype.add_argument('-mx', action="store_true", default=False, dest='MX', help="MX type")

    # DNS server name and lookup address
    parser.add_argument("address", action="store", help="DNS server ip address")
    parser.add_argument("name", action="store", help="Lookup domain name")
    
    return parser.parse_args()


def main():
    '''
    Main function
    ''' 
    # pass the cli input
    params = parse_input()

    # create a dns client 
    dns_client = DnsClient(params)

    # send the query and display the response
    dns_client.send_query()


if __name__ == "__main__":
    main()