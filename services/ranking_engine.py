"""
Student Ranking Engine - ULTIMATE v8.0
======================================
Comprehensive ranking and percentile calculation system
"""

from typing import List, Dict, Any, Optional, Tuple
import math
from datetime import datetime

class RankingEngine:
    """
    Advanced ranking system with multiple ranking methodologies
    
    Features:
    - Percentile calculation
    - Rank distribution analysis
    - Performance tiers
    - Trend analysis
    - Competitive insights
    """
    
    def __init__(self):
        self.ranking_cache: Dict[str, Dict] = {}  # exam_id -> rankings
        self.tier_thresholds = {
            'Top 1%': 99.0,
            'Top 5%': 95.0,
            'Top 10%': 90.0,
            'Top 25%': 75.0,
            'Top 50%': 50.0
        }
    
    def calculate_percentile(self, rank: int, total_students: int) -> float:
        """
        Calculate percentile from rank
        
        Args:
            rank: Student's rank (1 = best)
            total_students: Total number of students
        
        Returns:
            Percentile (0-100)
        """
        if total_students == 0:
            return 0.0
        
        if rank < 1 or rank > total_students:
            return 0.0
        
        # Percentile = (Number of students below you / Total students) * 100
        percentile = ((total_students - rank + 1) / total_students) * 100
        return round(percentile, 2)
    
    def rank_from_percentile(self, percentile: float, total_students: int) -> int:
        """
        Calculate rank from percentile
        
        Args:
            percentile: Percentile score (0-100)
            total_students: Total number of students
        
        Returns:
            Estimated rank
        """
        if total_students == 0 or percentile < 0 or percentile > 100:
            return 0
        
        # Rank = Total - (Percentile/100 * Total) + 1
        rank = int(total_students - (percentile / 100 * total_students) + 1)
        return max(1, min(total_students, rank))
    
    def get_performance_tier(self, percentile: float) -> str:
        """
        Determine performance tier based on percentile
        
        Args:
            percentile: Percentile score
        
        Returns:
            Tier name
        """
        for tier, threshold in self.tier_thresholds.items():
            if percentile >= threshold:
                return tier
        return "Below Average"
    
    def calculate_rank_from_scores(self, 
                                   scores: List[Tuple[int, float]]) -> List[Tuple[int, int, float]]:
        """
        Calculate ranks from list of (student_id, score) tuples
        
        Args:
            scores: List of (student_id, score)
        
        Returns:
            List of (student_id, rank, percentile) sorted by rank
        """
        # Sort by score descending
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        total = len(sorted_scores)
        
        results = []
        for rank, (student_id, score) in enumerate(sorted_scores, 1):
            percentile = self.calculate_percentile(rank, total)
            results.append((student_id, rank, percentile))
        
        return results
    
    def analyze_rank_distribution(self, scores: List[float]) -> Dict[str, Any]:
        """
        Analyze the distribution of scores
        
        Args:
            scores: List of scores
        
        Returns:
            Distribution statistics
        """
        if not scores:
            return {'status': 'No data'}
        
        n = len(scores)
        sorted_scores = sorted(scores)
        
        # Basic statistics
        mean_score = sum(scores) / n
        median_score = sorted_scores[n // 2]
        min_score = sorted_scores[0]
        max_score = sorted_scores[-1]
        score_range = max_score - min_score
        
        # Calculate quartiles
        q1 = sorted_scores[n // 4]
        q3 = sorted_scores[3 * n // 4]
        iqr = q3 - q1
        
        # Calculate standard deviation
        variance = sum((x - mean_score) ** 2 for x in scores) / n
        std_dev = math.sqrt(variance)
        
        # Determine distribution shape
        skewness = self._calculate_skewness(scores, mean_score, std_dev)
        
        return {
            'total_students': n,
            'mean': round(mean_score, 2),
            'median': round(median_score, 2),
            'min': round(min_score, 2),
            'max': round(max_score, 2),
            'range': round(score_range, 2),
            'q1': round(q1, 2),
            'q3': round(q3, 2),
            'iqr': round(iqr, 2),
            'std_dev': round(std_dev, 2),
            'skewness': round(skewness, 2),
            'distribution_shape': self._interpret_skewness(skewness)
        }
    
    def _calculate_skewness(self, scores: List[float], mean: float, std_dev: float) -> float:
        """Calculate skewness of distribution"""
        if std_dev == 0:
            return 0.0
        
        n = len(scores)
        skewness = sum(((x - mean) / std_dev) ** 3 for x in scores) / n
        return skewness
    
    def _interpret_skewness(self, skewness: float) -> str:
        """Interpret skewness value"""
        if skewness < -0.5:
            return "Left-skewed (easier exam)"
        elif skewness > 0.5:
            return "Right-skewed (harder exam)"
        else:
            return "Symmetric (balanced)"
    
    def get_competitive_insights(self, 
                                 student_percentile: float,
                                 total_students: int,
                                 exam_type: str = "JEE") -> Dict[str, Any]:
        """
        Generate competitive insights for student
        
        Args:
            student_percentile: Student's percentile
            total_students: Total students in comparison
            exam_type: Type of exam
        
        Returns:
            Competitive insights
        """
        rank = self.rank_from_percentile(student_percentile, total_students)
        tier = self.get_performance_tier(student_percentile)
        
        # Calculate how many students to beat for next tier
        next_tier = None
        students_to_beat = 0
        
        for tier_name, threshold in sorted(self.tier_thresholds.items(), key=lambda x: x[1]):
            if student_percentile < threshold:
                next_tier = tier_name
                target_rank = self.rank_from_percentile(threshold, total_students)
                students_to_beat = rank - target_rank
                break
        
        # Estimate improvement needed
        if student_percentile < 99:
            points_to_next_tier = (next_tier.split()[1].rstrip('%') if next_tier else 100) - student_percentile
        else:
            points_to_next_tier = 0
        
        return {
            'current_rank': rank,
            'percentile': student_percentile,
            'tier': tier,
            'total_students': total_students,
            'students_ahead': rank - 1,
            'students_behind': total_students - rank,
            'next_tier': next_tier or "Already at top",
            'students_to_beat': students_to_beat,
            'percentile_points_needed': round(points_to_next_tier, 1) if next_tier else 0,
            'top_percentage': round((rank / total_students) * 100, 2)
        }
    
    def predict_all_india_rank(self, 
                              percentile: float,
                              sample_size: int,
                              total_exam_takers: int) -> Dict[str, Any]:
        """
        Predict All India Rank based on sample performance
        
        Args:
            percentile: Student's percentile in sample
            sample_size: Size of current sample
            total_exam_takers: Estimated total exam takers
        
        Returns:
            Predicted rank and confidence interval
        """
        if sample_size == 0 or total_exam_takers == 0:
            return {'status': 'Insufficient data'}
        
        # Predicted rank
        predicted_rank = self.rank_from_percentile(percentile, total_exam_takers)
        
        # Confidence interval (wider for smaller samples)
        confidence_factor = math.sqrt(total_exam_takers / sample_size)
        margin = int(predicted_rank * 0.1 * confidence_factor)
        
        lower_bound = max(1, predicted_rank - margin)
        upper_bound = min(total_exam_takers, predicted_rank + margin)
        
        return {
            'predicted_rank': predicted_rank,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'confidence_level': max(50, min(95, int(100 * (sample_size / total_exam_takers)))),
            'sample_size': sample_size,
            'total_takers': total_exam_takers
        }
    
    def get_rank_history(self, 
                        student_id: int,
                        exam_history: List[Tuple[str, int, int]]) -> Dict[str, Any]:
        """
        Analyze rank trend over multiple exams
        
        Args:
            student_id: Student identifier
            exam_history: List of (exam_id, rank, total_students)
        
        Returns:
            Rank trend analysis
        """
        if not exam_history:
            return {'status': 'No history'}
        
        ranks = [rank for _, rank, _ in exam_history]
        percentiles = [self.calculate_percentile(rank, total) 
                      for _, rank, total in exam_history]
        
        # Calculate trend
        if len(ranks) >= 2:
            recent_avg = sum(percentiles[-3:]) / min(3, len(percentiles[-3:]))
            overall_avg = sum(percentiles) / len(percentiles)
            trend = "Improving" if recent_avg > overall_avg else "Declining"
        else:
            trend = "Insufficient data"
        
        return {
            'exams_taken': len(exam_history),
            'best_rank': min(ranks),
            'worst_rank': max(ranks),
            'avg_percentile': round(sum(percentiles) / len(percentiles), 2),
            'current_percentile': percentiles[-1],
            'trend': trend,
            'consistency': self._calculate_consistency(percentiles)
        }
    
    def _calculate_consistency(self, percentiles: List[float]) -> str:
        """Calculate performance consistency"""
        if len(percentiles) < 2:
            return "N/A"
        
        std_dev = math.sqrt(sum((p - sum(percentiles)/len(percentiles))**2 for p in percentiles) / len(percentiles))
        
        if std_dev < 5:
            return "Very Consistent"
        elif std_dev < 10:
            return "Consistent"
        elif std_dev < 20:
            return "Moderate"
        else:
            return "Inconsistent"

# Global instance
ranking_engine = RankingEngine()
