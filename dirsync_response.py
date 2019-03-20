import paramiko, sys, time, suds, logging


from os.path import abspath
from urllib.parse import urljoin
from urllib.request import pathname2url
import ssl
from suds.client import Client


## pulls the AXLAPI.wsdl

WSDL = urljoin('file:', pathname2url(abspath('schema/schema/11.5/AXLAPI.wsdl')))

# Allow insecure connections
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

CLIENT = Client(WSDL, location='https://%s:8443/axl/' % ('10.122.45.218'),
                username='admin', password='cisc0lab')

resp = CLIENT.service.getLdapSyncStatus(uuid='4FB92C8C-B421-ED34-CF05-E95AD3946376')
print(resp['return'])