#!/usr/bin/env python3
"""
Adaptive Learning Engine for Multi-Subject Educational Platform
Implements intelligent tutoring system with real-time difficulty adjustment
"""

import json
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class DifficultyLevel(Enum):
    VERY_EASY = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4


class Subject(Enum):
    MATHEMATICS = "mathematics"
    SCIENCE = "science"
    ENGLISH = "english"
    SOCIAL_STUDIES = "social_studies"
    HINDI = "hindi"
    ENGLISH = "english"


class LearningPath(Enum):
    REMEDIAL = "remedial"
    STANDARD = "standard"
    ACCELERATED = "accelerated"


@dataclass
class StudentPerformance:
    """Tracks student performance metrics"""
    total_attempts: int = 0
    correct_attempts: int = 0
    average_time: float = 0.0
    hint_usage_rate: float = 0.0
    confidence_level: float = 0.5
    streak_count: int = 0
    last_attempt_time: Optional[datetime] = None
    topic_mastery: Dict[str, float] = field(default_factory=dict)
    difficulty_performance: Dict[int, float] = field(default_factory=dict)


@dataclass
class Problem:
    """Represents a learning problem/question"""
    id: str
    subject: str
    topic: str
    difficulty: int
    question: str
    answer: str
    solution: str
    hint: str
    grade_level: int
    prerequisites: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)


@dataclass
class StudentSession:
    """Tracks current learning session"""
    student_id: str
    subject: str
    current_topic: str
    current_difficulty: int
    problems_attempted: List[str] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    performance_history: List[bool] = field(default_factory=list)


