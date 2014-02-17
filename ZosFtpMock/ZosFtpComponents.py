import os


from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.filesystems import AbstractedFS
from pyftpdlib.handlers import FTPHandler, DTPHandler
from pyftpdlib.log import logger
from pyftpdlib.servers import FTPServer

from random import randint
from shutil import rmtree
import tempfile

class ZosDTPHandler(DTPHandler):
    
    @property
    def complete_message(self):
        
        if self.cmd_channel.last_job_id:
            msg = "250 - It is known to JES as " + self.cmd_channel.last_job_id
            self.cmd_channel.last_job_id = None
        
        else:
            msg = "226 Transfer complete."
            
        return msg
    
    def handle_close(self):
        
        """
        Overridden method
        
        Should be fairly identical to the method in the ftp library,
        but instead obtains it's message from a property. Could merit
        a pull request as a feature. 
        """
        
        if not self._closed:
            if self.receive:
                self.transfer_finished = True
            else:
                self.transfer_finished = len(self.producer_fifo) == 0
            try:
                if self.transfer_finished:
                    self._resp = (self.complete_message, logger.debug)
                else:
                    tot_bytes = self.get_transmitted_bytes()
                    self._resp = ("426 Transfer aborted; %d bytes transmitted."
                                  % tot_bytes, logger.debug)
            finally:
                self.close()
        
        
class ZosFtpFilesystem(AbstractedFS):
    
    def __init__(self, root, cmd_channel):
        
        # Always use a temporary directory as the FTP root.
        self.ftp_dir = unicode(tempfile.mkdtemp(prefix='zOSFTPSIM_'))
        
        AbstractedFS.__init__(self, self.ftp_dir, cmd_channel)
    
    def __del__(self):
        
        # Delete temporary ftp directory.
        rmtree(self.ftp_dir)
    
    
class ZosFTPHandler(FTPHandler):
    
    @property
    def last_job_id(self):
        
        if hasattr(self, '_last_job_id'):
            return self._last_job_id
        else:
            return None
    
    @last_job_id.setter
    def last_job_id(self, val):
        
        self._last_job_id = val
    
    
    def __init__(self, *args, **kwargs):
        
        self.abstracted_fs = ZosFtpFilesystem
        self.dtp_handler = ZosDTPHandler
        
        FTPHandler.__init__(self, *args, **kwargs)
    
        self.proto_cmds.update({
            'SITE FILETYPE=JES': {
                'perm': 'M',
                'auth': True,
                'arg': False,
                'method_name' : 'ftp_SITE_FILETYPE'
            }
        })
        
    def _make_job_id(self):
        self.last_job_id = 'JOB' + str(randint(11111,99999))
        
    def ftp_STOR(self, file, mode='w'):
        
        self._make_job_id()
        
        rewritten_filename = u'{path}/{jobID}.x'.format(
            path = self.fs.ftp2fs(self.fs.cwd),
            jobID = self.last_job_id
        )
        
        file = FTPHandler.ftp_STOR(self, rewritten_filename, mode)
        return file
    
    def ftp_DELE(self, path):
        return FTPHandler.ftp_DELE(self, path + u'.x')
    
    def ftp_SITE_FILETYPE(self, line):
        self.respond("200 Site command was accepted")

class ZosFtpServer(object):
    
    ip = ''
    port = '2121'
    
    def __init__(self):
        self._configure_users()
    
    @property
    def authorizer(self):
        return self._authorizer
        
    @authorizer.setter
    def authorizer(self, val):
        self._authorizer = val
    
    @property
    def handler(self):
        return self._handler
    
    @handler.setter
    def handler(self, val):
        self._handler = val
        
        if self.authorizer:
            self._handler.authorizer = self.authorizer 
    
    def _configure_users(self):
        self.authorizer = DummyAuthorizer()
        self.authorize_user('KC12345', 'webjcl')
        
    def _configure_handler(self):
        self.handler = ZosFTPHandler
    
    def _configure_server(self):
        address = (self.ip, self.port)
        self.server = FTPServer(address, self.handler)
        
    def authorize_user(self, name, pw):
        self.authorizer.add_user(name, pw, '.', perm='elradfmwM')
        
    def start(self):
        self._configure_handler()
        self._configure_server()
        
        self.server.serve_forever()
