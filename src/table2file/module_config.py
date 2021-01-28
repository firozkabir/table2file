## module_config.py

import os 

class ModuleConfig():


    """A class representing all the configurations needed to run a module."""

    def __init__(self, modulename, configfile,
                db_username = None,
                db_password = None,
                db_host = None,
                db_port = None,
                db_sid = None,
                table_list = None,
                cleanup_list = None,
                procedure_list = None,
                file_type = None,
                scp_user = None,
                scp_server = None,
                scp_directory = None,
                spool_directory = None,
                log_directory = None,
                email_to = None):
        
        """ this constructor is minimal on purose.
        Use setters to set properties after initialization"""

        self.modulename = modulename
        self.configfile = configfile
        self.db_username = None
        self.db_password = None
        self.db_host = None
        self.db_port = None
        self.db_sid = None
        self.table_list = None
        self.cleanup_list = None
        self.procedure_list = None
        self.file_type = None
        self.scp_user = None
        self.scp_server = None
        self.scp_directory = None
        self.spool_directory = None
        self.log_directory = None
        self.email_to = None

    @property
    def modulename(self):
        """Return the modulename."""
        return self._modulename
    
    @modulename.setter
    def modulename(self, modulename):
        """Set the modulename."""
        self._modulename = modulename

    @property
    def configfile(self):
        """Return the configfile."""
        return self._configfile
    
    @configfile.setter
    def configfile(self, configfile):
        """Set the configfile."""
        self._configfile = configfile

    @property
    def db_username(self):
        """Return the db_username."""
        return self._db_username
    
    @db_username.setter
    def db_username(self, db_username):
        """Set the db_username."""
        self._db_username = db_username    

    @property
    def db_password(self):
        """Return the db_password."""
        return self._db_password
    
    @db_password.setter
    def db_password(self, db_password):
        """Set the db_password."""
        self._db_password = db_password
    
    @property
    def db_host(self):
        """Return the db_host."""
        return self._db_host
    
    @db_host.setter
    def db_host(self, db_host):
        """Set the db_host."""
        self._db_host = db_host

    @property
    def db_port(self):
        """Return the db_port."""
        return self._db_port
    
    @db_port.setter
    def db_port(self, db_port):
        """Set the db_port."""
        self._db_port = db_port

    @property
    def db_sid(self):
        """Return the db_sid."""
        return self._db_sid
    
    @db_sid.setter
    def db_sid(self, db_sid):
        """Set the db_sid."""
        self._db_sid = db_sid

    @property
    def table_list(self):
        """Return the table_list."""
        return self._table_list
    
    @table_list.setter
    def table_list(self, table_list):
        """Set the table_list."""
        self._table_list = table_list

    @property
    def cleanup_list(self):
        """Return the cleanup_list."""
        return self._cleanup_list
    
    @cleanup_list.setter
    def cleanup_list(self, cleanup_list):
        """Set the cleanup_list."""
        self._cleanup_list = cleanup_list
    
    @property
    def procedure_list(self):
        """Return the procedure_list."""
        return self._procedure_list
    
    @procedure_list.setter
    def procedure_list(self, procedure_list):
        """Set the procedure_list."""
        self._procedure_list = procedure_list

    @property
    def file_type(self):
        """Return the file_type."""
        return self._file_type
    
    @file_type.setter
    def file_type(self, file_type):
        """Set the file_type."""
        self._file_type = file_type

    @property
    def scp_user(self):
        """Return the scp_user."""
        return self._scp_user
    
    @scp_user.setter
    def scp_user(self, scp_user):
        """Set the scp_user."""
        self._scp_user = scp_user

    @property
    def scp_server(self):
        """Return the scp_server."""
        return self._scp_server
    
    @scp_server.setter
    def scp_server(self, scp_server):
        """Set the scp_server."""
        self._scp_server = scp_server

    @property
    def scp_directory(self):
        """Return the scp_directory."""
        return self._scp_directory
    
    @scp_directory.setter
    def scp_directory(self, scp_directory):
        """Set the scp_directory."""
        self._scp_directory = scp_directory
    
    @property
    def spool_directory(self):
        """Return the spool_directory."""
        return self._spool_directory
    
    @spool_directory.setter
    def spool_directory(self, spool_directory):
        """Set the spool_directory."""
        self._spool_directory = spool_directory

    @property
    def log_directory(self):
        """Return the log_directory."""
        return self._log_directory
    
    @log_directory.setter
    def log_directory(self, log_directory):
        """Set the log_directory."""
        self._log_directory = log_directory

    @property
    def email_to(self):
        """Return the email_to."""
        return self._email_to
    
    @email_to.setter
    def email_to(self, email_to):
        """Set the email_to."""
        self._email_to = email_to

    def get_log_filename(self):
        return self.log_directory + os.path.sep + self.modulename + ".log"
    
    def get_db_connection_string(self):
        return f"{self.db_host}:{self.db_port}/{self.db_sid}"

    def __str__(self):
        """Return ModuleConfig string for str()."""
        return ('ModuleConfig(' +
        f'modulename={self.modulename}, ' +
        f'configfile={self.configfile}, ' +
        f'db_username={self.db_username}, ' +
        f'db_password={self.db_password}, ' +
        f'db_host={self.db_host}, ' +
        f'db_port={self.db_port}, ' +
        f'db_sid={self.db_sid}, ' +
        f'table_list={self.table_list}, ' +
        f'cleanup_list={self.cleanup_list}, ' +
        f'procedure_list={self.procedure_list}, ' +
        f'file_type={self.file_type}, ' +
        f'scp_user={self.scp_user}, ' +
        f'scp_server={self.scp_server}, ' +
        f'scp_directory={self.scp_directory}, ' +
        f'spool_directory={self.spool_directory}, ' +
        f'log_directory={self.log_directory}, ' +
        f'email_to={self.email_to}' +
        ')')