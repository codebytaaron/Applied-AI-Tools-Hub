from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from grader import grade_work, GradeRequest

app = FastAPI(title="Honest Grader AI")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/grade", response_class=HTMLResponse)
async def grade(
    request: Request,
    assignment_type: str = Form(...),
    grade_level: str = Form(...),
    rubric: str = Form(...),
    student_work: str = Form(...),
    strictness: str = Form("medium"),
):
    req = GradeRequest(
        assignment_type=assignment_type,
        grade_level=grade_level,
        rubric=rubric,
        student_work=student_work,
        strictness=strictness,
    )

    result = await grade_work(req)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "result": result,
            "req": req,
        },
    )
