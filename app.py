from pathlib import Path
import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from utils.utils import is_allowed_file, MAX_FILE_SIZE, get_unique_name
from fastapi.staticfiles import StaticFiles
from fastapi import Form

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context=context)


@app.get("/gallery/", response_class=HTMLResponse)
async def images_page(request: Request):
    print("Route /gallery/ is active!")
    image_dir = Path("images")
    image_files = [f.name for f in image_dir.iterdir() if f.is_file()]
    return templates.TemplateResponse("gallery.html", {"request": request, "images": image_files})


@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("upload.html", context=context)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    print(f"File {file.filename} recieved")

    my_file = Path(file.filename)

    if is_allowed_file(my_file):
        print("Allowed extension")
    else:
        print("Not allowed extension")
        raise HTTPException(status_code=400, detail="Extension not allowed, please upload jpg, jpeg, png, gif")

    content = await file.read(MAX_FILE_SIZE + 1)
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File is too big, 50mb max")

    new_file_name = get_unique_name(my_file)

    print(f"app.py {new_file_name}")

    image_dir = Path("images")
    image_dir.mkdir(exist_ok=True)
    save_path = image_dir / new_file_name

    save_path.write_bytes(content)

    print(f"{save_path=}")

    return PlainTextResponse(f"POST request completed {file.filename}")

@app.post("/delete-image/")
async def delete_image(image_name: str = Form(...)):
    image_path = Path("images") / image_name
    if image_path.exists():
        image_path.unlink()
    else:
        raise HTTPException(status_code=404, detail="Image not found")

    return RedirectResponse(url="/images/", status_code=303)

# uvicorn app:app --reload --host localhost --port 8001
if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
