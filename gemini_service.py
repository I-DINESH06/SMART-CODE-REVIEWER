import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def validate_review(review, original_code):
    """
    Validate and normalize the AI response.
    """

    # ---------- Score ----------
    try:
        score = float(review.get("score", 0))
    except Exception:
        score = 0.0

    score = max(0.0, min(10.0, score))
    review["score"] = round(score, 1)

    # ---------- Status ----------
    if not review.get("status"):
        review["status"] = "Review Completed"

    # ---------- Problems ----------
    problems = review.get("problems", [])

    if not isinstance(problems, list):
        problems = []

    if len(problems) == 0:
        problems = ["No major issues found."]

    review["problems"] = problems

    # ---------- Suggestions ----------
    suggestions = review.get("suggestions", [])

    if not isinstance(suggestions, list):
        suggestions = []

    if len(suggestions) == 0:
        suggestions = ["No improvements suggested."]

    review["suggestions"] = suggestions[:5]

    # ---------- Complexity ----------
    if not review.get("time_complexity"):
        review["time_complexity"] = "Not Available"

    if not review.get("space_complexity"):
        review["space_complexity"] = "Not Available"

    # ---------- Optimized Code ----------
    if not review.get("optimized_code"):
        review["optimized_code"] = original_code

    return review


def review_code(language, code):

    prompt = f"""
You are a Senior Software Engineer performing a professional code review.

IMPORTANT RULES

1. Return ONLY valid JSON.
2. Do NOT use markdown.
3. Do NOT use triple backticks.
4. Do NOT explain outside JSON.

Evaluation Criteria

Correctness: 40%
Readability: 20%
Maintainability: 15%
Performance: 15%
Security: 10%

Scoring Rules

- Score must be between 0 and 10.
- Never return a score greater than 10.
- Runtime errors should usually score below 5.
- Good production-quality code should score between 8 and 10.

Problems

- If there are no problems,
return:

["No major issues found."]

Suggestions

- Maximum 5 suggestions.
- Keep them short.

Complexity

Return only Big-O notation.

Examples:

"O(n)"
"O(log n)"
"O(1)"

Optimized Code

- Preserve functionality.
- Improve readability.
- Don't rewrite the whole program unless necessary.

Return EXACTLY this JSON format:

{{
    "score": 0,
    "status": "",
    "problems": [],
    "suggestions": [],
    "time_complexity": "",
    "space_complexity": "",
    "optimized_code": ""
}}

Programming Language:
{language}

Code:

{code}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        review = json.loads(text)

        return validate_review(review, code)

    except Exception as e:

        return {
            "score": 0.0,
            "status": "AI Review Failed",
            "problems": [
                str(e)
            ],
            "suggestions": [
                "Please try again."
            ],
            "time_complexity": "Not Available",
            "space_complexity": "Not Available",
            "optimized_code": code
        }