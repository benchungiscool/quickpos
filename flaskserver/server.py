from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def ShowMain():
  return render_template("index.html")
