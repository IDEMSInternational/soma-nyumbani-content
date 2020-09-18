import json
import os
import couchdb

# upload a json document to the database
# note - should contain _id field as document id 
def upload_to_db(doc):
    print("id:",doc["_id"])
    DB_URL = os.getenv("DB_URL")
    if DB_URL:
        couch=couchdb.Server(DB_URL)
        db = couch["somanyumbani_testing"]
        attachment = open('outputs/'+ doc["_id"]+'.pdf', 'rb')
        try:
            # check for existing docs, if found check if identical to
            # generated and save updated doc if not
            # NOTE - an error will be thrown if doc does not exist
            # so handle case in except by simply creating
            existing = db[doc["_id"]]
            doc["_rev"]=existing["_rev"]
            # compare if the docs are identical (ignoring pdf attachment as is altered on upload)
            if '_attachments' in existing:
                del existing['_attachments']
            cf1 = json.dumps(doc, sort_keys=True)
            cf2 = json.dumps(existing, sort_keys=True)
            if cf1 != cf2:
                db.save(doc)
                db.put_attachment(doc, attachment, filename=None, content_type=None)
                print('updated')
            else:
                print('skipped')    
        except:
            doc_id, doc_rev = db.save(doc)
            db.put_attachment(doc, attachment, filename=None, content_type=None)
            print("created")