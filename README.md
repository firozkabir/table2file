# table2file
A python application to spool files from database tables and export them to remote server over scp. 
Designed to be a re-usable application through configurations for all file based outbound data integration


## Deployment

```bash
cd /usr/local/sis/sisbat
mkdir table2file
cd table2file
cvs co -d dist src/python/table2file/dist
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip3 install dist/table2file-0.1.1-py3-none-any.whl
```

## Usage

```bash
table2file ${modulename} ${configfile}
# example: table2file civitas /usr/local/sis/sisbat/table2file/config.ini
```

## Sample Configuration File

This is a sample config.ini file

```bash
[mymodule]
db_username = username
db_password = password
db_host = db.host.comd
db_port = 1521
db_sid = dbsid
table_list = 'SCHEMA.TABLE_ONE',
    'SCHEMA.VIEW_TWO'
cleanup_list = 'SCHEMA.TABLE_ONE'
procedure_list = 'SCHEMA.PROCEDURE_ONE'
scp_user = myusername
scp_server = sftp.host.comd
scp_directory = /home/myusername/mymodule
spool_directory = /home/batchuser/APPDATA/table2file/spool/civitas
log_directory = /home/batchuser/APPDATA/table2file/log
file_type = xlsx   # other options are pipe_delimited
email_to = myuser@email.com
```



## Developer's Notes: 

* configure virtualenv for development: 

```bash
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip3 install cx_Oracle pandas xlsxwriter argparse colorama
```

* build using setuptools

```bash
python3 setup.py sdist bdist_wheel
```

## Release Notes: 

* v0.1.0:
    - inital release, only handled civitas, nothing was parameterized

* v0.1.1 2020-08-11: 
	- Added the ability to use config.ini to to support multiple modules (e.g. civitas, fgsadjudication) (2020-06-15)
	- Replaced openpyxl with xlsxwriter (2020-06-15)
    - Added a chunksize of 1,000,000 to support export of large files (2020-08-11)
