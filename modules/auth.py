import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Request

from . import environment


def generate_uuid(email):
    identifier = uuid.uuid5(uuid.NAMESPACE_DNS, email)
    return str(identifier)

def generate_hash(password):
    hashed_password = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def check_password(password, hashed_password):
    validity = bcrypt.checkpw(bytes(password, "utf-8"), hashed_password.encode("utf-8"))
    return validity

def generate_jwt(identifier):
    token = jwt.encode({"uuid": identifier, "exp": datetime.now(tz=timezone.utc) + timedelta(days=1)}, environment.AUTH_SECRET)
    return str(token, "utf-8")

def header_to_identifier(req: Request):
    try:
        token = req.headers["Authorization"]
        decoded = jwt.decode(token[7:], environment.AUTH_SECRET)
        identifier = decoded["uuid"]
        return identifier
    except:
        return ""
