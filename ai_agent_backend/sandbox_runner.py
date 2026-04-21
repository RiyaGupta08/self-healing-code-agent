"""
Sandbox Execution Module
Safely executes code with resource limits, timeout protection, and error capture.
"""

import subprocess
import sys
import io
import signal
import logging
import time
from typing import Tuple, Optional, Dict, Any
from dataclasses import dataclass
from contextlib import contextmanager

try:
    from config_settings import (
        EXECUTION_TIMEOUT_SECONDS, MAX_MEMORY_MB, MAX_OUTPUT_CHARS
    )
except ImportError:
    EXECUTION_TIMEOUT_SECONDS = 5
    MAX_MEMORY_MB = 512
    MAX_OUTPUT_CHARS = 10000


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class ExecutionResult:
    """Result of code execution"""
    success: bool                   # True if code ran without exceptions
    stdout: str                     # Standard output
    stderr: str                     # Standard error
    return_code: int                # Process return code
    execution_time: float           # Time taken in seconds
    error_type: Optional[str]       # Error type if failed
    error_message: Optional[str]    # Error message if failed
    was_timeout: bool               # True if execution timed out
    was_memory_limited: bool        # True if memory was exceeded
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "stdout": self.stdout[:MAX_OUTPUT_CHARS],
            "stderr": self.stderr[:MAX_OUTPUT_CHARS],
            "return_code": self.return_code,
            "execution_time": round(self.execution_time, 4),
            "error_type": self.error_type,
            "error_message": self.error_message,
            "timeout": self.was_timeout,
            "memory_limited": self.was_memory_limited
        }


# ============================================================================
# SANDBOX RUNNER
# ============================================================================

class SandboxRunner:
    """
    Executes Python code in isolated subprocess with safety constraints.
    
    Safety measures:
    - Timeout protection
    - Memory limits
    - Resource limits
    - Output capture
    - Error isolation
    """
    
    def __init__(self, timeout: int = EXECUTION_TIMEOUT_SECONDS,
                 logger: Optional[logging.Logger] = None):
        """
        Initialize sandbox runner.
        
        Args:
            timeout: Timeout in seconds
            logger: Optional logger instance
        """
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)
    
    def execute(self, code: str) -> ExecutionResult:
        """
        Execute code safely in subprocess.
        
        Args:
            code: Python code to execute
            
        Returns:
            ExecutionResult with output and status
        """
        self.logger.info(f"Executing code (timeout: {self.timeout}s)")
        
        start_time = time.time()
        
        try:
            # Create subprocess
            process = subprocess.Popen(
                [sys.executable, "-c", code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=self._set_resource_limits if hasattr(signal, 'SIGALRM') else None
            )
            
            # Wait for completion with timeout
            try:
                stdout, stderr = process.communicate(timeout=self.timeout)
                execution_time = time.time() - start_time
                return_code = process.returncode
                was_timeout = False
                
            except subprocess.TimeoutExpired:
                # Kill process if timeout
                process.kill()
                stdout, stderr = process.communicate()
                execution_time = time.time() - start_time
                return_code = -1
                was_timeout = True
                stderr = f"TIMEOUT: Execution exceeded {self.timeout}s"
            
            # Analyze result
            success = return_code == 0 and not was_timeout
            
            if success:
                error_type = None
                error_message = None
            else:
                error_type = self._extract_error_type(stderr)
                error_message = self._extract_error_message(stderr)
            
            return ExecutionResult(
                success=success,
                stdout=stdout[:MAX_OUTPUT_CHARS],
                stderr=stderr[:MAX_OUTPUT_CHARS],
                return_code=return_code,
                execution_time=execution_time,
                error_type=error_type,
                error_message=error_message,
                was_timeout=was_timeout,
                was_memory_limited=False
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"Execution error: {e}")
            
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=execution_time,
                error_type=type(e).__name__,
                error_message=str(e),
                was_timeout=False,
                was_memory_limited=False
            )
    
    def execute_with_input(self, code: str, input_data: str) -> ExecutionResult:
        """
        Execute code with stdin input.
        
        Args:
            code: Python code to execute
            input_data: Input to provide via stdin
            
        Returns:
            ExecutionResult with output and status
        """
        self.logger.info(f"Executing code with input")
        
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                [sys.executable, "-c", code],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=self._set_resource_limits if hasattr(signal, 'SIGALRM') else None
            )
            
            try:
                stdout, stderr = process.communicate(
                    input=input_data,
                    timeout=self.timeout
                )
                execution_time = time.time() - start_time
                return_code = process.returncode
                was_timeout = False
                
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                execution_time = time.time() - start_time
                return_code = -1
                was_timeout = True
                stderr = f"TIMEOUT: Execution exceeded {self.timeout}s"
            
            success = return_code == 0 and not was_timeout
            
            if success:
                error_type = None
                error_message = None
            else:
                error_type = self._extract_error_type(stderr)
                error_message = self._extract_error_message(stderr)
            
            return ExecutionResult(
                success=success,
                stdout=stdout[:MAX_OUTPUT_CHARS],
                stderr=stderr[:MAX_OUTPUT_CHARS],
                return_code=return_code,
                execution_time=execution_time,
                error_type=error_type,
                error_message=error_message,
                was_timeout=was_timeout,
                was_memory_limited=False
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=execution_time,
                error_type=type(e).__name__,
                error_message=str(e),
                was_timeout=False,
                was_memory_limited=False
            )
    
    def _set_resource_limits(self) -> None:
        """Set resource limits for subprocess (Unix only)"""
        try:
            import resource
            
            # Memory limit
            max_memory = MAX_MEMORY_MB * 1024 * 1024  # Convert to bytes
            resource.setrlimit(resource.RLIMIT_AS, (max_memory, max_memory))
            
            # CPU time limit (soft, hard)
            resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout + 1))
            
        except ImportError:
            # Windows doesn't have resource module
            pass
    
    def _extract_error_type(self, stderr: str) -> str:
        """Extract error type from stderr"""
        if not stderr:
            return "Unknown"
        
        # Look for error type in traceback
        for line in stderr.split("\n"):
            if "Error:" in line:
                error_type = line.split(":")[0].strip()
                return error_type if error_type else "Unknown"
        
        return "Unknown"
    
    def _extract_error_message(self, stderr: str) -> str:
        """Extract error message from stderr"""
        if not stderr:
            return ""
        
        lines = stderr.split("\n")
        # Get last non-empty line
        for line in reversed(lines):
            if line.strip():
                return line.strip()
        
        return ""


