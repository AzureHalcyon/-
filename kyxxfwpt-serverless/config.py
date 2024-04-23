import os

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", '')
db_address = os.environ.get("MYSQL_ADDRESS", 'sh-cynosdbmysql-grp-941a8nki.sql.tencentcdb.com:27674')

