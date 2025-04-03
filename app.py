from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to My Flask App</h1>"

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
