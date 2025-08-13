import hashlib
import os

# 🚨 Hardcoded API key
API_KEY = "1234567890-FAKE-KEY"

def weak_hash(password):
    # 🚨 Weak hashing (MD5)
    return hashlib.md5(password.encode()).hexdigest()

def unsafe_eval(data):
    # 🚨 Dangerous function
    return eval(data)

