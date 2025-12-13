from adaptive_learning_engine import AdaptiveLearningEngine
import json
import random

def simulate_student_activity(engine, student_name, profile_type, num_problems=15):
    """
    Simulates student activity based on a profile type.
    profile_type: 'good' or 'struggling'
    """
    print(f"\n--- Simulating activity for {student_name} ({profile_type} progress) ---")
    
    # Initialize profile
    engine.create_student_profile(student_name)
    
    # Simulation parameters
    if profile_type == 'good':
        accuracy_prob = 0.9
        min_time, max_time = 15, 45
        hint_prob = 0.1
    else: # struggling
        accuracy_prob = 0.4
        min_time, max_time = 40, 150
        hint_prob = 0.7

    subjects = ["mathematics", "science"]
    
    for i in range(num_problems):
        # 1. Select a problem (Engine decides difficulty)
        subject = random.choice(subjects)
        problem = engine.select_next_problem(student_name, subject)
        
        # 2. Simulate User Behavior
        is_correct = random.random() < accuracy_prob
        
        # If struggling and difficulty is high, accuracy drops further
        if profile_type == 'struggling' and problem.difficulty > 2:
            is_correct = random.random() < (accuracy_prob - 0.2)

        time_taken = random.uniform(min_time, max_time)
        used_hint = random.random() < hint_prob
        
        # If hint used, maybe higher chance of correctness? (Optional logic, keeping simple)
        if used_hint and not is_correct: 
             # Slight boost if hint used but still failed?
             if random.random() < 0.3: is_correct = True

        # 3. Process Response
        result = engine.process_student_response(
            student_name, 
            problem.id, 
            is_correct, 
            time_taken, 
            used_hint
        )
        
        # print(f"  Q{i+1} [Diff:{problem.difficulty}]: {'✅' if is_correct else '❌'} (Time: {int(time_taken)}s, Hint: {used_hint}) -> New Confidence: {result['updated_metrics']['confidence']:.2f}")

def generate_report(engine, student_name):
    analytics = engine.get_learning_analytics(student_name)
    
    report = f"""
################################################################
# DETAILED STUDENT REPORT: {student_name.upper()}
################################################################

## 1. PERFORMANCE SUMMARY
----------------------------------------------------------------
- Total Problems Solved : {analytics['overall_performance']['total_attempts']}
- Overall Accuracy      : {analytics['overall_performance']['accuracy']*100:.1f}%
- Average Response Time : {analytics['overall_performance']['average_response_time']:.1f} seconds
- AI Confidence Score   : {analytics['overall_performance']['confidence_level']:.2f} / 1.0
- Current Streak        : {analytics['overall_performance']['streak_count']}

## 2. SKILL ANALYSIS
----------------------------------------------------------------
"""
    
    report += "### Topic Mastery:\n"
    for topic, score in analytics['topic_mastery'].items():
        status = "🟢 Mastered" if score > 0.8 else ("🟡 Learning" if score > 0.5 else "🔴 Needs Attention")
        report += f"- {topic:<20} : {score*100:.0f}%  {status}\n"

    report += "\n### Difficulty Performance:\n"
    for diff, score in analytics['difficulty_performance'].items():
        report += f"- Level {diff:<14} : {score*100:.0f}%\n"

    report += """
## 3. IDENTIFIED WEAKNESSES & AI DIAGNOSIS
----------------------------------------------------------------
"""
    weaknesses = analytics['weaknesses']
    if not weaknesses:
        report += "No significant weaknesses detected.\n"
    else:
        for key, w in weaknesses.items():
            report += f"- [{key.replace('_', ' ').title()}]: {w['recommendation']}\n"

    report += """
## 4. AI RECOMMENDATIONS & CURRICULUM PATH
----------------------------------------------------------------
"""
    for rec in analytics['recommendations']:
        report += f"• {rec}\n"
        
    return report

if __name__ == "__main__":
    # Initialize Engine
    sample_db = {
        "subjects": {
            "mathematics": {"topics": ["algebra", "geometry", "calculus"]},
            "science": {"topics": ["physics", "chemistry", "biology"]}
        }
    }
    engine = AdaptiveLearningEngine(sample_db)
    
    # Run Simulations
    simulate_student_activity(engine, "Ram", "good", num_problems=20)
    simulate_student_activity(engine, "Rahul", "struggling", num_problems=20)
    
    # Generate and Print Reports
    ram_report = generate_report(engine, "Ram")
    rahul_report = generate_report(engine, "Rahul")
    
    print("\n" + "="*60 + "\n")
    print(ram_report)
    print("\n" + "="*60 + "\n")
    print(rahul_report)
