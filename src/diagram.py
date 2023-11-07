import plotly.express as px
import pandas as pd




def create_diagram(sensor_history, uuid):

    k = len(sensor_history)
    x_list = []
    for n in range(0, k):
        x_list.append(n)

    print("reached")

    # df = pd.DataFrame(dict(
    #     time = list(x_list),
    #     temp = list(sensor_history)))    

    df = pd.DataFrame(dict(
        x = [1, 3, 2, 4],
        y = [1, 2, 3, 4]
    ))

    print(df)

    fig = px.line(df, x="x", y="y") 
    #fig.show()


    # geht vermutlich nicht, weil es ein extra thread ist

    print("reached3")
    #fig = px.scatter(x=range(10), y=range(10))
    path = f"static/charts/{uuid}.html"
    print(f"safe to path: {path}")
    fig.write_html(path)