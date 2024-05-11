from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from utils import *
from fastapi import FastAPI, Form
app = FastAPI()
px = [0]
otp_verification_status = [False]
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def homepage():
    return FileResponse("static/login.html")


@app.get("/Check_Login")
def check_credentials_api(email: str, password: str):
    result = check_credentials(email, password)
    if result == "VERIFY OTP":
        x = otp(email)
        px[0]= x
    return {"message": result}

@app.get("/Verify_OTP")
def verify_otp_api(otp: str):
    if int(otp) == int(px[0]):
        otp_verification_status[0]= True
        return  {"message": "Verified"}
    else:
        return {"message": "OTP does not match"}

@app.post("/Add_account")
def add_new_user_api(email: str = Form(...), password: str = Form(...)):
    if otp_verification_status[0]:
        add_new_user(email, password)
        return {"message": "New user added successfully"}
    else:
        return {"message": "Verify yourself with otp"}

@app.post("/update_password")
def update_password_api(email: str = Form(...), old_password: str = Form(...), new_password: str = Form(...)):
    if otp_verification_status[0]:
        result = update_password(email, old_password, new_password)
        return {"message": result}
    else:
        return {"message": "Verify yourself with otp"}


@app.delete("/Delete_account")
def delete_account_api(email: str = Form(...), password: str = Form(...)):
    if otp_verification_status[0]:
        result = delete_account(email, password)
        return {"message": result}
    else:
        return {"message": "Verify yourself with otp"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=3000)
