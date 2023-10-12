#!/usr/bin/env python3

from parser import ArgParser
from ultra_auth import UltraApi

def replace_rrset(client, domain, record_type, owner_name, ttl, rdata):
    """Replace the RRSet of a domain using the PUT method.

    Args:
    - client (UltraApi): An instance of the UltraApi class.
    - domain (str): The domain name.
    - record_type (str): The DNS record type (e.g., "A").
    - owner_name (str): The owner (host) name.
    - ttl (int): The time to live.
    - rdata (list): The record data.

    Returns:
    - dict: The response body.
    """
    endpoint = f"/v3/zones/{domain}/rrsets/{record_type}/{owner_name}"

    rrset_data = {
        "ttl": ttl,
        "rdata": rdata
    }

    return client.put(endpoint, rrset_data)

def main():
    parser = ArgParser.create_domain_parser()
    args = parser.parse_args()

    client = UltraApi(args.username, args.password)

    print(f"Replacing A records for {args.domain} using PUT: {replace_rrset(client, args.domain, 'A', args.domain, 600, ['192.0.2.2'])}")

if __name__ == "__main__":
    main()
