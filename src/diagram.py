import plotly.express as px
import pandas as pd
#import plotly.io as pio
#pio.renderers.default
import time
from db_tables import Sensor_logs, Sensors
from datetime import datetime



def create_diagram(sensor_history, uuid):
    k = len(sensor_history)
    x_list = []

    for n in range(0-k, 0):
        x_list.append(n)

    df = pd.DataFrame(dict(
        Zeit = list(x_list),
        Temperatur = list(sensor_history)))   


    fig = px.line(df, x="Zeit", y="Temperatur")#,range_y=[min(sensor_history),max(sensor_history)]) 
    path = f"src/static/charts/{uuid}.html"
    fig.write_html(path)



def create_diagrams(database):
    

    while True:
        db_temp_sensors = database.query(Sensors).filter(Sensors.sensor_type == "temp").all()
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
            k = 20
            while len(temp_sensors_value_history[sensor]) > k:
                temp_sensors_value_history[sensor].pop(0)
            #print(f"DIAGRAMS: create Diagram for {sensor}")
            start_time = datetime.now()
            create_diagram(temp_sensors_value_history[sensor], sensor)
            end_time = datetime.now()
            time_diff = end_time - start_time
            #print(f"DIAGRAMS: Done in {time_diff} seconds")


        time.sleep(60)


