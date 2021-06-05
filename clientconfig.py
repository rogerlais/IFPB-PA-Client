import sys


class ClientConfig():

    def __init__(self, servername , port ):
        #todo usar parser para padronizar entrada de linha de comando como argumentos
        super().__init__()
        self._servername = servername
        self._port = port

    @property
    def servername(self):
        return self._servername

    @property
    def port(self):
        return self._port
