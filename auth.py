"""Authenticate module for API"""

import base64
import hashlib
import uuid

import bcrypt
import jwt

import environment


def generate_uuid(email):
    """Generates reproducible UUIDs for user identification"""
    # Generate and return stringified UUID5 object
    identifier = uuid.uuid5(uuid.NAMESPACE_DNS, email)
    return str(identifier)

def encode_password(password):
    """(Password - > Bytes - > SHA256 - > Base64)"""
    # Convert password to bytes object
    password = password.encode('utf-8')
    # Apply SHA256 and Base64 encoding to avoid max character length problems
    password = base64.b64encode(hashlib.sha256(password).digest())
    return password

def generate_hash(password):
    """Generates hashes to store in databases"""
    # Generate and return stringified hash
    hashed_password = bcrypt.hashpw(encode_password(password), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):
    """Check if inputted password corresponds to stored hash"""
    # Return Boolean corresponding to validity of password
    validity = bcrypt.checkpw(encode_password(password), hashed_password.encode('utf-8'))
    return validity

def generate_jwt(identifier):
    """Generate JWT token for authentication"""
    # Generate and return encoded JSON based upon UUID
    encoded_jwt = jwt.encode({'uuid': identifier}, environment.AUTH_SECRET, algorithm="HS256")
    return encoded_jwt.decode('utf-8')
