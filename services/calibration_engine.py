"""
Question Calibration Engine - ULTIMATE v8.0
===========================================
Calibrates question difficulty based on student performance
"""

from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import math

class CalibrationEngine:
    """
    Calibrates question difficulty using empirical performance data
    
    Features:
    - Empirical difficulty calculation
    - Discrimination parameter estimation
    - Question quality metrics
    - Performance-based adjustments
    """
    
    def __init__(self):
        self.question_stats: Dict[str, Dict] = {}  # question_id -> stats
        self.difficulty_cache: Dict[str, float] = {}
    
    def calibrated_difficulty(self, attempts: int, correct_count: int) -> float:
        """
        Calculate calibrated difficulty based on performance
        
        Args:
            attempts: Total number of attempts
            correct_count: Number of correct attempts
        
        Returns:
            Calibrated difficulty (0=very easy to 5=very hard)
        """
        if attempts == 0:
            return 3.0  # Default medium difficulty
        
        if attempts < 5:
            # Insufficient data - use preliminary estimate with uncertainty
            accuracy = correct_count / attempts
            base_difficulty = self._accuracy_to_difficulty(accuracy)
            # Add uncertainty factor
            return base_difficulty + (0.5 * (1 - attempts/5))
        
        # Sufficient data - use empirical calculation
        accuracy = correct_count / attempts
        return self._accuracy_to_difficulty(accuracy)
    
    def _accuracy_to_difficulty(self, accuracy: float) -> float:
        """
        Convert accuracy rate to difficulty scale
        
        Args:
            accuracy: Accuracy rate (0 to 1)
        
        Returns:
            Difficulty (0 to 5)
        """
        # Inverse relationship: high accuracy = low difficulty
        if accuracy >= 0.90:
            return 1.0  # Very easy
        elif accuracy >= 0.75:
            return 2.0  # Easy
        elif accuracy >= 0.60:
            return 3.0  # Medium
        elif accuracy >= 0.40:
            return 4.0  # Hard
        else:
            return 5.0  # Very hard
    
    def estimate_discrimination(self, performance_by_ability: List[Tuple[float, bool]]) -> float:
        """
        Estimate discrimination parameter (how well question differentiates ability)
        
        Args:
            performance_by_ability: List of (theta, correct) tuples
        
        Returns:
            Discrimination parameter (higher = better differentiation)
        """
        if len(performance_by_ability) < 10:
            return 1.0  # Default discrimination
        
        # Sort by ability
        sorted_perf = sorted(performance_by_ability, key=lambda x: x[0])
        
        # Split into quartiles
        n = len(sorted_perf)
        q1_correct = sum(1 for _, correct in sorted_perf[:n//4] if correct)
        q4_correct = sum(1 for _, correct in sorted_perf[3*n//4:] if correct)
        
        q1_size = n // 4
        q4_size = len(sorted_perf[3*n//4:])
        
        if q1_size == 0 or q4_size == 0:
            return 1.0
        
        # Calculate discrimination as difference in accuracy between high/low ability
        discrimination = abs((q4_correct/q4_size) - (q1_correct/q1_size))
        
        # Scale to reasonable range (0.5 to 2.5)
        return 0.5 + (discrimination * 2.0)
    
    def calculate_quality_metrics(self, 
                                  attempts: int,
                                  correct_count: int,
                                  avg_time_seconds: float) -> Dict[str, float]:
        """
        Calculate comprehensive quality metrics for a question
        
        Args:
            attempts: Total attempts
            correct_count: Correct attempts
            avg_time_seconds: Average time spent
        
        Returns:
            Quality metrics dictionary
        """
        if attempts == 0:
            return {
                'reliability': 0.0,
                'clarity': 0.0,
                'appropriateness': 0.0,
                'overall_quality': 0.0
            }
        
        accuracy = correct_count / attempts
        
        # Reliability: based on number of attempts (more = more reliable)
        reliability = min(1.0, attempts / 50.0)
        
        # Clarity: based on time spent (moderate time = clear question)
        # Assume ideal time is 60-90 seconds
        if 60 <= avg_time_seconds <= 90:
            clarity = 1.0
        elif avg_time_seconds < 60:
            clarity = max(0.5, avg_time_seconds / 60)
        else:
            clarity = max(0.5, 90 / avg_time_seconds)
        
        # Appropriateness: based on accuracy (40-80% is ideal)
        if 0.40 <= accuracy <= 0.80:
            appropriateness = 1.0
        elif accuracy < 0.40:
            appropriateness = max(0.3, accuracy / 0.40)
        else:
            appropriateness = max(0.3, (1.0 - accuracy) / 0.20)
        
        # Overall quality
        overall_quality = (reliability * 0.3 + clarity * 0.3 + appropriateness * 0.4)
        
        return {
            'reliability': round(reliability, 3),
            'clarity': round(clarity, 3),
            'appropriateness': round(appropriateness, 3),
            'overall_quality': round(overall_quality, 3)
        }
    
    def update_question_stats(self, 
                             question_id: str,
                             student_theta: float,
                             correct: bool,
                             time_taken: float):
        """
        Update statistics for a question
        
        Args:
            question_id: Unique question identifier
            student_theta: Student's ability level
            correct: Whether answer was correct
            time_taken: Time spent on question (seconds)
        """
        if question_id not in self.question_stats:
            self.question_stats[question_id] = {
                'attempts': 0,
                'correct': 0,
                'total_time': 0.0,
                'performance_by_ability': []
            }
        
        stats = self.question_stats[question_id]
        stats['attempts'] += 1
        if correct:
            stats['correct'] += 1
        stats['total_time'] += time_taken
        stats['performance_by_ability'].append((student_theta, correct))
        
        # Clear difficulty cache to force recalculation
        if question_id in self.difficulty_cache:
            del self.difficulty_cache[question_id]
    
    def get_question_difficulty(self, question_id: str) -> float:
        """Get calibrated difficulty for a question"""
        if question_id not in self.question_stats:
            return 3.0  # Default medium difficulty
        
        if question_id in self.difficulty_cache:
            return self.difficulty_cache[question_id]
        
        stats = self.question_stats[question_id]
        difficulty = self.calibrated_difficulty(stats['attempts'], stats['correct'])
        
        # Cache for performance
        self.difficulty_cache[question_id] = difficulty
        return difficulty
    
    def get_question_analysis(self, question_id: str) -> Dict:
        """Get comprehensive analysis for a question"""
        if question_id not in self.question_stats:
            return {'status': 'No data'}
        
        stats = self.question_stats[question_id]
        avg_time = stats['total_time'] / stats['attempts'] if stats['attempts'] > 0 else 0
        
        difficulty = self.calibrated_difficulty(stats['attempts'], stats['correct'])
        quality = self.calculate_quality_metrics(
            stats['attempts'],
            stats['correct'],
            avg_time
        )
        discrimination = self.estimate_discrimination(stats['performance_by_ability'])
        
        return {
            'attempts': stats['attempts'],
            'accuracy': round(stats['correct'] / stats['attempts'], 3) if stats['attempts'] > 0 else 0,
            'difficulty': round(difficulty, 2),
            'avg_time_seconds': round(avg_time, 1),
            'discrimination': round(discrimination, 2),
            **quality
        }

# Global instance
calibration_engine = CalibrationEngine()
