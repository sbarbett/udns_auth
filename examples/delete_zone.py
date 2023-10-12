#!/usr/bin/env python3

from parser import ArgParser
from ultra_auth import UltraApi

def delete_domain(client, domain):
    """Delete a domain from UltraDNS.

    Args:
    - client (UltraApi): An instance of the UltraApi class.
    - domain (str): The domain name to be deleted.

    Returns:
    - dict: The response body.
    """
    return client.delete(f"/v3/zones/{domain}")

def main():
    """The main function. This is the entry point for the script. It parses the command line arguments and calls the
    delete_domain function."""
    parser = ArgParser.create_domain_parser()
    args = parser.parse_args()

    # Create an instance of your client
    client = UltraApi(args.username, args.password)

    # Delete the domain
    print(f"Deleting domain {args.domain}: {delete_domain(client, args.domain)}")

if __name__ == "__main__":
    main()
