import os
import shutil
import json
import sys
import pkgutil

from scripts.db_scripts import upload_to_db
from scripts.cms_scripts import cms_session_to_json
from scripts.gdrive_scripts import gdoc_to_pdf

# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

inputjson=json.loads(open('sessions.json','r').read())
# clear any existing outputs
shutil.rmtree("outputs") 
os.mkdir("outputs")
# interate over each row of input json, convert doc html to custom tags structure,
# download doc as pdf, and upload to db
for row in inputjson:
    session = cms_session_to_json(row)
    _id = session['slug']
    session['_id']=_id
    fts = "outputs/" + session['slug']+".json"
    with open(fts, 'w') as outfile:
        json.dump(session, outfile)
    # TODO - only download pdf if doc changed (call from db method) 
    gdoc_to_pdf(session["gdoc_id"],_id)
    print('pdf exported, uploading')
    upload_to_db(session)    