## worker.py

import cx_Oracle
import csv
import pandas as pd
import os
import smtplib
from email.message import EmailMessage
from colorama import Fore, Style
import subprocess

def get_db_connection(db_username, db_password, db_connection_string):
    orcl = cx_Oracle.connect(db_username, db_password, db_connection_string)
    orcl.autocommit = False    
    return orcl

def execute_procedures(db_connection, procedure_list, logger):

    sql = """select owner || '.' || object_name as procedure_name
                from all_procedures
                where owner || '.' || object_name in ({0}) 
                and object_type = 'PROCEDURE'""".format(procedure_list)
    
    
    # validate procedure_list from data dictionary 
    try: 
        logger.info("worker.execute_procedures() - validating procedure_list from data dictionary")
        curs = db_connection.cursor()
        curs.execute(sql)
        resultset = curs.fetchall()
    
    except Exception as e:
        logger.error(f"{Fore.RED} worker.execute_procedures() - error while validating procedure_list from data dictionary {Style.RESET_ALL}")
        raise

    finally:
        curs.close()


    # call procedures validated agains't data dictionary
    logger.info("worker.execute_procedures() - calling procedures validated from data dictionary")
    for row_data in resultset:
        procedure_name = row_data[0]
        if procedure_name:

            try:

                logger.info(f"worker.execute_procedures() - calling procedure {procedure_name}")
                curs = db_connection.cursor()
                curs.callproc(procedure_name)
                db_connection.commit()
                logger.info(f"worker.execute_procedures() - procedure {procedure_name} finished and commited")
            
            except Exception as e:
                logger.error(f"{Fore.RED} worker.execute_procedures() - errir calling procedure {procedure_name} {Style.RESET_ALL}")
                raise

            finally:
                curs.close()


def spool_file(sql_string, table_name, module_config, db_connection, logger, clean=False):

    logger.info(f"worker.spool_file() - working on table {table_name} into {module_config.file_type} format")

    file_path = module_config.spool_directory + os.path.sep + str.lower(table_name).split(".")[-1]
    if module_config.file_type == "pipe_delimited":
        file_path = file_path + ".tsv"
    elif module_config.file_type == "xlsx":
        file_path = file_path + ".xlsx"


    # remap known nullable sequences from float of int64
    integer_sql = """select t.column_name
                   from all_tab_cols t 
                   where t.owner || '.' || t.table_name = '{0}'
                   and t.data_type = 'NUMBER'
                   and (t.data_scale = 0 or t.column_name = 'SEQPERSPROG')""".format(table_name)

    # this is old code which produces error "MemoryError: Unable to allocate ..." while spooling 3 million rows from view_civitas_course_grade
    ## 
    # df = pd.read_sql(sql_string, db_connection)    

    # fix FK - 20200811
    # we are now spooling chunks of 1,000,000 rows at a time
    # read_sql returns an interable of dataframes 
    # we "write" the first and "append" subsequent dataframe

    # getting dataframes as iterators
    df_iterator = pd.read_sql(sql=sql_string, con=db_connection, chunksize=1000000)
    first_iteration = True
    for df in df_iterator:

        # remap known nullable sequences from float64 of int64
        try: 
            logger.info(f"worker.spool_file() - remapping known nullable seqnueces from float64 to int64")
            curs = db_connection.cursor()
            curs.execute(integer_sql)
            resultset = curs.fetchall()

            for row_data in resultset:
                column_name = row_data[0]
                df[column_name] = df[column_name].astype(pd.Int64Dtype())
                logger.info(f"worker.spool_file() - remapped {table_name}.{column_name} to int64")

        except Exception as e: 
            logger.error(f"{Fore.RED} worker.spool_file() - error getting known nullable int64 columns {Style.RESET_ALL}")
            raise
        
        finally: 
            curs.close() 


        if clean:
            logger.info(f"worker.spool_files() - cleaning table {table_name}")
            for column in df:
                if df[column].dtype == object: 
                    df[column] = df[column].str.replace(pat=r'(\r\n)|(\r)|(\n)', repl=', ', regex=True)

        #file_path = module_config.spool_directory + os.path.sep + str.lower(table_name).split(".")[-1]

        if module_config.file_type == "pipe_delimited":
            #file_path = file_path + ".tsv"
            if first_iteration:
                logger.info(f"worker.spool_files() - first iteration, spooling file {file_path} in write mode")
                df.to_csv(file_path, sep='|', header=True, encoding='utf-8', quoting=csv.QUOTE_NONE, escapechar='\\', index=False) 
                first_iteration = False
            else:
                logger.info(f"worker.spool_files() - subsequent iteration, spooling file {file_path} in append mode")
                df.to_csv(file_path, sep='|', mode='a', header=False, encoding='utf-8', quoting=csv.QUOTE_NONE, escapechar='\\', index=False)
                first_iteration = False
        
        if module_config.file_type == "xlsx":
            #file_path = file_path + ".xlsx"
            if first_iteration:
                logger.info(f"worker.spool_files() - first iteration, spooling file {file_path} in write mode")
                df.to_excel(file_path, index=False)
                first_iteration = False
            else:
                logger.info(f"worker.spool_files() - subsequent iteration, spooling file {file_path} in append mode")
                with pd.ExcelWriter(file_path, mode='a') as writer:
                    df.to_excel(writer, index=False, header=False)
                first_iteration = False

        logger.info(f"worker.spool_files() - spooled {table_name} into {file_path}")


    return file_path



