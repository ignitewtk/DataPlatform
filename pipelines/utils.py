from pyspark.sql import SparkSession

def connect_cosmos(spark):
    """Connect to source"""
    return spark.read.format("cosmos.oltp")\
        .option("spark.synapse.linkedService", "cosmos-link")\
        .option("spark.cosmos.accountEndpoint", os.getenv("COSMOS_ENDPOINT"))\
        .option("spark.cosmos.accountKey", os.getenv("COSMOS_KEY"))\
        .option("spark.cosmos.database", "user-interaction")\
        .option("spark.cosmos.container", "raw-data")\
        .option("spark.cosmos.read.inferSchema.enabled", "true")\
        .option("spark.cosmos.read.maxItemCount", "1000")\
        .option("spark.cosmos.read.customQuery", "SELECT * FROM c WHERE c.timestamp >= '2023-08-01'")



def write_to_datalake(df, file_path):
    """Use ABFS protocol to write into Data Lake"""
    df.write.mode("overwrite")\
        .format("parquet")\
        .save(f"abfss://processed-data@{os.getenv('STORAGE_ACCOUNT_NAME')}.dfs.core.windows.net/{file_path}")


def read_from_datalake():
    pass

def connect_warehouse():
    pass

def load_warehouse():
    pass