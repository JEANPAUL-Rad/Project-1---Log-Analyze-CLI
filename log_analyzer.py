import argparse

# Create argument parser
parser = argparse.ArgumentParser(description="Log Analyzer")

# Accept log file path
parser.add_argument("-file", required=True, help="Path to log file")

# Read arguments
args = parser.parse_args()

print("Selected file:", args.file)