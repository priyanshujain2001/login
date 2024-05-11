import math, random
import hashlib
import pymongo
import os
from dotenv import load_dotenv
from gmail_services.f_send_Email import f_send_Email
load_dotenv()
mongo_url = os.getenv("mongodb_connection_string")
def mongo_db_collection(mongourl = mongo_url):
    myclient = pymongo.MongoClient(mongourl)
    mydb = myclient["Users_data"]
    mycol = mydb["Login_info2"]
    return mycol



col = mongo_db_collection()
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(email, password, hash_password=hash_password, col = col):
    hashed_password = hash_password(password)
    if col.find_one( {"email": email} ) is None:
        return "Account Not Found"
    else:
        data= col.find_one( {"email": email} )
        if data["hashed_password"] == hashed_password:
             return "VERIFY OTP"
        else:
            return "Incorrect Password"


def add_new_user(email, password, hash_password=hash_password, col = col):
    hashed_password = hash_password(password)
    if col.find_one( {"email": email} ) is None:
        new_entry = {
        "email": email,
        "password": password,
        "hashed_password": hashed_password
    }
        col.insert_one(new_entry)
        return "Account Created"
    else:
        return "This Email is already Registered"
    

    


def delete_account(email, password, hash_password=hash_password, col = col):
    hashed_password = hash_password(password)
    if col.find_one( {"email": email} ) is None:
        return "Account Not Found"
    else:
        data= col.find_one( {"email": email} )
        if data["hashed_password"] == hashed_password:
            col.delete_one({"email": email, "password": password, "hashed_password": hashed_password})
            return "Account Deleted"
        else:
            return "Incorrect Password"
        
        
def update_password(email, old_password, new_password,  hash_password=hash_password, col = col):
    hashed_password_old = hash_password(old_password)
    hashed_password_new = hash_password(new_password)
    if col.find_one( {"email": email} ) is None:
        return "Account Not Found"
    else:
        data= col.find_one( {"email": email} )
        if data["hashed_password"] == hashed_password_old:
            col.update_one({"email": email, "password": old_password, "hashed_password": hashed_password_old},{"$set":{"email": email, "password": new_password, "hashed_password": hashed_password_new}})
            return "Account Password Updated"
        else:
            return "Incorrect Password"
        
        


def otp(to):
    digits = "0123456789"
    OTP= ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    mail_body = f'OTP to enter the application is {OTP}'
    f_send_Email(to,"OTP to enter the application", mail_body)
    return OTP
        
    

