from pybars import Compiler
from solcx import install_solc
from solcx import compile_source
import os

class Schema:
    global types
    types = [
        'bool',
        'int',
        'uint',
        'fixed',
        'ufixed',
        'address',
        'string',
        'byte',
        'bytes',
        'enum'
    ]

    def __init__(self, modelDefinition, contractSP, web3Provider):
        self.isDeployed = False
        self.web3 = web3Provider
        self.idType = None
        self.account = None
        self.modelDefinition = modelDefinition
        self.propertyNames = []
        self.contractSavePath = contractSP
        self.idField = None
        self.contractDeployed = None
        self.transactionOptions = {}
        self.deployedContract = None
        install_solc(version='latest')

    def setAccount(self, accountToSet):
        self.account = accountToSet

    def preprocessId(self, Id):
        return self.web3.utils.asciiToHex(Id) if 'bytes' in self.idType else Id

    def validate(self):
        idFound = 0
        for i in range(1, 33):
            types.append('bytes'+str(i))

        if 'name' not in self.modelDefinition:
            raise Exception('name property is required')

        if 'contractName' not in self.modelDefinition:
            raise Exception('contractName property is required')

        if not isinstance(self.modelDefinition['properties'], list):
            raise TypeError('properties must be an array')

        self.propertyNames = map(
            lambda p: p.name, self.modelDefinition['properties'])

        for i in range(0, len(self.modelDefinition['properties'])):
            if 'name' not in self.modelDefinition['properties'][i]:
                raise Exception('Property at index' +
                                str(i) + 'is missing name')

            if 'type' not in self.modelDefinition['properties'][i]:
                raise Exception('Property at index' +
                                str(i) + 'is missing type')

            if self.modelDefinition['properties'][i]['type'] not in types:
                raise TypeError('Property at index' +
                                str(i) + ' has wrong type')

            if self.modelDefinition['properties'][i]['type'] == 'enum':
                if 'values' not in self.modelDefinition['properties'][i]:
                    raise TypeError('Property at index' +
                                    str(i) + ' is missing values property which is mandatory for fields of type enum')

                if 'defaultValue' not in self.modelDefinition['properties'][i]:
                    raise TypeError('Property at index' +
                                    str(i) + ' is missing defaultValue property which is mandatory for fields of type enum')

                if self.modelDefinition['properties'][i]['defaultValue'] not in self.modelDefinition['properties'][i]['values']:
                    raise TypeError('Property at index' +
                                    str(i) + ' defaultValue is not included in the set of values. The defaultValue of an enum type must be included in the set of values.')

                if len(self.modelDefinition['properties'][i]['values']) != len(set(self.modelDefinition['properties'][i]['values'])):
                     raise TypeError('Property at index' +
                                    str(i) + ' values must contain only unique values. It seems duplicate values exist')

            if 'primaryKey' in  self.modelDefinition['properties'][i]:
                if self.modelDefinition['properties'][i]['primaryKey'] == True:
                    idFound += 1
                    self.idField = self.modelDefinition['properties'][i]['name']
                    self.idType = self.modelDefinition['properties'][i]['type']

        if idFound == 0 or idFound > 1:
            raise Exception('One property must be primary key of the model.')


    def generateContract(self, contractSavePath):
        self.validate()
        file = open(os.path.dirname(__file__) + '/contractTemplate.txt', 'r')
        templateFile = file.read()
        compiler = Compiler()
        handleBarsTemplate = compiler.compile(source=templateFile)
        contractResult = handleBarsTemplate({
            'contract': {
                'name': self.modelDefinition['contractName'],
                'structName': self.modelDefinition['name'],
                'idDataType': self.idType,
                'license': self.modelDefinition['license'] if 'license' in self.modelDefinition else 'UNLICENSED',
            }
        })

        try:
            with open(contractSavePath + '/' + self.modelDefinition['contractName'] + '.sol', 'w') as f:
                f.write(contractResult)
                return contractResult
        except FileNotFoundError:
            raise Exception('Contract save path does not exist')

    def deploy(self):
        if self.isDeployed:
            raise Exception('Model ' + self.modelDefinition['contractName'] + ' is already deployed')
        
        generatedContact = self.generateContract(self.contractSavePath)
        compiledContract = compile_source(generatedContact, output_values=['abi','bin'])
        contractId, contractInterface = compiledContract.popitem()
        bytecode = contractInterface['bin']
        abi = contractInterface['abi']

        self.web3.eth.defaultAccount = self.account if self.account else self.web3.eth.accounts[0]
        contract = self.web3.eth.contract(abi=abi,bytecode=bytecode)

        #deploy tx
        tx_hash = contract.constructor().transact()
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

        self.deployedContract = self.web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        self.isDeployed = True