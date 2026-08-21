import { useState } from "react";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const reviewCode = async () => {
    if (!code.trim()) {
      setResult({
        success: false,
        message: "Please enter some code first."
      });
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            code: code
          })
        }
      );

      if (!response.ok) {
        throw new Error(
          `Backend returned status ${response.status}`
        );
      }

      const data = await response.json();

      setResult(data);
    } catch (error) {
      console.error("Backend connection error:", error);

      setResult({
        success: false,
        message:
          "Could not connect to backend. Make sure FastAPI is running on port 8000."
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">

        <h1>AI Software Engineering Agent</h1>

        <p className="subtitle">
          Analyze your code with an AI-powered software engineering assistant.
        </p>

        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste your Python code here..."
        />

        <button
          onClick={reviewCode}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Review Code"}
        </button>

        {result && (
          <div className="result">

            <h2>Analysis Result</h2>

            <p>
              <strong>Status:</strong>{" "}
              {result.success ? "Success" : "Error"}
            </p>

            <p>
              {result.message}
            </p>

            {result.lines !== undefined && (
              <p>
                <strong>Lines:</strong> {result.lines}
              </p>
            )}

            {result.issues && (
              <div>
                <h3>Suggestions</h3>

                <ul>
                  {result.issues.map((issue, index) => (
                    <li key={index}>
                      {issue}
                    </li>
                  ))}
                </ul>
              </div>
            )}

          </div>
        )}

      </div>
    </div>
  );
}

export default App;