from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router

app = FastAPI()

origins = [
    "http://localhost:8089",    # Svelte Frontend 서버 주소 업데이트 해야 정상 작동함
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/build", StaticFiles(directory="Frontend_Audit/public/build"))

@app.get("/")
def index():
    return FileResponse("Frontend_Audit/public/index.html")