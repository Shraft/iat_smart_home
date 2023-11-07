import plotly.express as px
import pandas as pd
#import plotly.io as pio
#pio.renderers.default
import time
from db_tables import Sensor_logs, Sensors



def create_diagram(sensor_history, uuid):
    k = len(sensor_history)
    x_list = []
    for n in range(0, k):
        x_list.append(n)

    df = pd.DataFrame(dict(
        time = list(x_list),
        temp = list(sensor_history)))   


    fig = px.line(df, x="time", y="temp", title="Sorted Input",) 
    #fig.show()

    fig = px.scatter(x=range(10), y=range(10))
    path = f"static/charts/{uuid}.html"
    print(f"safe to path: {path}")
    fig.write_html(path)



def create_diagrams(database):

    while True:
        db_temp_sensors = database.query(Sensors).filter(Sensors.sensor_type == "tmp").all()
        db_sensors_history = database.query(Sensor_logs).all()

        temp_sensors_value_history = {}

        if db_temp_sensors == None or db_sensors_history == None:
            return

        for temp_sensor in db_temp_sensors:
            for any_sensor in db_sensors_history:
                if temp_sensor.sid == any_sensor.sid:
                    if temp_sensor.uuid in temp_sensors_value_history:
                        value_list = temp_sensors_value_history[temp_sensor.uuid]
                        value_list.append(any_sensor.value)
                    else:
                        value_list = []
                        value_list.append(any_sensor.value)
                        temp_sensors_value_history[temp_sensor.uuid] = value_list

        #websocket.emit("temp_sensor_history", json.dumps(temp_sensors_value_history))
        for sensor in temp_sensors_value_history:
            k = 10
            while len(temp_sensors_value_history[sensor]) > k:
                temp_sensors_value_history[sensor].pop(0)
            print("create Diagram")
            create_diagram(temp_sensors_value_history[sensor], sensor)


        time.sleep(60)


