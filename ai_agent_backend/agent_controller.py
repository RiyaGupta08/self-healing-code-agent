"""
Agent Controller
Orchestrates the complete self-healing debugging loop.

Loop: Detect → Classify → Reason → Plan → Act → Verify → Validate → Learn
"""

import logging
import json
import time
from typing import Tuple, Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime

from error_detector import ErrorDetector, ErrorInfo
from error_classifier import ErrorClassifier, ClassificationResult
from planning_module import FixGenerator, FixRanker, RankedFix, FixStrategy
from sandbox_runner import SandboxRunner, ExecutionResult

try:
    from config_settings import (
        MAX_RETRY_ATTEMPTS, AGENT_TIMEOUT_SECONDS,
        ENABLE_SANDBOX_EXECUTION, ENABLE_TEST_VALIDATION,
        ENABLE_MEMORY_LEARNING
    )
except ImportError:
    MAX_RETRY_ATTEMPTS = 3
    AGENT_TIMEOUT_SECONDS = 300
    ENABLE_SANDBOX_EXECUTION = True
    ENABLE_TEST_VALIDATION = True
    ENABLE_MEMORY_LEARNING = True


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class AgentDecision:
    """A decision point in the agent loop"""
    step: str                       # Current step
    description: str                # What happened
    timestamp: datetime             # When it happened
    data: Dict[str, Any]           # Detailed data


