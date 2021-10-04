from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, participants, players, tournaments


app = FastAPI(debug=True, title="Tournaments API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth.router)
v1_router.include_router(players.router)
v1_router.include_router(tournaments.router)
v1_router.include_router(participants.router)
app.include_router(v1_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", reload=True)
