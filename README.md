# EthAir Balloons
<img src="https://raw.githubusercontent.com/petrosDemetrakopoulos/ethairballoons/master/logo_official.png" width="300">


A strictly typed ORM library for Ethereum blockchain.
It allows you to use Ethereum blockchain as a persistent storage in an organized and model-oriented way <strong>without writing custom complex Smart contracts</strong>.


<strong>Note:
As transaction fees may be huge, it is strongly advised to only deploy EthAir Balloons models in private Ethereum blockchains or locally using
`ganache` .
</strong>


# Installation
```
pip install ethairballoons
```

# Setup

```python
from ethairballoons import ethairBalloons

# frist parameter is the IP of the Ethereum network we want to store data
# seconda parameter is the path to save to smart contract
provider = ethairBalloons('127.0.0.1', '../')

mySchema = provider.createSchema(modelDefinition={
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
```

As you can see you can very easily create a new ethAirBaloons provider (line 3) by setting only 2 arguments.
1) the URL of the Ethereum blockchain provider that you want to use
(in the example it is set to a local `ganache` provider),
2) the path where you want to save the automatically generated smart contracts of your models.

After you create the provider you can create new data schemas using the `createSchema()` function and pass the schema details in dictionary format.
Of course you can (an it is advised) keep the schema definitions in separate .JSON files and then import them using the `import json` and then `json.load()` statements.


 `createSchema()` returns a  `Schema` object.
 In order to successfully initialize a `Schema` object, *only one* property
 of the schema definition must have `primaryKey` field set to `True` (as shown in the example above)
 and the `type` field must be set to one of the legal [Solidity data types](https://solidity.readthedocs.io/en/v0.5.3/types.html).

 # Functions of `Schema` object
`Schema` object implements all the functions needed to perform CRUD operations.
As all blockchains have an asynchronous nature, all functions in the library return a callback function.
After you initialize a `Schema`, you can call the following functions:

deploy()
--------
It is the fist function that you must call in order to set your model up "up and running".
This function generates the solidity Smart contract of your model and it deploys
it in the Ethereum based blockchain that you have set in the first step.
It returns a boolean indicating if the deploy is successfull and an error object that will be undefined if the deploy is successfull.
After deploy completes you can call the other functions.

Example:

```python
mySchema.deploy()
```

save()
------
Saves a new record in th blockchain. Make sure to set the primary key field in the object you want to save, otherwise an error will be returned.
It returns the saved object and an error object that will be undefined if the object is saved successfully.

Example:
 ```python
save_receipt = mySchema.save({
    'model': 'A4',
    'engine': 'V8',
    'cylinders': '8'
})
```

find()
------
Returns all the records of our Schema.
Example:
 ```python
all_records = mySchema.find()
```

findById()
----------
Returns the record with a specific primary key value if exists.
Otherwise it will return an error object mentioning that 'record with this id does not exist'.

Example:
 ```python
record_by_id = mySchema.findById('A4')
```


deleteById()
------------
Deletes the record with a specific primary key value if exists. It returns `True` if the operation completed successfully.
Otherwise it will return `False`.

Example:
 ```python
delete_receipt = mySchema.deleteById('A4')
```

updateById()
------------
Updates the record with a specific primary key value if exists.
Otherwise it will return an error object mentioning that 'record with this id does not exist'.
It returns the True or False that indicates if the operation completed successfullt or not.

The first parameter is the primary key value of the record we want to update.
The second parameter is the updated object.
Note that is contrary with save() function it is not necessary to set the primary key field and if you do so, it will NOT be updated.
If you want to reassign a stored record to a different id you must first delete it and then save a new one with the different primary key value.

Example:
 ```python
update_receipt = mySchema.updateById('A4', {'model': 'A4',
                                 'engine': 'V18',
                                 'cylinders': '18'})
```

setAccount(account)
------------
With this function you can explicitly set the ETH account that you want to use for the model.
If not set, account is set by default to the first account of the provider.

# JavaScript version
EthairBalloons is also available for JavaScript in [this GitHub repository](https://github.com/petrosDemetrakopoulos/ethairballoons).

You can also install it via `npm install ethairballoons`


# License
EthAir Balloons are licensed under MIT license.