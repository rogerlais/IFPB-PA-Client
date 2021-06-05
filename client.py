from protoclient import ServerSession
from clientconfig import ClientConfig
import common.constants as CONSTANTS


class Client():

    def __init__(self, cfg ):
        super().__init__()
        self._cfg = cfg

    @property
    def config(self):
        return self._cfg

    def showInfo( self ):
        print( "VAGOAMIN: Vara de Goiabeira no Ambientalmente Incorreto.")
        print( 'Servido didático da disciplina de Protocolos de Aplicação.')
        print( 'Prof.: Leonidas Francisco de Lima Junior')
        print( "Aluno: Rogerlais Andrade e Silva")
        print( "Módulo cliente" )
        print( "Versão: %s" % CONSTANTS.APP_VERSION)
    #showInfo


    def updateStatus( self ):
        ss = ServerSession( self.config.servername, self.config.port )
        ss.servername = self.config.servername
        ss.port = self.config.port
        ret = ss.sendInfo()
        return ret