# ============================================================================
# COMPARISON RUNNER (For testing fix validity)
# ============================================================================

class ComparisonRunner:
    """
    Runs code and compares outputs.
    Useful for validating if a fix produces expected output.
    """
    
    def __init__(self, timeout: int = EXECUTION_TIMEOUT_SECONDS,
                 logger: Optional[logging.Logger] = None):
        """Initialize comparison runner"""
        self.runner = SandboxRunner(timeout, logger)
        self.logger = logger or logging.getLogger(__name__)
    
    def compare_outputs(
        self,
        original_code: str,
        fixed_code: str,
        input_data: Optional[str] = None,
        expected_output: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare outputs of original and fixed code.
        
        Args:
            original_code: Original code
            fixed_code: Fixed code
            input_data: Optional input to provide
            expected_output: Optional expected output
            
        Returns:
            Dictionary with comparison results
        """
        self.logger.info("Comparing outputs")
        
        # Run both versions
        if input_data:
            original_result = self.runner.execute_with_input(original_code, input_data)
            fixed_result = self.runner.execute_with_input(fixed_code, input_data)
        else:
            original_result = self.runner.execute(original_code)
            fixed_result = self.runner.execute(fixed_code)
        
        # Analyze results
        original_failed = not original_result.success
        fixed_succeeded = fixed_result.success
        outputs_differ = original_result.stdout != fixed_result.stdout
        
        return {
            "original": original_result.to_dict(),
            "fixed": fixed_result.to_dict(),
            "original_failed": original_failed,
            "fixed_succeeded": fixed_succeeded,
            "outputs_differ": outputs_differ,
            "fix_resolved_error": original_failed and fixed_succeeded,
            "expected_output_matches": (
                fixed_result.stdout.strip() == expected_output.strip()
                if expected_output else None
            )
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def run_code(code: str, timeout: int = EXECUTION_TIMEOUT_SECONDS) -> ExecutionResult:
    """Execute code and return result"""
    runner = SandboxRunner(timeout)
    return runner.execute(code)


def run_code_with_input(
    code: str,
    input_data: str,
    timeout: int = EXECUTION_TIMEOUT_SECONDS
) -> ExecutionResult:
    """Execute code with input"""
    runner = SandboxRunner(timeout)
    return runner.execute_with_input(code, input_data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test 1: Simple successful code
    print("Test 1: Simple successful code")
    result = run_code("print('Hello, World!')")
    print(f"Success: {result.success}")
    print(f"Output: {result.stdout}")
    print()
    
    # Test 2: Code with error
    print("Test 2: Code with error")
    result = run_code("x = 1 / 0")
    print(f"Success: {result.success}")
    print(f"Error: {result.error_type}")
    print()
    
    # Test 3: Timeout
    print("Test 3: Infinite loop (timeout)")
    result = run_code("while True: pass", timeout=2)
    print(f"Timeout: {result.was_timeout}")
    print(f"Time: {result.execution_time:.2f}s")
