# local_parse.py
from drain3 import TemplateMiner
from drain3.template_miner_config import TemplateMinerConfig
import csv
import os

# Initialize Drain3
config = TemplateMinerConfig()
config.load("drain3.ini")
template_miner = TemplateMiner(config=config)

input_log_path = "HDFS.log"  # Make sure this matches your extracted log file name
output_csv_path = "parsed_logs.csv"

# Configuration for testing
LIMIT_LINES = True  # Set to False when you are ready to process all 11M lines!
MAX_LINES_TO_PROCESS = 100000 

if not os.path.exists(input_log_path):
    print(f"❌ Error: Could not find '{input_log_path}' in this folder. Please ensure the file is fully downloaded and extracted.")
    exit()

print("🚀 Starting streaming log parse...")

with open(input_log_path, "r", encoding="utf-8", errors="ignore") as infile, open(output_csv_path, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["line_id", "template_id"]) # CSV Header
    
    for line_id, line in enumerate(infile):
        # Stream parse line by line (keeps RAM extremely low)
        result = template_miner.add_log_message(line.strip())
        template_id = result["cluster_id"]
        
        writer.writerow([line_id, template_id])
        
        # Print progress updates every 25,000 lines
        if line_id % 25000 == 0 and line_id > 0:
            print(f"Processed {line_id} lines successfully...")
            
        if LIMIT_LINES and line_id >= MAX_LINES_TO_PROCESS:
            print(f"Stopping early at {MAX_LINES_TO_PROCESS} lines for testing.")
            break

print(f"Finished! Your output is saved in '{output_csv_path}'")  