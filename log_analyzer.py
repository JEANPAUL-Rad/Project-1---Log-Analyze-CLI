import argparse
import json
import csv


parser = argparse.ArgumentParser(description="Log Analyzer")

parser.add_argument("-file", required=True, help="Path to log file")
parser.add_argument("--level", help="Filter by level (ERROR, INFO, WARNING)")
parser.add_argument("--export", help="Export summary to CSV file")

args = parser.parse_args()

logs = []
errors = 0
warnings = 0
info = 0
error_messages = {}
failure_timestamps = []


with open(args.file, "r") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        try:
            log = json.loads(line)
            timestamp = log["timestamp"]
            level = log["level"]
            message = log["message"]

        except json.JSONDecodeError:
            parts = line.split(maxsplit=3)
            timestamp = parts[0] + " " + parts[1]
            level = parts[2]
            message = parts[3]


        if args.level and level != args.level:
            continue

        logs.append({
            "timestamp": timestamp,
            "level": level,
            "message": message
        })

        if level == "ERROR":
            errors += 1
            failure_timestamps.append(timestamp)

            error_messages[message] = error_messages.get(message, 0) + 1

        elif level == "WARNING":
            warnings += 1

        elif level == "INFO":
            info += 1


most_common_error = None

if error_messages:
    most_common_error = max(error_messages, key=error_messages.get)



print("\n===== LOG SUMMARY =====")
print(f"Total logs: {len(logs)}")
print(f"Errors: {errors}")
print(f"Warnings: {warnings}")
print(f"Info: {info}")

print(f'Most frequent error: "{most_common_error}"')
print(f"Failure timestamps: {', '.join(failure_timestamps)}")


if args.export:
    with open(args.export, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["metric", "value"])
        writer.writerow(["total_logs", len(logs)])
        writer.writerow(["errors", errors])
        writer.writerow(["warnings", warnings])
        writer.writerow(["info", info])
        writer.writerow(["most_common_error", most_common_error])