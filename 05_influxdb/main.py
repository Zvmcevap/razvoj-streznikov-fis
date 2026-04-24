
import matplotlib.pyplot as plt
from datetime import datetime
from influxdb import InfluxDBClient

# Connect
host = '149.62.71.186'
user = 'admin'
password = 'fis_influx'
port = 8086
client = InfluxDBClient(host, port, user, password)

client.create_database('BenoZupanc')
client.switch_database('BenoZupanc')

# WRITE
with open('temperature_data.txt') as f:
    for line in f.readlines():
        list_line = line.split(',')
        temp_1, temp_2, cas, oseba = map(lambda x: x.strip(), line.split(','))
        print(temp_1, temp_2, cas, oseba)
        point = {"measurement": "Temperature",
                 "tags": {"oseba": oseba, "tag2": 'nvem'},
                 "time": cas,
                 "fields": {"T1": float(temp_1), "T2": float(temp_2)}}
        client.write_points([point])

# READ

field = 'T1'
measurement = 'Temperature'
database = 'Naloga 0'
tag_type = 'user'
tag_value = 'user1'


def narisi_od_tag_c(database, measurement, field, tag):
    tag_type = list(tag.keys())[0]
    tag_value = tag[tag_type]
    result = client.query(
        f'SELECT "{field}" FROM "{database}".."{measurement}" WHERE "{tag_type}"=\'{tag_value}\'')
    items = result.items()

    for item in items:
        descripiton, generator = item
        meas, tag_ = descripiton
        values, times = [], []
        for point in generator:
            times.append(point['time'])
            values.append(point['T1'])

        # turn to seconds
        dt = [datetime.fromisoformat(
            i.replace('Z', '+00:00')).timestamp() for i in times]
        # start from zero time
        dt_zero = [i-dt[0] for i in dt]

        plt.figure(figsize=(12, 4))
        plt.plot(dt_zero, values)


narisi_od_tag_c(database, measurement, field, {tag_type: tag_value})
