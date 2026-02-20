"""
Export and Backup System - ULTIMATE
===================================
Comprehensive data export and backup functionality
"""

import json
import csv
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from config import Config
import db

# ══════════════════════════════════════════════════════════════════════════════
# EXPORT FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

class ExportManager:
    """Manage data exports in various formats"""
    
    @staticmethod
    def export_student_results_csv(student_id: int, filepath: Optional[Path] = None) -> Path:
        """Export student results to CSV"""
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = Config.system.EXPORT_DIR / f"student_{student_id}_results_{timestamp}.csv"
        
        conn = db.get_connection()
        cursor = conn.execute("""
            SELECT 
                e.exam_name,
                e.exam_type,
                ea.score,
                ea.total_marks,
                ea.time_taken,
                ea.submitted_at
            FROM exam_attempts ea
            JOIN exams e ON ea.exam_id = e.exam_id
            WHERE ea.student_id = ?
            ORDER BY ea.submitted_at DESC
        """, (student_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Exam Name', 'Type', 'Score', 'Total', 'Percentage', 'Time (min)', 'Date'])
            
            for row in results:
                exam_name, exam_type, score, total, time_taken, submitted_at = row
                percentage = round((score / total * 100) if total > 0 else 0, 2)
                time_min = round(time_taken / 60) if time_taken else 0
                
                writer.writerow([
                    exam_name, exam_type, score, total, percentage, time_min, submitted_at
                ])
        
        return filepath
    
    @staticmethod
    def export_student_results_json(student_id: int, filepath: Optional[Path] = None) -> Path:
        """Export student results to JSON"""
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = Config.system.EXPORT_DIR / f"student_{student_id}_results_{timestamp}.json"
        
        conn = db.get_connection()
        cursor = conn.execute("""
            SELECT 
                e.exam_name,
                e.exam_type,
                ea.score,
                ea.total_marks,
                ea.time_taken,
                ea.submitted_at,
                ea.answers
            FROM exam_attempts ea
            JOIN exams e ON ea.exam_id = e.exam_id
            WHERE ea.student_id = ?
            ORDER BY ea.submitted_at DESC
        """, (student_id,))
        
        results = []
        for row in cursor.fetchall():
            exam_name, exam_type, score, total, time_taken, submitted_at, answers = row
            
            results.append({
                'exam_name': exam_name,
                'exam_type': exam_type,
                'score': score,
                'total_marks': total,
                'percentage': round((score / total * 100) if total > 0 else 0, 2),
                'time_taken_minutes': round(time_taken / 60) if time_taken else 0,
                'submitted_at': submitted_at,
                'answers': json.loads(answers) if answers else None
            })
        
        conn.close()
        
        export_data = {
            'student_id': student_id,
            'exported_at': datetime.now().isoformat(),
            'total_exams': len(results),
            'results': results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    @staticmethod
    def export_exam_statistics_csv(exam_id: int, filepath: Optional[Path] = None) -> Path:
        """Export exam statistics to CSV"""
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = Config.system.EXPORT_DIR / f"exam_{exam_id}_stats_{timestamp}.csv"
        
        conn = db.get_connection()
        cursor = conn.execute("""
            SELECT 
                u.username,
                u.full_name,
                ea.score,
                ea.total_marks,
                ea.time_taken,
                ea.submitted_at
            FROM exam_attempts ea
            JOIN users u ON ea.student_id = u.user_id
            WHERE ea.exam_id = ?
            ORDER BY ea.score DESC
        """, (exam_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Full Name', 'Score', 'Total', 'Percentage', 'Time (min)', 'Submitted'])
            
            for row in results:
                username, full_name, score, total, time_taken, submitted_at = row
                percentage = round((score / total * 100) if total > 0 else 0, 2)
                time_min = round(time_taken / 60) if time_taken else 0
                
                writer.writerow([
                    username, full_name, score, total, percentage, time_min, submitted_at
                ])
        
        return filepath
    
    @staticmethod
    def export_performance_report_pdf(student_id: int, filepath: Optional[Path] = None) -> Optional[Path]:
        """Export comprehensive performance report as PDF"""
        # This would require a PDF library like reportlab
        # Placeholder for now
        return None

# ══════════════════════════════════════════════════════════════════════════════
# BACKUP FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

class BackupManager:
    """Manage database backups"""
    
    @staticmethod
    def create_backup(backup_name: Optional[str] = None) -> Path:
        """
        Create a backup of the database
        
        Returns:
            Path to backup file
        """
        if backup_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"cbt_backup_{timestamp}.db"
        
        backup_path = Config.system.BACKUP_DIR / backup_name
        
        # Copy database file
        shutil.copy2(Config.system.DATABASE_PATH, backup_path)
        
        return backup_path
    
    @staticmethod
    def restore_backup(backup_path: Path) -> bool:
        """
        Restore database from backup
        
        Args:
            backup_path: Path to backup file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not backup_path.exists():
                return False
            
            # Create a backup of current database before restoring
            current_backup = BackupManager.create_backup(
                backup_name=f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            )
            
            # Restore from backup
            shutil.copy2(backup_path, Config.system.DATABASE_PATH)
            
            return True
        except Exception as e:
            print(f"Restore failed: {e}")
            return False
    
    @staticmethod
    def list_backups() -> List[Dict[str, Any]]:
        """
        List all available backups
        
        Returns:
            List of backup information dictionaries
        """
        backups = []
        
        for backup_file in Config.system.BACKUP_DIR.glob("*.db"):
            stat = backup_file.stat()
            backups.append({
                'name': backup_file.name,
                'path': backup_file,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        
        return backups
    
    @staticmethod
    def auto_backup(keep_last: int = 10) -> Optional[Path]:
        """
        Create automatic backup and clean old ones
        
        Args:
            keep_last: Number of recent backups to keep
        
        Returns:
            Path to created backup
        """
        # Create new backup
        backup_path = BackupManager.create_backup()
        
        # Clean old backups
        all_backups = BackupManager.list_backups()
        
        if len(all_backups) > keep_last:
            for backup in all_backups[keep_last:]:
                try:
                    backup['path'].unlink()
                except Exception:
                    pass
        
        return backup_path
    
    @staticmethod
    def export_full_database_json(filepath: Optional[Path] = None) -> Path:
        """
        Export entire database to JSON format
        
        Returns:
            Path to export file
        """
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = Config.system.EXPORT_DIR / f"full_database_{timestamp}.json"
        
        conn = db.get_connection()
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'database_version': '5.0',
            'tables': {}
        }
        
        # Get all table names
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = [row[0] for row in cursor.fetchall()]
        
        # Export each table
        for table in tables:
            cursor = conn.execute(f"SELECT * FROM {table}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            export_data['tables'][table] = {
                'columns': columns,
                'data': [dict(zip(columns, row)) for row in rows]
            }
        
        conn.close()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return filepath

# ══════════════════════════════════════════════════════════════════════════════
# IMPORT FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

class ImportManager:
    """Manage data imports"""
    
    @staticmethod
    def import_questions_csv(filepath: Path, exam_type: str = "JEE") -> int:
        """
        Import questions from CSV file
        
        CSV format:
        Question,Option A,Option B,Option C,Option D,Correct,Subject,Topic,Difficulty
        
        Returns:
            Number of questions imported
        """
        count = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Process and store question
                # This would integrate with the question storage system
                count += 1
        
        return count
    
    @staticmethod
    def import_students_csv(filepath: Path) -> int:
        """
        Import students from CSV file
        
        CSV format:
        Username,Full Name,Email,Date of Birth,Phone
        
        Returns:
            Number of students imported
        """
        count = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Create student account
                    # This would integrate with user registration
                    count += 1
                except Exception as e:
                    print(f"Failed to import student {row.get('Username')}: {e}")
        
        return count