def spool_and_send_files(db_connection, module_config, logger):

    table_list_sql = """select owner || '.' || object_name table_name
                        from all_objects
                        where owner || '.' || object_name in ({0})
                        and object_type in ('TABLE','VIEW')""".format(module_config.table_list)

    # validate table_list from data dictionary
    try: 
        logger.info("worker.spool_and_send_files() - validating table_list from data dictionary")
        curs = db_connection.cursor()
        curs.execute(table_list_sql)
        tableset = curs.fetchall()
    
    except Exception as e:
        logger.error("{Fore.RED} worker.spool_and_send_files() - error while validating table_list from data dictionary {Style.RESET_ALL}")
        raise

    finally:
        curs.close()
    

    # export tables validated agains't data dictionary
    logger.info("worker.spool_and_send_files() - spooling tables that have been validated from data dictionary")
    for row_data in tableset:
        table_name = row_data[0]
        
        # spool the file if table_name is valid
        if table_name:
            logger.info(f"worker.spool_and_send_files() - spooling table {table_name}")
            sql_string = f"select * from {table_name}"
            
            # clean the file if in clean list
            clean = False
            if table_name in module_config.cleanup_list:
                clean = True
                logger.info(f"worker.spool_and_send_files() - table {table_name} will be cleaned during spool")
            
            # spooling file here
            spooled_file = spool_file(sql_string, table_name, module_config, db_connection, logger, clean)

            # file spooled, now send to remote via scp
            logger.info(f"done spooling {spooled_file}, now sending to {module_config.scp_server}")
            subprocess.run(["scp", spooled_file, f"{module_config.scp_user}@{module_config.scp_server}:{module_config.scp_directory}/."])
            logger.info(f"done sending {spooled_file} to {module_config.scp_server}")






def email_logfile(email_to, log_filename, modulename, logger):
    """
    """
    
    logger.info(f"worker.email_logfile() - emailing logfile {log_filename} to {email_to}")
    
    
    with open(log_filename) as fp:
        msg = EmailMessage()
        msg.set_content(fp.read())

    msg['Subject'] = f"{modulename}: {log_filename}"
    msg['From'] = 'sis@yorku.ca'
    msg['To'] = email_to

    try:
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        logger.info(f"worker.email_logfile() - email sent to {email_to}")
        s.quit()

    except Exception as e:
        logger.error(f"{Fore.RED} worker.email_logfile() - failed to sent email to {email_to}. Moving on without raising an exception.{Style.RESET_ALL}")
        #logger.error(e, exec_info=True)
        
