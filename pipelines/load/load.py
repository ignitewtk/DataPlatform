
from pipelines.utils import connect_warehouse, load_warehouse, read_from_datalake


def main():
    pass

    # Connect to Source stage 3 (processed)
    # Fetch data from Azure Data Lake Storage Gen 2
    read_from_datalake()
    
    # Load / Save data into data warehouse or data mart for reporting
    connect_warehouse()
    load_warehouse()


if __name__ == "__main__":
    main()