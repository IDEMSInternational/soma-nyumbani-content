# Soma Nyumbani Content

This repo contains scripts used to convert google docs to custom-formatted json objects, and populate a corresponding couchdb database instance with both json and exported pdfs.

The scripts expect an input file `sessions.json`, which is generated using [Google Drive CMS](https://www.drivecms.xyz/)

They populate an output folder, with an individual json for each row

## Setup

1. Copy `.env.sample` to `.env` and populate with database credentials (if sending outputs to a couchdb instance)

2. Populate `sessions.json` with output from Google Drive CMS

3. Run `python main.py`

This will initially extract html found in `sessions.json` to individual files in the `outputs` folder, with additional metadata populated as read from the html.

Once extracted, this will also attempt to download the documents as pdf to send to the database, along with the output json. Authorisation will be requested to download from the google drive data source.

While populating the database, an initial test will first be done of any existing documents, and where identical will be skipped.
