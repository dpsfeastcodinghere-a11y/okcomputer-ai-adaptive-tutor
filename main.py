from flask import Flask, request, jsonify, send_from_directory
from adaptive_learning_engine import AdaptiveLearningEngine, EduAIModel
import os

app = Flask(__name__, static_url_path='')

# Initialize Engines
sample_db = {
    "subjects": {
        "science": {"topics": ["physics", "chemistry", "biology"]},
        "mathematics": {"topics": ["algebra", "geometry"]},
        "social_studies": {"topics": ["history", "geography", "civics", "economics"]}
    }
}
adaptive_engine = AdaptiveLearningEngine(sample_db)
# Note: EduAIModel init might simulate a delay
ai_model = EduAIModel()

@app.route('/')
def root():
    # Serve dashboard as the entry point? Or login? 
    # Current codebase seems to imply dashboard.html is main hub.
    if os.path.exists('dashboard.html'):
        return send_from_directory('.', 'dashboard.html')
    return send_from_directory('.', 'learning.html')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

@app.route('/api/generate-question', methods=['POST'])
def generate_question():
    try:
        data = request.get_json(silent=True) or {}
        topic = str(data.get('topic', 'General'))
        raw_ps = data.get('problemsSolved', data.get('problems_solved', 0))
        try:
            problems_solved = int(raw_ps) if raw_ps is not None else 0
        except Exception:
            problems_solved = 0
        
        response = ai_model.generate_ai_question(topic, problems_solved=problems_solved)
        return jsonify(response)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/solve-doubt', methods=['POST'])
def solve_doubt():
    try:
        data = request.get_json(silent=True) or {}
        doubt = str(data.get('doubt', data.get('question', '')))
        
        response = ai_model.solve_doubt(doubt)
        return jsonify({"answer": response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting EduAI Server on http://0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
