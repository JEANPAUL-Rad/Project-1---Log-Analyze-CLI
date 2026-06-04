import argparse

parser = argparse.ArgumentParser(description="Log Analyzer")

parser.add_argument("-file", required=True, help="Path to log file")

args = parser.parse_args()

with open(args.file, "r") as file:
    for number, line in enumerate(file, start=1):
        print(f"Line {number}: {line.strip()}")