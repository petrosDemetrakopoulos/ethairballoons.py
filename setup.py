from setuptools import setup, find_packages


setup(
    name='ethairballoons',
    version='1.0.0',
    license='MIT',
    author="Petros Demetrakopoulos",
    author_email='petrosdem@gamil.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/petrosDemetrakopoulos/ethairballoons.py',
    keywords='blockchain ethereum web3 orm data',
    install_requires=[
          'web3',
          'py-solc-x'
      ]
)