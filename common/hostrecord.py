import json
import datetime;

class HostRecord():

    def __init__(self, hostname, MAC, Address, loggedUser ):
        super().__init__()
        self._hostname = hostname
        self._MAC = MAC
        self._loggedUser = loggedUser
        self._timestamp =  datetime.datetime.now().timestamp()
        #todo ver demais atributos
    #construtor

    @staticmethod
    def getFromComputer():
        ret = HostRecord( 'fake-pcname', 'fak-mac', 'fake-addr', 'fake-user')
        return ret

    @property
    def hostname( self ):
        return self._hostname

    @property
    def MAC( self ):
        return self._MAC

    @property
    def loggedUser( self ):
        return self._loggedUser

    @property
    def timestamp( self ):
        return self._timestamp

    def export( self ):
        meDict = {'hostname': self.hostname, 'MAC': self._MAC, 'loggedUser': self.loggedUser }
        ret = json.dumps(meDict)
        print(ret)
        return ret