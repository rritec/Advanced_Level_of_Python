# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 17:04:09 2019

@author: vmyla1
"""

from flask import Flask, jsonify,request,render_template,redirect
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient(u"mongodb://localhost:27017")        
mydb = myclient["rritec_20191109"] 
coll_name='frameworks'    
mycol = mydb[coll_name]

# added as part of UI
@app.route('/')
def hello_world():
    return render_template('index.html')
# Insert one document into mongo collection

@app.route('/framework', methods=['POST'])
def add_framework():
    #framework = mongo.db.framework 

    name = request.form['name']
    language = request.form['language']

    framework_id = mycol.insert({'name' : name, 
                                     'language' : language})
    new_framework = mycol.find_one({'_id' : framework_id})

    output = {'name' : new_framework['name'], 'language' : new_framework['language']}

    return f"Inseted a row successfully with below details {output} "

# Get all documents from mongo collection

@app.route('/framework', methods=['GET'])
def get_all_frameworks():
    output = []

    for q in mycol.find():
        output.append({'name' : q['name'], 'language' : q['language']})

    return jsonify({'result' : output})

# Get one documents from mongo collection by filtering on name    
@app.route('/framework/<name>', methods=['GET'])
def get_one_frameworks(name):
    output = []

    q = mycol.find_one({'name' : name})
    print(q)

    if q:
        output = {'name' : q['name'], 'language' : q['language']}
    else:
        output = 'No results found'

    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)