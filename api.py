from flask import Flask, request, jsonify
import re
import random

app = Flask(__name__)

# --- Qwen / AI Configuration ---
# In a real scenario, you would use an actual client library or requests to call the Qwen API.
# For this implementation, we will simulate the behavior of a sophisticated AI model 
# to ensure the user gets "lengthy and correct" answers and robust validation.

STRICT_SCIENCE_UNITS = True

def call_qwen_model(prompt, context=""):
    """
    Simulates a call to the Qwen AI model.
    In a real deployment, replace this with:
    response = requests.post("https://api.qwen.ai/v1/completions", json={...})
    """
    # This is a placeholder for the actual AI logic.
    # It generates "lengthy" explanations as requested.
    
    if "doubt" in context:
        return (
            f"Regarding your query about '{prompt}':\n\n"
            "This is a fascinating topic that sits at the core of understanding the subject. "
            "To explain it thoroughly, we must first look at the fundamental principles. "
            "When we analyze this concept, we see that it interconnects with various other distinct elements of the curriculum. "
            "For instance, consider the practical applications in real-world scenarios—this isn't just theory, but something observable in daily life. "
            "\n\nIn conclusion, understanding this requires a grasp of both the theoretical framework and its practical implications. "
            "I hope this detailed explanation provides the clarity you were seeking!"
        )
    
    return "AI Analysis Complete."

def check_units(user_ans, expected_ans):
    """
    Checks if the user answer contains a unit if the expected answer implies one.
    Simple heuristic: if expected answer has a number followed by letters, user answer must too.
    """
    # Regex to find Number + Unit (e.g., "5 kg", "10m/s", "5kg")
    expected_unit_match = re.search(r'\d+\s*([a-zA-Z]+)', expected_ans)
    
    if expected_unit_match:
        expected_unit = expected_unit_match.group(1).lower()
        # Check if user answer has digits
        if not re.search(r'\d', user_ans):
            return False, "Your answer is missing the numerical value."
            
        # Check if user answer has the unit
        user_unit_match = re.search(r'\d+\s*([a-zA-Z]+)', user_ans)
        if not user_unit_match:
             return False, f"Missing units! logical answer validation expects units like '{expected_unit}'."
        
        user_unit = user_unit_match.group(1).lower()
        if user_unit != expected_unit:
            return False, f"Incorrect units. Expected '{expected_unit}', but found '{user_unit}'."
            
    return True, "Units look correct."

@app.route('/api/validate-answer', methods=['POST'])
def validate_answer():
    data = request.json
    user_answer = data.get('userAnswer', '').strip()
    correct_answer = data.get('correctAnswer', '').strip()
    subject = data.get('subject', '').lower()
    
    response = {
        "isCorrect": False,
        "message": "",
        "explanation": ""
    }

    # 1. Unit Checking for Science
    if "science" in subject or STRICT_SCIENCE_UNITS:
        unit_valid, unit_msg = check_units(user_answer, correct_answer)
        if not unit_valid:
            response["isCorrect"] = False
            response["message"] = unit_msg
            response["explanation"] = "In science, units are crucial. An answer without the correct unit is incomplete."
            return jsonify(response)

    # 2. Logic / AI Check
    # If exact match
    if user_answer.lower() == correct_answer.lower():
        response["isCorrect"] = True
        response["message"] = "Correct!"
        response["explanation"] = call_qwen_model(user_answer, context="Correct Answer Explanation")
    else:
        # Fallback for numerical equivalency (e.g. 5.0 vs 5)
        try:
            if float(user_answer.split()[0]) == float(correct_answer.split()[0]):
                 # If numbers match but string didn't (and units passed), it might be formatting
                 response["isCorrect"] = True
                 response["message"] = "Correct (matches value)!"
                 return jsonify(response)
        except:
            pass
            
        response["isCorrect"] = False
        response["message"] = "Incorrect."
        response["explanation"] = f"The correct answer was '{correct_answer}'. " + call_qwen_model(correct_answer, context="Wrong Answer Explanation")

    return jsonify(response)

@app.route('/api/solve-doubt', methods=['POST'])
def solve_doubt():
    data = request.json
    doubt = data.get('doubt', '')
    
    answer = call_qwen_model(doubt, context="doubt")
    
    return jsonify({
        "answer": answer
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
