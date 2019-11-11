from flask import Flask, json, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import cursor
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
import pandas as pd
from werkzeug.utils import secure_filename
import json
import os
import uuid

ALLOWED_EXTENSIONS = {'csv'} #Only allowing files in the type of cvs to be uploaded.

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'RCLog'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/RCLog'
app.config['JWT_SECRET_KEY'] = 'secret'

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class mergeError:
    def __init__(self, usersObject, uId, loadedObject, lId):
        self.useObj = usersObject,
        self.uId = uId,
        self.loaObj = loadedObject,
        self.lId = lId

################################################
################# REGISTRATION #################
################################################

@app.route('/users/register', methods=['POST'])
def register_user():
    users = mongo.db.RCLogCol
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    user_id = users.insert({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created,
        'accessType': ['user'],
        'docType': 'user',
        'entries': [],
        'license': []
    })

    new_user = users.find_one({'_id': user_id})

    result = {'email': new_user['email'] + ' registered'}

    return jsonify({'result' : result})

@app.route('/new/register', methods=['POST'])
def register_admin():
    users = mongo.db.RCLogCol
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()
    #I Removed the enries-list
    mergeConflict = []

    user_id = users.insert({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created,
        'accessType': ['admin'],
        'docType': 'user'
    })

    new_user = users.find_one({'_id': user_id})

    result = {'email': new_user['email'] + ' registered'}

    return jsonify({'result' : result})

################################################
#################### LOGIN #####################
################################################

