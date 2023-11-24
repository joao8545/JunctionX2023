from flask import Flask, render_template, request
from datetime import datetime,timezone
from fake_db import *

app = Flask(__name__)



@app.route('/')
def student():
   return render_template('index.html')

@app.route('/machine/<string:iname>',methods=['GET'])
def machine(iname):
    global board
    query_result=get_machine_data(iname)
    return render_template('machine.html',sname=iname,obj=query_result)
    pass



if __name__ == '__main__':
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.run(debug = True)