class AdaptiveLearningEngine:
    """
    Core adaptive learning engine that personalizes education based on student performance
    """
    
    def __init__(self, problems_database: Dict):
        self.problems_db = problems_database
        self.student_profiles: Dict[str, StudentPerformance] = {}
        self.active_sessions: Dict[str, StudentSession] = {}
        
        # Configuration parameters
        self.mastery_threshold = 0.75
        self.difficulty_adaptation_rate = 0.2
        self.hint_penalty = 0.1
        self.time_weight = 0.3
        self.accuracy_weight = 0.5
        self.consistency_weight = 0.2
        
    def create_student_profile(self, student_id: str) -> StudentPerformance:
        """Initialize new student profile with diagnostic assessment"""
        profile = StudentPerformance()
        self.student_profiles[student_id] = profile
        return profile
    
    def diagnose_weaknesses(self, student_id: str, subject: str) -> Dict[str, Any]:
        """
        Comprehensive diagnostic assessment to identify student weaknesses
        Returns detailed weakness analysis with recommendations
        """
        if student_id not in self.student_profiles:
            self.create_student_profile(student_id)
        
        profile = self.student_profiles[student_id]
        weaknesses = {}
        
        # Analyze performance patterns
        if profile.total_attempts > 0:
            overall_accuracy = profile.correct_attempts / profile.total_attempts
            
            # Check for low accuracy in specific difficulties
            for difficulty, performance in profile.difficulty_performance.items():
                if performance < self.mastery_threshold:
                    weaknesses[f"difficulty_{difficulty}"] = {
                        "type": "difficulty_struggle",
                        "level": difficulty,
                        "accuracy": performance,
                        "recommendation": self._get_difficulty_recommendation(difficulty, performance)
                    }
            
            # Check for slow problem-solving
            if profile.average_time > 120:  # 2 minutes threshold
                weaknesses["slow_problem_solving"] = {
                    "type": "speed_issue",
                    "average_time": profile.average_time,
                    "recommendation": "Practice basic concepts to improve speed"
                }
            
            # Check for high hint dependency
            if profile.hint_usage_rate > 0.5:
                weaknesses["hint_dependency"] = {
                    "type": "dependency_issue",
                    "hint_rate": profile.hint_usage_rate,
                    "recommendation": "Reduce hint usage to build independence"
                }
            
            # Analyze topic-specific weaknesses
            for topic, mastery in profile.topic_mastery.items():
                if mastery < self.mastery_threshold:
                    weaknesses[topic] = {
                        "type": "topic_weakness",
                        "mastery_level": mastery,
                        "recommendation": f"Focus on {topic} fundamentals"
                    }
        
        # If no clear weaknesses identified, provide general assessment
        if not weaknesses:
            weaknesses["general"] = {
                "type": "general_assessment",
                "recommendation": "Continue with balanced practice across all topics"
            }
        
        return weaknesses
    
    def _get_difficulty_recommendation(self, difficulty: int, performance: float) -> str:
        """Generate specific recommendations based on difficulty performance"""
        if difficulty == 1 and performance < 0.8:
            return "Review fundamental concepts and basic operations"
        elif difficulty == 2 and performance < 0.75:
            return "Practice more word problems and applications"
        elif difficulty == 3 and performance < 0.7:
            return "Work on multi-step problem solving strategies"
        elif difficulty == 4 and performance < 0.65:
            return "Break down complex problems into smaller steps"
        return "Continue practicing at current level"
    
    def recommend_learning_path(self, student_id: str, subject: str) -> LearningPath:
        """Recommend optimal learning path based on diagnostic results"""
        weaknesses = self.diagnose_weaknesses(student_id, subject)
        profile = self.student_profiles[student_id]
        
        # Decision logic for learning path selection
        if profile.total_attempts < 10:
            return LearningPath.STANDARD  # Default for new students
        
        # Count significant weaknesses
        significant_weaknesses = sum(1 for weakness in weaknesses.values() 
                                   if weakness.get("accuracy", 1) < 0.6 or 
                                   weakness.get("type") in ["speed_issue", "dependency_issue"])
        
        if significant_weaknesses >= 3:
            return LearningPath.REMEDIAL
        elif significant_weaknesses == 0 and profile.confidence_level > 0.8:
            return LearningPath.ACCELERATED
        else:
            return LearningPath.STANDARD
    
    def select_next_problem(self, student_id: str, subject: str, topic: Optional[str] = None) -> Problem:
        """
        Intelligently select the next problem based on student performance
        """
        profile = self.student_profiles.get(student_id)
        if not profile:
            profile = self.create_student_profile(student_id)
        
        # Determine optimal difficulty level
        target_difficulty = self._calculate_optimal_difficulty(profile)
        
        # Filter problems by criteria
        available_problems = self._get_available_problems(subject, topic, target_difficulty)
        
        if not available_problems:
            # Fallback to any available problem
            available_problems = self._get_all_problems(subject)
        
        # Select problem using intelligent algorithm
        selected_problem = self._intelligent_problem_selection(
            available_problems, profile, target_difficulty
        )
        
        return selected_problem
    
    def _calculate_optimal_difficulty(self, profile: StudentPerformance) -> int:
        """Calculate the optimal difficulty level for next problem"""
        if profile.total_attempts == 0:
            return 2  # Start with easy problems
        
        # Base calculation on recent performance
        recent_accuracy = self._calculate_recent_accuracy(profile)
        current_difficulty = profile.current_difficulty if hasattr(profile, 'current_difficulty') else 2
        
        # Adjust difficulty based on performance
        if recent_accuracy > 0.8:
            return min(4, current_difficulty + 1)  # Increase difficulty
        elif recent_accuracy < 0.6:
            return max(1, current_difficulty - 1)  # Decrease difficulty
        else:
            return current_difficulty  # Maintain current level
    
    def _calculate_recent_accuracy(self, profile: StudentPerformance, window: int = 5) -> float:
        """Calculate accuracy over recent attempts"""
        if profile.total_attempts == 0:
            return 0.5
        
        # For demo purposes, use overall accuracy
        return profile.correct_attempts / profile.total_attempts
    
    def _get_available_problems(self, subject: str, topic: Optional[str], difficulty: int) -> List[Problem]:
        """Get problems matching the criteria"""
        problems = []
        
        # Access problems from database
        subject_data = self.problems_db.get("subjects", {}).get(subject, {})
        
        # For now, return sample problems based on difficulty
        sample_problems = {
            "mathematics": [
                Problem("m1", "mathematics", "algebra", 2, "Solve: 2x + 5 = 13", "x = 4", 
                       "Subtract 5 from both sides: 2x = 8, then divide by 2: x = 4",
                       "Try to isolate x by performing the same operation on both sides", 7),
                Problem("m2", "mathematics", "geometry", 3, "Find the area of a rectangle with length 8cm and width 5cm", 
                       "40 cm²", "Area = length × width = 8 × 5 = 40 cm²",
                       "Remember the formula: Area = length × width", 7),
                Problem("m3", "mathematics", "fractions", 2, "Simplify: 12/16", "3/4", 
                       "Divide numerator and denominator by 4: 12÷4 / 16÷4 = 3/4",
                       "Find the greatest common divisor of 12 and 16", 6)
            ],
            "science": [
                Problem("s1", "science", "physics", 2, "What is the boiling point of water?", "100°C", 
                       "Water boils at 100°C at standard atmospheric pressure",
                       "Think about the temperature at which water changes to steam", 7),
                Problem("s2", "science", "chemistry", 3, "What is the chemical formula for water?", "H₂O", 
                       "Water consists of 2 hydrogen atoms and 1 oxygen atom",
                       "Remember that water has hydrogen and oxygen", 8)
            ],
            "social_studies": [
                Problem("sst1", "social_studies", "history", 2, "Who was the first Prime Minister of India?", "Jawaharlal Nehru",
                       "Jawaharlal Nehru was the first Prime Minister of independent India.",
                       "He was often called Chacha Nehru.", 6),
                Problem("sst2", "social_studies", "geography", 2, "Which is the largest continent in the world?", "Asia",
                       "Asia is the largest continent by both land area and population.",
                       "India is part of this continent.", 6),
                Problem("sst3", "social_studies", "civics", 3, "What is the minimum age for voting in India?", "18 years",
                       "The voting age in India is 18 years and above.",
                       "It was lowered from 21 to 18 in 1988.", 9),
                 Problem("sst4", "social_studies", "economics", 3, "Which sector is known as the service sector?", "Tertiary Sector",
                       "The Tertiary sector provides services rather than producing goods.",
                       "Banking, teaching, and transport belong to this sector.", 10)
            ]
        }
        
        return sample_problems.get(subject, [])
    
    def _get_all_problems(self, subject: str) -> List[Problem]:
        """Get all problems for a subject"""
        return self._get_available_problems(subject, None, 2)
    
    def _intelligent_problem_selection(self, problems: List[Problem], profile: StudentPerformance, 
                                     target_difficulty: int) -> Problem:
        """Intelligently select the best problem from available options"""
        if not problems:
            # Return a default problem
            return Problem("default", "mathematics", "general", 2, "What is 2 + 2?", "4", 
                          "2 + 2 = 4", "Count on your fingers", 1)
        
        # Score each problem based on various factors
        scored_problems = []
        for problem in problems:
            score = self._score_problem(problem, profile, target_difficulty)
            scored_problems.append((score, problem))
        
        # Select the highest scoring problem
        scored_problems.sort(key=lambda x: x[0], reverse=True)
        return scored_problems[0][1]
    
    def _score_problem(self, problem: Problem, profile: StudentPerformance, target_difficulty: int) -> float:
        """Score a problem based on its suitability for the student"""
        score = 0.0
        
        # Difficulty match (higher score for closer match to target)
        difficulty_match = 1.0 / (1.0 + abs(problem.difficulty - target_difficulty))
        score += difficulty_match * 0.4
        
        # Topic mastery (lower score for mastered topics)
        topic_mastery = profile.topic_mastery.get(problem.topic, 0.5)
        if topic_mastery < self.mastery_threshold:
            score += (1.0 - topic_mastery) * 0.3
        
        # Diversity (higher score for less recent topics)
        if problem.topic not in profile.recent_topics if hasattr(profile, 'recent_topics') else True:
            score += 0.2
        
        # Learning objectives alignment
        if hasattr(profile, 'learning_goals') and any(obj in problem.learning_objectives 
                                                      for obj in profile.learning_goals):
            score += 0.1
        
        return score
    
    def process_student_response(self, student_id: str, problem_id: str, is_correct: bool, 
                               response_time: float, used_hint: bool = False) -> Dict[str, Any]:
        """
        Process student response and update learning model
        """
        profile = self.student_profiles.get(student_id)
        if not profile:
            profile = self.create_student_profile(student_id)
        
        # Update performance metrics
        profile.total_attempts += 1
        if is_correct:
            profile.correct_attempts += 1
            profile.streak_count += 1
        else:
            profile.streak_count = 0
        
        # Update average response time
        if profile.average_time == 0:
            profile.average_time = response_time
        else:
            profile.average_time = (profile.average_time * 0.7) + (response_time * 0.3)
        
        # Update hint usage
        if used_hint:
            total_hints = profile.hint_usage_rate * (profile.total_attempts - 1) + 1
            profile.hint_usage_rate = total_hints / profile.total_attempts
        
        # Update confidence level
        accuracy = profile.correct_attempts / profile.total_attempts if profile.total_attempts > 0 else 0
        time_factor = min(1.0, 60 / response_time) if response_time > 0 else 1.0
        hint_factor = 1.0 - (profile.hint_usage_rate * self.hint_penalty)
        
        profile.confidence_level = (accuracy * self.accuracy_weight + 
                                  time_factor * self.time_weight + 
                                  hint_factor * self.consistency_weight)
        
        # Update topic mastery (simplified)
        # In real implementation, this would be more sophisticated
        problem = self._get_problem_by_id(problem_id)
        if problem and problem.topic in profile.topic_mastery:
            current_mastery = profile.topic_mastery[problem.topic]
            if is_correct:
                new_mastery = min(1.0, current_mastery + 0.1)
            else:
                new_mastery = max(0.0, current_mastery - 0.05)
            profile.topic_mastery[problem.topic] = new_mastery
        
        # Generate feedback and next steps
        feedback = self._generate_feedback(is_correct, response_time, used_hint, profile)
        
        return {
            "is_correct": is_correct,
            "feedback": feedback,
            "updated_metrics": {
                "accuracy": accuracy,
                "confidence": profile.confidence_level,
                "streak": profile.streak_count,
                "average_time": profile.average_time
            },
            "next_recommendation": self._get_next_recommendation(profile)
        }
    
    def _get_problem_by_id(self, problem_id: str) -> Optional[Problem]:
        """Retrieve problem by ID (simplified implementation)"""
        # In real implementation, this would query the database
        return None
    
    def _generate_feedback(self, is_correct: bool, response_time: float, 
                          used_hint: bool, profile: StudentPerformance) -> str:
        """Generate personalized feedback based on performance"""
        if is_correct:
            if response_time < 30:
                return "Excellent! Quick and accurate! 🎉"
            elif response_time < 60:
                return "Great job! Correct answer! 👍"
            else:
                return "Good work! Try to solve faster next time! 💪"
        else:
            if used_hint:
                return "Let's practice more! Review the hint and try again. 📚"
            else:
                return "Not quite right. Would you like a hint? 🤔"
    
    def _get_next_recommendation(self, profile: StudentPerformance) -> str:
        """Generate recommendation for next steps"""
        if profile.confidence_level > 0.8:
            return "You're doing great! Try some challenging problems."
        elif profile.confidence_level < 0.4:
            return "Let's build your confidence with some easier problems."
        else:
            return "Keep practicing at your current level."
    
    def get_learning_analytics(self, student_id: str) -> Dict[str, Any]:
        """Generate comprehensive learning analytics"""
        profile = self.student_profiles.get(student_id)
        if not profile:
            return {"error": "Student not found"}
        
        return {
            "overall_performance": {
                "total_attempts": profile.total_attempts,
                "accuracy": profile.correct_attempts / profile.total_attempts if profile.total_attempts > 0 else 0,
                "average_response_time": profile.average_time,
                "confidence_level": profile.confidence_level,
                "streak_count": profile.streak_count
            },
            "topic_mastery": profile.topic_mastery,
            "difficulty_performance": profile.difficulty_performance,
            "weaknesses": self.diagnose_weaknesses(student_id, ""),
            "recommendations": self._generate_learning_recommendations(profile)
        }
    
    def _generate_learning_recommendations(self, profile: StudentPerformance) -> List[str]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        if profile.hint_usage_rate > 0.6:
            recommendations.append("Try solving problems without hints to build independence")
        
        if profile.average_time > 120:
            recommendations.append("Practice basic concepts to improve speed")
        
        if profile.confidence_level < 0.5:
            recommendations.append("Focus on easier problems to build confidence")
        
        # Add more sophisticated recommendations based on topic analysis
        weak_topics = [topic for topic, mastery in profile.topic_mastery.items() 
                      if mastery < self.mastery_threshold]
        
        if weak_topics:
            recommendations.append(f"Focus on these topics: {', '.join(weak_topics[:3])}")
        
        return recommendations


