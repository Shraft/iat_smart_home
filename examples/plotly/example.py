import plotly.express as px
import pandas as pd



def crete():
    df = pd.DataFrame(dict(
        x = [1, 3, 2, 4],
        y = [1, 2, 3, 4]
    ))

    df = df.sort_values(by="x")
    fig = px.line(df, x="x", y="y", title="Sorted Input") 
    #fig.show()
    fig.write_html("file.html")
    print("done")


crete()


