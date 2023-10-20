from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/")
def root():
    return redirect("/home")

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/allsensors')
def allsensors():
    return render_template('allsensors.html')

if __name__ == '__main__':
    app.run(debug=True)