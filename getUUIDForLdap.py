## Connects to CUCM, obtains the list of CallParks and prints the results into a file.
## Reference the axl-schema-reference from devnet.

## The following libraries have to be imported. some listed are not required. ###

import paramiko, sys, time, suds, pandas, logging


from os.path import abspath
from urllib.parse import urljoin
from urllib.request import pathname2url
import ssl
from suds.client import Client
from suds.sudsobject import asdict


## pulls the AXLAPI.wsdl

WSDL = urljoin('file:', pathname2url(abspath('schema/schema/11.5/AXLAPI.wsdl')))

# Allow insecure connections
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

CLIENT = Client(WSDL, location='https://%s:8443/axl/' % ('10.122.45.218'),
                username='admin', password='cisc0lab')

## Look at the AXL Schema Reference. Might need to look at the REQ and RES references to understand the response received.

ldapsearch = CLIENT.service.listLdapDirectory(
    searchCriteria={'name':'%'},
    returnedTags={
        'name':'',
        'ldapDn':'',
        })

#print (ldapsearch['return']['ldapDirectory'])



def find_ldap_uuid():
    '''
    runs a SQL query to find the UID of the Ldap server
    Requires that the Ldap Name contains 'CUCM' on the name
    '''
    sql = CLIENT.service.executeSQLQuery(
    sql= 'select pkid from directorypluginconfig where name like "%CUCM%"')
    sql_params = (sql['return']['row'])
    ##Using Pandas to convert the parameters into a list
    ##Getting the values and obtaining UUID from the list
    df = pandas.DataFrame(sql_params)
    uuid = df.values.tolist()[0][0][1]
    print (uuid)

uuid = find_ldap_uuid

uuid()








