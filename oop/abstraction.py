from abc import ABC, abstractmethod


# This is our Abstraction (the contract)
class DataReader(ABC):
    @abstractmethod
    def connect(self):
        """Establish connection to the data source."""
        pass

    @abstractmethod
    def fetch_data(self, query: str):
        """Fetch and return the data."""
        pass


# Implementation 1: Local Database
class PostgresReader(DataReader):
    def connect(self):
        print("Connecting to Postgres via psycopg2...")

    def fetch_data(self, query: str):
        print(f"Executing '{query}' on Postgres...")
        return {"data": "postgres_results"}


# Implementation 2: Cloud Storage
class S3ParquetReader(DataReader):
    def connect(self):
        print("Authenticating with AWS S3...")

    def fetch_data(self, query: str):
        print(f"Filtering Parquet files in S3 for '{query}'...")
        return {"data": "s3_results"}


def run_analytics(reader: DataReader):
    # The business logic relies on the abstraction, not the concrete class.
    reader.connect()
    data = reader.fetch_data("SELECT * FROM trades")
    print("Processing:", data)


if __name__ == "__main__":
    # You can swap the implementation without changing the analytics logic
    db_reader = PostgresReader()
    run_analytics(db_reader)
