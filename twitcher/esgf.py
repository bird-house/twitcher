"""
Retrieve an ESGF certificate using a esgf access token and
prepare a `.dodsrc` file for OpenDAP_ access to the ESGF data archive.

This module uses code from esgf-slcs-client-example_ and esgf-pyclient_.


.. _esgf-slcs-client-example: https://github.com/cedadev/esgf-slcs-client-example
.. _esgf-pyclient: https://github.com/ESGF/esgf-pyclient
.. _OpenDAP: http://docs.opendap.org/index.php/Wiki_Testing/OPeNDAPUserGuideA

"""

import os
import shutil
import tempfile
from OpenSSL import crypto
import base64
import requests
from requests_oauthlib import OAuth2Session

import logging
logger = logging.getLogger(__name__)


ESGF_CERTS_DIR = 'certificates'
ESGF_CREDENTIALS = 'credentials.pem'
HTTP_RC = '.httprc'
DAP_CONFIG = '.dodsrc'
DAP_CONFIG_MARKER = '<<< Managed by twitcher >>>'

DAP_CONFIG_TEMPL = """\
# BEGIN {marker}
HTTP.VERBOSE={verbose}
HTTP.COOKIEJAR={base_dir}/.dods_cookies
HTTP.SSL.VALIDATE=0
HTTP.SSL.CERTIFICATE={esgf_credentials}
HTTP.SSL.KEY={esgf_credentials}
HTTP.SSL.CAPATH={esgf_certs_dir}
# END {marker}
"""


def fetch_certificate(request):
    url = request.environ['esgf_slcs_service_url']
    access_token = request.environ['esgf_access_token']
    logger.debug("Fetch certificate for %s", access_token)
    test_credentials = None

    workdir = request.workdir
    prefix = request.prefix
    tempdir = tempfile.mkdtemp(prefix=prefix, dir=workdir)
    logger.debug('Created twitcher tempdir %s', tempdir)
    try:
        mgr = ESGFAccessManager(url, base_dir=tempdir)
        mgr.logon(access_token)
        if test_credentials and os.path.isfile(test_credentials):
            logger.warn('Overwriting credentials.pem with %s', test_credentials)
            shutil.copy2(test_credentials, mgr.esgf_credentials)
    except IOError:
        logger.error("Could not copy test credentials.")
    except:
        logger.error("Could not fetch certificate.")
    return tempdir


class ESGFAccessManager(object):
    def __init__(self, slcs_service_url, base_dir=None):
        self.certificate_url = "{}/oauth/certificate/".format(slcs_service_url)
        self.base_dir = base_dir or '.'
        self.esgf_credentials = os.path.join(self.base_dir, ESGF_CREDENTIALS)
        self.esgf_certs_dir = os.path.join(self.base_dir, ESGF_CERTS_DIR)
        self.dap_config = os.path.join(self.base_dir, DAP_CONFIG)
        self.httprc = os.path.join(self.base_dir, HTTP_RC)

        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    def logon(self, access_token, timeout=1):
        cert = self._get_certificate(access_token, timeout=timeout)
        self._write_certificate(cert)
        self._write_dap_config()

    def _get_certificate(self, access_token, timeout=1):
        """
        Generates a new private key and certificate request, submits the request to be
        signed by the SLCS CA and returns the certificate.
        """
        # Generate a new key pair
        key_pair = crypto.PKey()
        key_pair.generate_key(crypto.TYPE_RSA, 2048)
        private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key_pair).decode("utf-8")

        # Generate a certificate request using that key-pair
        cert_request = crypto.X509Req()

        # Create public key object
        cert_request.set_pubkey(key_pair)

        # Add the public key to the request
        cert_request.sign(key_pair, 'md5')
        der_cert_req = crypto.dump_certificate_request(crypto.FILETYPE_ASN1, cert_request)

        encoded_cert_req = base64.b64encode(der_cert_req)

        # Build the OAuth session object
        token = {'access_token': access_token, 'token_type': 'Bearer'}
        slcs = OAuth2Session(token=token)
        # headers = {}
        # headers['Authorization'] = 'Bearer %s' % access_token
        # post_data = urllib.urlencode({'certificate_request': encoded_cert_req})

        response = slcs.post(
            self.certificate_url,
            data={'certificate_request': encoded_cert_req},
            verify=False,
            timeout=timeout,
        )

        # response = requests.post(self.url,
        #                          headers=headers,
        #                          data=post_data,
        #                          verify=False)
        if response.status_code == 200:
            content = "{} {}".format(response.text, private_key)
        else:
            msg = "Could not get certificate: {} {}".format(response.status_code, response.reason)
            raise Exception(msg)
        return content

    def _write_certificate(self, certificate):
        with open(self.esgf_credentials, 'w') as fh:
            fh.write(certificate)

    def _write_dap_config(self, verbose=False, validate=False):
        content = DAP_CONFIG_TEMPL.format(
            verbose=1 if verbose else 0,
            validate=1 if validate else 0,
            base_dir=self.base_dir,
            esgf_certs_dir=self.esgf_certs_dir,
            esgf_credentials=self.esgf_credentials,
            marker=DAP_CONFIG_MARKER,
        )
        with open(self.dap_config, 'w') as fh:
            fh.write(content)
        shutil.copy2(self.dap_config, self.httprc)
