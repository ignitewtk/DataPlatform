from pipelines.utils import connect_cosmos, read_from_datalake, write_to_datalake
from pyspark.sql import SparkSession

def transform_data(raw_df):
    pass

def main():
    # Initiate Spark session (local)
    spark = SparkSession.builder \
        .appName("CosmosDB_ETL") \
        .config("spark.jars.packages", "com.azure.cosmos.spark:azure-cosmos-spark_3-3_2-12:4.16.0") \
        .getOrCreate()

    # Connect to Source stage 2 (staging) and fetch data
    read_from_datalake()
    
    # Batch process and transform using PySpark
    raw_df = connect_cosmos(spark).load()
    transformed_df = transform_data(raw_df)
 

    # Store result into Azure Data Lake Storage Gen 2 as stage 3 (processed)
    write_to_datalake(
        transformed_df, 
        "user-interactions/year=2023/month=08/day=01"
    )
    
    spark.stop()

if __name__ == "__main__":
    main()