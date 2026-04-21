"""
Planning Module
Generates multiple fix strategies and ranks them by likelihood of success.
"""

import logging
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from config_settings import (
        MAX_FIXES_TO_GENERATE, WEIGHT_ML_CONFIDENCE, 
        WEIGHT_HISTORICAL_SUCCESS, WEIGHT_COMPLEXITY,
        COMPLEXITY_SIMPLE, COMPLEXITY_MEDIUM, COMPLEXITY_HIGH
    )
except ImportError:
    MAX_FIXES_TO_GENERATE = 5
    WEIGHT_ML_CONFIDENCE = 0.40
    WEIGHT_HISTORICAL_SUCCESS = 0.40
    WEIGHT_COMPLEXITY = 0.20
    COMPLEXITY_SIMPLE = 1
    COMPLEXITY_MEDIUM = 2
    COMPLEXITY_HIGH = 3


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class FixType(Enum):
    """Types of fixes"""
    TYPE_CONVERSION = "type_conversion"
    NULL_CHECK = "null_check"
    BOUNDS_CHECK = "bounds_check"
    OPERATOR_FIX = "operator_fix"
    SYNTAX_FIX = "syntax_fix"
    LOGIC_FIX = "logic_fix"
    ERROR_HANDLING = "error_handling"
    VARIABLE_RENAME = "variable_rename"
    IMPORT_FIX = "import_fix"
    ATTRIBUTE_FIX = "attribute_fix"


@dataclass
class FixStrategy:
    """A proposed fix for an error"""
    fix_type: FixType               # Type of fix
    description: str                # Human-readable description
    code_change: str                # The actual code change
    complexity: int                 # 1=simple, 2=medium, 3=hard
    confidence: float               # Confidence this fix will work [0, 1]
    reasoning: str                  # Why this fix was suggested
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "fix_type": self.fix_type.value,
            "description": self.description,
            "code_change": self.code_change,
            "complexity": self.complexity,
            "confidence": round(float(self.confidence), 4),
            "reasoning": self.reasoning
        }


@dataclass
class RankedFix:
    """A fix with ranking score"""
    fix: FixStrategy
    ranking_score: float            # Final ranking score [0, 100]
    ml_confidence_component: float  # Component from ML confidence
    success_rate_component: float   # Component from historical success
    complexity_component: float     # Component from complexity
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "fix": self.fix.to_dict(),
            "ranking_score": round(self.ranking_score, 2),
            "breakdown": {
                "ml_confidence": round(self.ml_confidence_component, 2),
                "success_rate": round(self.success_rate_component, 2),
                "complexity": round(self.complexity_component, 2),
            }
        }


# ============================================================================
# FIX GENERATOR
# ============================================================================

