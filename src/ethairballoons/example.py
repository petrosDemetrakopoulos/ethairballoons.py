from ethairballoons import ethairBalloons

prov = ethairBalloons('127.0.0.1','../')

mySchema = prov.createSchema(modelDefinition={
    'name': "Car",
    'contractName': "carsContract",
    'properties': [{
            'name': "model",
            'type': "bytes32",
            'primaryKey': True
        },
        {
            'name': "engine",
            'type': "bytes32",
        },
        {
            'name': "cylinders",
            'type': "uint"
        }
    ]
})
mySchema.deploy()