class EduAIModel:
    def __init__(self, model_id="Qwen2-0.5B-Instruct-q4f16_1-MLC"):
        self.model_id = model_id
        self.engine = None
        self.is_loading = False
    
    def init_engine(self):
        """
        Simulates engine initialization.
        In a real Python implementation, you would load the model here
        using mlc_llm, transformers, or an API client.
        """
        if self.engine:
            return self.engine
            
        print("Initializing Edu AI Engine... (approx 300MB, one time)")
        self.is_loading = True
        
        # Simulate loading delay
        time.sleep(1) 
        
        try:
            # Placeholder for actual model loading
            # self.engine = mlc_llm.MLCEngine(self.model_id) 
            self.engine = "MOCK_ENGINE_READY" 
            self.is_loading = False
            print("Edu AI Ready!")
            return self.engine
        except Exception as e:
            print(f"AI Init Error: {e}")
            print("Error loading Edu AI. Falling back to offline mode.")
            self.is_loading = False
            return None

    def generate_ai_question(self, topic, problems_solved=0):
        """
        Generates a 5-question limit check and then attempts to generate a question via AI.
        Returns a dict with question data or None if limit reached.
        """
        if problems_solved >= 5:
            return {"status": "complete", "message": "Quiz Complete! You have finished 5 questions."}

        engine = self.init_engine()
        
        # Fallback if engine fails
        if not engine:
            print("Using fallback (Mock) AI")
            return self.generate_mock_question(topic)

        print(f"🤖 Edu AI is generating a question for {topic}...")

        prompt = f"""
        Generate 1 MCQ about "{topic}" (Class 9).
        Strict JSON format:
        {{
            "question": "Question text?",
            "options": ["A", "B", "C", "D"],
            "answer": "Correct Option",
            "hint": "Hint",
            "explanation": "Short info"
        }}
        """

        try:
            # In a real scenario, this would be:
            # response = self.engine.chat.completions.create(...)
            
            # Simulating AI response for demonstration purposes
            # (In a real migration, connect this to your Python LLM backend)
            raw_content = self._mock_llm_response(prompt, topic)
            
            # JSON Extraction Logic
            json_str = raw_content.replace('```json', '').replace('```', '').strip()
            start = json_str.find('{')
            end = json_str.rfind('}')
            
            if start != -1 and end != -1:
                json_str = json_str[start:end+1]
                
            quiz_data = json.loads(json_str)
            
            # Validation
            if not all(key in quiz_data for key in ["question", "options", "answer"]):
                raise ValueError("Incomplete JSON data")
                
            return quiz_data

        except Exception as e:
            print(f"Generation Error: {e}")
            print("AI failed, switching to fallback.")
            return self.generate_mock_question(topic)

    def generate_mock_question(self, topic):
        """
        Fallback mock question generator.
        """
        topic_lower = topic.lower()
        data = {}

        if 'matter' in topic_lower:
            data = {
                "question": "Which of the following serves as evidence that matter is made of particles?",
                "options": ["The smell of perfume spreads across a room", "Wood is hard", "Ice melts", "Iron rusts"],
                "answer": "The smell of perfume spreads across a room",
                "hint": "Think about diffusion.",
                "explanation": "Diffusion of gas particles shows that matter is particulate and particles are in motion."
            }
        elif 'cell' in topic_lower:
            data = {
                "question": "Which organelle is known as the powerhouse of the cell?",
                "options": ["Nucleus", "Mitochondria", "Ribosome", "Golgi Apparatus"],
                "answer": "Mitochondria",
                "hint": "It generates ATP.",
                "explanation": "Mitochondria release energy in the form of ATP."
            }
        else:
            templates = [
                {
                    "q": f"Which of the following is true about {topic}?",
                    "options": ["It is related to physics", "It is related to music", "It involves cooking", "None of the above"],
                    "a": "It is related to physics",
                    "why": "Because we are studying science!"
                },
                {
                    "q": f"What is the primary characteristic of {topic}?",
                    "options": ["Constant change", "Stability", "Randomness", "Color"],
                    "a": "Constant change",
                    "why": "Most scientific phenomena involve change."
                }
            ]
            t = random.choice(templates)
            data = {
                "question": t["q"],
                "options": t["options"],
                "answer": t["a"],
                "hint": "Think logically.",
                "explanation": t["why"]
            }

        data["question"] += " (Offline Mode)"
        return data

    def solve_doubt(self, doubt_text):
        """
        Generates an answer for a doubt.
        """
        if not doubt_text:
            return None

        engine = self.init_engine()
        
        if not engine:
             return (f"<strong>Auto-Response (AI Unavailable):</strong><br>"
                     f"That's a great question about \"{doubt_text}\". <br><br>"
                     f"Since I'm currently running in offline mode, I'd suggest checking your textbook for keywords related to this topic.")

        prompt = f"""
        You are a helpful, encouraging teacher for school students (Class 6-10).
        The student has asked: "{doubt_text}"
        
        Explain the answer clearly, simply, and accurately. 
        Use bullet points if needed. Keep it under 100 words.
        """
        
        try:
            # Simulate streaming or full response
            # response = self.engine.chat...
            
            # Mock success response
            return f"Here is an explanation for '{doubt_text}': [AI generated content would appear here based on '{prompt}']"
            
        except Exception as e:
            print(f"Doubt Error: {e}")
            return "Sorry, I couldn't process that doubt. Try again."

    def _mock_llm_response(self, prompt, topic):
        """
        Internal helper to simulate LLM JSON return for the 'generate_ai_question' method
        if the actual engine isn't connected.
        """
        # This purely exists to make the 'try' block in generate_ai_question succeed during testing/porting
        mock_json = {
            "question": f"What is a key feature of {topic}?",
            "options": ["Feature A", "Feature B", "Feature C", "Feature D"],
            "answer": "Feature A",
            "hint": "Look at the first option.",
            "explanation": "Feature A is the correct answer because of reasons."
        }
        return "```json\n" + json.dumps(mock_json) + "\n```"


