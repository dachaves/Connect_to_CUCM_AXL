import paramiko, sys, time, suds


from os.path import abspath
from urllib.parse import urljoin
from urllib.request import pathname2url
import ssl
from suds.client import Client


WSDL = urljoin('file:', pathname2url(abspath('schema/11.5/AXLAPI.wsdl')))

# Allow insecure connections
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

CLIENT = Client(WSDL, location='https://%s:8443/axl/' % ('10.122.45.218'),
                username='admin', password='cisc0lab')


try:
    response = CLIENT.service.listPhone(
        searchCriteria={
            'name': '%'
        },
        returnedTags={
            'description': True,
            'product': True
        })
    print(response['return']['phone'])

except Exception:
    print('CUCM AXL login failed, incorrect host or username/password ?')


