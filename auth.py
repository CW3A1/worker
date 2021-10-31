import uuid
from secrets import token_hex
from time import time_ns

import bcrypt

import database
import environment


def generate_uuid(email):
    identifier = uuid.uuid5(uuid.NAMESPACE_DNS, email)
    return str(identifier)

def generate_hash(password):
    hashed_password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):
    validity = bcrypt.checkpw(bytes(password, 'utf-8'), hashed_password.encode('utf-8'))
    return validity

def add_user(email, password):
    if email and password and len(password) < 72:
        identifier = generate_uuid(email)
        if not database.get_row(environment.DB_TABLE_USERS, "uuid", identifier):
            hashed_password, jwt = generate_hash(password), token_hex()
            database.add_user(identifier, hashed_password, jwt)
            return True
        return {"error": "user already exists"}
    return {"error": "invalid email or password"}

def auth_user(email, password):
    if email and password:
        identifier = generate_uuid(email)
        if database.get_row(environment.DB_TABLE_USERS, "uuid", identifier):
            if check_password(password, database.user_hash(identifier)):
                resp = database.user_info("uuid", identifier)
                if resp["expiry"] <= time_ns():
                    database.update_jwt(resp["jwt"], new_token:=token_hex(), new_expiry:=time_ns()+24*60*60*1e9)
                    resp["jwt"], resp["expiry"] = new_token, int(new_expiry)
                return resp
            return {"error": "wrong password"}
        return {"error": "user does not exist"}
    return {"error": "invalid email or password"}
