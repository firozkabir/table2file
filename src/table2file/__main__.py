## __main__.py

from datetime import datetime
import subprocess

from table2file import cli
from table2file import worker

def main():
    
    # get configurations 
    modconf = cli.get_module_config()

    # setup logging
    log_filename = modconf.get_log_filename() 
    logger,handler = cli.setup_logger(log_filename)

    
    # application starts here
    logger.info(f"*** start - {modconf.modulename} - {datetime.now()} ***")

    # setup database connection
    
    try: 
        
        # setup database connection
        orcl = worker.get_db_connection(modconf.db_username, modconf.db_password, modconf.get_db_connection_string())

        # execute procedures to refresh database
        worker.execute_procedures(orcl, modconf.procedure_list, logger)

        # export and send files 
        worker.spool_and_send_files(orcl, modconf, logger) 

        
        logger.info(f"on remote - {modconf.scp_server}, creating done file, making files group read/write, showing ls output")
        
        # add done file on remote
        subprocess.run( ["ssh", 
                        f"{modconf.scp_user}@{modconf.scp_server}", 
                        f"echo $(date) > {modconf.scp_directory}/done"
                    ] 
                )

        # change permissions on remote
        subprocess.run( ["ssh", 
                        f"{modconf.scp_user}@{modconf.scp_server}", 
                        f"chmod 660 {modconf.scp_directory}/*"
                    ]  
                )

        # show what is on remote 
        ls_output = subprocess.run(["ssh", 
                                    f"{modconf.scp_user}@{modconf.scp_server}", 
                                    f"ls -ltrah {modconf.scp_directory}"
                                ], 
                                stdout=subprocess.PIPE, 
                                universal_newlines=True
                            )
        
        logger.info(f"* showing what is on {modconf.scp_server} *: \n\n {ls_output.stdout} \n")

        
    except Exception as e:
        orcl.rollback()
        raise
        
    finally: 
        orcl.close()
        
    
    # email logs
    worker.email_logfile(modconf.email_to, modconf.get_log_filename(), modconf.modulename, logger)

    logger.info(f"=== end - {modconf.modulename} - {datetime.now()} ===")
    # application ends here

    # rotating logfile
    handler.doRollover()

if __name__ == "__main__":
    main()