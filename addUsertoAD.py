from typing import List, Any


from pyad import *
from pyad import aduser
from pyad.adbase import set_defaults
from pyad import adquery
from pyad import adobject
from pyad import pyadutils
from pyad.adobject import ADObject


#list of items needed:
ad ='10.122.45.236'
ADusername ='pyuser'
ADpassword = 'C1sco123'
OrgUnit = 'OU=CUCMUsers,DC=dachaveslab,DC=net'


user = 'test6'
userpwd = 'C1sco123'
user_attributes = {
    'givenname':'Alonso',
    'sn':'perez',
    'displayName':'Alonso Perez',
    'title':'Cisco NCE',
    'department':'Engineering',
    'company':'CRG'
    }





def force_pwd_change(new_user):
    print('forcing the pwd change on login')
    try:
        fcd_pwd = pyad.aduser.ADUser.force_pwd_change_on_login(new_user)
        print ('user set to change password succesfully')
    except  Exception as error:
        print ('operation failure - error ' + str (error))



def set_managed_by(new_user):
    print('forcing managed by')
    mgr = 'CN=Luis Alvarez,OU=CUCMUsers,DC=dachaveslab,DC=net'
    try:
        mgd_by = pyad.adobject.ADObject.set_managedby(new_user,mgr)
        print ('manager assigned succesfully')
    except  Exception as error:
        print ('operation failure - error ' + str (error))



if __name__ == '__main__':
    '''
    This function uses Pyad for connecting to MS Active Directory
    Sets the defaults for Pyad and adds a new user based on the user attributes dictionary
    '''
    print ('setting pyad defaults')

    pyad.set_defaults(ldap_server=ad, username=ADusername, password=ADpassword)

    print ('defining the OU')
    ou = pyad.adcontainer.ADContainer.from_dn(OrgUnit)


    print ('creating new user')
    try:
        new_user = pyad.aduser.ADUser.create(user, ou, password=userpwd, optional_attributes=user_attributes)
        print (str(new_user) + 'was created succesfully')

    except Exception as error:
        print ('operation failure - error ' + str (error))

    #force_pwd_change(new_user)
    set_managed_by(new_user)





