import sys
import getpass
import argcomplete
import argparse

from twitcher.client import TwitcherService
from twitcher.namesgenerator import get_random_name

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARN)
LOGGER = logging.getLogger("TWITCHER")


class TwitcherCtl(object):
    """
    Command line to interact with the xmlrpc interface of the ``twitcher`` service.
    """

    def create_parser(self):
        parser = argparse.ArgumentParser(
            prog="twitcherctl",
            description='twitcherctl -- control twitcher service from the cmd line.',
        )
        parser.add_argument("--debug",
                            help="Enable debug mode.",
                            action="store_true")
        parser.add_argument('-s', '--serverurl',
                            metavar='URL',
                            default='http://localhost:8000',
                            help='URL on which twitcher server is listening (default "http://localhost:8000").')
        parser.add_argument("-u", "--username",
                            help="Username to use for authentication with server.")
        parser.add_argument("-p", "--password",
                            help="Password to use for authentication with server")
        parser.add_argument("-k", "--insecure",  # like curl
                            help="Don't validate the server's certificate.",
                            action="store_true")

        # commands
        subparsers = parser.add_subparsers(
            dest='cmd',
            title='command',
            description='List of available commands',
        )

        # token management
        # ----------------

        # gentoken
        subparser = subparsers.add_parser('gentoken', help="Generates an access token.")
        subparser.add_argument('-H', '--valid-in-hours', type=int, default=1,
                               help="Set how long the token is valid in hours (default: 1 hour).")

        # revoke
        subparser = subparsers.add_parser('revoke', help="Remove given access token.")
        subparser.add_argument('token', nargs="?", help="access token")
        subparser.add_argument('-A', '--all', action="store_true",
                               help="Remove all access tokens.")

        # service registry
        # ----------------

        # list
        subparser = subparsers.add_parser('list', help="Lists all registered OWS services used by OWS proxy.")

        # clear
        subparser = subparsers.add_parser('clear', help="Removes all OWS services from the registry.")

        # register
        subparser = subparsers.add_parser('register',
                                          help="Adds OWS service to the registry to be used by the OWS proxy.")
        subparser.add_argument('url', help="Service url.")
        subparser.add_argument('--name', help="Service name. If not set then a name will be generated.")
        subparser.add_argument('--type', default='wps',
                               help="Service type (wps, wms). Default: wps.")
        subparser.add_argument('--purl', default='',
                               help="Service optional public URL.")
        subparser.add_argument('--public', action='store_true',
                               help="If set then service has no access restrictions.")
        subparser.add_argument('--auth', default='token',
                               help="Authentication method (token, cert). Default: token.")
        subparser.add_argument('--verify', default='true',
                               help="Verify SSL service certificate (true, false, /path/to/cert). Default: true.")

        # unregister
        subparser = subparsers.add_parser('unregister', help="Removes OWS service from the registry.")
        subparser.add_argument('name', help="Service name.")

        return parser

    def run(self, args):
        if args.debug:
            LOGGER.setLevel(logging.DEBUG)

        if args.insecure:
            LOGGER.warn('disabled certificate verification!')

        password = args.password
        if args.username:
            # username = raw_input('Username:')
            if not password:
                password = getpass.getpass(prompt='Password:')

        verify_ssl = args.insecure is False
        service = TwitcherService(url=args.serverurl,
                                  username=args.username,
                                  password=password,
                                  verify=verify_ssl)
        result = None
        try:
            if args.cmd == 'list':
                result = service.list_services()
            elif args.cmd == 'register':
                data = {'type': args.type,
                        'purl': args.purl,
                        'public': args.public,
                        'auth': args.auth,
                        'verify': args.verify}
                result = service.register_service(
                    name=args.name or get_random_name(),
                    url=args.url,
                    data=data,
                )
            elif args.cmd == 'unregister':
                result = service.unregister_service(name=args.name)
            elif args.cmd == 'clear':
                result = service.clear_services()
            elif args.cmd == 'gentoken':
                result = service.generate_token(valid_in_hours=args.valid_in_hours)
            elif args.cmd == 'revoke':
                if args.all is True:
                    result = service.revoke_all_tokens()
                else:
                    result = service.revoke_token(token=args.token)
        except Exception as e:
            LOGGER.error("Error: {}".format(e))
        else:
            LOGGER.info("Result: {}".format(result))
            return result


def main():
    LOGGER.setLevel(logging.INFO)

    ctl = TwitcherCtl()
    parser = ctl.create_parser()
    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    return ctl.run(args)


if __name__ == '__main__':
    sys.exit(main())
