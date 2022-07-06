from ethairballoons import ethairBalloons

prov = ethairBalloons('127.0.0.1', '../')

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

rec = mySchema.save({
    'model': 'A4',
    'engine': 'V8',
    'cylinders': '8'
})
print(rec)
print(mySchema.find())
print(mySchema.findById('A567'))
print(mySchema.updateById('A4', {'model': 'A4',
                                 'engine': 'V18',
                                 'cylinders': '18'}))
print(mySchema.find())
print(mySchema.deleteById('A4'))
print(mySchema.find())