# Example usage and testing
if __name__ == "__main__":
    # Initialize the engine with sample data
    sample_data = {
        "subjects": {
            "mathematics": {
                "topics": ["algebra", "geometry", "fractions"]
            }
        }
    }
    
    engine = AdaptiveLearningEngine(sample_data)
    
    # Test the system
    student_id = "student_001"
    
    print("=== Adaptive Learning Engine Demo ===")
    print(f"Creating profile for student: {student_id}")
    
    # Simulate some student responses
    responses = [
        {"correct": True, "time": 45, "hint": False},
        {"correct": True, "time": 38, "hint": False},
        {"correct": False, "time": 120, "hint": True},
        {"correct": True, "time": 52, "hint": False},
        {"correct": False, "time": 95, "hint": True}
    ]
    
    for i, response in enumerate(responses):
        result = engine.process_student_response(
            student_id, f"problem_{i}", 
            response["correct"], response["time"], response["hint"]
        )
        print(f"\nProblem {i+1}: {'Correct' if response['correct'] else 'Incorrect'}")
        print(f"Feedback: {result['feedback']}")
        print(f"Accuracy: {result['updated_metrics']['accuracy']:.2f}")
        print(f"Confidence: {result['updated_metrics']['confidence']:.2f}")
    
    # Generate analytics
    print("\n=== Learning Analytics ===")
    analytics = engine.get_learning_analytics(student_id)
    print(f"Overall Accuracy: {analytics['overall_performance']['accuracy']:.2f}")
    print(f"Average Response Time: {analytics['overall_performance']['average_response_time']:.1f}s")
    print(f"Confidence Level: {analytics['overall_performance']['confidence_level']:.2f}")
    
    print("\nRecommendations:")
    for rec in analytics['recommendations']:
        print(f"• {rec}")
    
    # Diagnose weaknesses
    print("\n=== Weakness Analysis ===")
    weaknesses = engine.diagnose_weaknesses(student_id, "mathematics")
    for weakness_type, details in weaknesses.items():
        print(f"{weakness_type}: {details['recommendation']}")