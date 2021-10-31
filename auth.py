import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

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

def generate_jwt(identifier):
    token = str(jwt.encode({"uuid": identifier, "exp": datetime.now(tz=timezone.utc) + timedelta(days=1)}, environment.AUTH_SECRET), "utf-8")
    return token

def bearer_to_uuid(bearer):
    try:
        decoded = jwt.decode(bearer[7:], environment.AUTH_SECRET)
        return decoded["uuid"]
    except:
        return False

def add_user(email, password):
    identifier = generate_uuid(email)
    if not database.get_row(environment.DB_TABLE_USERS, "uuid", identifier):
        hashed_password = generate_hash(password)
        database.add_user(identifier, hashed_password)
        return {"uuid": identifier, "jwt": generate_jwt(identifier) }
    return {"error": "user already exists"}

def auth_user(email, password):
    identifier = generate_uuid(email)
    if database.get_row(environment.DB_TABLE_USERS, "uuid", identifier):
        if check_password(password, database.user_hash(identifier)):
            return {"uuid": identifier, "jwt": generate_jwt(identifier) }
        return {"error": "wrong password"}
    return {"error": "user does not exist"}
