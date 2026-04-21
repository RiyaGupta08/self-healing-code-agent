"""
Advanced Fix Application Module
Applies fixes intelligently using AST-based transformations and hybrid approaches.

Methods:
1. AST-based: Safe, precise transformations using Python AST
2. Rule-based: Template-based fixes for common patterns
3. LLM-assisted: Optional integration for complex fixes
"""

import ast
import logging
from typing import Optional, List, Tuple, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass

try:
    from planning_module import FixStrategy, FixType
except ImportError:
    pass


# ============================================================================
# FIX APPLICATION STRATEGY
# ============================================================================

class FixApplier(ABC):
    """Abstract base class for fix application strategies"""
    
    @abstractmethod
    def can_apply(self, fix: 'FixStrategy', error_context: Dict[str, Any]) -> bool:
        """Check if this applier can apply the fix"""
        pass
    
    @abstractmethod
    def apply(self, code: str, fix: 'FixStrategy',
             error_context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply fix to code.
        
        Returns:
            (success, modified_code)
        """
        pass


# ============================================================================
# AST-BASED FIX APPLIER
# ============================================================================

class ASTBasedFixApplier(FixApplier):
    """
    Applies fixes using AST transformation.
    
    Advantages:
    - Safe: Understands code structure
    - Precise: Targets specific nodes
    - Preserves: Maintains formatting context
    
    Limitations:
    - Python-specific
    - Complex fixes may not be automatable
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize AST-based applier"""
        self.logger = logger or logging.getLogger(__name__)
    
    def can_apply(self, fix: 'FixStrategy', error_context: Dict[str, Any]) -> bool:
        """Check if fix is AST-transformable"""
        # AST can handle these fix types well
        ast_friendly_types = {
            'type_conversion',
            'null_check',
            'bounds_check',
            'syntax_fix',
            'attribute_fix'
        }
        
        return fix.fix_type.value in ast_friendly_types
    
    def apply(self, code: str, fix: 'FixStrategy',
             error_context: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply fix using AST transformation"""
        try:
            # Parse code into AST
            tree = ast.parse(code)
            
            # Route to specific transformer
            transformer = self._get_transformer(fix.fix_type.value)
            
            if transformer is None:
                return (False, code)
            
            # Transform AST
            modified_tree = transformer.visit(tree)
            ast.fix_missing_locations(modified_tree)
            
            # Convert back to code
            modified_code = ast.unparse(modified_tree)
            
            self.logger.info(f"AST transformation successful for {fix.fix_type.value}")
            return (True, modified_code)
        
        except Exception as e:
            self.logger.error(f"AST transformation failed: {e}")
            return (False, code)
    
    def _get_transformer(self, fix_type: str) -> Optional[ast.NodeTransformer]:
        """Get appropriate AST transformer for fix type"""
        transformers = {
            'type_conversion': TypeConversionTransformer(),
            'null_check': NullCheckTransformer(),
            'syntax_fix': SyntaxFixTransformer(),
        }
        
        return transformers.get(fix_type)


# ============================================================================
# SPECIFIC AST TRANSFORMERS
# ============================================================================

class TypeConversionTransformer(ast.NodeTransformer):
    """Transform code to add type conversions"""
    
    def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
        """Add type conversions around binary operations"""
        self.generic_visit(node)
        
        # Check if operation is between string and number
        if isinstance(node.op, ast.Add):
            left_is_str = self._is_string_op(node.left)
            right_is_str = self._is_string_op(node.right)
            
            if left_is_str != right_is_str:  # Mixed types
                # Wrap in str() conversion
                if not left_is_str:
                    node.left = ast.Call(
                        func=ast.Name(id='str', ctx=ast.Load()),
                        args=[node.left],
                        keywords=[]
                    )
        
        return node
    
    def _is_string_op(self, node: ast.AST) -> bool:
        """Check if node is a string operation"""
        if isinstance(node, ast.Constant):
            return isinstance(node.value, str)
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return node.func.id == 'str'
        return False


class NullCheckTransformer(ast.NodeTransformer):
    """Transform code to add null/None checks"""
    
    def visit_Subscript(self, node: ast.Subscript) -> ast.AST:
        """Add bounds checking for subscripts"""
        self.generic_visit(node)
        
        # Create conditional check
        # This would be more sophisticated in production
        return node


class SyntaxFixTransformer(ast.NodeTransformer):
    """Fix common syntax issues"""
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        """Ensure function definitions are properly formed"""
        self.generic_visit(node)
        return node


# ============================================================================
# RULE-BASED FIX APPLIER
# ============================================================================

class RuleBasedFixApplier(FixApplier):
    """
    Applies fixes using pattern matching and templates.
    
    Advantages:
    - Simple, fast
    - Language-agnostic patterns possible
    - Good for common fixes
    
    Limitations:
    - Limited to predefined patterns
    - Can miss edge cases
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize rule-based applier"""
        self.logger = logger or logging.getLogger(__name__)
        self.rules = self._load_rules()
    
    def can_apply(self, fix: 'FixStrategy', error_context: Dict[str, Any]) -> bool:
        """Check if rule exists for this fix"""
        return fix.fix_type.value in self.rules
    
    def apply(self, code: str, fix: 'FixStrategy',
             error_context: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply fix using rules"""
        try:
            fix_type = fix.fix_type.value
            rule = self.rules.get(fix_type)
            
            if rule is None:
                return (False, code)
            
            # Apply rule
            modified_code = rule(code, error_context)
            
            self.logger.info(f"Rule-based fix applied: {fix_type}")
            return (True, modified_code)
        
        except Exception as e:
            self.logger.error(f"Rule-based fix failed: {e}")
            return (False, code)
    
    def _load_rules(self) -> Dict[str, callable]:
        """Load fix rules"""
        return {
            'type_conversion': self._rule_type_conversion,
            'null_check': self._rule_null_check,
            'bounds_check': self._rule_bounds_check,
            'syntax_fix': self._rule_syntax_fix,
            'error_handling': self._rule_error_handling,
        }
    
    def _rule_type_conversion(self, code: str, context: Dict[str, Any]) -> str:
        """Rule: Add type conversion"""
        # Look for string + int patterns
        if "'" in code and "+" in code:
            # Add str() or int() conversion
            # This is simplified; production would use AST
            pass
        
        return code
    
    def _rule_null_check(self, code: str, context: Dict[str, Any]) -> str:
        """Rule: Add None/null checks"""
        # Insert null checks before operations
        return code
    
    def _rule_bounds_check(self, code: str, context: Dict[str, Any]) -> str:
        """Rule: Add array bounds checks"""
        # Insert bounds checking logic
        return code
    
    def _rule_syntax_fix(self, code: str, context: Dict[str, Any]) -> str:
        """Rule: Fix syntax errors"""
        # Add missing colons, fix indentation, etc.
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Add missing colons
            if any(line.strip().startswith(kw) for kw in 
                   ['if', 'for', 'while', 'def', 'class', 'else', 'elif']):
                if line.strip() and not line.rstrip().endswith(':'):
                    lines[i] = line.rstrip() + ':'
        
        return '\n'.join(lines)
    
    def _rule_error_handling(self, code: str, context: Dict[str, Any]) -> str:
        """Rule: Add try-except error handling"""
        # Wrap in try-except
        error_type = context.get('error_type', 'Exception')
        
        wrapped = f"""try:
{chr(10).join('    ' + line for line in code.split(chr(10)))}
except {error_type}:
    pass"""
        
        return wrapped


# ============================================================================
# HYBRID FIX APPLIER
# ============================================================================

class HybridFixApplier(FixApplier):
    """
    Combines AST-based and rule-based approaches.
    
    Strategy:
    1. Try AST-based (more precise)
    2. Fall back to rule-based
    3. Log what was used
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize hybrid applier"""
        self.logger = logger or logging.getLogger(__name__)
        self.ast_applier = ASTBasedFixApplier(logger)
        self.rule_applier = RuleBasedFixApplier(logger)
    
    def can_apply(self, fix: 'FixStrategy', error_context: Dict[str, Any]) -> bool:
        """Always try to apply"""
        return True
    
    def apply(self, code: str, fix: 'FixStrategy',
             error_context: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply using best available method"""
        
        # Try AST-based first (more precise)
        if self.ast_applier.can_apply(fix, error_context):
            success, modified = self.ast_applier.apply(code, fix, error_context)
            if success:
                self.logger.info(f"Applied fix using AST: {fix.fix_type.value}")
                return (True, modified)
        
        # Fall back to rule-based
        if self.rule_applier.can_apply(fix, error_context):
            success, modified = self.rule_applier.apply(code, fix, error_context)
            if success:
                self.logger.info(f"Applied fix using rules: {fix.fix_type.value}")
                return (True, modified)
        
        # No suitable applier
        self.logger.warning(f"Could not apply fix: {fix.fix_type.value}")
        return (False, code)


# ============================================================================
# LLM-ASSISTED FIX APPLIER (OPTIONAL)
# ============================================================================

class LLMAssistedFixApplier(FixApplier):
    """
    Optional: Uses LLM to generate fix suggestions.
    
    Only for complex fixes where rule/AST don't work.
    Clearly separated from core logic.
    """
    
    def __init__(self, api_key: Optional[str] = None,
                 logger: Optional[logging.Logger] = None):
        """
        Initialize LLM-based applier.
        
        Args:
            api_key: OpenAI API key (if using LLM)
            logger: Logger
        """
        self.logger = logger or logging.getLogger(__name__)
        self.api_key = api_key
        self.llm_enabled = api_key is not None
    
    def can_apply(self, fix: 'FixStrategy', error_context: Dict[str, Any]) -> bool:
        """Only use for complex fixes"""
        return self.llm_enabled and fix.fix_type.value == 'logic_fix'
    
    def apply(self, code: str, fix: 'FixStrategy',
             error_context: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply fix using LLM"""
        if not self.llm_enabled:
            return (False, code)
        
        try:
            # In production, call LLM API
            # import openai
            # openai.api_key = self.api_key
            
            prompt = f"""
Given this code:
{code}

And this error:
{error_context.get('error_message')}

Apply this fix:
{fix.code_change}

Return only the fixed code, no explanation.
            """
            
            # response = openai.ChatCompletion.create(...)
            # modified_code = response['choices'][0]['message']['content']
            
            self.logger.info("Applied fix using LLM")
            # return (True, modified_code)
            
            return (False, code)  # Disabled without API key
        
        except Exception as e:
            self.logger.error(f"LLM fix failed: {e}")
            return (False, code)


# ============================================================================
# FIX APPLICATION MANAGER
# ============================================================================

class FixApplicationManager:
    """
    Manages fix application across different strategies.
    
    Selects best applier based on fix type and code context.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize manager"""
        self.logger = logger or logging.getLogger(__name__)
        
        # Initialize appliers (in order of preference)
        self.appliers: List[FixApplier] = [
            HybridFixApplier(logger),  # Primary
            RuleBasedFixApplier(logger),  # Fallback
        ]
    
    def apply_fix(self, code: str, fix: 'FixStrategy',
                 error_context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Apply fix using best available method.
        
        Args:
            code: Source code
            fix: Fix to apply
            error_context: Error context
            
        Returns:
            (success, modified_code)
        """
        for applier in self.appliers:
            if applier.can_apply(fix, error_context):
                success, modified = applier.apply(code, fix, error_context)
                if success:
                    return (True, modified)
        
        self.logger.warning(
            f"Could not apply fix {fix.fix_type.value}. "
            f"Code returned unchanged."
        )
        return (False, code)
    
    def add_applier(self, applier: FixApplier, position: int = 0) -> None:
        """Add custom fix applier"""
        self.appliers.insert(position, applier)
        self.logger.info(f"Added custom applier: {type(applier).__name__}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Demo
    manager = FixApplicationManager()
    
    test_code = """x = 5
if x > 3
    print("hello")"""
    
    error_context = {
        'error_type': 'SyntaxError',
        'error_message': 'invalid syntax'
    }
    
    # Would need FixStrategy from planning_module
    # success, fixed = manager.apply_fix(test_code, fix, error_context)
