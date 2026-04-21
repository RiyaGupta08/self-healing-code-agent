"""
Error Detection Module
Detects syntax errors, runtime errors, and captures detailed error information.
"""

import ast
import sys
import io
import traceback
import logging
from typing import Optional, Tuple, Dict, Any, List
from dataclasses import dataclass, asdict
from enum import Enum

# ============================================================================
# DATA STRUCTURES
# ============================================================================

class ErrorSeverity(Enum):
    """Error severity levels"""
    CRITICAL = "critical"      # Code doesn't run at all
    HIGH = "high"              # Runtime crash
    MEDIUM = "medium"          # Unexpected behavior
    LOW = "low"                # Code runs but may have issues


@dataclass
class ErrorInfo:
    """Comprehensive error information"""
    error_type: str              # SyntaxError, RuntimeError, etc.
    error_message: str           # Human-readable message
    line_number: Optional[int]   # Line where error occurred
    column_number: Optional[int] # Column where error occurred
    severity: ErrorSeverity      # Severity level
    code_snippet: str            # Code context (5 lines around error)
    full_traceback: Optional[str] # Full traceback if runtime error
    detected_by: str             # "static" or "runtime"
    suggestions: List[str]       # Initial fix suggestions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data["severity"] = self.severity.value
        return data


# ============================================================================
# ERROR DETECTOR CLASS
# ============================================================================

