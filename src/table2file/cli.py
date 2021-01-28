## cli.py

import argparse 
from table2file import module_config as  mc
import configparser
import sys
from colorama import Fore, Style
import logging
import logging.handlers


#from module_config import ModuleConfig

def get_module_config():
    
    """Collects modulename and configfile from cli.
    Reads through the configuration file.
    Creates a ModuleConfig object with all necessary values.
    Returns the object to call to work with configs for this given module"""

    # setup cli parser 
    parser = argparse.ArgumentParser()
    
    parser.add_argument("modulename", help="module to process (required)", type=str)
    parser.add_argument("configfile", help="path to configuration file (required)", type=str)
    
    args = parser.parse_args()

    # construct ModuleConfig class from cli
    modconf = mc.ModuleConfig(args.modulename, args.configfile)

    # try to load the config file
    try:
        config = configparser.ConfigParser()
        config.read(modconf.configfile)
        config.sections()
        
        modconf.db_username = config[modconf.modulename]['db_username']
        modconf.db_password = config[modconf.modulename]['db_password']
        modconf.db_host = config[modconf.modulename]['db_host']
        modconf.db_port = config[modconf.modulename]['db_port']
        modconf.db_sid = config[modconf.modulename]['db_sid']
        
        modconf.scp_user = config[modconf.modulename]['scp_user']
        modconf.scp_server = config[modconf.modulename]['scp_server']
        modconf.scp_directory = config[modconf.modulename]['scp_directory']
        modconf.spool_directory = config[modconf.modulename]['spool_directory']
        modconf.log_directory = config[modconf.modulename]['log_directory']
        modconf.email_to = config[modconf.modulename]['email_to']
        modconf.file_type = config[modconf.modulename]['file_type']

        modconf.table_list = config[modconf.modulename]['table_list']
        modconf.cleanup_list = config[modconf.modulename]['cleanup_list']
        modconf.procedure_list = config[modconf.modulename]['procedure_list']

        # add properties from configfile to ModuleConfig object

    except KeyError as ke:
        print(f"{Fore.RED}Abort:{Style.RESET_ALL} cannot find required configuration {ke.args} in configfile {modconf.configfile}")
        sys.exit(1)

    except Exception as e:
        print(e)
        raise
   
    return modconf



def setup_logger(log_filename):
    """
    """
    
    try: 
        logger = logging.getLogger('table2file')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_filename)
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        handler = logging.handlers.RotatingFileHandler(log_filename, mode='w', backupCount=5)

    except FileNotFoundError as fe:
        print(f"{Fore.RED}Abort:{Style.RESET_ALL} cannot write logfile {log_filename}. {fe.args}")
        sys.exit(1)


    except Exception as e:
        print(e)
        raise

    
    return (logger, handler)
    