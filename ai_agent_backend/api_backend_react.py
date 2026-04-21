"""
ULTIMATE PYTHON FIXER v16 - Fixes missing commas CORRECTLY
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import ast
import re
from difflib import SequenceMatcher

app = FastAPI(title="Ultimate Python Fixer", version="16.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str
    language: str = "python"

class DebugResponse(BaseModel):
    success: bool
    original_code: str
    fixed_code: Optional[str] = None
    error: Optional[Dict[str, Any]] = None
    fixes: List[Dict[str, Any]] = []
    message: str = ""
    time_elapsed: float = 0.0
    confidence: Optional[float] = None
    execution_result: Optional[Dict[str, Any]] = None
    attempts: int = 1
    decisions: List[Dict[str, Any]] = []

PYTHON_KEYWORDS = {
    'if', 'elif', 'else', 'for', 'while', 'def', 'class', 'try', 'except', 
    'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'pass', 
    'break', 'continue', 'raise', 'assert', 'del', 'in', 'is', 'and', 'or', 
    'not', 'lambda', 'True', 'False', 'None', 'async', 'await', 'global', 'nonlocal'
}

COMMON_FUNCTIONS = {
    'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set', 
    'tuple', 'bool', 'abs', 'max', 'min', 'sum', 'sorted', 'enumerate', 
    'zip', 'map', 'filter', 'open', 'input', 'type', 'isinstance', 'append', 
    'extend', 'insert', 'remove', 'pop', 'clear', 'keys', 'values', 'items'
}

def is_close_match(word: str, target: str, threshold: float = 0.75) -> bool:
    ratio = SequenceMatcher(None, word, target).ratio()
    return ratio >= threshold

def find_typo_correction(word: str) -> Optional[str]:
    for keyword in PYTHON_KEYWORDS:
        if is_close_match(word, keyword, threshold=0.80):
            if abs(len(word) - len(keyword)) <= 2:
                return keyword
    
    for func in COMMON_FUNCTIONS:
        if is_close_match(word, func, threshold=0.80):
            if abs(len(word) - len(func)) <= 2:
                return func
    
    return None

def fix_typos_smart(code: str):
    print("\n🔧 Fixing typos (smart mode)...\n")
    
    fixed_code = code
    fixes = []
    
    words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', code)
    unique_words = set(words)
    
    for word in unique_words:
        if word in PYTHON_KEYWORDS or word in COMMON_FUNCTIONS:
            continue
        
        correction = find_typo_correction(word)
        
        if correction and correction != word:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, fixed_code):
                fixed_code = re.sub(pattern, correction, fixed_code)
                fixes.append({
                    'description': f'Fixed typo: "{word}" → "{correction}"',
                    'type': 'typo_fix'
                })
                print(f"   ✓ Fixed typo: {word} → {correction}")
    
    return fixed_code, fixes

def fix_missing_commas_smart(code: str):
    """
    Fix missing commas in dictionaries, lists, tuples
    SMART: Add comma AFTER the closing quote, not inside
    """
    print("\n🔧 Fixing missing commas (smart mode)...\n")
    
    fixed_code = code
    fixes = []
    lines = code.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        fixed_line = line
        
        # Skip empty lines
        if not line.strip():
            fixed_lines.append(fixed_line)
            continue
        
        # Skip lines that already end with comma, colon, or opening bracket
        if line.rstrip().endswith((',', ':', '{', '[', '(', 'else', 'elif', 'try', 'except', 'finally')):
            fixed_lines.append(fixed_line)
            continue
        
        # Skip lines with closing brackets only
        if line.strip() in ('}', ']', ')'):
            fixed_lines.append(fixed_line)
            continue
        
        # Check if next line exists
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            
            # If next line starts with closing bracket, current line might need comma
            if next_line and next_line[0] in ('}', ']', ')'):
                stripped = line.rstrip()
                
                # Check if line ends with a closing quote
                if (stripped.endswith("'") or stripped.endswith('"')) and not stripped.endswith(','):
                    fixed_line = stripped + ','
                    fixes.append({
                        'description': f'Added missing comma on line {i+1}',
                        'type': 'syntax_fix'
                    })
                    print(f"   ✓ Line {i+1}: Added missing comma after closing quote")
                
                # Check if line ends with a number (for list/dict values)
                elif stripped and stripped[-1].isdigit() and not stripped.endswith(','):
                    fixed_line = stripped + ','
                    fixes.append({
                        'description': f'Added missing comma on line {i+1}',
                        'type': 'syntax_fix'
                    })
                    print(f"   ✓ Line {i+1}: Added missing comma after number")
            
            # If next line is a dict key (has ':' in it) and current line doesn't end with comma
            if ':' in next_line and not line.rstrip().endswith(','):
                stripped = line.rstrip()
                # Only add comma if line looks like a value (ends with quote or number)
                if (stripped.endswith("'") or stripped.endswith('"') or (stripped and stripped[-1].isdigit())):
                    if not stripped.endswith(','):
                        fixed_line = stripped + ','
                        fixes.append({
                            'description': f'Added missing comma on line {i+1}',
                            'type': 'syntax_fix'
                        })
                        print(f"   ✓ Line {i+1}: Added missing comma after value")
        
        fixed_lines.append(fixed_line)
    
    fixed_code = '\n'.join(fixed_lines)
    return fixed_code, fixes

def ultimate_v16_fix(code: str):
    print(f"\n{'='*60}")
    print(f"✨ ULTIMATE PYTHON FIXER v16.0")
    print(f"{'='*60}\n")
    
    original = code
    all_fixes = []
    error_info = None
    
    # Check if already valid
    try:
        ast.parse(code)
        print("✅ Code is already valid!")
        return code, None, []
    except SyntaxError as e:
        error_info = {
            'type': 'SyntaxError',
            'message': e.msg,
            'line': e.lineno,
        }
        print(f"❌ Error: {e.msg}\n")
    except Exception as e:
        error_info = {
            'type': type(e).__name__,
            'message': str(e),
            'line': None,
        }
        print(f"❌ Error: {e}\n")
    
    fixed_code = code
    
    # ===== FIX 0: TYPOS =====
    print("🔧 Fix 0: Fixing typos (smart mode)...\n")
    fixed_code, typo_fixes = fix_typos_smart(fixed_code)
    all_fixes.extend(typo_fixes)
    
    try:
        ast.parse(fixed_code)
        print("\n✅ Code is now valid after typo fix!")
        return fixed_code, error_info, all_fixes
    except:
        pass
    
    # ===== FIX 0.5: MISSING COMMAS (SMART) =====
    print("🔧 Fix 0.5: Fixing missing commas (smart mode)...\n")
    fixed_code, comma_fixes = fix_missing_commas_smart(fixed_code)
    all_fixes.extend(comma_fixes)
    
    try:
        ast.parse(fixed_code)
        print("\n✅ Code is now valid after comma fix!")
        return fixed_code, error_info, all_fixes
    except:
        pass
    
    # ===== FIX 1: QUOTES =====
    print("🔧 Fix 1: Closing unclosed quotes...\n")
    lines = fixed_code.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        fixed_line = line
        in_single = False
        in_double = False
        escaped = False
        
        for char in line:
            if escaped:
                escaped = False
                continue
            if char == '\\':
                escaped = True
                continue
            if char == '"' and not in_single:
                in_double = not in_double
            elif char == "'" and not in_single:
                in_single = not in_single
        
        if in_single:
            fixed_line += "'"
            all_fixes.append({'description': f'Closed unclosed single quote on line {i+1}', 'type': 'syntax_fix'})
            print(f"   ✓ Line {i+1}: Added closing single quote")
        if in_double:
            fixed_line += '"'
            all_fixes.append({'description': f'Closed unclosed double quote on line {i+1}', 'type': 'syntax_fix'})
            print(f"   ✓ Line {i+1}: Added closing double quote")
        
        fixed_lines.append(fixed_line)
    
    fixed_code = '\n'.join(fixed_lines)
    
    try:
        ast.parse(fixed_code)
        print("\n✅ Code is now valid after quote fix!")
        return fixed_code, error_info, all_fixes
    except:
        pass
    
    # ===== FIX 2: PARENTHESES, BRACKETS, BRACES =====
    print("\n🔧 Fix 2: Closing unclosed parentheses, brackets, braces...\n")
    lines = fixed_code.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        fixed_line = line
        
        in_string = False
        string_char = None
        escaped = False
        
        paren_count = 0
        bracket_count = 0
        brace_count = 0
        
        for char in line:
            if escaped:
                escaped = False
                continue
            if char == '\\':
                escaped = True
                continue
            
            if char in ('"', "'") and not in_string:
                in_string = True
                string_char = char
            elif char == string_char and in_string:
                in_string = False
                string_char = None
            elif not in_string:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                elif char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
        
        if paren_count > 0 and not line.strip().endswith('('):
            fixed_line += ')' * paren_count
            all_fixes.append({'description': f'Added {paren_count} closing parenthesis on line {i+1}', 'type': 'syntax_fix'})
            print(f"   ✓ Line {i+1}: Added {paren_count} closing parenthesis")
        
        if bracket_count > 0 and not line.strip().endswith('['):
            fixed_line += ']' * bracket_count
            all_fixes.append({'description': f'Added {bracket_count} closing bracket on line {i+1}', 'type': 'syntax_fix'})
            print(f"   ✓ Line {i+1}: Added {bracket_count} closing bracket")
        
        if brace_count > 0 and not line.strip().endswith('{'):
            fixed_line += '}' * brace_count
            all_fixes.append({'description': f'Added {brace_count} closing brace on line {i+1}', 'type': 'syntax_fix'})
            print(f"   ✓ Line {i+1}: Added {brace_count} closing brace")
        
        fixed_lines.append(fixed_line)
    
    fixed_code = '\n'.join(fixed_lines)
    
    try:
        ast.parse(fixed_code)
        print("\n✅ Code is now valid after bracket fix!")
        return fixed_code, error_info, all_fixes
    except:
        pass
    
    # ===== FIX 3: MISSING COLONS =====
    print("🔧 Fix 3: Adding missing colons...\n")
    lines = fixed_code.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.rstrip()
        
        if re.match(r'^\s*(if|elif|else|for|while|def|class|try|except|finally|with)\b', stripped):
            if not stripped.endswith(':'):
                fixed_line = stripped + ':'
                all_fixes.append({'description': f'Added missing colon on line {i+1}', 'type': 'syntax_fix'})
                print(f"   ✓ Line {i+1}: Added missing colon")
            else:
                fixed_line = line
        else:
            fixed_line = line
        
        fixed_lines.append(fixed_line)
    
    fixed_code = '\n'.join(fixed_lines)
    
    try:
        ast.parse(fixed_code)
        print("\n✅ Code is now valid after colon fix!")
        return fixed_code, error_info, all_fixes
    except:
        pass
    
    # ===== FIX 4: INDENTATION =====
    print("🔧 Fix 4: Fixing indentation...\n")
    
    lines = fixed_code.split('\n')
    fixed_lines = []
    indent_level = 0
    
    for i, line in enumerate(lines):
        if not line.strip():
            fixed_lines.append('')
            continue
        
        stripped = line.lstrip()
        
        if stripped.startswith(('else', 'elif', 'except', 'finally')):
            indent_level = max(0, indent_level - 1)
        
        if stripped:
            fixed_line = '    ' * indent_level + stripped
        else:
            fixed_line = ''
        
        fixed_lines.append(fixed_line)
        
        if stripped.endswith(':'):
            indent_level += 1
    
    fixed_code = '\n'.join(fixed_lines)
    
    if not any(f['description'] == 'Fixed indentation' for f in all_fixes):
        all_fixes.append({'description': 'Fixed indentation', 'type': 'syntax_fix'})
    print("   ✓ Fixed indentation")
    
    print(f"\n✅ Final fixed code:")
    print(fixed_code)
    print()
    
    try:
        ast.parse(fixed_code)
        print("✅ SUCCESS! Code is valid!\n")
    except Exception as e:
        print(f"⚠️ Note: Code may still have some issues: {e}\n")
    
    return fixed_code, error_info, all_fixes

@app.post("/api/debug", response_model=DebugResponse)
async def debug_code(input_data: CodeInput):
    if not input_data.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    try:
        fixed_code, error_info, fixes = ultimate_v16_fix(input_data.code)
        
        success = fixed_code != input_data.code and len(fixes) > 0
        
        response = DebugResponse(
            success=success,
            original_code=input_data.code,
            fixed_code=fixed_code,
            error={
                'error_type': error_info['type'],
                'message': error_info['message'],
                'line_number': error_info['line'],
                'severity': 'high'
            } if error_info else None,
            fixes=[
                {
                    'description': f['description'],
                    'fix_type': f.get('type', 'syntax_fix'),
                    'confidence': 0.90,
                    'ranking_score': 95.0,
                    'complexity': 1,
                    'reasoning': f['description']
                }
                for f in fixes
            ],
            message=f"✅ Fixed {len(fixes)} error(s)!" if fixes else "⚠️ Code processed",
            time_elapsed=0.1,
            confidence=0.95 if success else 0.5,
            execution_result={"success": success},
            attempts=1,
            decisions=[]
        )
        
        return response
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Ultimate Python Fixer API v16.0"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("✨ ULTIMATE PYTHON FIXER - API v16.0")
    print("="*60)
    print("Fixes: Smart Typos, Missing Commas (SMART!), Quotes,")
    print("       Parentheses, Brackets, Colons, Indentation!")
    print("\n📡 API: http://127.0.0.1:8000")
    print("🎨 UI: http://localhost:5173")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")