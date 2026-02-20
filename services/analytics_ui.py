"""
Analytics UI Components - ULTIMATE v8.0
=======================================
Beautiful, professional analytics visualizations
"""

import streamlit as st
from typing import Dict, Any, List, Optional

# ══════════════════════════════════════════════════════════════════════════════
# THETA & ABILITY CARDS
# ══════════════════════════════════════════════════════════════════════════════

def render_theta_card(theta: float, show_label: bool = True):
    """
    Render beautiful theta (ability) score card
    
    Args:
        theta: Theta score (-3 to +3)
        show_label: Whether to show descriptive label
    """
    # Determine color based on theta
    if theta >= 2.0:
        color = "#10b981"  # Green - Excellent
        label = "Excellent"
    elif theta >= 1.0:
        color = "#3b82f6"  # Blue - Good
        label = "Good"
    elif theta >= 0:
        color = "#a78bfa"  # Purple - Average
        label = "Average"
    elif theta >= -1.0:
        color = "#f59e0b"  # Orange - Below Average
        label = "Needs Improvement"
    else:
        color = "#ef4444"  # Red - Weak
        label = "Weak"
    
    st.markdown(
        f"""
        <div style='padding:16px;border-radius:16px;
                    background:linear-gradient(135deg,#1e293b,#0f172a);
                    border:2px solid {color}44;text-align:center;
                    box-shadow:0 4px 15px rgba(0,0,0,0.3);'>
            <div style='font-size:36px;font-weight:900;color:{color};
                        text-shadow:0 0 20px {color}88;'>{theta:.2f}</div>
            <div style='font-size:13px;color:#94a3b8;margin-top:4px;
                        font-weight:600;text-transform:uppercase;
                        letter-spacing:1px;'>Ability Score (θ)</div>
            {f"<div style='font-size:14px;color:{color};margin-top:8px;font-weight:600;'>{label}</div>" if show_label else ""}
        </div>
        """, unsafe_allow_html=True
    )

def render_percentile_card(percentile: float, total_students: Optional[int] = None):
    """
    Render beautiful percentile card
    
    Args:
        percentile: Percentile score (0-100)
        total_students: Optional total students for context
    """
    # Determine color and tier
    if percentile >= 99:
        color = "#10b981"
        tier = "Top 1%"
    elif percentile >= 95:
        color = "#3b82f6"
        tier = "Top 5%"
    elif percentile >= 90:
        color = "#6366f1"
        tier = "Top 10%"
    elif percentile >= 75:
        color = "#8b5cf6"
        tier = "Top 25%"
    elif percentile >= 50:
        color = "#a78bfa"
        tier = "Top 50%"
    else:
        color = "#94a3b8"
        tier = "Below Average"
    
    context_text = f"<div style='font-size:12px;color:#64748b;margin-top:4px;'>Among {total_students} students</div>" if total_students else ""
    
    st.markdown(
        f"""
        <div style='padding:16px;border-radius:16px;
                    background:linear-gradient(135deg,#1e293b,#0f172a);
                    border:2px solid {color}44;text-align:center;
                    box-shadow:0 4px 15px rgba(0,0,0,0.3);'>
            <div style='font-size:36px;font-weight:900;color:{color};
                        text-shadow:0 0 20px {color}88;'>{percentile:.1f}%</div>
            <div style='font-size:13px;color:#94a3b8;margin-top:4px;
                        font-weight:600;text-transform:uppercase;
                        letter-spacing:1px;'>Percentile</div>
            <div style='font-size:14px;color:{color};margin-top:8px;
                        font-weight:600;padding:4px 12px;
                        background:{color}22;border-radius:12px;
                        display:inline-block;'>{tier}</div>
            {context_text}
        </div>
        """, unsafe_allow_html=True
    )

