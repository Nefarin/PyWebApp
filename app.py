from flask import Flask
from flask import render_template
from flask import request
from flask import session
from inter import mIntermedica
from flask import redirect
from flask import url_for
from flask import abort
from flask.ext.session import Session
from flask_sqlalchemy import SQLAlchemy
import json

import json
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)

SESSION_TYPE = 'sqlalchemy'
app.config.from_object(__name__)
Session(app)


class DiceaseGraph(db.Model):
    __tablename__ = "dicease_graph"
    id = db.Column(db.Integer, primary_key = True)
    probs = db.Column(db.String(3000))
    names = db.Column(db.String(3000))
    indexes = db.Column(db.String(3000))


    def __init__(self, probs, names, indexes):
        self.probs = json.dumps(probs)
        self.names = json.dumps(names)
        self.indexes = json.dumps(indexes)

        
    
    
@app.route('/')
def main_page():
    header = render_template("header.html", home=True)
    page = render_template("main_page.html")
    footer = render_template("footer.html")
    return header + page + footer

@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis_page():
    handler = mIntermedica()
   # symptoms = handler.getSymptoms()
    symptoms = "Nothing to do there"
    #symptomsDict, symptomsList, symptomsValues = handler.parseSearch(symptoms)
    if request.method == "POST":
        phrase = handler.search(request.form["phrase"], sex=request.form["sex"])
        phraseDict, phrases, values = handler.parseSearch(phrase)
        session['phrasesDict'] = phraseDict
        session['result'] = phrase
        draws = len(phrases) != 0
        page = render_template("diagnosis_page.html") + render_template("search_symptoms.html", input = phrases, draw=draws)
    else:
        page = render_template("diagnosis_page.html", symptoms = symptoms)
    header = render_template("header.html", diagnosis=True)  
    footer = render_template("footer.html")
    return header + page + footer
    
@app.route('/visualization')
def visualization_page():
    graphData = DiceaseGraph.query.all()
    
    header = render_template("header.html", visualization=True)
    page = render_template("visualization_page.html", graphData = graphData)
    footer = render_template("footer.html")
    return header + page + footer
    
@app.route('/about')
def about_page():
    header = render_template("header.html", about=True)
    page = render_template("about_page.html")
    footer = render_template("footer.html")
    return header + page + footer
    
@app.route('/diagnose', methods = ['POST'])
def diagnose():
    phraseDict = session['phrasesDict']
    result = session['result']
    #presences = [request.form[str(x)] for x in phraseDict.keys()]
    symptoms = []
    for item in phraseDict.keys():
       temp = dict(id = phraseDict[item], presence=request.form[str(item)])
       symptoms.append(temp)

    handler = mIntermedica()
    try:
        diagnose = handler.diagnose(symptoms)
        conditions = diagnose.conditions
        probs = []
        names = []
        for condition in conditions:
            probs.append(condition['probability'])
            names.append(condition['name'])
        indexes = list(range(0, len(probs)))
        session['probs'] = probs
        session['names'] = names
        session['indexes'] = indexes
        page = render_template("debug.html", input=diagnose, probs = probs, names = names, index = indexes)
    except:
        page = render_template("diagnosis_empty.html")
    
    header = render_template("header.html")  
    footer = render_template("footer.html")
    return header + page + footer

@app.route('/save', methods=['POST'])
def save():

    wtf = DiceaseGraph(session['probs'] , session['names'] , session['indexes'] )
    db.session.add(wtf)
    db.session.commit()
    
    return redirect('visualization')
    
if __name__ == '__main__':
    app.run()
    
    