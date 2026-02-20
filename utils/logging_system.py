"""
Logging and Monitoring System - ULTIMATE
========================================
Comprehensive logging, error handling, and performance monitoring
"""

import logging
import time
import traceback
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from functools import wraps
from config import Config

# ══════════════════════════════════════════════════════════════════════════════
# LOGGER SETUP
# ══════════════════════════════════════════════════════════════════════════════

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

def setup_logger(name: str = "CBT") -> logging.Logger:
    """Setup comprehensive logger"""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if Config.system.DEBUG_MODE else logging.INFO)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with colors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if Config.system.VERBOSE_LOGGING else logging.INFO)
    console_format = ColoredFormatter(
        '%(levelname)s | %(asctime)s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    if Config.system.LOG_DIR.exists():
        log_file = Config.system.LOG_DIR / Config.system.LOG_FILE
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(levelname)s | %(asctime)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

# Global logger instance
logger = setup_logger()

# ══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE MONITORING
# ══════════════════════════════════════════════════════════════════════════════

class PerformanceMonitor:
    """Monitor and track performance metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, list] = {}
        self.start_times: Dict[str, float] = {}
    
    def start(self, operation: str):
        """Start timing an operation"""
        self.start_times[operation] = time.time()
    
    def end(self, operation: str) -> Optional[float]:
        """End timing and record metric"""
        if operation in self.start_times:
            duration = time.time() - self.start_times[operation]
            
            if operation not in self.metrics:
                self.metrics[operation] = []
            
            self.metrics[operation].append({
                'duration': duration,
                'timestamp': datetime.now().isoformat()
            })
            
            del self.start_times[operation]
            return duration
        return None
    
    def get_stats(self, operation: str) -> Dict[str, Any]:
        """Get statistics for an operation"""
        if operation not in self.metrics or not self.metrics[operation]:
            return {}
        
        durations = [m['duration'] for m in self.metrics[operation]]
        return {
            'count': len(durations),
            'min': min(durations),
            'max': max(durations),
            'avg': sum(durations) / len(durations),
            'total': sum(durations)
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get all statistics"""
        return {
            operation: self.get_stats(operation)
            for operation in self.metrics.keys()
        }
    
    def clear(self):
        """Clear all metrics"""
        self.metrics.clear()
        self.start_times.clear()

# Global performance monitor
perf_monitor = PerformanceMonitor()

# ══════════════════════════════════════════════════════════════════════════════
# DECORATORS
# ══════════════════════════════════════════════════════════════════════════════

def log_execution(func: Callable) -> Callable:
    """Decorator to log function execution"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = f"{func.__module__}.{func.__name__}"
        logger.debug(f"Executing: {func_name}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Completed: {func_name}")
            return result
        except Exception as e:
            logger.error(f"Error in {func_name}: {str(e)}")
            logger.debug(traceback.format_exc())
            raise
    
    return wrapper

def monitor_performance(operation_name: Optional[str] = None):
    """Decorator to monitor performance"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            
            perf_monitor.start(op_name)
            try:
                result = func(*args, **kwargs)
                duration = perf_monitor.end(op_name)
                
                if duration and duration > 1.0:  # Log if takes more than 1 second
                    logger.info(f"⏱️ {op_name} took {duration:.2f}s")
                
                return result
            except Exception as e:
                perf_monitor.end(op_name)
                raise
        
        return wrapper
    return decorator

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry function on failure"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries} failed for {func.__name__}: {e}"
                        )
                        time.sleep(delay * (attempt + 1))  # Exponential backoff
                    else:
                        logger.error(f"All {max_retries} attempts failed for {func.__name__}")
            
            raise last_exception
        
        return wrapper
    return decorator

def safe_execute(default_return: Any = None):
    """Decorator to safely execute function with error handling"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Safe execution caught error in {func.__name__}: {e}")
                logger.debug(traceback.format_exc())
                return default_return
        
        return wrapper
    return decorator

# ══════════════════════════════════════════════════════════════════════════════
# ERROR TRACKING
# ══════════════════════════════════════════════════════════════════════════════

class ErrorTracker:
    """Track and analyze errors"""
    
    def __init__(self):
        self.errors: list = []
        self.error_counts: Dict[str, int] = {}
    
    def log_error(self, error: Exception, context: str = ""):
        """Log an error with context"""
        error_info = {
            'type': type(error).__name__,
            'message': str(error),
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc()
        }
        
        self.errors.append(error_info)
        
        error_key = f"{error_info['type']}:{error_info['context']}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        logger.error(f"Error tracked: {error_info['type']} in {context}: {error_info['message']}")
    
    def get_recent_errors(self, limit: int = 10) -> list:
        """Get recent errors"""
        return self.errors[-limit:]
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary"""
        return {
            'total_errors': len(self.errors),
            'error_counts': self.error_counts,
            'recent_errors': self.get_recent_errors(5)
        }
    
    def clear(self):
        """Clear error history"""
        self.errors.clear()
        self.error_counts.clear()

# Global error tracker
error_tracker = ErrorTracker()

# ══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ══════════════════════════════════════════════════════════════════════════════

class HealthCheck:
    """System health check"""
    
    @staticmethod
    def check_database() -> bool:
        """Check database connectivity"""
        try:
            import db
            db.init_database()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    @staticmethod
    def check_ollama() -> bool:
        """Check Ollama availability"""
        try:
            from ollama_manager import is_model_ready
            return is_model_ready()
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False
    
    @staticmethod
    def check_translation() -> bool:
        """Check translation availability"""
        try:
            import argostranslate
            return True
        except ImportError:
            return False
    
    @staticmethod
    def get_status() -> Dict[str, Any]:
        """Get complete system status"""
        return {
            'timestamp': datetime.now().isoformat(),
            'database': HealthCheck.check_database(),
            'ollama': HealthCheck.check_ollama(),
            'translation': HealthCheck.check_translation(),
            'performance': perf_monitor.get_all_stats(),
            'errors': error_tracker.get_error_summary()
        }

# ══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def log_system_info():
    """Log system information"""
    import platform
    import sys
    
    logger.info("="*70)
    logger.info(f"🚀 {Config.system.APP_NAME} v{Config.system.APP_VERSION}")
    logger.info("="*70)
    logger.info(f"Python: {sys.version.split()[0]}")
    logger.info(f"Platform: {platform.system()} {platform.release()}")
    logger.info(f"Debug Mode: {Config.system.DEBUG_MODE}")
    logger.info(f"Database: {Config.system.DATABASE_PATH}")
    logger.info("="*70)

def save_performance_report(filepath: Optional[Path] = None):
    """Save performance report to file"""
    if filepath is None:
        filepath = Config.system.LOG_DIR / f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'performance': perf_monitor.get_all_stats(),
        'errors': error_tracker.get_error_summary(),
        'health': HealthCheck.get_status()
    }
    
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"Performance report saved to: {filepath}")
    return filepath

# ══════════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ══════════════════════════════════════════════════════════════════════════════

# Log system info on import
if Config.system.VERBOSE_LOGGING:
    log_system_info()
