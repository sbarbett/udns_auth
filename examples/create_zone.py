#!/usr/bin/env python3

from parser import ArgParser
from ultra_auth import UltraApi

def create_zone(client, domain):
    """Create a zone in UltraDNS. This function will create a zone with the name specified in the domain argument.
    It uses the accounts API to get the account name. This is required to create a zone.

    Args:
    - client (UltraApi): An instance of the UltraApi class.
    - domain (str): The domain name to be created.

    Returns:
    - dict: The response body.
    """

    account_data = client.get("/accounts")
    account_name = account_data['accounts'][0]['accountName']

    zone_data = {
        "properties": {
            "name": domain,
            "accountName": account_name,
            "type": "PRIMARY"
        },
        "primaryCreateInfo": {
            "forceImport": True,
            "createType": "NEW"
        },
        "changeComment": f"Created zone for {domain} via API"
    }

    return client.post("/v3/zones", zone_data)


def create_rrset(client, domain, record_type, owner_name, ttl, rdata):
    """Create a resource record set in UltraDNS. This function will create a resource record set with the name specified
    in the owner_name argument.

    Args:
    - client (UltraApi): An instance of the UltraApi class.
    - domain (str): The domain name.
    - record_type (str): The DNS record type.
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

    return client.post(endpoint, rrset_data)

def create_a_record(client, domain):
    """Create an A record in UltraDNS. This function will create an A record with the name specified in the domain

    Args:
    - client (UltraApi): An instance of the UltraApi class.
    - domain (str): The domain name.
    """
    return create_rrset(client, domain, "A", domain, 300, ["192.0.2.1"])


def create_cname_record(client, domain):
    """Create a CNAME record in UltraDNS. This function will create a CNAME record with the name specified in the domain

    Args:
    - client (UltraApi): An instance of the UltraApi class.
    - domain (str): The domain name.

    Returns:
    - dict: The response body.
    """
    return create_rrset(client, domain, "CNAME", f"www.{domain}", 300, [domain])

def main():
    """The main function. This is the entry point for the script. It parses the command line arguments and calls the
    create_zone, create_a_record, and create_cname_record functions."""
    parser = ArgParser.create_domain_parser()
    args = parser.parse_args()

    # Create an instance of your client
    client = UltraApi(args.username, args.password)

    # Create the domain
    print(f"Creating zone {args.domain}: {create_zone(client, args.domain)}")

    # Create an A record for the domain
    print(f"Creating an A record pointing to 192.0.2.1: {create_a_record(client, args.domain)}")

    # Create a CNAME record for the domain
    print(f"Creating a 'www' CNAME pointing to {args.domain}: {create_cname_record(client, args.domain)}")

if __name__ == "__main__":
    main()
