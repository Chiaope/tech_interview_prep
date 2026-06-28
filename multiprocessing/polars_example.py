"""
Only use multiprocessing when you have a heavy custom Python function that cannot be vectorized or optimized using Polars' built-in functions.
This is because multiprocessing incurs overhead from inter-process communication and data serialization/deserialization, which can negate the benefits of parallelization for lightweight operations.
In general, you should prefer using Polars' built-in functions and expressions, which are optimized for performance and can handle large datasets efficiently without the need for multiprocessing.
"""


import polars as pl
from concurrent.futures import ProcessPoolExecutor
import time

# 1. Define the custom, heavy Python function
# This function will receive a subset of the DataFrame containing one group
def heavy_computation(sub_df: pl.DataFrame) -> pl.DataFrame:
    # Simulate a time-consuming custom Python operation
    time.sleep(1) 
    
    # Perform your custom logic here
    # Example: Just adding a new column based on some custom python logic
    group_name = sub_df["group"][0]
    result_df = sub_df.with_columns(
        pl.lit(f"Processed_{group_name}").alias("status")
    )
    return result_df

def main():
    # 2. Create sample data
    df = pl.DataFrame({
        "group": ["A", "A", "B", "B", "C", "C", "D", "D"],
        "value": [1, 2, 3, 4, 5, 6, 7, 8]
    })

    # 3. Split the DataFrame into a list of DataFrames based on the group
    # as_dict=False returns a list of DataFrames instead of a Dictionary
    partitions = df.partition_by("group", as_dict=False)

    # 4. Use ProcessPoolExecutor to map the function across the partitions
    # max_workers dictates how many parallel processes to spawn
    with ProcessPoolExecutor(max_workers=4) as executor:
        # executor.map will distribute the list of DataFrames to the worker processes
        results = list(executor.map(heavy_computation, partitions))

    # 5. Recombine the processed DataFrames back into a single DataFrame
    final_df = pl.concat(results)
    
    print(final_df)

if __name__ == "__main__":
    main()