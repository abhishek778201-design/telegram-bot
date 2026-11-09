"""Mini App - FastAPI application with Telegram WebApp authentication."""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from shared.config import Config
from shared.reports import HTMLReportGenerator


# Initialize FastAPI app
app = FastAPI(
    title="Telegram Quiz Platform - Mini App",
    description="Interactive quiz player with practice and exam mode",
    version="1.0.0"
)

# Initialize report generator
report_generator = HTMLReportGenerator(theme="dark")


# Pydantic models for request/response

class QuizSession(BaseModel):
    """Session model for quiz player."""
    quiz_id: str
    user_id: str
    current_question_id: str
    score: int
    total_questions: int
    time_taken: float
    created_at: str


class QuizResult(BaseModel):
    """Quiz result model."""
    quiz_id: str
    score: int
    total_questions: int
    percentage: float
    time_taken: float
    questions: list


class WebAppResponse(BaseModel):
    """WebApp response model."""
    title: str
    description: str
    theme: str
    current_question: str
    score: int
    total_questions: int
    time_taken: float


# In-memory storage for demo (replace with actual database in production)
quiz_sessions = {}


@app.get("/", response_model=WebAppResponse)
async def index(request: Request) -> WebAppResponse:
    """Home page of the Mini App."""
    return WebAppResponse(
        title="Quiz Platform",
        description="Interactive quiz player with practice and exam mode",
        theme="dark",
        current_question="",
        score=0,
        total_questions=0,
        time_taken=0.0
    )


@app.get("/quiz/{quiz_id}", response_model=QuizSession)
async def get_quiz(quiz_id: str) -> QuizSession:
    """Get quiz details."""
    if not quiz_id:
        raise HTTPException(status_code=400, detail="Quiz ID required")
    
    # In a real implementation, query the database
    # For now, return a placeholder
    return QuizSession(
        quiz_id=quiz_id,
        user_id="user_123",
        current_question_id="q1",
        score=0,
        total_questions=10,
        time_taken=0.0,
        created_at="2026-11-09T00:00:00Z"
    )


@app.post("/quiz/start", response_model=QuizSession)
async def start_quiz(quiz_id: str) -> QuizSession:
    """Start a quiz session."""
    if not quiz_id:
        raise HTTPException(status_code=400, detail="Quiz ID required")
    
    # In a real implementation, create a new session
    session = QuizSession(
        quiz_id=quiz_id,
        user_id="user_123",
        current_question_id="q1",
        score=0,
        total_questions=10,
        time_taken=0.0,
        created_at="2026-11-09T00:00:00Z"
    )
    
    # Store session
    quiz_sessions[quiz_id] = session
    
    return session


@app.post("/quiz/next")
async def next_question(session_id: str) -> QuizSession:
    """Move to the next question."""
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID required")
    
    if session_id not in quiz_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = quiz_sessions[session_id]
    
    # Simulate advancing to next question
    session.current_question_id = f"q{int(session.current_question_id) + 1}"
    session.score = 0  # Reset score for new question
    
    return session


@app.post("/quiz/submit")
async def submit_quiz(session_id: str) -> QuizResult:
    """Submit quiz answers."""
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID required")
    
    if session_id not in quiz_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = quiz_sessions[session_id]
    
    # Simulate quiz completion
    score = 8  # Example score
    total = 10
    percentage = (score / total) * 100
    time_taken = 300.0  # 5 minutes
    
    return QuizResult(
        quiz_id=session_id,
        score=score,
        total_questions=total,
        percentage=percentage,
        time_taken=time_taken,
        questions=[]
    )


@app.get("/leaderboard")
async def get_leaderboard() -> list:
    """Get the leaderboard."""
    # In a real implementation, query the database
    return [
        {"rank": 1, "name": "User1", "score": 95},
        {"rank": 2, "name": "User2", "score": 85},
        {"rank": 3, "name": "User3", "score": 75},
    ]


@app.get("/analytics")
async def get_analytics() -> dict:
    """Get analytics data."""
    return {
        "total_quizzes": 150,
        "active_users": 320,
        "completed_quizzes": 450,
        "average_score": 78.5,
        "top_quiz_type": "standard"
    }


@app.post("/webapp/auth")
async def webapp_auth(request: Request) -> dict:
    """Handle Telegram WebApp authentication."""
    # In a real implementation, verify WebApp token
    # and return user info
    return {
        "status": "authenticated",
        "user_id": "user_123",
        "theme": "dark"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.mini_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
