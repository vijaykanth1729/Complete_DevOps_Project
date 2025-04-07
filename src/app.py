from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return return '<h1 style="background-color: lightblue;">Welcome to My Flask App! Deployed to ECS Using GitHub Actions</h1>'

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