class FixGenerator:
    """
    Generates multiple fix strategies based on error type.
    
    Each error type triggers specific fix templates that address
    common causes of that error.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize fix generator"""
        self.logger = logger or logging.getLogger(__name__)
    
    def generate_fixes(
        self,
        error_type: str,
        error_message: str,
        code_snippet: str,
        line_number: Optional[int] = None
    ) -> List[FixStrategy]:
        """
        Generate possible fixes for an error.
        
        Args:
            error_type: Type of error (e.g., "TypeError")
            error_message: Error message text
            code_snippet: Code around error
            line_number: Line number of error
            
        Returns:
            List of FixStrategy objects
        """
        self.logger.info(f"Generating fixes for {error_type}")
        
        # Route to specific generator based on error type
        fixes = {
            "SyntaxError": self._generate_syntax_fixes,
            "TypeError": self._generate_type_fixes,
            "ValueError": self._generate_value_fixes,
            "NameError": self._generate_name_fixes,
            "IndexError": self._generate_index_fixes,
            "KeyError": self._generate_key_fixes,
            "AttributeError": self._generate_attribute_fixes,
            "ZeroDivisionError": self._generate_division_fixes,
            "RuntimeError": self._generate_runtime_fixes,
            "LogicError": self._generate_logic_fixes,
            "IndentationError": self._generate_indentation_fixes,
            "ImportError": self._generate_import_fixes,
        }.get(error_type, self._generate_generic_fixes)
        
        return fixes(error_message, code_snippet, line_number)
    
    # ========================================================================
    # SPECIFIC ERROR FIX GENERATORS
    # ========================================================================
    
    def _generate_syntax_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for SyntaxError"""
        fixes = []
        
        msg_lower = error_msg.lower()
        
        # Missing colon
        if "colon" in msg_lower or ":" in msg_lower:
            fixes.append(FixStrategy(
                fix_type=FixType.SYNTAX_FIX,
                description="Add missing colon",
                code_change="Add ':' at end of if/for/while/def/class statement",
                complexity=COMPLEXITY_SIMPLE,
                confidence=0.95,
                reasoning="Most syntax errors involve missing colons in Python"
            ))
        
        # Indentation
        if "indent" in msg_lower:
            fixes.append(FixStrategy(
                fix_type=FixType.SYNTAX_FIX,
                description="Fix indentation",
                code_change="Align code blocks with consistent indentation",
                complexity=COMPLEXITY_SIMPLE,
                confidence=0.90,
                reasoning="Indentation errors common in Python"
            ))
        
        # Unexpected token
        if "unexpected" in msg_lower:
            fixes.append(FixStrategy(
                fix_type=FixType.SYNTAX_FIX,
                description="Remove or fix unexpected token",
                code_change="Review and correct syntax around error line",
                complexity=COMPLEXITY_MEDIUM,
                confidence=0.80,
                reasoning="Unknown token requires manual review"
            ))
        
        # Missing parentheses
        if "(" in msg_lower or ")" in msg_lower:
            fixes.append(FixStrategy(
                fix_type=FixType.SYNTAX_FIX,
                description="Add/fix parentheses",
                code_change="Ensure all parentheses are balanced",
                complexity=COMPLEXITY_SIMPLE,
                confidence=0.85,
                reasoning="Mismatched or missing parentheses"
            ))
        
        return fixes if fixes else [self._generic_fix_strategy()]
    
    def _generate_type_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for TypeError"""
        fixes = []
        
        # String + int
        if ("str" in error_msg and "int" in error_msg) or \
           ("str" and "+" in code):
            fixes.append(FixStrategy(
                fix_type=FixType.TYPE_CONVERSION,
                description="Convert types before operation",
                code_change="Use str() or int() to convert: str(x) or int(x)",
                complexity=COMPLEXITY_SIMPLE,
                confidence=0.92,
                reasoning="String-integer concatenation requires conversion"
            ))
        
        # Call non-callable
        if "not callable" in error_msg or "call" in error_msg:
            fixes.append(FixStrategy(
                fix_type=FixType.SYNTAX_FIX,
                description="Remove parentheses or fix function call",
                code_change="Either remove () if not a function, or add () if it is",
                complexity=COMPLEXITY_SIMPLE,
                confidence=0.85,
                reasoning="Trying to call non-callable object"
            ))
        
        # Unsupported operation
        fixes.append(FixStrategy(
            fix_type=FixType.TYPE_CONVERSION,
            description="Add type conversion",
            code_change="Convert operands to compatible types",
            complexity=COMPLEXITY_MEDIUM,
            confidence=0.80,
            reasoning="Type mismatch in operation"
        ))
        
        return fixes
    
    def _generate_value_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for ValueError"""
        fixes = []
        
        # Invalid literal
        if "invalid literal" in error_msg:
            fixes.append(FixStrategy(
                fix_type=FixType.ERROR_HANDLING,
                description="Add validation/try-except",
                code_change="Wrap in try-except or validate input before conversion",
                complexity=COMPLEXITY_MEDIUM,
                confidence=0.88,
                reasoning="Input value cannot be converted to target type"
            ))
        
        # Out of range
        if "out of range" in error_msg or "range" in error_msg:
            fixes.append(FixStrategy(
                fix_type=FixType.BOUNDS_CHECK,
                description="Check value is in valid range",
                code_change="Add condition: if min_val <= x <= max_val",
                complexity=COMPLEXITY_SIMPLE,
                confidence=0.85,
                reasoning="Value is outside acceptable range"
            ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.ERROR_HANDLING,
            description="Use try-except for error handling",
            code_change="try:\\n    # code\\nexcept ValueError:\\n    # handle",
            complexity=COMPLEXITY_MEDIUM,
            confidence=0.80,
            reasoning="Catch ValueError and handle gracefully"
        ))
        
        return fixes
    
    def _generate_name_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for NameError"""
        fixes = []
        
        fixes.append(FixStrategy(
            fix_type=FixType.VARIABLE_RENAME,
            description="Define variable before use",
            code_change="Add variable assignment before first use",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.90,
            reasoning="Variable used but never defined"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.VARIABLE_RENAME,
            description="Check variable spelling",
            code_change="Verify variable name matches definition",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.85,
            reasoning="Typo in variable name"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.IMPORT_FIX,
            description="Add missing import",
            code_change="Add: from module import name",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.80,
            reasoning="Name may be from unimported module"
        ))
        
        return fixes
    
    def _generate_index_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for IndexError"""
        fixes = []
        
        fixes.append(FixStrategy(
            fix_type=FixType.BOUNDS_CHECK,
            description="Check list length before access",
            code_change="if idx < len(list): # safe access",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.92,
            reasoning="Accessing list index out of bounds"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.ERROR_HANDLING,
            description="Use try-except for index access",
            code_change="try: x = list[idx] \\nexcept IndexError: x = None",
            complexity=COMPLEXITY_MEDIUM,
            confidence=0.85,
            reasoning="Safely handle out-of-bounds access"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.LOGIC_FIX,
            description="Fix loop bounds",
            code_change="for i in range(len(list)): # not beyond length",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.88,
            reasoning="Loop index exceeds list length"
        ))
        
        return fixes
    
    def _generate_key_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for KeyError"""
        fixes = []
        
        fixes.append(FixStrategy(
            fix_type=FixType.NULL_CHECK,
            description="Check if key exists before access",
            code_change="if key in dict: # safe access",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.90,
            reasoning="Dictionary key doesn't exist"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.LOGIC_FIX,
            description="Use dict.get() with default value",
            code_change="value = dict.get(key, default_value)",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.92,
            reasoning="Safe dictionary access with fallback"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.ERROR_HANDLING,
            description="Use try-except for key access",
            code_change="try: x = dict[key] \\nexcept KeyError: x = None",
            complexity=COMPLEXITY_MEDIUM,
            confidence=0.85,
            reasoning="Catch missing key error"
        ))
        
        return fixes
    
    def _generate_attribute_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for AttributeError"""
        fixes = []
        
        fixes.append(FixStrategy(
            fix_type=FixType.ATTRIBUTE_FIX,
            description="Check if attribute exists",
            code_change="if hasattr(obj, 'attr'): # safe access",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.88,
            reasoning="Object doesn't have expected attribute"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.ATTRIBUTE_FIX,
            description="Use getattr with default",
            code_change="value = getattr(obj, 'attr', default)",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.90,
            reasoning="Safe attribute access with fallback"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.VARIABLE_RENAME,
            description="Check attribute name spelling",
            code_change="Verify attribute name is correct",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.80,
            reasoning="Typo in attribute name"
        ))
        
        return fixes
    
    def _generate_division_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for ZeroDivisionError"""
        fixes = []
        
        fixes.append(FixStrategy(
            fix_type=FixType.NULL_CHECK,
            description="Check denominator before division",
            code_change="if denominator != 0: result = numerator / denominator",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.95,
            reasoning="Most reliable fix for division by zero"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.ERROR_HANDLING,
            description="Use try-except for division",
            code_change="try: x = a/b \\nexcept ZeroDivisionError: x = 0",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.92,
            reasoning="Handle division by zero gracefully"
        ))
        
        return fixes
    
    def _generate_runtime_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for RuntimeError"""
        fixes = []
        
        fixes.append(FixStrategy(
            fix_type=FixType.ERROR_HANDLING,
            description="Add error handling",
            code_change="Wrap code in try-except block",
            complexity=COMPLEXITY_MEDIUM,
            confidence=0.70,
            reasoning="Generic runtime error handling"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.LOGIC_FIX,
            description="Review algorithm logic",
            code_change="Debug and fix algorithmic issues",
            complexity=COMPLEXITY_HIGH,
            confidence=0.65,
            reasoning="May require logic review"
        ))
        
        return fixes
    
    def _generate_logic_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for LogicError"""
        fixes = []
        
        fixes.append(FixStrategy(
            fix_type=FixType.LOGIC_FIX,
            description="Review algorithm implementation",
            code_change="Debug logic and adjust algorithm",
            complexity=COMPLEXITY_HIGH,
            confidence=0.70,
            reasoning="Logic error requires algorithmic review"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.BOUNDS_CHECK,
            description="Check edge cases",
            code_change="Test boundary conditions and special cases",
            complexity=COMPLEXITY_MEDIUM,
            confidence=0.75,
            reasoning="May be edge case handling issue"
        ))
        
        return fixes
    
    def _generate_indentation_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for IndentationError"""
        fixes = []
        
        fixes.append(FixStrategy(
            fix_type=FixType.SYNTAX_FIX,
            description="Fix inconsistent indentation",
            code_change="Use consistent indentation (4 spaces or tabs)",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.93,
            reasoning="Python requires consistent indentation"
        ))
        
        return fixes
    
    def _generate_import_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate fixes for ImportError"""
        fixes = []
        
        fixes.append(FixStrategy(
            fix_type=FixType.IMPORT_FIX,
            description="Add missing import",
            code_change="import module or from module import name",
            complexity=COMPLEXITY_SIMPLE,
            confidence=0.90,
            reasoning="Module not imported"
        ))
        
        fixes.append(FixStrategy(
            fix_type=FixType.IMPORT_FIX,
            description="Install missing package",
            code_change="pip install missing_package",
            complexity=COMPLEXITY_MEDIUM,
            confidence=0.85,
            reasoning="Package not installed"
        ))
        
        return fixes
    
    def _generate_generic_fixes(
        self, error_msg: str, code: str, line: Optional[int]
    ) -> List[FixStrategy]:
        """Generate generic fixes for unknown error types"""
        return [
            FixStrategy(
                fix_type=FixType.ERROR_HANDLING,
                description="Add error handling",
                code_change="Wrap in try-except block",
                complexity=COMPLEXITY_MEDIUM,
                confidence=0.60,
                reasoning="Generic error handling approach"
            )
        ]
    
    def _generic_fix_strategy(self) -> FixStrategy:
        """Create a generic fix strategy"""
        return FixStrategy(
            fix_type=FixType.ERROR_HANDLING,
            description="Add error handling",
            code_change="Wrap in try-except block",
            complexity=COMPLEXITY_MEDIUM,
            confidence=0.60,
            reasoning="Generic error handling"
        )


