from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Literal, Optional

from src.hashtag_ai import generate_hashtags_ai
from src.hashtag_rules import generate_hashtags_rules

app = FastAPI(title="Hashtag Gen AI")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

Platform = Literal["instagram", "tiktok", "youtube", "x", "linkedin"]

class HashtagRequest(BaseModel):
    platform: Platform = "instagram"
    caption: str = Field(..., min_length=1, max_length=2000)
    context: Optional[str] = Field(default="", max_length=2000)
    niche: Optional[str] = Field(default="", max_length=200)
    hashtag_count: int = Field(default=18, ge=5, le=30)
    include_branded: bool = True
    brand_tag: Optional[str] = Field(default="", max_length=40)  # like "zylos" -> #zylos

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/generate")
def generate(req: HashtagRequest):
    # Try AI first, fallback if not available or fails
    try:
        tags = generate_hashtags_ai(
            platform=req.platform,
            caption=req.caption,
            context=req.context or "",
            niche=req.niche or "",
            hashtag_count=req.hashtag_count,
            include_branded=req.include_branded,
            brand_tag=req.brand_tag or "",
        )
        source = "ai"
    except Exception:
        tags = generate_hashtags_rules(
            platform=req.platform,
            caption=req.caption,
            context=req.context or "",
            niche=req.niche or "",
            hashtag_count=req.hashtag_count,
            include_branded=req.include_branded,
            brand_tag=req.brand_tag or "",
        )
        source = "rules"

    return JSONResponse({"hashtags": tags, "source": source})
