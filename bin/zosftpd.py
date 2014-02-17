#!/usr/bin/env python

"""
This script will run an FTP server on port 2121 which will behave in a 
way that JESFtp / WebJCL expects the marist mainframe to respond.

This script requires a modified version of pyftpdlib which allows for 
flexible SITE commands. We need this so that it will accept the 
SITE FILETYPE=JES command.
"""

from ZosFtpMock import ZosFtpServer

import argparse

# Argument parsing.

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--port", default=2121)
parser.add_argument("-H", "--hang", action="store_true", default=False,
                    help="Cause the job to take a long time"
)
parser.add_argument("-C", "--credentials", default=None,
                    help="Provide authorized credentials in the " +
                          "following format username:password")

args = parser.parse_args()



# Start server with config.

server = ZosFtpServer()

if args.credentials != None:
    credentials = args.credentials.split(':')
    server.authorize_user(credentials[0], credentials[1])

server.port = args.port

server.start()