# ============================================================================
# FIX RANKER
# ============================================================================

class FixRanker:
    """
    Ranks fixes based on multiple factors.
    
    Scoring formula:
    score = (ml_conf * W1) + (success_rate * W2) + ((1 - complexity/3) * W3)
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize ranker"""
        self.logger = logger or logging.getLogger(__name__)
    
    def rank_fixes(
        self,
        fixes: List[FixStrategy],
        ml_confidence: float = 0.8,
        historical_success_rates: Dict[str, float] = None
    ) -> List[RankedFix]:
        """
        Rank fixes by likelihood of success.
        
        Args:
            fixes: List of FixStrategy objects
            ml_confidence: Confidence from ML classifier [0, 1]
            historical_success_rates: Dict of fix_type -> success_rate
            
        Returns:
            List of RankedFix objects, sorted by score (best first)
        """
        if not fixes:
            return []
        
        if historical_success_rates is None:
            historical_success_rates = {}
        
        ranked = []
        
        for fix in fixes:
            # Component 1: ML confidence (use fix's confidence * ML confidence)
            ml_component = (fix.confidence * ml_confidence) * 100 * WEIGHT_ML_CONFIDENCE
            
            # Component 2: Historical success rate
            success_rate = historical_success_rates.get(
                fix.fix_type.value, 0.5  # Default 50% if no history
            )
            success_component = success_rate * 100 * WEIGHT_HISTORICAL_SUCCESS
            
            # Component 3: Inverse of complexity (lower complexity is better)
            complexity_component = (
                (1.0 - (fix.complexity / 3.0)) * 100 * WEIGHT_COMPLEXITY
            )
            
            # Total score
            total_score = ml_component + success_component + complexity_component
            
            ranked.append(RankedFix(
                fix=fix,
                ranking_score=total_score,
                ml_confidence_component=ml_component,
                success_rate_component=success_component,
                complexity_component=complexity_component
            ))
        
        # Sort by score (highest first)
        ranked.sort(key=lambda x: x.ranking_score, reverse=True)
        
        self.logger.info(f"Ranked {len(ranked)} fixes")
        for i, rf in enumerate(ranked[:3]):
            self.logger.info(
                f"  {i+1}. {rf.fix.description}: {rf.ranking_score:.2f}"
            )
        
        return ranked


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def generate_and_rank_fixes(
    error_type: str,
    error_message: str,
    code: str,
    line: Optional[int] = None,
    ml_confidence: float = 0.8
) -> List[RankedFix]:
    """Generate and rank fixes for an error"""
    generator = FixGenerator()
    ranker = FixRanker()
    
    fixes = generator.generate_fixes(error_type, error_message, code, line)
    ranked = ranker.rank_fixes(fixes, ml_confidence)
    
    return ranked


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test fix generation
    ranked_fixes = generate_and_rank_fixes(
        error_type="TypeError",
        error_message="unsupported operand type(s) for +: 'int' and 'str'",
        code="x = 5 + 'hello'",
        ml_confidence=0.92
    )
    
    print("\nGenerated Fixes (ranked):")
    for i, rf in enumerate(ranked_fixes[:3], 1):
        print(f"\n{i}. {rf.fix.description}")
        print(f"   Score: {rf.ranking_score:.2f}")
        print(f"   Change: {rf.fix.code_change}")
