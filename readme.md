# FastAPI + IBM APP ID Authentication
[FastAPI](https://fastapi.tiangolo.com/) is the new kid on the block! It has OAuth integeration built in the core source code. This repo shows how to use IBM APP ID as the authenticator server.

## Run the code
1. Create a virtual environment:
   1. Using python:
   ```
   python3 -m venv venv
   ```
   2. Activate the virtual environment:
   ```
   source venv/bin/activate 
   ```
2. Install pip requirements. Note the versions at the time of this writing.
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.sample` to `.env` and fill out the attributes from the APP ID application credentials:
   1. Create [APP ID service](https://cloud.ibm.com/catalog/services/app-id). It has a generous free tier.
   2. Create new application by `adding application`. 
   3. Get the credentails and fill out the `.env` file.
4. Run the main:app application. The `--reload` option will restart the server on file change.
   `uvicorn main:app --reload`
5. Use the in built swagger docs to test the authentication [http://localhost:8000/docs](http://localhost:8000/docs)

# Run as docker container
TBD