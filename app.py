import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context=context)


@app.get("/images/", response_class=HTMLResponse)
async def images(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("images.html", context=context)


@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("upload.html", context=context)


# uvicorn app:app --reload --host localhost --port 8001
if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
