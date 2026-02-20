"""
Unified Adaptive Exam Engine - ULTIMATE v8.0
============================================
IRT-based adaptive difficulty system with comprehensive tracking
"""

import math
from typing import Tuple, Dict, Any, Optional
from datetime import datetime

class UnifiedExamEngine:
    """
    Advanced Item Response Theory (IRT) based adaptive exam engine.
    
    Features:
    - Theta estimation (student ability)
    - Dynamic difficulty adjustment
    - Performance prediction
    - Learning rate optimization
    """
    
    def __init__(self, theta_learning_rate: float = 0.4):
        """
        Initialize adaptive engine
        
        Args:
            theta_learning_rate: Learning rate for theta updates (0.2-0.6)
        """
        self.learning_rate = theta_learning_rate
        self.theta_history: Dict[int, list] = {}  # student_id -> theta history
        self.performance_log: Dict[int, list] = {}  # student_id -> performance log
    
    def theta_to_difficulty(self, theta: float) -> int:
        """
        Convert theta (student ability) to question difficulty level
        
        Args:
            theta: Student ability score (-3 to +3)
        
        Returns:
            Difficulty level (1=Very Easy, 2=Easy, 3=Medium, 4=Hard, 5=Very Hard)
        """
        if theta < -2.0:
            return 1  # Very Easy
        elif theta < -0.5:
            return 2  # Easy
        elif theta < 0.5:
            return 3  # Medium
        elif theta < 2.0:
            return 4  # Hard
        else:
            return 5  # Very Hard
    
    def difficulty_to_theta(self, difficulty: int) -> float:
        """
        Convert difficulty level to theta value
        
        Args:
            difficulty: Difficulty level (1-5)
        
        Returns:
            Corresponding theta value
        """
        difficulty_map = {
            1: -2.5,  # Very Easy
            2: -1.0,  # Easy
            3: 0.0,   # Medium
            4: 1.0,   # Hard
            5: 2.5    # Very Hard
        }
        return difficulty_map.get(difficulty, 0.0)
    
    def calculate_probability(self, theta: float, difficulty: float) -> float:
        """
        Calculate probability of correct answer using IRT 2PL model
        
        Args:
            theta: Student ability
            difficulty: Question difficulty
        
        Returns:
            Probability of correct answer (0 to 1)
        """
        try:
            # IRT 2-Parameter Logistic Model
            # P(correct) = 1 / (1 + exp(-(theta - difficulty)))
            exponent = -(theta - difficulty)
            probability = 1.0 / (1.0 + math.exp(exponent))
            return max(0.01, min(0.99, probability))  # Bound between 0.01 and 0.99
        except OverflowError:
            # Handle extreme values
            if exponent > 20:
                return 0.01
            else:
                return 0.99
    
    def update_theta(self, 
                     theta: float, 
                     difficulty: float, 
                     correct: bool, 
                     learning_rate: Optional[float] = None) -> float:
        """
        Update student ability (theta) based on performance
        
        Args:
            theta: Current ability estimate
            difficulty: Question difficulty
            correct: Whether answer was correct
            learning_rate: Optional custom learning rate
        
        Returns:
            Updated theta value
        """
        lr = learning_rate if learning_rate is not None else self.learning_rate
        
        # Calculate expected probability
        p = self.calculate_probability(theta, difficulty)
        
        # Calculate error (actual - expected)
        actual = 1.0 if correct else 0.0
        error = actual - p
        
        # Update theta using gradient descent
        new_theta = theta + (lr * error)
        
        # Bound theta to reasonable range (-3 to +3)
        return max(-3.0, min(3.0, new_theta))
    
    def batch_update_theta(self, 
                          theta: float, 
                          performance: list) -> Tuple[float, Dict[str, Any]]:
        """
        Update theta based on multiple question performances
        
        Args:
            theta: Initial theta
            performance: List of (difficulty, correct) tuples
        
        Returns:
            (final_theta, statistics)
        """
        current_theta = theta
        theta_changes = []
        
        for difficulty, correct in performance:
            old_theta = current_theta
            current_theta = self.update_theta(current_theta, difficulty, correct)
            theta_changes.append(current_theta - old_theta)
        
        stats = {
            'initial_theta': theta,
            'final_theta': current_theta,
            'total_change': current_theta - theta,
            'avg_change_per_question': sum(theta_changes) / len(theta_changes) if theta_changes else 0,
            'improvement_rate': 'Improving' if current_theta > theta else 'Declining' if current_theta < theta else 'Stable'
        }
        
        return current_theta, stats
    
    def predict_score(self, theta: float, num_questions: int, avg_difficulty: float = 0.0) -> Dict[str, Any]:
        """
        Predict exam performance based on theta
        
        Args:
            theta: Student ability
            num_questions: Number of questions in exam
            avg_difficulty: Average difficulty of questions
        
        Returns:
            Prediction statistics
        """
        expected_prob = self.calculate_probability(theta, avg_difficulty)
        expected_correct = int(num_questions * expected_prob)
        
        return {
            'expected_correct': expected_correct,
            'expected_percentage': round(expected_prob * 100, 2),
            'confidence_lower': max(0, expected_correct - int(num_questions * 0.1)),
            'confidence_upper': min(num_questions, expected_correct + int(num_questions * 0.1)),
            'difficulty_match': self.theta_to_difficulty(theta)
        }
    
    def get_recommended_difficulty(self, theta: float, target_accuracy: float = 0.7) -> float:
        """
        Get recommended question difficulty for target accuracy
        
        Args:
            theta: Student ability
            target_accuracy: Desired accuracy (0.5 to 0.9)
        
        Returns:
            Recommended difficulty level
        """
        # For target accuracy of 0.7, difficulty should be slightly below theta
        # P(correct) = 0.7 when difficulty ≈ theta - 0.85
        adjustment = -math.log((1/target_accuracy) - 1)
        return theta - adjustment
    
    def track_student_progress(self, student_id: int, theta: float):
        """Track theta history for a student"""
        if student_id not in self.theta_history:
            self.theta_history[student_id] = []
        
        self.theta_history[student_id].append({
            'theta': theta,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_student_progress(self, student_id: int) -> Dict[str, Any]:
        """Get progress statistics for a student"""
        if student_id not in self.theta_history or not self.theta_history[student_id]:
            return {'status': 'No data'}
        
        history = self.theta_history[student_id]
        thetas = [entry['theta'] for entry in history]
        
        return {
            'current_theta': thetas[-1],
            'initial_theta': thetas[0],
            'total_improvement': thetas[-1] - thetas[0],
            'average_theta': sum(thetas) / len(thetas),
            'max_theta': max(thetas),
            'min_theta': min(thetas),
            'attempts': len(thetas),
            'trend': 'Improving' if thetas[-1] > thetas[0] else 'Declining'
        }

# Global instance
adaptive_engine = UnifiedExamEngine()
