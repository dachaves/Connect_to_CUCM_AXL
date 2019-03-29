import paramiko, sys, time, suds, logging, pandas

from os.path import abspath
from urllib.parse import urljoin
from urllib.request import pathname2url
import ssl
from suds.client import Client


def start_sync(CLIENT, uuid):
    try:
        sync = CLIENT.service.doLdapSync(uuid=uuid, sync=True)
        print(sync['return'])
        return True
    except Exception:
        print('unable to perform a sync')
        return False


def get_uuid(CLIENT):
    '''
    Function to Query Ldap UUID, Run an LdapSync and query to make sure that it completes
    it executes a SQL query and then uses doLdapSync and getLdapSyncStatus
    '''
    try:
        print('executing query to find UUID')
        sql = CLIENT.service.executeSQLQuery(
            # sql='select pkid from directorypluginconfig where name like "%CUCM%"')  ##Ldap Config must have CUCM on its name.
            sql='select pkid from directorypluginconfig where name like "%CUCM%"')  ##Ldap Config must have CUCM on its name.
        sql_params = (sql['return']['row'])
        ##Using Pandas to convert the parameters into a list
        ##Getting the values and obtaining UUID from the list
        df = pandas.DataFrame(sql_params)
        uuid = df.values.tolist()[0][0][1]
        print('performing sync')
        return uuid
    except Exception:
        logging.debug('unable to obtain UUID')
        return None


def get_sync_status(CLIENT, uuid):
    try:
        resp = CLIENT.service.getLdapSyncStatus(uuid=uuid)
        while resp['return'] != 'Sync is performed succesfully':
            print('sleeping for 1 sec')
            time.sleep(1)
            resp = CLIENT.service.getLdapSyncStatus(uuid=uuid)
            if resp['return'] == 'Sync is performed successfully':
                print('sync was successful')
                break
        return resp
    except Exception:
        print('unable to detect LdapSyncStatus')
        return False


if __name__ == '__main__':
    ## pulls the AXLAPI.wsdl

    WSDL = urljoin('file:', pathname2url(abspath('schema/schema/11.5/AXLAPI.wsdl')))

    ## Allow insecure connections
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    CLIENT = Client(WSDL, location='https://%s:8443/axl/' % ('10.122.45.218'),
                    username='admin', password='cisc0lab')

    uuid = get_uuid(CLIENT)
    if start_sync(CLIENT, uuid):
        get_sync_status(CLIENT, uuid)
    else:
        print('error')