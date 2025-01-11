import csv

def readFlowLogs(filePath: str):
    with open(filePath, 'r') as file:
        for line in file:
            yield line

def readLookupTable(filePath: str):
    with open(filePath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row

def writeStats(stats: list[dict], filePath: str):
    with open(filePath, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=stats[0].keys())
        writer.writeheader()
        writer.writerows(stats)