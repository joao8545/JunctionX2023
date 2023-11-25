from flask import Flask, render_template, request,jsonify
from datetime import datetime,timezone
import database_interface as db
from ntfy_wrapper import Notifier


ntfy = Notifier(topics="patient3")
app = Flask(__name__)


patients=db.get_all_patients()
machines=db.get_all_machines()
names=list(map(lambda x: x.get_name(), patients))

@app.route('/')
def index():
    global ntfy
    ntfy("It is time")
    return render_template('index.html')

@app.route('/machines/<string:iname>',methods=['GET'])
def machine(iname):
    timeline_data=db.get_machine_schedule(iname)
    return render_template('machine.html',timeline_data=timeline_data)


@app.route('/machines')
def machine_base():
    timeline_data = generate_timeline_data()
    return render_template('machine.html',timeline_data=timeline_data)

@app.route('/appointment')
def new_appointment():
    return render_template('appointment.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('search')
    results = [name for name in names if search.lower() in name.lower()]
    return jsonify(results)

@app.route('/patient_info', methods=['GET'])
def user_info():
    name = request.args.get('name')
    user = next((user for user in patients if user.get_name().lower() == name.lower()), None)
    if user:
        return jsonify({"region": user.region, "topic": user.ntfy_topic})
    else:
        return jsonify({})

@app.route('/check_availability', methods=['GET'])
def check_availability():
    name = request.args.get('name')
    user = next((user for user in patients if user.get_name().lower() == name.lower()), None)
    if user:
        region = user.region
        avaiable_machines = list(map(lambda mm:mm.get_name(),filter(lambda m:m.can_treat(region),machines)))
        return jsonify({"available_machines": avaiable_machines})
    else:
        return jsonify({})




def generate_timeline_data():
    timeline_data = []

    for i in range(8,18):
        hour_label = f'{i}:00'
        timeline_data.append({'label': hour_label, 'bars': generate_bars()})
    #print(timeline_data)
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