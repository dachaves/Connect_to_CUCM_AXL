from typing import List, Any


from pyad import *
from pyad import aduser
from pyad.adbase import set_defaults
from pyad import adquery
from pyad import adobject
from pyad import pyadutils
from pyad.adobject import ADObject
from pyad import adgroup


#list of items needed:
ad ='10.122.45.236'
ADusername ='pyuser'
ADpassword = 'C1sco123'
OrgUnit = 'OU=CUCMUsers,DC=dachaveslab,DC=net'


user = 'test7'
userpwd = 'C1sco123'
mgr = 'CN=Luis Alvarez,OU=CUCMUsers,DC=dachaveslab,DC=net'
user_attributes = {
    'givenname':'Daniel',
    'sn':'Chaves',
    'displayName':'Daniel Chaves',
    'title':'Cisco NCE',
    'department':'Engineering',
    'company':'CRG',
    'manager':mgr
    }


def create_user(user):
    '''
    This function creates the user using the create function within
    the ADUser class from pyad
    '''
    print ('creating new user')
    try:
        new_user = pyad.aduser.ADUser.create(user, ou, password=userpwd, optional_attributes=user_attributes)
        print (str(new_user) + 'was created succesfully !!! \n ------------------------- ')
        return new_user

    except Exception as error:
        print ('operation failure - error ' + str (error))
        return False

def check_if_user_exists(userlookup):
    print ('checking if user exists')
    try:
        q = pyad.adgroup.ADGroup.from_dn(userlookup)
        print ('User ID already exists')
        return False

    except Exception as error:
        print ('user does not exist')
        return True


def force_pwd_change(new_user):
    '''
    This function forces the user to change the password on login calling the
    force_pwd_change_on_login function
    '''
    try:
        fcd_pwd = pyad.aduser.ADUser.force_pwd_change_on_login(new_user)
        print ('user set to change password succesfully')
        return True
    except  Exception as error:
        print ('operation failure - error ' + str (error))
        return False


if __name__ == '__main__':
    '''
    This function uses Pyad for connecting to MS Active Directory
    Sets the defaults for Pyad and adds a new user based on the user attributes dictionary
    '''
    print ('setting pyad defaults')

    pyad.set_defaults(ldap_server=ad, username=ADusername, password=ADpassword)

    ou = pyad.adcontainer.ADContainer.from_dn(OrgUnit)

    userlookup = ('CN=' + user + ',' +OrgUnit)

    if check_if_user_exists(userlookup)== True:
        new_user = create_user(user)
        if new_user == False:
            print ('unable to create user')
        else:
            force_pwd_change(new_user)
    else:
        print ('user not created')


