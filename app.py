from flask import Flask

# creation of Flask object, deals with interacting with the web
app = Flask(__name__)

# Think of this as an event listener (ex. button on click listeners in Kotlin), when we load the
# home page, then this function runs.
@app.route("/")
def home():
    return "homepage"

if __name__ == "__main__":
    app.run(debug=True)