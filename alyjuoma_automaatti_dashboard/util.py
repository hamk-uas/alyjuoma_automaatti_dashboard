import csv

def downloadable(data):
    csv_data = csv.writer(open('data.csv', 'w'))
    csv_data.writerow(['id', 'dtime', 'farm_id', 'station_id', 'realtime','parameter_type', 'parameter_value'])
    for row in data:
        csv_data.writerow([row["id"], row["dtime"], row["farm_id"], row["station_id"], row['realtime'], row["parameter_type"], row["parameter_value"]])