"""SimpleApp.py"""
import pyspark
import os

### This is a sample Spark application that can be submitted with the spark-submit operator
## or by simply calling `python sample_spark_app.py`. It is intended to be run from inside the Jupyter
## container, which already has the neccesary dependencies and environment variables.

# The configuration below is exactly the same as in the example notebook, which can be run interactively (i.e. line-by-line)

S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY")
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")
S3_ENDPOINT = os.environ.get("S3_ENDPOINT")
# S3_ACCESS_KEY = "sparkaccesskey"
# S3_BUCKET = "test"
# S3_SECRET_KEY = "sparksupersecretkey"
# S3_ENDPOINT = "http://minio:9000"

conf = pyspark.SparkConf().setMaster("spark://spark:7077")
conf.set("spark.jars.packages", 'org.apache.hadoop:hadoop-aws:3.3.3,io.delta:delta-core_2.12:2.1.0')
# conf.set('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider')
conf.set('spark.hadoop.fs.s3a.endpoint', S3_ENDPOINT)
conf.set('spark.hadoop.fs.s3a.access.key', S3_ACCESS_KEY)
conf.set('spark.hadoop.fs.s3a.secret.key', S3_SECRET_KEY)
conf.set('spark.hadoop.fs.s3a.path.style.access', "true")
conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

sc = pyspark.SparkContext(conf=conf)

spark = pyspark.sql.SparkSession(sc)

### In the example below, we simply read a csv file and write it to object storage (Minio)
## However, you can do any operations you want below, whether thats making an HTTP request, doing ETL, etc...
## Spark operations will automatically be distributed across all available worker nodes

df = spark.read.option("header", "true").csv("/data/sales_info.csv")

delta_table_name = "my_sales_data_from_spark_application"
df.write.format("delta").save(f"s3a://{S3_BUCKET}/{delta_table_name}", mode="overwrite")

print("SUCCESSFULLY EXECUTED SPARK APPLICATION")

spark.stop()
