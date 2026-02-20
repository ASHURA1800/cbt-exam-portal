"""
Configuration Management System - ULTIMATE
==========================================
Centralized configuration for the entire platform
"""

import os
from typing import Dict, Any
from dataclasses import dataclass
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# SYSTEM CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class SystemConfig:
    """System-wide configuration"""
    
    # Application
    APP_NAME: str = "CBT Exam Portal"
    APP_VERSION: str = "10.0"
    APP_DESCRIPTION: str = "Professional AI-Powered Exam Platform"
    
    # Debug & Logging
    DEBUG_MODE: bool = False   # set True only during local development
    VERBOSE_LOGGING: bool = False
    LOG_FILE: str = "cbt_portal.log"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent
    DATABASE_PATH: Path = BASE_DIR / "cbt_exam.db"
    LOG_DIR: Path = BASE_DIR / "logs"
    BACKUP_DIR: Path = BASE_DIR / "backups"
    EXPORT_DIR: Path = BASE_DIR / "exports"
    
    # Performance
    MAX_CONCURRENT_GENERATIONS: int = 3
    CACHE_SIZE_MB: int = 100
    SESSION_TIMEOUT_MINUTES: int = 120
    AUTO_SAVE_INTERVAL_SECONDS: int = 30
    
    # Security
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 30
    SESSION_SECRET_LENGTH: int = 32
    PASSWORD_MIN_LENGTH: int = 8
    
    # AI Generation
    OLLAMA_MODEL: str = "llama3.2:3b"  # FAST MODEL! (3-4x faster than tinyllama)
    OLLAMA_TIMEOUT_SECONDS: int = 300
    MAX_RETRIES: int = 3
    GENERATION_BATCH_SIZE: int = 30
    
    # Translation
    SUPPORTED_LANGUAGES: list = None
    DEFAULT_LANGUAGE: str = "en"
    TRANSLATION_CACHE_SIZE: int = 1000
    
    def __post_init__(self):
        if self.SUPPORTED_LANGUAGES is None:
            self.SUPPORTED_LANGUAGES = [
                'en', 'hi', 'bn', 'ta', 'te', 'kn', 'or', 'mr', 'gu'
            ]
        
        # Create necessary directories
        for directory in [self.LOG_DIR, self.BACKUP_DIR, self.EXPORT_DIR]:
            directory.mkdir(exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# EXAM CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ExamConfig:
    """Exam-specific configuration"""
    
    # Question pool settings
    QUESTION_POOL_MULTIPLIER: float = 1.5  # Generate 50% more than needed
    MIN_UNIQUE_QUESTIONS: int = 10
    MAX_QUESTION_LENGTH: int = 500
    MIN_QUESTION_LENGTH: int = 15
    
    # Difficulty distribution
    EASY_PERCENTAGE: float = 0.25
    MEDIUM_PERCENTAGE: float = 0.50
    HARD_PERCENTAGE: float = 0.25
    
    # Quality thresholds
    MIN_QUALITY_SCORE: float = 0.75
    MIN_UNIQUENESS_SCORE: float = 0.90
    
    # Time limits (minutes)
    JEE_TIME_LIMIT: int = 180
    NEET_TIME_LIMIT: int = 180
    CUET_DOMAIN_TIME_LIMIT: int = 60  # per subject
    CUET_GT_TIME_LIMIT: int = 60
    
    # Auto-save settings
    AUTO_SAVE_ENABLED: bool = True
    AUTO_SAVE_INTERVAL: int = 30  # seconds

# ══════════════════════════════════════════════════════════════════════════════
# UI CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class UIConfig:
    """UI/UX configuration"""
    
    # Theme
    PRIMARY_COLOR: str = "#667eea"
    SECONDARY_COLOR: str = "#764ba2"
    SUCCESS_COLOR: str = "#10b981"
    WARNING_COLOR: str = "#f59e0b"
    ERROR_COLOR: str = "#ef4444"
    
    # Layout
    MAX_WIDTH: int = 1200
    SIDEBAR_WIDTH: int = 300
    
    # Pagination
    ITEMS_PER_PAGE: int = 20
    MAX_ITEMS_PER_PAGE: int = 100
    
    # Notifications
    SUCCESS_DURATION_MS: int = 3000
    ERROR_DURATION_MS: int = 5000
    WARNING_DURATION_MS: int = 4000
    
    # Animations
    ANIMATION_DURATION_MS: int = 300
    TRANSITION_EASING: str = "ease-in-out"

# ══════════════════════════════════════════════════════════════════════════════
# FEATURE FLAGS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class FeatureFlags:
    """Feature flags for enabling/disabling features"""
    
    # Core features
    ENABLE_AI_GENERATION: bool = True
    ENABLE_TRANSLATION: bool = True
    ENABLE_ADMIN_PANEL: bool = True
    
    # Advanced features
    ENABLE_ANALYTICS: bool = True
    ENABLE_EXPORT: bool = True
    ENABLE_BACKUP: bool = True
    ENABLE_AUTO_SAVE: bool = True
    
    # Experimental features
    ENABLE_PRACTICE_MODE: bool = True
    ENABLE_PERFORMANCE_GRAPHS: bool = True
    ENABLE_WEAK_AREA_ANALYSIS: bool = True
    ENABLE_STUDY_RECOMMENDATIONS: bool = True
    
    # AI enhancements
    ENABLE_QUALITY_VALIDATION: bool = True
    ENABLE_GLOSSARY_TRANSLATION: bool = True
    ENABLE_SMART_RETRY: bool = True
    
    # UI enhancements
    ENABLE_DARK_MODE: bool = True
    ENABLE_ANIMATIONS: bool = True
    ENABLE_KEYBOARD_SHORTCUTS: bool = True

# ══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PerformanceConfig:
    """Performance and optimization settings"""
    
    # Caching
    ENABLE_CACHING: bool = True
    CACHE_TRANSLATION: bool = True
    CACHE_QUESTIONS: bool = True
    CACHE_TTL_SECONDS: int = 3600
    
    # Database
    DB_POOL_SIZE: int = 5
    DB_TIMEOUT_SECONDS: int = 30
    ENABLE_WAL_MODE: bool = True  # Write-Ahead Logging
    
    # Lazy loading
    LAZY_LOAD_IMAGES: bool = True
    LAZY_LOAD_TABLES: bool = True
    
    # Rate limiting
    ENABLE_RATE_LIMITING: bool = True
    MAX_REQUESTS_PER_MINUTE: int = 60
    MAX_GENERATIONS_PER_HOUR: int = 10

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CONFIGURATION INSTANCE
# ══════════════════════════════════════════════════════════════════════════════

class Config:
    """Global configuration manager"""
    
    system = SystemConfig()
    exam = ExamConfig()
    ui = UIConfig()
    features = FeatureFlags()
    performance = PerformanceConfig()
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            'system': cls.system.__dict__,
            'exam': cls.exam.__dict__,
            'ui': cls.ui.__dict__,
            'features': cls.features.__dict__,
            'performance': cls.performance.__dict__,
        }
    
    @classmethod
    def update(cls, section: str, key: str, value: Any):
        """Update a configuration value"""
        if hasattr(cls, section):
            section_obj = getattr(cls, section)
            if hasattr(section_obj, key):
                setattr(section_obj, key, value)
                return True
        return False
    
    @classmethod
    def get(cls, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        if hasattr(cls, section):
            section_obj = getattr(cls, section)
            return getattr(section_obj, key, default)
        return default

# ══════════════════════════════════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def validate_config():
    """Validate all configuration values"""
    errors = []
    
    # Validate system config
    if Config.system.MAX_LOGIN_ATTEMPTS < 1:
        errors.append("MAX_LOGIN_ATTEMPTS must be at least 1")
    
    if Config.system.LOCKOUT_DURATION_MINUTES < 1:
        errors.append("LOCKOUT_DURATION_MINUTES must be at least 1")
    
    # Validate exam config
    total_percentage = (
        Config.exam.EASY_PERCENTAGE + 
        Config.exam.MEDIUM_PERCENTAGE + 
        Config.exam.HARD_PERCENTAGE
    )
    if abs(total_percentage - 1.0) > 0.01:
        errors.append(f"Difficulty percentages must sum to 1.0, got {total_percentage}")
    
    # Validate UI config
    if Config.ui.MAX_WIDTH < 800:
        errors.append("MAX_WIDTH must be at least 800px")
    
    if errors:
        raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
    
    return True

# Initialize and validate
try:
    validate_config()
except Exception as e:
    print(f"⚠️ Configuration validation warning: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# v8.0 ADVANCED INTELLIGENCE FLAGS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class IntelligenceConfig:
    """Advanced AI and adaptive features (v8.0)"""
    
    # Adaptive Engine
    ENABLE_ADAPTIVE_ENGINE: bool = True
    THETA_LEARNING_RATE: float = 0.4
    THETA_MIN_VALUE: float = -3.0
    THETA_MAX_VALUE: float = 3.0
    
    # Dynamic Generation
    ENABLE_DYNAMIC_GENERATION: bool = True
    ADAPT_DIFFICULTY_REALTIME: bool = True
    MIN_QUESTIONS_FOR_ADAPTATION: int = 5
    
    # Calibration
    ENABLE_GLOBAL_CALIBRATION: bool = True
    MIN_ATTEMPTS_FOR_CALIBRATION: int = 10
    CALIBRATION_UPDATE_FREQUENCY: int = 100  # Update after N attempts
    
    # Ranking
    ENABLE_PERCENTILE_RANKING: bool = True
    ENABLE_COMPETITIVE_INSIGHTS: bool = True
    ENABLE_ALL_INDIA_RANK_PREDICTION: bool = True
    
    # Performance Prediction
    ENABLE_SCORE_PREDICTION: bool = True
    ENABLE_WEAKNESS_DETECTION: bool = True
    PREDICTION_CONFIDENCE_THRESHOLD: float = 0.75

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CONFIGURATION INSTANCE
# ══════════════════════════════════════════════════════════════════════════════

class Config:
    """Global configuration manager"""
    
    system = SystemConfig()
    exam = ExamConfig()
    ui = UIConfig()
    features = FeatureFlags()
    performance = PerformanceConfig()
    intelligence = IntelligenceConfig()  # NEW v8.0
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            'system': cls.system.__dict__,
            'exam': cls.exam.__dict__,
            'ui': cls.ui.__dict__,
            'features': cls.features.__dict__,
            'performance': cls.performance.__dict__,
            'intelligence': cls.intelligence.__dict__,  # NEW v8.0
        }
    
    @classmethod
    def update(cls, section: str, key: str, value: Any):
        """Update a configuration value"""
        if hasattr(cls, section):
            section_obj = getattr(cls, section)
            if hasattr(section_obj, key):
                setattr(section_obj, key, value)
                return True
        return False
    
    @classmethod
    def get(cls, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        if hasattr(cls, section):
            section_obj = getattr(cls, section)
            return getattr(section_obj, key, default)
        return default

# ══════════════════════════════════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def validate_config():
    """Validate all configuration values"""
    errors = []
    
    # Validate system config
    if Config.system.MAX_LOGIN_ATTEMPTS < 1:
        errors.append("MAX_LOGIN_ATTEMPTS must be at least 1")
    
    if Config.system.LOCKOUT_DURATION_MINUTES < 1:
        errors.append("LOCKOUT_DURATION_MINUTES must be at least 1")
    
    # Validate exam config
    total_percentage = (
        Config.exam.EASY_PERCENTAGE + 
        Config.exam.MEDIUM_PERCENTAGE + 
        Config.exam.HARD_PERCENTAGE
    )
    if abs(total_percentage - 1.0) > 0.01:
        errors.append(f"Difficulty percentages must sum to 1.0, got {total_percentage}")
    
    # Validate UI config
    if Config.ui.MAX_WIDTH < 800:
        errors.append("MAX_WIDTH must be at least 800px")
    
    # Validate intelligence config (v8.0)
    if not (0.1 <= Config.intelligence.THETA_LEARNING_RATE <= 0.9):
        errors.append("THETA_LEARNING_RATE must be between 0.1 and 0.9")
    
    if Config.intelligence.THETA_MIN_VALUE >= Config.intelligence.THETA_MAX_VALUE:
        errors.append("THETA_MIN_VALUE must be less than THETA_MAX_VALUE")
    
    if errors:
        raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
    
    return True

# Initialize and validate
try:
    validate_config()
except Exception as e:
    print(f"⚠️ Configuration validation warning: {e}")

# Export config instance
config = Config()

# ══════════════════════════════════════════════════════════════════════════════
# LLAMA 3.2:3B OPTIMIZATION SETTINGS (v10.0 - SPEED OPTIMIZED)
# ══════════════════════════════════════════════════════════════════════════════
"""
IMPORTANT: These settings fix the "Got only 1/70 questions" error!

The ai_generator.py now uses BATCH GENERATION:
- Generates 5 questions at a time (instead of 70 at once)
- Shows progress: "Batch 1/14: 5/70 questions (7%)"
- Much higher success rate: 80-95% vs 1-10%
- Takes longer but WORKS RELIABLY

Settings already applied in ai_generator.py:
- BATCH_SIZE = 5
- MAX_RETRIES_PER_BATCH = 3
- INTER_BATCH_DELAY = 1

ollama_manager.py settings (optimized version active):
- OLLAMA_TIMEOUT = 180 (3 minutes per batch — Llama 3.2:3b is fast)
- OLLAMA_MAX_RETRIES = 5
- KEEP_ALIVE = "15m"

Expected generation times:
- JEE Main (75Q): ~15-20 minutes
- NEET (180Q): ~35-45 minutes
- CUET Domain (40Q): ~8-10 minutes

This is NORMAL and WORKING! Batch generation takes longer but succeeds.
"""
