from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/network")
def network():
    return render_template("network.html")

@app.route("/signals")
def signals():
    return render_template("signals.html")

@app.route("/optimize")
def optimize():
    return render_template("optimize.html")



if __name__ == "__main__":
    app.run(debug=True)
