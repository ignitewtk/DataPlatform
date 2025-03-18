from pipelines.utils import connect_cosmos, write_to_datalake
from pyspark.sql import SparkSession
from azure.storage.filedatalake import DataLakeServiceClient
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()


# Preprocessing and clean data
def transform_data(df):
    from pyspark.sql.functions import col, from_json
    
    # parse nested json structure
    parsed_df = df.withColumn(
        "interaction_data", 
        from_json(col("data"), "map<string,string>")
    )

    cleaned_df = parsed_df.filter(
        col("interaction_data").isNotNull() &
        col("user_id").isNotNull()
    ).select(
        col("user_id"),
        col("timestamp"),
        col("interaction_type"),
        col("interaction_data")["page_url"].alias("page_url"),
        col("interaction_data")["duration_sec"].alias("duration_sec")
    )
    
    return cleaned_df


def main():
    # Initiate Spark session (local)
    spark = SparkSession.builder \
        .appName("CosmosDB_ETL") \
        .config("spark.jars.packages", "com.azure.cosmos.spark:azure-cosmos-spark_3-3_2-12:4.16.0") \
        .getOrCreate()

    
    # Fetch data from source (Azure Cosmos DB)
    raw_df = connect_cosmos(spark).load()

    # Store result into Azure Data Lake Storage Gen 2 as stage 1 (raw)
    write_to_datalake(
        transformed_df, 
        "user-interactions/year=2023/month=08/day=01"
    )

    # ETL process
    transformed_df = transform_data(raw_df)
    
    # Store result into Azure Data Lake Storage Gen 2 as stage 2 (staging)
    write_to_datalake(
        transformed_df, 
        "user-interactions/year=2023/month=08/day=01"
    )
    
    spark.stop()

if __name__ == "__main__":
    main()