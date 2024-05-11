from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from utils import *
from fastapi import FastAPI, Form
app = FastAPI()
OTP_global = 000000
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def homepage():
    return FileResponse("static/login.html")


@app.get("/Check_Login")
def check_credentials_api(email: str, password: str, OTP_global= OTP_global):
    result = check_credentials(email, password)
    if result == "VERIFY OTP":
        OTP_global = otp(email)
    return {"message": result}

@app.get("/Verify_OTP")
def verify_otp_api(otp, OTP_global= OTP_global):
    if otp == OTP_global:
        return "Verified"
    else:
        return "OTP does not match"

@app.post("/Add_account")
def add_new_user_api(email: str = Form(...), password: str = Form(...)):
    add_new_user(email, password)
    return {"message": "New user added successfully"}

@app.post("/update_password")
def update_password_api(email: str = Form(...), old_password: str = Form(...), new_password: str = Form(...)):
    result = update_password(email, old_password, new_password)
    return {"message": result}


@app.delete("/Delete_account")
def delete_account_api(email: str = Form(...), password: str = Form(...)):
    result = delete_account(email, password)
    return {"message": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
