## Connects to CUCM, obtains the list of CallParks and prints the results into a file.
## Reference the axl-schema-reference from devnet.

## The following libraries have to be imported. some listed are not required. ###

import paramiko, sys, time, suds


from os.path import abspath
from urllib.parse import urljoin
from urllib.request import pathname2url
import ssl
from suds.client import Client


## pulls the AXLAPI.wsdl

WSDL = urljoin('file:', pathname2url(abspath('schema/11.5/AXLAPI.wsdl')))

# Allow insecure connections
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

CLIENT = Client(WSDL, location='https://%s:8443/axl/' % ('10.122.45.218'),
                username='admin', password='cisc0lab')

## Look at the AXL Schema Reference. Might need to look at the REQ and RES references to understand the response received.

try:
    response = CLIENT.service.listCallPark(
        searchCriteria={
            'pattern': '%'
        },
        returnedTags={
            'pattern': True,
            'description': True
        })
    print(response['return']['callPark'], file = open('Results.txt', 'w+')) ## adding the argument to print the results to a file unformatted.
    print ('success at sending the response to a file')


except Exception:
    print('CUCM AXL login failed, incorrect host or username/password ?')


