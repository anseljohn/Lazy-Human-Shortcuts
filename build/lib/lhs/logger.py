import logging
import os
import sys
from pathlib import Path
from typing import Optional
from enum import Enum

import lhs.paths as paths

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    OUTPUT = "output"
    WARNING = "warning"
    ERROR = "error"

class LHSLogger:
    def __init__(self):
        self.logger = logging.getLogger('lhs')
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
            
        # Create formatter for file logging
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler (for all levels)
        log_file = paths.get_log_file()
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Add only file handler - we'll handle console output manually
        self.logger.addHandler(file_handler)
    
    def log(self, level: LogLevel, message: str):
        """Log a message with the specified level and appropriate output destination."""
        if level == LogLevel.OUTPUT:
            # OUTPUT level: print to console and log to file
            print(message, file=sys.stdout)
            self.logger.info(f"[OUTPUT] {message}")
        elif level == LogLevel.DEBUG:
            # DEBUG level: only log to file
            self.logger.debug(f"[DEBUG] {message}")
        elif level == LogLevel.INFO:
            # INFO level: only log to file
            self.logger.info(f"[INFO] {message}")
        elif level == LogLevel.WARNING:
            # WARNING level: print to console and log to file
            print(f"Warning: {message}", file=sys.stderr)
            self.logger.warning(f"[WARNING] {message}")
        elif level == LogLevel.ERROR:
            # ERROR level: print to console and log to file
            print(f"Error: {message}", file=sys.stderr)
            self.logger.error(f"[ERROR] {message}")
    
    def debug(self, message: str):
        """Log a debug message (file only)."""
        self.log(LogLevel.DEBUG, message)
    
    def info(self, message: str):
        """Log an info message (file only)."""
        self.log(LogLevel.INFO, message)
    
    def output(self, message: str):
        """Log an output message (console and file)."""
        self.log(LogLevel.OUTPUT, message)
    
    def warning(self, message: str):
        """Log a warning message (console and file)."""
        self.log(LogLevel.WARNING, message)
    
    def error(self, message: str):
        """Log an error message (console and file)."""
        self.log(LogLevel.ERROR, message)

# Global logger instance
_logger = None

def get_logger() -> LHSLogger:
    """Get the global logger instance."""
    global _logger
    if _logger is None:
        _logger = LHSLogger()
    return _logger

# Convenience functions
def LOG(level: LogLevel, message: str):
    """Main logging function."""
    get_logger().log(level, message)

def DEBUG(message: str):
    """Log debug message (file only)."""
    get_logger().debug(message)

def INFO(message: str):
    """Log info message (file only)."""
    get_logger().info(message)

def OUTPUT(message: str, end: str = "\n"):
    """Log output message (console and file)."""
    get_logger().output(message)

def WARNING(message: str):
    """Log warning message (console and file)."""
    get_logger().warning(message)

def ERROR(message: str):
    """Log error message (console and file)."""
    get_logger().error(message) 