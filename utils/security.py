"""
Input Validation and Security System - ULTIMATE
===============================================
Comprehensive validation, sanitization, and security
"""

import re
import html
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
from config import Config

# ══════════════════════════════════════════════════════════════════════════════
# INPUT VALIDATORS
# ══════════════════════════════════════════════════════════════════════════════

class InputValidator:
    """Validate and sanitize user inputs"""
    
    # Regex patterns
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,50}$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    DATE_PATTERN = re.compile(r'^\d{2}/\d{2}/\d{4}$')
    PHONE_PATTERN = re.compile(r'^\+?[0-9]{10,15}$')
    
    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        """
        Validate username
        
        Rules:
        - 3-50 characters
        - Alphanumeric and underscore only
        - No spaces
        """
        if not username:
            return False, "Username is required"
        
        username = username.strip()
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(username) > 50:
            return False, "Username must not exceed 50 characters"
        
        if not InputValidator.USERNAME_PATTERN.match(username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        # Check for reserved words
        reserved = ['admin', 'root', 'system', 'test', 'null', 'undefined']
        if username.lower() in reserved:
            return False, "This username is reserved"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        """Validate email address"""
        if not email:
            return False, "Email is required"
        
        email = email.strip().lower()
        
        if not InputValidator.EMAIL_PATTERN.match(email):
            return False, "Invalid email format"
        
        if len(email) > 255:
            return False, "Email too long"
        
        return True, ""
    
    @staticmethod
    def validate_date(date_str: str, format: str = "DD/MM/YYYY") -> tuple[bool, str]:
        """Validate date string"""
        if not date_str:
            return False, "Date is required"
        
        date_str = date_str.strip()
        
        if format == "DD/MM/YYYY":
            if not InputValidator.DATE_PATTERN.match(date_str):
                return False, "Date must be in DD/MM/YYYY format"
            
            try:
                day, month, year = map(int, date_str.split('/'))
                
                if not (1 <= day <= 31):
                    return False, "Invalid day"
                if not (1 <= month <= 12):
                    return False, "Invalid month"
                if not (1900 <= year <= datetime.now().year):
                    return False, "Invalid year"
                
                # Validate actual date
                datetime(year, month, day)
                
                return True, ""
            except ValueError:
                return False, "Invalid date"
        
        return False, "Unsupported date format"
    
    @staticmethod
    def validate_phone(phone: str) -> tuple[bool, str]:
        """Validate phone number"""
        if not phone:
            return True, ""  # Phone is optional
        
        phone = re.sub(r'[\s\-\(\)]', '', phone)  # Remove spaces, dashes, parentheses
        
        if not InputValidator.PHONE_PATTERN.match(phone):
            return False, "Invalid phone number format"
        
        return True, ""
    
    @staticmethod
    def validate_exam_name(name: str) -> tuple[bool, str]:
        """Validate exam name"""
        if not name:
            return False, "Exam name is required"
        
        name = name.strip()
        
        if len(name) < 3:
            return False, "Exam name must be at least 3 characters"
        
        if len(name) > 200:
            return False, "Exam name must not exceed 200 characters"
        
        # Check for potentially harmful content
        dangerous_patterns = ['<script', 'javascript:', 'onerror=', 'onclick=']
        for pattern in dangerous_patterns:
            if pattern.lower() in name.lower():
                return False, "Exam name contains invalid characters"
        
        return True, ""
    
    @staticmethod
    def validate_integer(value: Any, min_val: Optional[int] = None, max_val: Optional[int] = None) -> tuple[bool, str]:
        """Validate integer value"""
        try:
            int_val = int(value)
            
            if min_val is not None and int_val < min_val:
                return False, f"Value must be at least {min_val}"
            
            if max_val is not None and int_val > max_val:
                return False, f"Value must not exceed {max_val}"
            
            return True, ""
        except (ValueError, TypeError):
            return False, "Must be a valid number"
    
    @staticmethod
    def validate_float(value: Any, min_val: Optional[float] = None, max_val: Optional[float] = None) -> tuple[bool, str]:
        """Validate float value"""
        try:
            float_val = float(value)
            
            if min_val is not None and float_val < min_val:
                return False, f"Value must be at least {min_val}"
            
            if max_val is not None and float_val > max_val:
                return False, f"Value must not exceed {max_val}"
            
            return True, ""
        except (ValueError, TypeError):
            return False, "Must be a valid number"

# ══════════════════════════════════════════════════════════════════════════════
# SANITIZATION
# ══════════════════════════════════════════════════════════════════════════════

class Sanitizer:
    """Sanitize user inputs to prevent XSS and injection attacks"""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Escape HTML special characters"""
        if not text:
            return ""
        return html.escape(str(text))
    
    @staticmethod
    def sanitize_sql(text: str) -> str:
        """Sanitize SQL input (basic protection)"""
        if not text:
            return ""
        
        # Remove common SQL injection patterns
        dangerous = [
            ';', '--', '/*', '*/', 'xp_', 'sp_', 'DROP', 'DELETE', 'INSERT',
            'UPDATE', 'UNION', 'SELECT', 'EXEC', 'EXECUTE'
        ]
        
        sanitized = str(text)
        for pattern in dangerous:
            sanitized = sanitized.replace(pattern, '')
        
        return sanitized.strip()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations"""
        if not filename:
            return "untitled"
        
        # Remove path separators and dangerous characters
        sanitized = re.sub(r'[/\\:*?"<>|]', '', filename)
        
        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip('. ')
        
        # Limit length
        if len(sanitized) > 200:
            sanitized = sanitized[:200]
        
        return sanitized or "untitled"
    
    @staticmethod
    def sanitize_json_string(text: str) -> str:
        """Sanitize string for JSON encoding"""
        if not text:
            return ""
        
        # Escape special characters
        sanitized = str(text)
        sanitized = sanitized.replace('\\', '\\\\')
        sanitized = sanitized.replace('"', '\\"')
        sanitized = sanitized.replace('\n', '\\n')
        sanitized = sanitized.replace('\r', '\\r')
        sanitized = sanitized.replace('\t', '\\t')
        
        return sanitized

# ══════════════════════════════════════════════════════════════════════════════
# SECURITY CHECKS
# ══════════════════════════════════════════════════════════════════════════════

class SecurityChecker:
    """Perform security checks"""
    
    @staticmethod
    def check_password_strength(password: str) -> Dict[str, Any]:
        """
        Check password strength
        
        Returns:
            {
                'is_strong': bool,
                'score': int (0-100),
                'feedback': list of improvement suggestions
            }
        """
        score = 0
        feedback = []
        
        if len(password) < 8:
            feedback.append("Password should be at least 8 characters")
        else:
            score += 25
        
        if len(password) >= 12:
            score += 10
        
        if re.search(r'[a-z]', password):
            score += 15
        else:
            feedback.append("Add lowercase letters")
        
        if re.search(r'[A-Z]', password):
            score += 15
        else:
            feedback.append("Add uppercase letters")
        
        if re.search(r'\d', password):
            score += 15
        else:
            feedback.append("Add numbers")
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 20
        else:
            feedback.append("Add special characters")
        
        # Check for common patterns
        common_patterns = ['123456', 'password', 'qwerty', 'abc123']
        if any(pattern in password.lower() for pattern in common_patterns):
            score -= 30
            feedback.append("Avoid common patterns")
        
        return {
            'is_strong': score >= 70 and len(password) >= 8,
            'score': max(0, min(100, score)),
            'feedback': feedback
        }
    
    @staticmethod
    def is_safe_redirect(url: str) -> bool:
        """Check if URL is safe for redirect"""
        if not url:
            return False
        
        # Only allow relative URLs
        if url.startswith('/'):
            return True
        
        # Block external URLs
        if url.startswith('http://') or url.startswith('https://'):
            return False
        
        # Block javascript: and data: schemes
        if url.startswith(('javascript:', 'data:')):
            return False
        
        return True
    
    @staticmethod
    def detect_sql_injection(text: str) -> bool:
        """Detect potential SQL injection attempt"""
        if not text:
            return False
        
        dangerous_patterns = [
            r'union.*select',
            r'insert.*into',
            r'delete.*from',
            r'drop.*table',
            r'exec.*\(',
            r'execute.*\(',
            r'--.*',
            r'/\*.*\*/',
        ]
        
        text_lower = text.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    @staticmethod
    def detect_xss(text: str) -> bool:
        """Detect potential XSS attempt"""
        if not text:
            return False
        
        dangerous_patterns = [
            r'<script',
            r'javascript:',
            r'onerror=',
            r'onclick=',
            r'onload=',
            r'<iframe',
            r'eval\(',
        ]
        
        text_lower = text.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False

# ══════════════════════════════════════════════════════════════════════════════
# RATE LIMITING
# ══════════════════════════════════════════════════════════════════════════════

class RateLimiter:
    """Simple rate limiting"""
    
    def __init__(self):
        self.requests: Dict[str, List[datetime]] = {}
    
    def is_allowed(self, identifier: str, max_requests: int = 60, window_minutes: int = 1) -> bool:
        """
        Check if request is allowed
        
        Args:
            identifier: User identifier (IP, user_id, etc.)
            max_requests: Maximum requests allowed in window
            window_minutes: Time window in minutes
        
        Returns:
            True if allowed, False if rate limit exceeded
        """
        now = datetime.now()
        cutoff = now - timedelta(minutes=window_minutes)
        
        # Clean old requests
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > cutoff
            ]
        else:
            self.requests[identifier] = []
        
        # Check limit
        if len(self.requests[identifier]) >= max_requests:
            return False
        
        # Add new request
        self.requests[identifier].append(now)
        return True
    
    def get_remaining(self, identifier: str, max_requests: int = 60) -> int:
        """Get remaining requests in current window"""
        if identifier not in self.requests:
            return max_requests
        
        return max(0, max_requests - len(self.requests[identifier]))

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL INSTANCES
# ══════════════════════════════════════════════════════════════════════════════

# Global rate limiter
rate_limiter = RateLimiter()
