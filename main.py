from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import httpx
from starlette.config import Config
from typing import List
from pydantic import BaseModel
import base64

config = Config(".env")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def retrieve_token(username, password):

    client_id = config("CLIENT_ID")
    secret = config("SECRET")
    url = config("OAUTH_SERVER_URL") + "/token"
    grant_type = "password"

    usrPass = client_id + ":" + secret
    b64Val = base64.b64encode(usrPass.encode()).decode()
    headers = {"accept": "application/json", "Authorization": "Basic %s" % b64Val}

    data = {
        "grant_type": grant_type,
        "username": username,
        "password": password,
        "scope": "all",
    }

    response = httpx.post(url, headers=headers, data=data)

    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@app.get("/")
def read_root():
    """Unprotected root route"""
    return {"Hello": "World"}


# Get auth token
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Gets a token from IBM APP ID, given a username and a password. Depends on OAuth2PasswordRequestForm.

    Parameters
    ----------
    OAuth2PasswordRequestForm.form_data.username: str, required
    OAuth2PasswordRequestForm.form_data.password: str, required

    Returns
    -------
    token: str
    """
    return retrieve_token(form_data.username, form_data.password)


def validate(token: str = Depends(oauth2_scheme)):
    res = validate_token_IBM(
        token, config("OAUTH_SERVER_URL"), config("CLIENT_ID"), config("SECRET")
    )


def validate_token_IBM(token, authURL, clientId, clientSecret=Depends(oauth2_scheme)):
    usrPass = clientId + ":" + clientSecret
    b64Val = base64.b64encode(usrPass.encode()).decode()
    # headers = {'accept': 'application/json', 'Authorization': 'Basic %s' % b64Val}
    headers = {
        "accept": "application/json",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": "Basic %s" % b64Val,
    }
    data = {
        "client_id": clientId,
        "client_secret": clientSecret,
        "token": token,
    }
    url = authURL + "/introspect"

    response = httpx.post(url, headers=headers, data=data)

    return response.status_code == httpx.codes.OK and response.json()["active"]


class Recipe(BaseModel):
    id: int
    item: str


# Protected route
@app.get("/get_recipe", response_model=List[Recipe])
def get_recipe(valid: bool = Depends(validate)):
    return [
        Recipe.parse_obj({"id": 1, "item": "salt"}),
        Recipe.parse_obj({"id": 2, "item": "eggs"}),
        Recipe.parse_obj({"id": 3, "item": "avacado"}),
    ]