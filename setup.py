from setuptools import setup

setup(
    name='ZosFtpMock',
    version='0.1.1',
    author='Vincent Schramer',
    author_email='vinciple@gmail.com',
    
    packages=['ZosFtpMock'],
    scripts=['bin/zosftpd.py'],
    
    description='An FTP server that roughly mocks the Marist FTP server.',
    
    long_description=open('README.md').read(),
    
    install_requires=[
        "pyftpdlib >= 1.3.0",
        "argparse >= 1.2.1"
    ],
    
    dependency_links = [
        "https://github.com/scvnc/pyftpdlib-mod/tarball/49a576c#egg=pyftpdlib-1.3.0"
    ]
)