@app.route('/users/login', methods=['POST'])
def login():
    users = mongo.db.RCLogCol
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    response = users.find_one({'email': email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity = {
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'email': response['email'],
                'accessType':response['accessType'],
                'id': str(response['_id'])
            })
            result = jsonify({"token": access_token})
        else:
            result = jsonify({"error": "Invalid username and password"})
    else:
        result = jsonify({"result": "No results found"})
    return result

################################################
################### ENTRIES ####################
################################################

@app.route('/getAllEntries/<u_id>',methods=['GET'])
def getAllEntries(u_id):
    documents = mongo.db.RCLogCol
    en = {}
    entries = []
    for e in documents.find_one({'_id':ObjectId(u_id)})['entries']:
        entries.append(e)
    sortEntries(entries)
    en['entries'] = entries
    return jsonify(en)

@app.route('/oneentry/<u_id>/<list_id>', methods=['GET'])
def get_Entry(u_id,list_id):
    response_object = {'status': 'success'}
    users = mongo.db.RCLogCol
    entries = []
    for e in users.find_one({'_id':ObjectId(u_id)})['entries']:
        entries.append(e)
    for le in entries:
        if(le['list_id'] == list_id):
            response_object['entry'] = le

    return jsonify(response_object)

@app.route('/addentry/<u_id>', methods=['POST'])
def add_Entry(u_id):
    users = mongo.db.RCLogCol
    post_data = request.get_json()
    new_entry = {
        'list_id': uuid.uuid4().hex,
        'location': post_data.get('location'),
        'date': post_data.get('date'),
        'geo': post_data.get('geo'),
        'routeName': post_data.get('routeName'),
        'grade' : post_data.get('grade'),
        'length' : post_data.get('length')
    }
    response_object = {'status': 'success'}
    if(new_entry['location'] != None):
        users.update_one({'_id': ObjectId(u_id)}, {'$push': {'entries': new_entry}})
    return jsonify(response_object)
#function that returns
@app.route('/entries/<u_id>/<list_id>', methods=['DELETE'])
def delete_Entry(u_id,list_id):
    response_object = {'status': 'success'}
    users = mongo.db.RCLogCol
    users.update_one({'_id': ObjectId(u_id)}, { '$pull': { "entries" : { 'list_id': list_id } } })
    return jsonify(response_object)

@app.route('/editentry/<u_id>/<list_id>', methods=['PUT'])
def edit_Entry(u_id,list_id):
    response_object = {'status': 'success'}
    users = mongo.db.RCLogCol
    post_data = request.get_json()
    new_entry = {
        'list_id': uuid.uuid4().hex,
        'location': post_data.get('location'),
        'date': post_data.get('date'),
        'geo': post_data.get('geo'),
        'routeName': post_data.get('routeName'),
        'grade' : post_data.get('grade'),
        'length' : post_data.get('length')
    }
    users.update_one({'_id': ObjectId(u_id)}, {'$pull': { "entries" : { 'list_id': list_id } } })
    if(new_entry['location'] != None):
        users.update_one({'_id': ObjectId(u_id)}, {'$push': {'entries': new_entry}})

    return jsonify(response_object)

@app.route('/pushEntries/<username>', methods=['POST'])
def upload_csv_file(username):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'result': 'No file part'})
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({'result': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            CSVresults = import_csvfile_db(file, username)
    return jsonify(CSVresults)

def entryToDB(entry, user):
    collection = mongo.db.RCLogCol
    entry['list_id']= uuid.uuid4().hex
    collection.update_one(
        {'_id':ObjectId(user)},
        {'$push': {'entries':entry}}
    )


def entryToDB(entry, user):
    collection = mongo.db.RCLogCol
    if entry['location'] != None:
        entry['list_id'] = uuid.uuid4().hex
        collection.update_one(
            {'_id':ObjectId(user)},
            {'$push': {'entries':entry}}
        )


################################################
################### LICENSE ####################
################################################

@app.route('/viewusers', methods=['GET','POST'])
def view_users():
    response_object = {'status': 'success'}
    find_post = mongo.db.RCLogCol.find()
    name_list = []
    for info in find_post:
        user = False
        for i in info['accessType']:
            if i == "user":
                user = True
        if user:
            single_info = {
                'name': info['first_name']+' '+info['last_name'],
                'id': str(info['_id']),
                'link': "/user/entries/"+ str(info['_id']),
                'giveLicense': "/user/addLicense/"+ str(info['_id']),
                'viewLicense': "/user/license/"+str(info['_id'])
            }
            name_list.append(single_info)

    response_object['user_info'] = name_list

    return jsonify(response_object)


@app.route('/license/<username>', methods=["GET"])
def get_license(username):
    response_object = {'status':'success'}
    all_users = mongo.db.RCLogCol

    single_user = all_users.find_one({'_id': ObjectId(username)})
    licenses = sortLicense(single_user['license'])
    
    response_object['license'] = licenses

    return jsonify(response_object)


@app.route('/addLicense/<user>', methods=["POST"])
def post_license(user):
    response_object = {'status':'success or something'}
    collection = mongo.db.RCLogCol
    post_data = request.get_json()
    if post_data.get('date_from') != None:
        license_id = {
            'docType': "license",
            'date_from': post_data.get('date_from'),
            'date_to': post_data.get('date_to'),
            'list_id': uuid.uuid4().hex
        }
        collection.update_one(
            {'_id':ObjectId(user)},
            {'$push': {'license':license_id}}
        )

    return jsonify(response_object)

################################################
##################### CSV ######################
################################################

def import_csvfile_db(file, username):
    myDB = mongo.db.RCLogCol
    data = pd.read_csv(file)
    storedEntries = myDB.find_one({'_id':ObjectId(username)})['entries']
    dataInJSON = json.loads(data.to_json(orient='records'))
    totNewEntries = (len(dataInJSON))
    totDuplicates = 0
    totEntriesAdded = 0
    for i in dataInJSON:
        tempDuplicates = 0
#Check new entry for being potential duplicate:
        for j in storedEntries:
            if i['location'] == j['location'] and i['date'] == j['date'] and i['routeName'] == j['routeName']:
                tempDuplicates += 1
#If no match to existing, add the new entry:
        if tempDuplicates == 0:
            entryToDB(i, username)
            totEntriesAdded += 1
        else:
            totDuplicates += tempDuplicates

    result = {
        'totNewEntries':totNewEntries,
        'totEntriesAdded':totEntriesAdded,
        'totDuplicates':totDuplicates
    }
    print(result)
    return result

def allowed_file(filename): #Used for controlling the filename when uploading a file.
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


################################################
############### SORTING ALGORITM ###############
################################################

#   objs is the list of objects that we want to sort.
def sortEntries(objs):
    # third importance, sort by route name
    objs.sort(key=lambda obj: obj['routeName'])
    # second importance, sort by name of location
    objs.sort(key=lambda obj: obj['location'])
    # first importance, sort by date
    objs.sort(key=lambda obj: obj['date'])
    return objs

def sortLicense(objs):
    # third importance, sort by route name
    objs.sort(key=lambda obj: obj['date_to'])
    return objs

################################################
#################### OTHER #####################
################################################

CORS(app)
@app.route('/hello', methods=['GET'])
def get():
        documents = []
        users = mongo.db.RCLogCol
        for c in users.find({}):
            c.pop("_id")
            documents.append(c)
        return jsonify(documents)

if __name__ == '__main__':
    app.run(debug=True)
