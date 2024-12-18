from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from database import Database
from pydantic import BaseModel

app = FastAPI()
db = Database()

# 設定靜態檔案和模板
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TempData(BaseModel):
    temp: str
    humi: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    records = db.get_all_records()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "records": records}
    )

@app.post("/api/temp")
async def add_temp_data(data: TempData):
    return db.insert_temp_log(data.temp, data.humi)

@app.get("/api/temp")
async def get_temp_data():
    return db.get_all_records() 