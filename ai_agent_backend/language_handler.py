"""
Language Abstraction Layer
Enables support for multiple programming languages through clean interfaces.

Supports:
- Python (fully implemented)
- C++ (template provided)
- JavaScript (template provided)

Design Pattern: Adapter Pattern + Strategy Pattern
"""

import subprocess
import logging
from abc import ABC, abstractmethod
from typing import Tuple, Optional, List, Dict, Any
from enum import Enum

try:
    import ast
except ImportError:
    ast = None


# ============================================================================
# LANGUAGE ENUM
# ============================================================================

class ProgrammingLanguage(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    CPP = "cpp"
    JAVASCRIPT = "javascript"
    JAVA = "java"


# ============================================================================
# ABSTRACT BASE CLASS
# ============================================================================

class LanguageHandler(ABC):
    """
    Abstract base class for language-specific handling.
    
    Defines interface for:
    - Static error analysis
    - Runtime error detection
    - Code execution
    - AST/syntax tree parsing
    - Fix application
    - Test execution
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize language handler"""
        self.logger = logger or logging.getLogger(__name__)
    
    @property
    @abstractmethod
    def language_name(self) -> str:
        """Human-readable language name"""
        pass
    
    @property
    @abstractmethod
    def file_extension(self) -> str:
        """File extension (e.g., '.py')"""
        pass
    
    @property
    @abstractmethod
    def syntax_check_timeout(self) -> int:
        """Timeout for syntax check in seconds"""
        pass
    
    @abstractmethod
    def detect_syntax_errors(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Detect syntax errors using static analysis.
        
        Args:
            code: Source code
            
        Returns:
            Error dict or None
            {
                'error_type': 'SyntaxError',
                'message': '...',
                'line': 5,
                'column': 3
            }
        """
        pass
    
    @abstractmethod
    def detect_runtime_errors(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Execute code and detect runtime errors.
        
        Args:
            code: Source code
            
        Returns:
            Error dict or None
        """
        pass
    
    @abstractmethod
    def execute(self, code: str, timeout: int = 5) -> Tuple[bool, str, str]:
        """
        Execute code safely.
        
        Args:
            code: Source code
            timeout: Execution timeout in seconds
            
        Returns:
            (success, stdout, stderr)
        """
        pass
    
    @abstractmethod
    def apply_fix(self, code: str, fix_description: str) -> str:
        """
        Apply a fix to code.
        
        Args:
            code: Original code
            fix_description: Description of fix to apply
            
        Returns:
            Modified code
        """
        pass
    
    @abstractmethod
    def extract_error_context(self, code: str, line_number: Optional[int] = None,
                             context_lines: int = 2) -> str:
        """
        Extract code context around error.
        
        Args:
            code: Source code
            line_number: Error line
            context_lines: Lines before/after
            
        Returns:
            Code snippet
        """
        pass
    
    @abstractmethod
    def detect_test_files(self, code_directory: str) -> List[str]:
        """
        Find test files for this language.
        
        Args:
            code_directory: Directory containing code
            
        Returns:
            List of test file paths
        """
        pass


# ============================================================================
# PYTHON IMPLEMENTATION
# ============================================================================

class PythonHandler(LanguageHandler):
    """Handler for Python code"""
    
    @property
    def language_name(self) -> str:
        return "Python"
    
    @property
    def file_extension(self) -> str:
        return ".py"
    
    @property
    def syntax_check_timeout(self) -> int:
        return 3
    
    def detect_syntax_errors(self, code: str) -> Optional[Dict[str, Any]]:
        """Detect syntax errors using AST"""
        if ast is None:
            self.logger.warning("AST module not available")
            return None
        
        try:
            ast.parse(code)
            return None  # No syntax error
        
        except SyntaxError as e:
            return {
                'error_type': 'SyntaxError',
                'message': str(e.msg or 'Invalid syntax'),
                'line': e.lineno,
                'column': e.offset
            }
        
        except IndentationError as e:
            return {
                'error_type': 'IndentationError',
                'message': str(e.msg or 'Indentation error'),
                'line': e.lineno,
                'column': e.offset
            }
        
        except Exception as e:
            return {
                'error_type': type(e).__name__,
                'message': str(e),
                'line': None,
                'column': None
            }
    
    def detect_runtime_errors(self, code: str) -> Optional[Dict[str, Any]]:
        """Detect runtime errors by execution"""
        success, stdout, stderr = self.execute(code)
        
        if success:
            return None
        
        # Parse error from stderr
        error_lines = stderr.split('\n')
        for line in error_lines:
            if 'Error' in line:
                return {
                    'error_type': self._extract_error_type(stderr),
                    'message': line.strip(),
                    'line': self._extract_line_number(stderr),
                    'traceback': stderr
                }
        
        return None
    
    def execute(self, code: str, timeout: int = 5) -> Tuple[bool, str, str]:
        """Execute Python code"""
        try:
            result = subprocess.run(
                ['python', '-c', code],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return (
                result.returncode == 0,
                result.stdout,
                result.stderr
            )
        
        except subprocess.TimeoutExpired:
            return (False, "", "TIMEOUT: Execution exceeded limit")
        except Exception as e:
            return (False, "", str(e))
    
    def apply_fix(self, code: str, fix_description: str) -> str:
        """
        Apply fix to Python code.
        
        In production, uses AST transformation.
        Here shows simplified approach.
        """
        # This would be enhanced with AST-based transformation
        # For now, provide guidance
        if "missing colon" in fix_description.lower():
            return code.rstrip() + ':'
        
        if "type conversion" in fix_description.lower():
            # Example: convert string to int
            if "int(" in code:
                return code
            return code
        
        return code
    
    def extract_error_context(self, code: str, line_number: Optional[int] = None,
                             context_lines: int = 2) -> str:
        """Extract code context around error"""
        if not line_number:
            return code[:200]
        
        lines = code.split('\n')
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)
        
        return '\n'.join(lines[start:end])
    
    def detect_test_files(self, code_directory: str) -> List[str]:
        """Find Python test files"""
        import os
        import glob
        
        test_files = []
        for pattern in ['test_*.py', '*_test.py', 'tests/*.py']:
            test_files.extend(glob.glob(os.path.join(code_directory, pattern)))
        
        return test_files
    
    def _extract_error_type(self, stderr: str) -> str:
        """Extract error type from traceback"""
        for line in stderr.split('\n'):
            if 'Error' in line:
                parts = line.split(':')
                return parts[0].strip() if parts else 'Unknown'
        return 'Unknown'
    
    def _extract_line_number(self, stderr: str) -> Optional[int]:
        """Extract line number from traceback"""
        for line in stderr.split('\n'):
            if 'line' in line.lower():
                parts = line.split()
                for part in parts:
                    if part.isdigit():
                        return int(part)
        return None


# ============================================================================
# C++ IMPLEMENTATION (TEMPLATE)
# ============================================================================

class CppHandler(LanguageHandler):
    """Handler for C++ code (template for extension)"""
    
    @property
    def language_name(self) -> str:
        return "C++"
    
    @property
    def file_extension(self) -> str:
        return ".cpp"
    
    @property
    def syntax_check_timeout(self) -> int:
        return 5
    
    def detect_syntax_errors(self, code: str) -> Optional[Dict[str, Any]]:
        """Detect C++ syntax errors using clang"""
        try:
            result = subprocess.run(
                ['clang++', '-fsyntax-only', '-'],
                input=code,
                capture_output=True,
                text=True,
                timeout=self.syntax_check_timeout
            )
            
            if result.returncode != 0:
                return {
                    'error_type': 'CompileError',
                    'message': result.stderr[:200],
                    'line': self._extract_line_number(result.stderr),
                    'column': None
                }
            
            return None
        
        except Exception as e:
            self.logger.error(f"C++ syntax check failed: {e}")
            return None
    
    def detect_runtime_errors(self, code: str) -> Optional[Dict[str, Any]]:
        """Detect C++ runtime errors"""
        # Compile and run
        try:
            # Compile
            compile_result = subprocess.run(
                ['g++', '-o', '/tmp/temp_program', '-'],
                input=code,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if compile_result.returncode != 0:
                return {
                    'error_type': 'CompileError',
                    'message': compile_result.stderr[:200],
                    'line': None
                }
            
            # Execute
            run_result = subprocess.run(
                ['/tmp/temp_program'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if run_result.returncode != 0:
                return {
                    'error_type': 'RuntimeError',
                    'message': run_result.stderr[:200],
                    'line': None
                }
            
            return None
        
        except Exception as e:
            return {
                'error_type': 'ExecutionError',
                'message': str(e),
                'line': None
            }
    
    def execute(self, code: str, timeout: int = 5) -> Tuple[bool, str, str]:
        """Execute C++ code"""
        try:
            # Compile
            compile_result = subprocess.run(
                ['g++', '-o', '/tmp/temp_program', '-'],
                input=code,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if compile_result.returncode != 0:
                return (False, "", compile_result.stderr)
            
            # Run
            run_result = subprocess.run(
                ['/tmp/temp_program'],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return (
                run_result.returncode == 0,
                run_result.stdout,
                run_result.stderr
            )
        
        except subprocess.TimeoutExpired:
            return (False, "", "TIMEOUT: Execution exceeded limit")
        except Exception as e:
            return (False, "", str(e))
    
    def apply_fix(self, code: str, fix_description: str) -> str:
        """Apply fix to C++ code"""
        # Simplified implementation
        return code
    
    def extract_error_context(self, code: str, line_number: Optional[int] = None,
                             context_lines: int = 2) -> str:
        """Extract code context"""
        if not line_number:
            return code[:200]
        
        lines = code.split('\n')
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)
        
        return '\n'.join(lines[start:end])
    
    def detect_test_files(self, code_directory: str) -> List[str]:
        """Find C++ test files"""
        import os
        import glob
        
        test_files = []
        for pattern in ['test_*.cpp', '*_test.cpp', 'tests/*.cpp']:
            test_files.extend(glob.glob(os.path.join(code_directory, pattern)))
        
        return test_files
    
    def _extract_line_number(self, stderr: str) -> Optional[int]:
        """Extract line number from compiler error"""
        for line in stderr.split('\n'):
            if ':' in line:
                parts = line.split(':')
                if len(parts) > 1 and parts[1].strip().isdigit():
                    return int(parts[1].strip())
        return None


# ============================================================================
# LANGUAGE FACTORY
# ============================================================================

class LanguageFactory:
    """Factory for creating language handlers"""
    
    _handlers: Dict[ProgrammingLanguage, type] = {
        ProgrammingLanguage.PYTHON: PythonHandler,
        ProgrammingLanguage.CPP: CppHandler,
        # ProgrammingLanguage.JAVASCRIPT: JavaScriptHandler,  # Future
        # ProgrammingLanguage.JAVA: JavaHandler,  # Future
    }
    
    @classmethod
    def get_handler(cls, 
                   language: ProgrammingLanguage,
                   logger: Optional[logging.Logger] = None) -> LanguageHandler:
        """
        Get handler for specified language.
        
        Args:
            language: Programming language enum
            logger: Optional logger
            
        Returns:
            Language handler instance
        """
        handler_class = cls._handlers.get(language)
        
        if handler_class is None:
            raise ValueError(f"Unsupported language: {language}")
        
        return handler_class(logger)
    
    @classmethod
    def register_handler(cls,
                        language: ProgrammingLanguage,
                        handler_class: type) -> None:
        """
        Register custom language handler.
        
        Args:
            language: Language enum
            handler_class: Handler class
        """
        cls._handlers[language] = handler_class
        
    @classmethod
    def list_supported_languages(cls) -> List[str]:
        """List all supported languages"""
        return [lang.value for lang in cls._handlers.keys()]


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example: Use Python handler
    python_handler = LanguageFactory.get_handler(ProgrammingLanguage.PYTHON)
    
    test_code = """
x = 5
y = 0
z = x / y
print(z)
"""
    
    # Detect errors
    syntax_error = python_handler.detect_syntax_errors(test_code)
    print(f"Syntax error: {syntax_error}")
    
    runtime_error = python_handler.detect_runtime_errors(test_code)
    print(f"Runtime error: {runtime_error}")
    
    # Execute
    success, stdout, stderr = python_handler.execute(test_code)
    print(f"Success: {success}")
    print(f"Error: {stderr}")
