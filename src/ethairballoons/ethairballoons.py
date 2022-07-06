from web3 import Web3
from schema import Schema
class ethairBalloons:
    def __init__(self, ipAddress, contractSavePath):
        self.contractSavePath = contractSavePath
        self.web3Provider = Web3(Web3.WebsocketProvider('ws://' + ipAddress + ':8545', websocket_timeout=60))

    def createSchema(self, modelDefinition):
        return Schema(modelDefinition, self.contractSavePath, self.web3Provider)
 