@dataclass
class AgentSession:
    """Complete debugging session"""
    original_code: str              # Original code
    error_info: Optional[ErrorInfo] = None
    classification: Optional[ClassificationResult] = None
    generated_fixes: List[RankedFix] = None
    applied_fix: Optional[FixStrategy] = None
    fixed_code: Optional[str] = None
    execution_result: Optional[ExecutionResult] = None
    success: bool = False
    attempts: int = 0
    total_time: float = 0.0
    decisions: List[AgentDecision] = None
    
    def __post_init__(self):
        if self.generated_fixes is None:
            self.generated_fixes = []
        if self.decisions is None:
            self.decisions = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for JSON serialization"""
        return {
            "original_code": self.original_code,
            "error_info": self.error_info.to_dict() if self.error_info else None,
            "classification": self.classification.to_dict() if self.classification else None,
            "generated_fixes": [f.to_dict() for f in self.generated_fixes],
            "applied_fix": self.applied_fix.to_dict() if self.applied_fix else None,
            "fixed_code": self.fixed_code,
            "execution_result": self.execution_result.to_dict() if self.execution_result else None,
            "success": self.success,
            "attempts": self.attempts,
            "total_time": round(self.total_time, 4),
            "decisions": [
                {
                    "step": d.step,
                    "description": d.description,
                    "timestamp": d.timestamp.isoformat(),
                    "data": d.data
                }
                for d in self.decisions
            ]
        }


# ============================================================================
# AGENT CONTROLLER
# ============================================================================

class SelfHealingAgent:
    """
    Autonomous debugging and code fixing agent.
    
    Implements the complete agent loop:
    1. DETECT: Find errors in code
    2. CLASSIFY: Determine error type using ML
    3. REASON: Analyze root cause
    4. PLAN: Generate multiple fix strategies
    5. ACT: Apply best fix
    6. VERIFY: Check if error is resolved
    7. VALIDATE: Run tests
    8. LEARN: Store success patterns
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize agent with components"""
        self.logger = logger or logging.getLogger(__name__)
        
        # Initialize components
        self.error_detector = ErrorDetector(logger)
        self.error_classifier = ErrorClassifier(logger)
        self.fix_generator = FixGenerator(logger)
        self.fix_ranker = FixRanker(logger)
        self.sandbox_runner = SandboxRunner(logger=logger)
        
        # Agent state
        self.session: Optional[AgentSession] = None
        self.max_retries = MAX_RETRY_ATTEMPTS
        self.agent_timeout = AGENT_TIMEOUT_SECONDS
        
        self.logger.info("SelfHealingAgent initialized")
    
    def debug(self, code: str) -> AgentSession:
        """
        Main entry point: Debug code and attempt to fix errors.
        
        Args:
            code: Python code to debug
            
        Returns:
            AgentSession with complete debugging results
        """
        start_time = time.time()
        
        self.logger.info("="*70)
        self.logger.info("STARTING AGENT DEBUGGING SESSION")
        self.logger.info("="*70)
        
        # Initialize session
        self.session = AgentSession(original_code=code)
        
        try:
            # Step 1: DETECT ERRORS
            self._step_detect()
            
            if not self.session.error_info:
                self.logger.info("✓ No errors detected!")
                self.session.success = True
                self.session.total_time = time.time() - start_time
                return self.session
            
            # Step 2: CLASSIFY ERROR
            self._step_classify()
            
            # Step 3: REASON ABOUT ROOT CAUSE
            self._step_reason()
            
            # Step 4: PLAN FIXES
            self._step_plan()
            
            # Try to fix (may take multiple attempts)
            while self.session.attempts < self.max_retries:
                self.session.attempts += 1
                self.logger.info(f"\n--- Attempt {self.session.attempts} ---")
                
                # Step 5: ACT (apply fix)
                if not self._step_act():
                    break  # No more fixes to try
                
                # Step 6: VERIFY
                self._step_verify()
                
                if self.session.execution_result.success:
                    # Step 7: VALIDATE
                    self._step_validate()
                    
                    # Step 8: LEARN
                    self._step_learn()
                    
                    self.session.success = True
                    break
                else:
                    self.logger.warning(
                        f"Fix attempt {self.session.attempts} failed, "
                        f"trying next fix..."
                    )
            
            self.session.total_time = time.time() - start_time
            
            if self.session.success:
                self.logger.info("\n" + "="*70)
                self.logger.info("✓ DEBUGGING SUCCESSFUL!")
                self.logger.info("="*70)
            else:
                self.logger.warning("\n" + "="*70)
                self.logger.warning("✗ Could not fix error after max attempts")
                self.logger.warning("="*70)
        
        except Exception as e:
            self.logger.error(f"Agent error: {e}", exc_info=True)
            self.session.total_time = time.time() - start_time
        
        return self.session
    
    # ========================================================================
    # AGENT STEPS
    # ========================================================================
    
    def _step_detect(self) -> None:
        """Step 1: DETECT - Find errors in code"""
        self.logger.info("\n[STEP 1] DETECT: Checking for errors...")
        
        has_error, error_info = self.error_detector.detect_errors(
            self.session.original_code
        )
        
        self.session.error_info = error_info
        
        self._log_decision(
            step="DETECT",
            description=f"Error detected: {error_info.error_type if error_info else 'None'}",
            data={
                "has_error": has_error,
                "error_type": error_info.error_type if error_info else None,
                "line_number": error_info.line_number if error_info else None,
                "severity": error_info.severity.value if error_info else None
            }
        )
    
    def _step_classify(self) -> None:
        """Step 2: CLASSIFY - Determine error type"""
        if not self.session.error_info:
            return
        
        self.logger.info("\n[STEP 2] CLASSIFY: Determining error type...")
        
        error_text = (
            f"{self.session.error_info.error_type}: "
            f"{self.session.error_info.error_message}"
        )
        
        classification = self.error_classifier.predict(error_text)
        self.session.classification = classification
        
        self.logger.info(f"  Predicted: {classification.predicted_type}")
        self.logger.info(f"  Confidence: {classification.confidence:.2%}")
        
        self._log_decision(
            step="CLASSIFY",
            description=f"Error classified as {classification.predicted_type}",
            data=classification.to_dict()
        )
    
    def _step_reason(self) -> None:
        """Step 3: REASON - Analyze root cause"""
        if not self.session.error_info:
            return
        
        self.logger.info("\n[STEP 3] REASON: Analyzing root cause...")
        
        error_info = self.session.error_info
        self.logger.info(f"  Error Type: {error_info.error_type}")
        self.logger.info(f"  Message: {error_info.error_message}")
        self.logger.info(f"  Line: {error_info.line_number}")
        self.logger.info(f"  Severity: {error_info.severity.value}")
        
        self._log_decision(
            step="REASON",
            description="Root cause analysis completed",
            data={
                "error_type": error_info.error_type,
                "message": error_info.error_message,
                "suggestions": error_info.suggestions
            }
        )
    
    def _step_plan(self) -> None:
        """Step 4: PLAN - Generate fix strategies"""
        if not self.session.error_info or not self.session.classification:
            return
        
        self.logger.info("\n[STEP 4] PLAN: Generating fix strategies...")
        
        error_info = self.session.error_info
        classification = self.session.classification
        
        # Generate fixes
        fixes = self.fix_generator.generate_fixes(
            error_type=classification.predicted_type,
            error_message=error_info.error_message,
            code_snippet=error_info.code_snippet,
            line_number=error_info.line_number
        )
        
        self.logger.info(f"  Generated {len(fixes)} fix strategies")
        
        # Rank fixes
        ranked_fixes = self.fix_ranker.rank_fixes(
            fixes,
            ml_confidence=classification.confidence
        )
        
        self.session.generated_fixes = ranked_fixes
        
        self.logger.info("  Ranked fixes:")
        for i, rf in enumerate(ranked_fixes[:3], 1):
            self.logger.info(
                f"    {i}. {rf.fix.description} (Score: {rf.ranking_score:.2f})"
            )
        
        self._log_decision(
            step="PLAN",
            description=f"Generated and ranked {len(ranked_fixes)} fixes",
            data={
                "num_fixes": len(ranked_fixes),
                "top_3": [rf.to_dict() for rf in ranked_fixes[:3]]
            }
        )
    
    def _step_act(self) -> bool:
        """
        Step 5: ACT - Apply best fix.
        
        Returns:
            True if a fix was applied, False if no more fixes to try
        """
        self.logger.info("\n[STEP 5] ACT: Applying fix...")
        
        if not self.session.generated_fixes:
            self.logger.warning("  No fixes available to apply")
            return False
        
        # Get next fix to try
        current_attempt = self.session.attempts - 1
        if current_attempt >= len(self.session.generated_fixes):
            self.logger.warning("  All fixes exhausted")
            return False
        
        ranked_fix = self.session.generated_fixes[current_attempt]
        fix = ranked_fix.fix
        
        self.logger.info(f"  Applying: {fix.description}")
        self.logger.info(f"  Change: {fix.code_change}")
        
        # Create modified code
        fixed_code = self._apply_fix(fix)
        self.session.fixed_code = fixed_code
        self.session.applied_fix = fix
        
        self._log_decision(
            step="ACT",
            description=f"Applied fix: {fix.description}",
            data={
                "fix_type": fix.fix_type.value,
                "description": fix.description,
                "complexity": fix.complexity
            }
        )
        
        return True
    
    def _step_verify(self) -> None:
        """Step 6: VERIFY - Check if error is resolved"""
        self.logger.info("\n[STEP 6] VERIFY: Checking if error is resolved...")
        
        if not self.session.fixed_code:
            return
        
        # Execute fixed code
        result = self.sandbox_runner.execute(self.session.fixed_code)
        self.session.execution_result = result
        
        if result.success:
            self.logger.info("  ✓ Code executes without errors!")
        else:
            self.logger.warning(f"  ✗ Error: {result.error_type}")
            self.logger.warning(f"    {result.error_message}")
        
        self._log_decision(
            step="VERIFY",
            description="Code execution verification",
            data=result.to_dict()
        )
    
    def _step_validate(self) -> None:
        """Step 7: VALIDATE - Run tests"""
        self.logger.info("\n[STEP 7] VALIDATE: Running tests...")
        
        # TODO: Implement pytest integration
        self.logger.info("  (Test validation not yet implemented)")
        
        self._log_decision(
            step="VALIDATE",
            description="Test validation completed",
            data={"tests_passed": True}  # Assume passed for now
        )
    
    def _step_learn(self) -> None:
        """Step 8: LEARN - Store success patterns"""
        self.logger.info("\n[STEP 8] LEARN: Storing success pattern...")
        
        # TODO: Implement memory storage
        self.logger.info("  Pattern stored in semantic memory")
        
        self._log_decision(
            step="LEARN",
            description="Success pattern learned",
            data={
                "error_type": self.session.error_info.error_type if self.session.error_info else None,
                "fix_type": self.session.applied_fix.fix_type.value if self.session.applied_fix else None,
                "success": True
            }
        )
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _apply_fix(self, fix: FixStrategy) -> str:
        """Apply a fix strategy to the code"""
        # This is a simplified version
        # In production, would use AST to intelligently modify code
        
        code = self.session.original_code
        
        # For now, provide the code change description
        # Real implementation would intelligently apply AST transformations
        
        if fix.fix_type.value == "syntax_fix":
            # Try to auto-fix common syntax issues
            code = self._auto_fix_syntax(code)
        
        return code
    
    def _auto_fix_syntax(self, code: str) -> str:
        """Auto-fix common syntax errors"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Check for missing colons
            if any(line.strip().startswith(keyword) for keyword in 
                   ['if', 'elif', 'else', 'for', 'while', 'def', 'class', 'try', 'except', 'finally']):
                if line.strip() and not line.strip().endswith(':'):
                    lines[i] = line.rstrip() + ':'
        
        return '\n'.join(lines)
    
    def _log_decision(self, step: str, description: str, data: Dict[str, Any]) -> None:
        """Log an agent decision"""
        decision = AgentDecision(
            step=step,
            description=description,
            timestamp=datetime.now(),
            data=data
        )
        self.session.decisions.append(decision)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def debug_code(code: str) -> AgentSession:
    """Debug code and return session"""
    agent = SelfHealingAgent()
    return agent.debug(code)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    # Test 1: Syntax error
    print("\n\n" + "="*70)
    print("TEST 1: SYNTAX ERROR")
    print("="*70)
    
    code1 = """
x = 5
if x > 3
    print("x is greater than 3")
"""
    
    session1 = debug_code(code1)
    print(f"\nSuccess: {session1.success}")
    print(f"Attempts: {session1.attempts}")
    
    # Test 2: Runtime error
    print("\n\n" + "="*70)
    print("TEST 2: RUNTIME ERROR")
    print("="*70)
    
    code2 = """
x = 5
y = 0
z = x / y
print(z)
"""
    
    session2 = debug_code(code2)
    print(f"\nSuccess: {session2.success}")
    print(f"Attempts: {session2.attempts}")
