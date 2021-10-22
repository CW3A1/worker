import base64
import hashlib
import uuid

import bcrypt
import jwt

import environment


# Generates reproducible UUIDs for user identification
def generate_uuid(email):
    # Generate and return stringified UUID5 object
    identifier = uuid.uuid5(uuid.NAMESPACE_DNS, email)
    return str(identifier)

# (Password - > Bytes - > SHA256 - > Base64)
def encode_password(password):
    # Convert password to bytes object
    password = password.encode('utf-8')
    # Apply SHA256 and Base64 encoding to avoid max character length problems
    password = base64.b64encode(hashlib.sha256(password).digest())
    return password

# Generates hashes to store in databases
def generate_hash(password):
    # Generate and return stringified hash
    hashed_password = bcrypt.hashpw(encode_password(password), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

# Check if inputted password corresponds to stored hash
def check_password(password, hashed_password):
    # Return Boolean corresponding to validity of password
    validity = bcrypt.checkpw(encode_password(password), hashed_password.encode('utf-8'))
    return validity

# Generate JWT token for authentication
def generate_jwt(identifier):
    # Generate and return encoded JSON (stores UUID and hash so data doesn't get leaked in case of breach of database + database secret)
    encoded_jwt = jwt.encode({'uuid': identifier}, environment.auth_secret, algorithm = "HS256")
    return encoded_jwt.decode('utf-8')