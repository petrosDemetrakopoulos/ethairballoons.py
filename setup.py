from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ethairballoons',
    version='1.0.11',
    license='MIT',
    author="Petros Demetrakopoulos",
    author_email='petrosdem@gamil.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'ethairballoons': ['contractTemplate.txt']},
    include_package_data=True,
    url='https://github.com/petrosDemetrakopoulos/ethairballoons.py',
    keywords='blockchain ethereum web3 orm data database smart contracts library',
    install_requires=[
          'web3',
          'py-solc-x'
      ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)