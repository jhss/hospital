from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, array, collect_list, length, size, first
from pyspark import SparkConf
from src.utils import data_persist_postgresql
import subprocess

import psycopg2
from psycopg2 import sql
import sys
import os

envn = 'PROD'
appName = 'test'
user = 'sparkuser1'
password = 'user123'


def transform():
    master = 'yarn'

    os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-1.8.0-openjdk-amd64'
    os.environ['SPARK_HOME'] = '/opt/spark-3.2.2-bin-hadoop3.2'
    os.environ['YARN_CONF_DIR'] = '/opt/hadoop/etc/hadoop'
    os.environ['HADOOP_CONF_DIR'] = '/opt/hadoop/etc/hadoop'
    print("[DEBUG] YARN_CONF_DIR: ", os.environ['YARN_CONF_DIR'])

    sConf = SparkConf()
    sConf.set("spark.hadoop.fs.default.name", "hdfs://localhost:9000")
    sConf.set("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000")
    spark = SparkSession.builder.master("yarn").appName(appName).\
            config("spark.hadoop.fs.default.name", "hdfs://localhost:9000").\
            config("spark.jars", "/opt/spark-3.2.2-bin-hadoop3.2/jars/postgresql-42.2.19.jar").\
            config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    spark.conf.set("spark.sql.debug.maxToStringFields", 1000)


    header = 'True'
    inferSchema = 'True'
    #source_dir = "/home/airflow/dags/data/"
    target_dir = "/hospital/data/"

#file_list = ["HospitalEvaluation.csv", "HospitalTop5_final.csv", "HospitalTreatment.csv"]
    file_list = ["HospitalEvaluation.csv", "HospitalTreatment.csv"]
    csv_list = []
    for file_name in file_list:
        csv_file = spark.read.format('csv').options(header='True').\
                    options(inferSchema='True').load(target_dir + file_name)
        csv_list.append(csv_file)

    eval_csv = csv_list[0] 
#top5_csv = csv_list[1].drop(*['_c0', 'name'])
    tret_csv = csv_list[1].drop('_c0')

# [Step 1] Pre-processing eval_csv -> 'name', 'ykiho', ['asmGrd', ...]
    columns_to_list = ['asmGrd{:02}'.format(i) for i in range(1, 24)]
    eval_csv_new = eval_csv.withColumn('asmGrdList', 
                                        array(columns_to_list))
    eval_csv_new = eval_csv_new.drop(*columns_to_list).drop('_c0')

# [Step 2] groupBy 'tret_csv' over 'ykiho' to make a list of srch. 

    tret_csv_new = tret_csv.groupBy("ykiho").agg(first('name'), first('addr'), collect_list(col('srch')).alias('srch_list')).toDF('ykiho', 'name', 'addr', 'srch_list')

# [Step 3] join 'treatment' and 'evaluation'
    join_csv = tret_csv_new.join(eval_csv_new, tret_csv_new.ykiho == eval_csv_new.ykiho, 'inner').drop(eval_csv_new.ykiho).drop(eval_csv_new.name)
    print("join_csv finish")


    #con = psycopg2.connect(dbname='postgres', host = 'postgres', user='airflow', password='airflow', port='5432')
    #con.autocommit = True
    #cur = con.cursor()

    #cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier('hospital')))

    data_persist_postgresql(spark, join_csv, dfName = 'final', 
                            url="jdbc:postgresql://postgres:5432/hospital", driver='org.postgresql.Driver', 
                            dbtable='home_join_eval', mode='overwrite', user='airflow', password='airflow')
    
    print("[DEBUG] persist finish")
    '''
    print("tret_eval: ", join_csv.columns, join_csv.count())
# [Step 4] join 'prejoined' and 'top5'
    join_csv = join_csv.join(top5_csv, join_csv.ykiho == top5_csv.ykiho, 'inner').drop(top5_csv.ykiho)

    print("join: ", join_csv.columns, join_csv.count())
    print(join_csv.show(5))

    data_persist_postgresql(spark = spark, df = join_csv, dfName = "final", url = "jdbc:postgresql://localhost:5431/hospital", 
                            driver = "org.postgresql.Driver", dbtable = 'home_join_final', mode = 'overwrite',
                            user = 'sparkuser', password = 'password')
    '''

if __name__ == '__main__':
    transform()
