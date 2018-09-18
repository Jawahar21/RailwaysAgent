from flask import Flask
from chatbot_activities import Activites

app = Flask(__name__)

@app.route('/',methods =['GET','POST'])
def webhook():
    return Activites().checkActivity()

@app.route('/delayedResponse',methods = ['GET','POST'])
def getDelayedResponse():
    return Activites().callDelayedResoponse()

if (__name__ == "__main__"):
    app.run(port = 5000)
