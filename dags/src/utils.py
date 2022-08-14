import subprocess
def load_files_to_hdfs(spark, source_dir, target_dir, header, inferSchema):
    subprocess.run([f'hdfs dfs -put {source_dir} {target_dir}'], shell = True) 

    df = spark.read.format('csv').options(header=header).\
        options(inferSchema=inferSchema).load(target_dir)

    return df

def data_persist_postgresql(spark, df, dfName, url, driver, dbtable, mode, user, password):
	df.write.format("jdbc")\
			 .option("url", url)\
			 .option("driver", driver)\
			 .option("dbtable", dbtable)\
			 .mode(mode)\
			 .option("user", user)\
			 .option("password", password)\
			 .save()
