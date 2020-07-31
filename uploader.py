from flask import Flask, request, jsonify, make_response
import traceback
from uuid import uuid4
from flask_cors import CORS
from models.dbinsert import User, Tranasaction
import traceback
from idone import indone_auth

# Global initializations
app = Flask(__name__)
CORS(app)

@app.route('/upload/uid',methods=['GET'])
@indone_auth('6867a2d4-971b-4f63-a9a8-effc976ab38b')
def create_folder(*args, **kwargs):
    if request.method == 'GET':
        try:
            flag = True
            while(flag):
                current_user = str(kwargs['user_id'])
                _id = str(uuid4())
                flag = not(User.insert_upload(_id,current_user))
            Tranasaction.insert_process(user=current_user,uid=_id,step='1')
            #check if it exists -> if not: put _id in some db and return it
            return make_response(jsonify(
                {
                    'status' : 'success',
                    'desc' : '',
                    'result' : {
                        'uid':_id
                    }
                }
            ), 200)

        except:
            print(traceback.print_exc())
            return make_response(jsonify(
                {
                    'status' : 'fail',
                    'desc' : 'Error occured while generating UID',
                    'result' : {}
                }
            ), 201)
