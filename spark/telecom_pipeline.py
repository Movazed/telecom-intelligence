import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType
from pyspark.sql import functions as F

def create_session():
    """Creates and returns a SparkSession."""
    return SparkSession.builder \
        .appName("TelecomNetworkIntelligence") \
        .master("local[*]") \
        .getOrCreate()

def load(spark):
    """Task 2.1: Distributed Ingestion. Defines schema manually and loads CSVs."""
    print("Loading data into PySpark...")
    
    # We define the schema manually as requested (do not rely solely on inferSchema)
    # Matching the column order we discovered in Phase 1
    schema = StructType([
        StructField("timestamp_epoch", StringType(), True),
        StructField("grid_id", LongType(), True),
        StructField("country_code", StringType(), True),
        StructField("sms_in", DoubleType(), True),
        StructField("sms_out", DoubleType(), True),
        StructField("call_in", DoubleType(), True),
        StructField("call_out", DoubleType(), True),
        StructField("internet", DoubleType(), True)
    ])

    # Read all CSVs in the raw folder that match the pattern
    df = spark.read.csv("data/raw/sms-call-internet-mi-*.csv", schema=schema, header=True)
    
    print(f"Total records loaded: {df.count()}")
    return df

def clean(df):
    """Task 2.2: Cleaning & Standardization"""
    print("Cleaning and transforming data...")
    
    # 1. Cast timestamp (Convert epoch milliseconds to TimestampType)
    df = df.withColumn("timestamp", F.to_timestamp(F.col("timestamp_epoch")))
    
    # 2. Extract useful time columns for partitioning and grouping
    df = df.withColumn("date", F.to_date("timestamp")) \
           .withColumn("hour", F.hour("timestamp"))

    # 3. Normalize activity types by consolidating
    df = df.fillna(0.0, subset=["sms_in", "sms_out", "call_in", "call_out", "internet"])
    df = df.withColumn("call_count", F.col("call_in") + F.col("call_out")) \
           .withColumn("sms_count", F.col("sms_in") + F.col("sms_out")) \
           .withColumn("internet_usage", F.col("internet"))

    # 4. Filter out invalid rows (internet_usage < 0 or call_count is null)
    df = df.filter((F.col("internet_usage") >= 0) & (F.col("call_count").isNotNull()))
    
    # Drop intermediate columns to clean up schema
    df = df.select("grid_id", "timestamp", "date", "hour", "call_count", "sms_count", "internet_usage")
    
    return df

def enrich(spark, df):
    """Task 2.4 & 2.5: Joins with Geo Metadata and Performance Optimization"""
    print("Enriching with Geo Metadata...")
    
    # Load region mapping
    mapping_schema = StructType([
        StructField("grid_id", LongType(), True),
        StructField("region_name", StringType(), True),
        StructField("city", StringType(), True)
    ])
    region_df = spark.read.csv("data/raw/region_mapping.csv", schema=mapping_schema, header=True)
    
    # --- TASK 2.4: Broadcast Join ---
    # EXPLANATION: We use F.broadcast() here because region_mapping.csv is extremely small (just a few rows).
    # A broadcast join sends this tiny table to all worker nodes, avoiding a costly shuffle of the massive 'df' table over the network.
    df_enriched = df.join(F.broadcast(region_df), on="grid_id", how="left")
    
    # Fill in unknown regions
    df_enriched = df_enriched.fillna("Unknown", subset=["region_name", "city"])

    # --- TASK 2.5: Performance Optimization ---
    # 1. Column Pruning: We already selected only the needed columns at the end of the clean() function.
    # 2. Caching: We cache this dataframe because it will be reused for multiple KPI aggregations and writing.
    df_enriched = df_enriched.cache()
    
    # 3. Repartitioning: We repartition by date since we will write partitioned by date. 
    df_enriched = df_enriched.repartition("date")
    
    # Output execution plan to show optimizations
    print("\n--- Execution Plan (Optimizations Applied) ---")
    df_enriched.explain()
    print("----------------------------------------------\n")

    return df_enriched

def aggregate(df):
    """Task 2.3: Aggregations"""
    print("Computing KPIs...")
    summary = {}
    
    # Calls per hour (across all regions)
    summary['calls_per_hour'] = df.groupBy("hour").agg(F.sum("call_count").alias("total_calls")).orderBy("hour")
    
    # SMS per region per day
    summary['sms_per_region_day'] = df.groupBy("date", "region_name").agg(F.sum("sms_count").alias("total_sms"))
    
    # Internet usage per day
    summary['internet_per_day'] = df.groupBy("date").agg(F.sum("internet_usage").alias("total_internet")).orderBy("date")
    
    # Top 5 peak usage hours (based on internet usage)
    summary['top_peak_hours'] = df.groupBy("hour") \
                                  .agg(F.sum("internet_usage").alias("total_internet")) \
                                  .orderBy(F.desc("total_internet")) \
                                  .limit(5)
                                  
    return summary

def write(df, summary):
    """Task 2.6: Write Processed Output"""
    print("Writing Processed Data to Parquet...")
    
    # Write the main enriched dataset to Parquet, partitioned by date
    # mode("overwrite") ensures we don't duplicate data if we run the script twice
    output_path = "data/processed/telecom_usage/"
    df.write.mode("overwrite").partitionBy("date").parquet(output_path)
    print(f"Main dataset written successfully to {output_path}")
    
    # Note: For the summary, we would usually write these to small CSVs or JSONs for the dashboard, 
    # but for this script, we'll just show the peak hours as a success check!
    print("\n--- Top 5 Peak Hours KPI ---")
    summary['top_peak_hours'].show()

def main():
    """Task 2.7: Main Pipeline Wrapper"""
    spark = create_session()
    
    try:
        df_raw = load(spark)
        df_clean = clean(df_raw)
        df_enriched = enrich(spark, df_clean)
        summary = aggregate(df_enriched)
        write(df_enriched, summary)
        
        print("\n✅ Phase 2 PySpark Pipeline Completed Successfully!")
    except Exception as e:
        print(f"Pipeline failed: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()