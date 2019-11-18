import sys
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
from google.cloud.automl_v1beta1 import PredictionServiceClient
from PIL import Image
import os
from flask import Flask, redirect, url_for, request ,render_template
project_id = ""
model_id = ""
def get_prediction(content, project_id, model_id):
  prediction_client = PredictionServiceClient.from_service_account_file("AI_KEY.json")
  name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
  payload = {'image': {'image_bytes': content }}
  params = {}
  request = prediction_client.predict(name, payload, params)
  return request
app = Flask(__name__)
@app.route('/',methods = ['POST', 'GET'])
def index():
    return render_template("ai_web.html")
@app.route('/summit',methods = ['POST', 'GET'])
def summit():
    f = request.files['file']
    f.save(f.filename)
    try:
        with open(f.filename, 'rb') as ff:
            content = ff.read()
    except:
        re="You can only upload photo."
    try:
        response=get_prediction(content, project_id,  model_id)
        for result in response.payload:
            re=result.display_name.replace("Many_sugar","High sugar")
            break
    except:
        re="You can only upload photo."
    return render_template("summit_web.html",res=re)
