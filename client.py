from common.hostrecord import HostRecord
from clientconfig import ClientConfig
import common.constants as CONSTANTS
import socket
from common.datawrapper import DataWrapper


class Client():

    def __init__(self, cfg):
        super().__init__()
        self._cfg = cfg

    @property
    def config(self):
        return self._cfg

    def shutdown( self ):
        print( 'SUA MÁQUINA SERÁ DESLIGADA!!!!!')
        print( 'Brincadeira....')

    def poweron(self):
        print( 'CONCEDIDO PRIVILÉGIO DE PERMANECER LIGADO')
        print( 'Use com moderação!')

    def showInfo(self):
        print("VAGOAMIN: Vara de Goiabeira no Ambientalmente Incorreto.")
        print('Servido didático da disciplina de Protocolos de Aplicação.')
        print('Prof.: Leonidas Francisco de Lima Junior')
        print("Aluno: Rogerlais Andrade e Silva")
        print("Módulo cliente")
        print("Versão: %s" % CONSTANTS.APP_VERSION)
    # showInfo

    def bye( self ):
        host = HostRecord.getFromComputer()
        dw = DataWrapper(CONSTANTS.VERB_BYE, host.asJSON, 0, CONSTANTS.RESP_OK)
        ret = self.request(dw)
        return ret


    def updateStatus(self):
        host = HostRecord.getFromComputer()
        dw = DataWrapper(CONSTANTS.VERB_UPDATE, host.asJSON, 0, CONSTANTS.RESP_OK)
        ret = self.request(dw)
        return ret

    def checkVersion(self):
        host = HostRecord.getFromComputer()
        dw = DataWrapper(CONSTANTS.VERB_GET_VERSION, host.asJSON, 0, CONSTANTS.RESP_OK)
        ret = self.request(dw)
        return (ret.retcode == CONSTANTS.RESP_OK) & (ret.msg == CONSTANTS.APP_VERSION)

    def request(self, data):
        # Cria TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Ajusta dados do servidor
        server_address = ('localhost', self.config.port)
        sock.connect(server_address)
        # Prepare string com os dados da requisição
        msg = data.asJSON  
        sock.sendall(msg.encode('utf-8'))
        ret = sock.recv(CONSTANTS.BUFSIZE)
        print(ret)
        retData = DataWrapper.loadFromJSON(ret)
        return retData