def render_rank_card(rank: int, total_students: int):
    """
    Render beautiful rank card
    
    Args:
        rank: Student's rank
        total_students: Total students
    """
    # Determine medal/icon
    if rank == 1:
        icon = "🥇"
        color = "#fbbf24"  # Gold
    elif rank == 2:
        icon = "🥈"
        color = "#94a3b8"  # Silver
    elif rank == 3:
        icon = "🥉"
        color = "#f97316"  # Bronze
    elif rank <= 10:
        icon = "⭐"
        color = "#3b82f6"
    else:
        icon = "📊"
        color = "#6366f1"
    
    st.markdown(
        f"""
        <div style='padding:16px;border-radius:16px;
                    background:linear-gradient(135deg,#1e293b,#0f172a);
                    border:2px solid {color}44;text-align:center;
                    box-shadow:0 4px 15px rgba(0,0,0,0.3);'>
            <div style='font-size:48px;margin-bottom:8px;'>{icon}</div>
            <div style='font-size:36px;font-weight:900;color:{color};
                        text-shadow:0 0 20px {color}88;'>#{rank}</div>
            <div style='font-size:13px;color:#94a3b8;margin-top:4px;
                        font-weight:600;'>Out of {total_students}</div>
        </div>
        """, unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE VISUALIZATION
# ══════════════════════════════════════════════════════════════════════════════

def render_progress_bar(label: str, value: float, max_value: float = 100, color: str = "#3b82f6"):
    """
    Render animated progress bar
    
    Args:
        label: Progress bar label
        value: Current value
        max_value: Maximum value
        color: Bar color
    """
    percentage = min(100, (value / max_value) * 100)
    
    st.markdown(
        f"""
        <div style='margin:12px 0;'>
            <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
                <span style='font-size:13px;font-weight:600;color:#f1f5f9;'>{label}</span>
                <span style='font-size:13px;font-weight:700;color:{color};'>{value:.1f}/{max_value}</span>
            </div>
            <div style='width:100%;height:12px;background:#1e293b;
                        border-radius:10px;overflow:hidden;border:1px solid #334155;'>
                <div style='height:100%;width:{percentage}%;
                            background:linear-gradient(90deg,{color},{color}cc);
                            border-radius:10px;transition:width 0.5s ease;
                            box-shadow:0 0 10px {color}66;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

def render_stat_grid(stats: List[Dict[str, Any]]):
    """
    Render grid of statistics
    
    Args:
        stats: List of {label, value, icon, color} dictionaries
    """
    cols = st.columns(len(stats))
    
    for col, stat in zip(cols, stats):
        with col:
            color = stat.get('color', '#3b82f6')
            icon = stat.get('icon', '📊')
            
            st.markdown(
                f"""
                <div style='padding:12px;border-radius:12px;
                            background:linear-gradient(135deg,#1e293b,#0f172a);
                            border:1px solid {color}44;text-align:center;'>
                    <div style='font-size:24px;margin-bottom:4px;'>{icon}</div>
                    <div style='font-size:20px;font-weight:800;color:{color};'>{stat['value']}</div>
                    <div style='font-size:11px;color:#94a3b8;margin-top:2px;'>{stat['label']}</div>
                </div>
                """, unsafe_allow_html=True
            )

# ══════════════════════════════════════════════════════════════════════════════
# COMPARISON CHARTS
# ══════════════════════════════════════════════════════════════════════════════

def render_comparison_card(your_score: float, average_score: float, label: str = "Score"):
    """
    Render score comparison card
    
    Args:
        your_score: Student's score
        average_score: Average score
        label: Metric label
    """
    difference = your_score - average_score
    color = "#10b981" if difference >= 0 else "#ef4444"
    arrow = "↑" if difference >= 0 else "↓"
    comparison = "above" if difference >= 0 else "below"
    
    st.markdown(
        f"""
        <div style='padding:16px;border-radius:16px;
                    background:linear-gradient(135deg,#1e293b,#0f172a);
                    border:1px solid #334155;'>
            <div style='display:flex;justify-content:space-between;align-items:center;'>
                <div>
                    <div style='font-size:11px;color:#94a3b8;text-transform:uppercase;
                                letter-spacing:1px;margin-bottom:4px;'>Your {label}</div>
                    <div style='font-size:28px;font-weight:800;color:#f1f5f9;'>{your_score:.1f}</div>
                </div>
                <div style='text-align:right;'>
                    <div style='font-size:11px;color:#94a3b8;text-transform:uppercase;
                                letter-spacing:1px;margin-bottom:4px;'>Average</div>
                    <div style='font-size:20px;font-weight:600;color:#64748b;'>{average_score:.1f}</div>
                </div>
            </div>
            <div style='margin-top:12px;padding:8px 12px;background:{color}22;
                        border-radius:8px;border-left:3px solid {color};'>
                <span style='font-size:20px;margin-right:6px;'>{arrow}</span>
                <span style='font-size:14px;font-weight:600;color:{color};'>
                    {abs(difference):.1f} points {comparison} average
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# INSIGHTS & RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════

def render_insight_card(title: str, message: str, insight_type: str = "info"):
    """
    Render insight/recommendation card
    
    Args:
        title: Insight title
        message: Insight message
        insight_type: Type (info, success, warning, tip)
    """
    config = {
        'info': {'icon': 'ℹ️', 'color': '#3b82f6', 'bg': '#3b82f622'},
        'success': {'icon': '✅', 'color': '#10b981', 'bg': '#10b98122'},
        'warning': {'icon': '⚠️', 'color': '#f59e0b', 'bg': '#f59e0b22'},
        'tip': {'icon': '💡', 'color': '#a78bfa', 'bg': '#a78bfa22'}
    }
    
    style = config.get(insight_type, config['info'])
    
    st.markdown(
        f"""
        <div style='padding:16px;border-radius:12px;
                    background:{style['bg']};border-left:4px solid {style['color']};
                    margin:12px 0;'>
            <div style='display:flex;align-items:center;margin-bottom:8px;'>
                <span style='font-size:24px;margin-right:10px;'>{style['icon']}</span>
                <span style='font-size:15px;font-weight:700;color:{style['color']};'>{title}</span>
            </div>
            <div style='font-size:14px;color:#e2e8f0;line-height:1.6;
                        padding-left:34px;'>{message}</div>
        </div>
        """, unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_performance_color(percentage: float) -> str:
    """Get color based on performance percentage"""
    if percentage >= 90:
        return "#10b981"  # Excellent
    elif percentage >= 75:
        return "#3b82f6"  # Good
    elif percentage >= 60:
        return "#a78bfa"  # Average
    elif percentage >= 40:
        return "#f59e0b"  # Below Average
    else:
        return "#ef4444"  # Poor

def format_large_number(num: int) -> str:
    """Format large numbers with K/M suffixes"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    else:
        return str(num)
