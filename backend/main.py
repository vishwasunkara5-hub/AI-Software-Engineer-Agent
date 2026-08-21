from ai_engine.llm_service import review_code
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="AI Software Engineering Agent",
    description="AI-powered software engineering assistant",
    version="1.0.0"
)

# Allow the React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeRequest(BaseModel):
    code: str


@app.get("/")
def home():
    return {
        "message": "AI Software Engineering Agent is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
def analyze_code(request: CodeRequest):

    code = request.code.strip()

    if not code:
        return {
            "success": False,
            "message": "Please enter some code."
        }

    issues = []

    if "print(" in code:
        issues.append("Debug print statement detected.")

    if "except:" in code:
        issues.append("Avoid using a bare except statement.")

    if "eval(" in code:
        issues.append("eval() can be unsafe. Avoid it when possible.")

    if len(code.splitlines()) > 100:
        issues.append(
            "The code is quite long. Consider splitting it into functions or modules."
        )

    try:
        ai_review = review_code(code)
    except Exception as error:
        ai_review = f"AI review unavailable: {str(error)}"

    if not issues:
        issues.append("No obvious basic issues detected.")

    return {
        "success": True,
        "message": "Code analyzed successfully.",
        "issues": issues,
        "ai_review": ai_review,
        "lines": len(code.splitlines()),
        "code": code
    }