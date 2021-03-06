#!/usr/bin/env python3

import os
import sys
from client import Client
import common.constants as CONSTANTS
import clientconfig

def main():
    if( len( sys.argv ) >= 3 ):
        arg2 = int( sys.argv[3] )
        arg1 = sys.argv[2]
    elif ( len( sys.argv ) >= 2):
        arg2 = CONSTANTS.DEFAULT_PORT
        arg1 = sys.argv[2]
    else:
        arg2 = CONSTANTS.DEFAULT_PORT
        arg1 = CONSTANTS.DEFAULT_SERVERNAME
    cfg = clientconfig.ClientConfig( arg1, arg2 )

    client = Client( cfg )
    client.showInfo()
    try:
        if( client.checkVersion() ):
            hostStatus = client.updateStatus()
            if( hostStatus.msg == CONSTANTS.VERB_POWEROFF ):
                client.shutdown()
            else:
                client.poweron()
        else:
            print( 'Servidor desatualizado')
            print( 'Cliente inerte')
    except Exception as e:
        print( e )    


if __name__ == '__main__':
    main()