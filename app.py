from flask import Flask, render_template, request
from datetime import datetime,timezone
from fake_db import *
from ntfy_wrapper import Notifier

ntfy = Notifier(topics="patient1")
app = Flask(__name__)



@app.route('/')
def index():
    global ntfy
    ntfy("It is time")
    return render_template('index.html')

@app.route('/machines/<string:iname>',methods=['GET'])
def machine(iname):
    global board
    query_result=get_machine_data(iname)
    return render_template('machine.html',sname=iname,obj=query_result)


@app.route('/machines')
def machine_base():
    timeline_data = generate_timeline_data()
    return render_template('machine.html',timeline_data=timeline_data)









def generate_timeline_data():
    timeline_data = []

    for i in range(8,18):
        hour_label = f'{i}:00'
        timeline_data.append({'label': hour_label, 'bars': generate_bars()})
    return timeline_data

def generate_bars():
    bars=[]
    for j in range(12):
        start=j * 5
        status='idle' if j>5 else 'patient'
        label='joao da silva'if status=='patient' else '\n'
        bars.append({'start': start, 'status':status, 'label':label})
    return bars


if __name__ == '__main__':
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.run(debug = True)