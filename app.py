from flask import Flask 
from views import views

# below part moves to view.py
# @app.route("/")
# def home():
#     return "this is the home page"

#http://127.0.0.1:8000/poolRecorder

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    #app.run(debug=True,port=8000)  #for local testing
    app.run(debug=True)
