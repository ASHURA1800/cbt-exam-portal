"""
Services Package - ULTIMATE v8.0
================================
Advanced exam intelligence services

Features:
- Adaptive difficulty engine (IRT-based)
- Question calibration system
- Student ranking engine
- Analytics UI components
"""

from .unified_engine import UnifiedExamEngine, adaptive_engine
from .calibration_engine import CalibrationEngine, calibration_engine
from .ranking_engine import RankingEngine, ranking_engine
from .analytics_ui import (
    render_theta_card,
    render_percentile_card,
    render_rank_card,
    render_progress_bar,
    render_stat_grid,
    render_comparison_card,
    render_insight_card,
    get_performance_color,
    format_large_number
)

__all__ = [
    # Engines
    'UnifiedExamEngine',
    'CalibrationEngine',
    'RankingEngine',
    'adaptive_engine',
    'calibration_engine',
    'ranking_engine',
    
    # UI Components
    'render_theta_card',
    'render_percentile_card',
    'render_rank_card',
    'render_progress_bar',
    'render_stat_grid',
    'render_comparison_card',
    'render_insight_card',
    'get_performance_color',
    'format_large_number',
]
