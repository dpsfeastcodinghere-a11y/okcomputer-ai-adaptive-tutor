from flask import Flask, request, jsonify
import re
import random
import os

app = Flask(__name__)

# ============================================
# LIGHTWEIGHT OPEN-SOURCE AI CONFIGURATION
# ============================================
# Using Hugging Face Inference API with FLAN-T5 Small
# - Lightweight (77M parameters)
# - Fast inference
# - Free tier available
# - Open source (Apache 2.0 license)
#
# Get your FREE API key: https://huggingface.co/settings/tokens
# Set as environment variable: HUGGINGFACE_API_KEY

HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

# Alternative lightweight models:
# - "google/flan-t5-base" (250M params - better quality)
# - "distilgpt2" (82M params - conversational)
# - "facebook/opt-125m" (125M params - very fast)
# - "EleutherAI/gpt-neo-125M" (125M params - open source GPT)

STRICT_SCIENCE_UNITS = True

def call_ai_model(prompt, context=""):
    """
    Calls Hugging Face API with lightweight FLAN-T5 model.
    Falls back to template responses if API key not set.
    """
    
    # If no API key, use fallback
    if not HUGGINGFACE_API_KEY:
        print("⚠️ No Hugging Face API key found. Using fallback responses.")
        print("💡 Get free API key at: https://huggingface.co/settings/tokens")
        return generate_fallback_response(prompt, context)
    
    try:
        import requests
        
        # Prepare prompt based on context
        if "doubt" in context.lower():
            full_prompt = f"""Answer this student's question clearly and educationally:

Question: {prompt}

Provide a detailed explanation suitable for a school student (Classes 6-10)."""
        
        elif "validate" in context.lower():
            full_prompt = f"Explain this concept briefly: {prompt}"
        
        elif "generate_question" in context.lower():
            full_prompt = f"Generate an educational question about: {prompt}"
        
        else:
            full_prompt = prompt
        
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_length": 250,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True
            }
        }
        
        response = requests.post(
            HUGGINGFACE_API_URL, 
            headers=headers, 
            json=payload, 
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                if generated_text:
                    return generated_text
            elif isinstance(result, dict):
                generated_text = result.get('generated_text', '')
                if generated_text:
                    return generated_text
            
            # If no valid response, use fallback
            return generate_fallback_response(prompt, context)
        
        elif response.status_code == 503:
            # Model is loading
            return "The AI model is warming up. Please try again in a moment."
        
        else:
            print(f"Hugging Face API Error: {response.status_code} - {response.text}")
            return generate_fallback_response(prompt, context)
            
    except Exception as e:
        print(f"AI Model Error: {e}")
        return generate_fallback_response(prompt, context)

def generate_fallback_response(prompt, context=""):
    """
    Fallback responses when AI is not available.
    Ensures app works without API key (for testing/demo).
    """
    if "doubt" in context.lower():
        return (
            f"📚 Regarding your query about '{prompt}':\n\n"
            "This is an important concept in your curriculum. "
            "To understand this better, let's break it down:\n\n"
            "1. **Foundation**: Start with the basic principles\n"
            "2. **Application**: See how it applies in real scenarios\n"
            "3. **Practice**: Solve related problems to strengthen understanding\n\n"
            "💡 Tip: Consult your textbook chapter on this topic for detailed explanations. "
            "You can also try rephrasing your question for better clarity!"
        )
    
    elif "validate" in context.lower():
        return (
            f"Good effort! {prompt} is an interesting concept. "
            "Keep practicing to master it!"
        )
    
    return "✅ Analysis complete. Keep learning!"

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
             return False, f"Missing units! Expected units like '{expected_unit}'."
        
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
        response["message"] = "Correct! 🎉"
        response["explanation"] = call_ai_model(
            f"Explain why '{correct_answer}' is the correct answer", 
            context="validate"
        )
    else:
        # Fallback for numerical equivalency (e.g. 5.0 vs 5)
        try:
            if float(user_answer.split()[0]) == float(correct_answer.split()[0]):
                 # If numbers match but string didn't (and units passed), it might be formatting
                 response["isCorrect"] = True
                 response["message"] = "Correct (matches value)! ✓"
                 return jsonify(response)
        except:
            pass
            
        response["isCorrect"] = False
        response["message"] = "Not quite right. Try again!"
        response["explanation"] = (
            f"The correct answer is: **{correct_answer}**\n\n" + 
            call_ai_model(
                f"Explain the concept: {correct_answer}", 
                context="validate"
            )
        )

    return jsonify(response)

@app.route('/api/solve-doubt', methods=['POST'])
def solve_doubt():
    data = request.json
    doubt = data.get('doubt', '')
    
    if not doubt:
        return jsonify({
            "answer": "Please enter your question!"
        })
    
    answer = call_ai_model(doubt, context="doubt")
    
    return jsonify({
        "answer": answer
    })

@app.route('/api/generate-question', methods=['POST'])
def generate_question():
    """
    Generate AI-powered questions for a given topic.
    """
    data = request.json
    topic = data.get('topic', '')
    difficulty = data.get('difficulty', 'medium')
    subject = data.get('subject', '')
    
    if not topic:
        return jsonify({
            "error": "Topic is required"
        }), 400
    
    prompt = f"Generate a {difficulty} level {subject} question about {topic} for school students (Classes 6-10)."
    
    question_text = call_ai_model(prompt, context="generate_question")
    
    return jsonify({
        "question": question_text,
        "topic": topic,
        "difficulty": difficulty
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return jsonify({
        "status": "healthy",
        "ai_enabled": bool(HUGGINGFACE_API_KEY),
        "model": "google/flan-t5-small",
        "message": "EduAI API is running!"
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