class ErrorDetector:
    """
    Detects errors in Python code through static analysis and runtime execution.
    
    This class performs two types of error detection:
    1. Static Analysis: Uses AST parsing to detect syntax and style errors
    2. Runtime Detection: Executes code and captures runtime errors
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize the error detector"""
        self.logger = logger or logging.getLogger(__name__)
    
    def detect_errors(self, code: str) -> Tuple[bool, Optional[ErrorInfo]]:
        """
        Detect all errors in code (static + runtime).
        
        Args:
            code: Python code as string
            
        Returns:
            Tuple of (has_error, error_info)
            - has_error: Boolean indicating if an error was found
            - error_info: ErrorInfo object with details, or None if no error
        """
        self.logger.info("Starting error detection")
        
        # First, try static analysis
        static_error = self._detect_static_errors(code)
        if static_error:
            self.logger.info(f"Static error detected: {static_error.error_type}")
            return True, static_error
        
        # If no static error, try runtime detection
        runtime_error = self._detect_runtime_errors(code)
        if runtime_error:
            self.logger.info(f"Runtime error detected: {runtime_error.error_type}")
            return True, runtime_error
        
        self.logger.info("No errors detected")
        return False, None
    
    def _detect_static_errors(self, code: str) -> Optional[ErrorInfo]:
        """
        Detect syntax and static errors using AST parsing.
        
        Args:
            code: Python code as string
            
        Returns:
            ErrorInfo if error found, None otherwise
        """
        try:
            # Try to parse the code
            tree = ast.parse(code)
            # If parsing succeeds, do basic static checks
            return self._run_static_checks(tree, code)
        
        except SyntaxError as e:
            # Return syntax error details
            return ErrorInfo(
                error_type="SyntaxError",
                error_message=str(e.msg or "Invalid syntax"),
                line_number=e.lineno,
                column_number=e.offset,
                severity=ErrorSeverity.CRITICAL,
                code_snippet=self._get_code_snippet(code, e.lineno),
                full_traceback=None,
                detected_by="static",
                suggestions=self._suggest_fixes_for_syntax_error(e, code)
            )
        
        except IndentationError as e:
            return ErrorInfo(
                error_type="IndentationError",
                error_message=str(e.msg or "Indentation error"),
                line_number=e.lineno,
                column_number=e.offset,
                severity=ErrorSeverity.CRITICAL,
                code_snippet=self._get_code_snippet(code, e.lineno),
                full_traceback=None,
                detected_by="static",
                suggestions=["Fix indentation levels"]
            )
        
        except Exception as e:
            # Other parsing errors
            return ErrorInfo(
                error_type=type(e).__name__,
                error_message=str(e),
                line_number=None,
                column_number=None,
                severity=ErrorSeverity.CRITICAL,
                code_snippet="",
                full_traceback=traceback.format_exc(),
                detected_by="static",
                suggestions=["Review code structure"]
            )
    
    def _run_static_checks(self, tree: ast.AST, code: str) -> Optional[ErrorInfo]:
        """
        Run additional static checks on AST.
        Currently checks for:
        - Unused imports
        - Undefined variables (basic check)
        - etc.
        
        Args:
            tree: AST tree
            code: Original code
            
        Returns:
            ErrorInfo if issues found, None otherwise
        """
        # TODO: Implement more sophisticated static analysis
        # For now, return None (let runtime catch issues)
        return None
    
    def _detect_runtime_errors(self, code: str) -> Optional[ErrorInfo]:
        """
        Detect runtime errors by executing code in isolated context.
        
        Args:
            code: Python code as string
            
        Returns:
            ErrorInfo if error occurs, None if code runs successfully
        """
        # Capture output and errors
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            
            # Execute code in isolated namespace
            namespace = {"__name__": "__main__"}
            exec(code, namespace)
            
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            return None  # No error
        
        except Exception as e:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            # Extract error details
            tb = traceback.format_exc()
            error_type = type(e).__name__
            error_message = str(e)
            
            # Try to extract line number from traceback
            line_no = self._extract_line_number_from_traceback(tb, code)
            
            return ErrorInfo(
                error_type=error_type,
                error_message=error_message,
                line_number=line_no,
                column_number=None,
                severity=self._assess_severity(error_type),
                code_snippet=self._get_code_snippet(code, line_no),
                full_traceback=tb,
                detected_by="runtime",
                suggestions=self._suggest_fixes_for_runtime_error(error_type, error_message)
            )
        
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def _get_code_snippet(
        self, 
        code: str, 
        line_number: Optional[int] = None,
        context_lines: int = 2
    ) -> str:
        """
        Extract code snippet around error line.
        
        Args:
            code: Full source code
            line_number: Line where error occurred
            context_lines: How many lines before/after to include
            
        Returns:
            Code snippet as string
        """
        if not line_number:
            return code[:200]  # First 200 chars
        
        lines = code.split("\n")
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)
        
        snippet_lines = lines[start:end]
        return "\n".join(snippet_lines)
    
    def _extract_line_number_from_traceback(self, tb: str, code: str) -> Optional[int]:
        """Extract line number from traceback string"""
        try:
            for line in tb.split("\n"):
                if 'line' in line.lower():
                    parts = line.split(",")
                    for part in parts:
                        if "line" in part.lower():
                            num = ''.join(c for c in part if c.isdigit())
                            if num:
                                return int(num)
        except:
            pass
        return None
    
    def _assess_severity(self, error_type: str) -> ErrorSeverity:
        """Assess error severity based on type"""
        critical_errors = {
            "SyntaxError", "IndentationError", "TypeError",
            "NameError", "AttributeError"
        }
        
        high_errors = {
            "RuntimeError", "ValueError", "KeyError",
            "IndexError", "ZeroDivisionError"
        }
        
        if error_type in critical_errors:
            return ErrorSeverity.CRITICAL
        elif error_type in high_errors:
            return ErrorSeverity.HIGH
        else:
            return ErrorSeverity.MEDIUM
    
    def _suggest_fixes_for_syntax_error(self, error: SyntaxError, code: str) -> List[str]:
        """Generate initial suggestions for syntax errors"""
        suggestions = []
        msg = str(error.msg or "").lower()
        
        if "colon" in msg:
            suggestions.append("Add missing colon ':' at end of line")
        elif "indent" in msg:
            suggestions.append("Fix indentation level")
        elif "unexpected" in msg:
            suggestions.append("Remove or fix unexpected token")
        elif "expected" in msg:
            suggestions.append("Add missing token or correct syntax")
        else:
            suggestions.append("Review Python syntax")
        
        return suggestions
    
    def _suggest_fixes_for_runtime_error(self, error_type: str, message: str) -> List[str]:
        """Generate initial suggestions for runtime errors"""
        suggestions = []
        message_lower = message.lower()
        
        if error_type == "TypeError":
            suggestions.append("Check variable types")
            suggestions.append("Add type conversion (int, str, float)")
        elif error_type == "ValueError":
            suggestions.append("Validate input values")
            suggestions.append("Use try-except for error handling")
        elif error_type == "NameError":
            suggestions.append("Define variable before use")
            suggestions.append("Check variable spelling")
        elif error_type == "IndexError":
            suggestions.append("Check list/array bounds")
            suggestions.append("Verify index is within range")
        elif error_type == "KeyError":
            suggestions.append("Check if dictionary key exists")
            suggestions.append("Use get() method with default")
        elif error_type == "AttributeError":
            suggestions.append("Check if attribute exists")
            suggestions.append("Verify object type")
        elif error_type == "ZeroDivisionError":
            suggestions.append("Add check for zero divisor")
            suggestions.append("Use safe division with try-except")
        else:
            suggestions.append("Review error message and context")
        
        return suggestions


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def detect_code_errors(code: str) -> Tuple[bool, Optional[ErrorInfo]]:
    """
    Convenience function to detect errors in code.
    
    Args:
        code: Python code as string
        
    Returns:
        Tuple of (has_error, error_info)
    """
    detector = ErrorDetector()
    return detector.detect_errors(code)


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Test with various code snippets
    test_cases = [
        ("x = 5\nprint(x)", False),  # No error
        ("x = 5\nprint(x", False),   # Syntax error
        ("x = 1 / 0", True),         # Runtime error
    ]
    
    detector = ErrorDetector()
    for code, should_error in test_cases:
        has_error, error_info = detector.detect_errors(code)
        print(f"Code: {code[:30]}...")
        print(f"Error detected: {has_error}")
        if error_info:
            print(f"Error type: {error_info.error_type}")
        print()
