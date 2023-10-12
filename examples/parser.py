import argparse

class ArgParser:
    """This class is used to create a parser for the command line arguments. It is used by the example scripts to parse
    the arguments passed to them."""

    @staticmethod
    def create_domain_parser():
        """Create a parser for the domain name argument."""
        parser = argparse.ArgumentParser(description="Create a domain in UltraDNS with A and CNAME records.")
        parser.add_argument("domain", help="The domain name to be created.")
        parser.add_argument("-u", "--username", help="Username for authentication.", required=True)
        parser.add_argument("-p", "--password", help="Password for authentication.", required=True)
        return parser