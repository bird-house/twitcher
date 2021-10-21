"""
The ``twitcherctl`` is a command line tool to control the twitcher service.
It is used to generate access tokens and to register OWS services.

``twitcherctl`` is part of the twitcher installation:

.. code-block:: console

   $ twitcherctl -h

`twitcherctl` Commands and Options
----------------------------------

``twitcherctl`` has the following command line options:

-h, --help

   Print usage message and exit

-s, --serverurl

   URL on which twitcher server is listening (default "http://localhost:8000/").

-u, --username

   Username to access twitcher server.

-p, --password

   Password to access twitcher server.

-k, --insecure

   Don't validate the server's certificate.

List of available commands:

add
    Add OAuth2 client application.
gentoken
    Generates an access token.
list
    Lists all registered OWS services used by OWS proxy.
clear
    Removes all OWS services from the registry.
register
   Adds OWS service to the registry to be used by the OWS proxy.
unregister
   Removes OWS service from the registry.

Add an OAuth2 client application
--------------------------------

Register an application using basic authentication with username and password
(name and redirect-uri are optional):

.. code-block:: console

    $ twitcherctl -k --username demo --password demo add --name demo_app --redirect-uri http://localhost/demo_app
    {'client_id': 'id', 'client_secret': 'secret'}

The result is an OAuth *client_id* and *client_secret*.

Generate an access token
------------------------

Get an OAuth access token using *client_id* and *client_secret* for given *scope*:

.. code-block:: console

   $ twitcherctl -k gentoken -i client_id -s client_secret --scope compute
   {'access_token': 'TOKEN', 'expires_in': 3600, 'scope': ['compute'], 'token_type': 'Bearer'}

Possible scopes are: compute, register.

You can also get a token from a Keycloak OAuth service using the client credentials workflow:

.. code-block:: console

   $ twitcherctl -k -s http://localhost:8080 gentoken -i client_id -s client_secret --scope compute --keycloak

Register an OWS Service for the OWS Proxy
-----------------------------------------

See the available options:

.. code-block:: console

   twitcherctl -k register -h

Register a local WPS service using an OAuth access token:

.. code-block:: console

   $ twitcherctl -k --username demo --password demo register http://localhost:5000/wps
   tiny_buzzard

You can use the ``--name`` option to provide a name (used by the OWS proxy).
Otherwise a nice name will be generated.

List registered services
------------------------

The ``list`` command shows the registered OWS services:

.. code-block:: console

   $ twitcherctl -k --username demo --password demo list
   [{'url': 'http://localhost:5000/wps', 'type': 'wps', 'name': 'tiny_buzzard', 'auth': 'token'}]

"""

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
    Command line to interact with the OAuth and OpenAPI interface of the ``twitcher`` service.
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

        # add client app
        # --------------

        # add
        subparser = subparsers.add_parser('add', help="Add OAuth2 client application")
        subparser.add_argument("-n", "--name",
                               help="Client application name")
        subparser.add_argument("-r", "--redirect-uri",
                               help="Client application redirect URI")

        # token management
        # ----------------

        # gentoken
        subparser = subparsers.add_parser('gentoken', help="Generates an OAuth2 access token.")
        subparser.add_argument("-i", "--client-id", help="OAuth client-id")
        subparser.add_argument("-s", "--client-secret", help="OAuth client-secret")
        subparser.add_argument("-S", "--scope", nargs='+', default='compute', help="OAuth scope: compute or register")
        subparser.add_argument("-K", "--keycloak",
                               help="Use keycloak token endpoint.",
                               action="store_true")

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
        subparser.add_argument('--auth', default='token',
                               help="Authentication method (token, cert, public). Default: token.")
        subparser.add_argument('--verify', default='true',
                               help="Verify SSL service certificate (true, false). Default: true.")

        # unregister
        subparser = subparsers.add_parser('unregister', help="Removes OWS service from the registry.")
        subparser.add_argument('name', help="Service name.")

        return parser

    def run(self, args):
        if args.debug:
            LOGGER.setLevel(logging.DEBUG)

        if args.insecure:
            # See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
            import urllib3
            urllib3.disable_warnings()
            LOGGER.warning('disabled certificate verification!')

        username = password = None
        if args.cmd != 'gentoken':
            username = args.username
            if not username:
                username = input('Username: ')
            password = args.password
            if not password:
                password = getpass.getpass(prompt='Password: ')

        verify_ssl = args.insecure is False
        service = TwitcherService(
            url=args.serverurl,
            username=username,
            password=password,
            verify=verify_ssl)

        try:
            if args.cmd == 'list':
                return service.list_services()
            elif args.cmd == 'register':
                data = {'type': args.type,
                        'purl': args.purl,
                        'auth': args.auth,
                        'verify': args.verify}
                return service.register_service(
                    name=args.name or get_random_name(),
                    url=args.url,
                    data=data,
                )
            elif args.cmd == 'unregister':
                return service.unregister_service(name=args.name)
            elif args.cmd == 'clear':
                return service.clear_services()
            elif args.cmd == 'add':
                return service.add_client_app(
                    name=args.name,
                    redirect_uri=args.redirect_uri)
            elif args.cmd == 'gentoken':
                client_id = args.client_id
                if not client_id:
                    client_id = input('Client ID: ')
                client_secret = args.client_secret
                if not client_secret:
                    client_secret = getpass.getpass(prompt='Client Secret: ')
                return service.fetch_token(
                    client_id=client_id,
                    client_secret=client_secret,
                    scope=args.scope,
                    keycloak=args.keycloak)
        except Exception as e:
            LOGGER.error("Error: {}".format(e))
        return None


def main():
    LOGGER.setLevel(logging.INFO)

    ctl = TwitcherCtl()
    parser = ctl.create_parser()
    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    return ctl.run(args)


if __name__ == '__main__':
    sys.exit(main())
