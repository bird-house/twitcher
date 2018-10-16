"""
Retrieve an ESGF certificate using a esgf access token and
prepare a `.dodsrc` file for OpenDAP_ access to the ESGF data archive.

This module uses code from esgf-slcs-client-example_ and esgf-pyclient_.


.. _esgf-slcs-client-example: https://github.com/cedadev/esgf-slcs-client-example
.. _esgf-pyclient: https://github.com/ESGF/esgf-pyclient
.. _OpenDAP: http://docs.opendap.org/index.php/Wiki_Testing/OPeNDAPUserGuideA

"""

import os
from OpenSSL import crypto
import base64
import requests
from requests_oauthlib import OAuth2Session

from twitcher.utils import is_valid_url

import logging
LOGGER = logging.getLogger('TWITCHER')


ESGF_CERTS_DIR = 'certificates'
ESGF_CREDENTIALS = 'credentials.pem'


def fetch_certificate(workdir='.', data={}):
    try:
        url = data.get('esgf_slcs_service_url')
        access_token = data.get('esgf_access_token')
        test_credentials = data.get('esgf_credentials')
        mgr = ESGFAccessManager(url, base_dir=workdir)
        mgr.logon(access_token, test_credentials)
        LOGGER.debug('Prepared twitcher workdir %s', workdir)
    except Exception:
        LOGGER.warn("Could not fetch certificate.")
        return False
    return True


class ESGFAccessManager(object):
    def __init__(self, slcs_service_url, base_dir=None):
        self.certificate_url = "{}/oauth/certificate/".format(slcs_service_url)
        self.base_dir = base_dir or '.'
        self.esgf_credentials = os.path.join(self.base_dir, ESGF_CREDENTIALS)

        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    def logon(self, access_token, cert_url=None, timeout=1):
        if access_token:
            self._retrieve_certificate(access_token, timeout=timeout)
        elif cert_url:
            self._download_certificate(cert_url)
        else:
            raise Exception("Need either access_token or cert_url.")
        # fix permission
        try:
            os.chmod(self.esgf_credentials, 0o400)
        except Exception:
            LOGGER.warn("Could not update permission of credentials.")
        return True

    def _download_certificate(self, url):
        if is_valid_url(url):
            LOGGER.debug('Download cert from %s', url)
            response = requests.get(url, stream=True)
            with open(self.esgf_credentials, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=128):
                    fd.write(chunk)
            return True
        else:
            return False

    def _retrieve_certificate(self, access_token, timeout=3):
        """
        Generates a new private key and certificate request, submits the request to be
        signed by the SLCS CA and returns the certificate.
        """
        LOGGER.debug("Retrieve certificate with token.")

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
        client = OAuth2Session(token=token)

        response = client.post(
            self.certificate_url,
            data={'certificate_request': encoded_cert_req},
            verify=False,
            timeout=timeout,
        )

        if response.ok:
            content = "{} {}".format(response.text, private_key)
            with open(self.esgf_credentials, 'w') as fh:
                fh.write(content)
            LOGGER.debug('Fetched certificate successfully.')
        else:
            msg = "Could not get certificate: {} {}".format(response.status_code, response.reason)
            raise Exception(msg)
        return True
