"""
Performance Code Analyzer
Analyzes Python code for common performance anti-patterns.
"""

import ast
import sys
from typing import List, Tuple


class PerformanceAnalyzer(ast.NodeVisitor):
    """AST-based analyzer for performance anti-patterns"""
    
    def __init__(self):
        self.issues = []
        self.current_function = None
    
    def visit_FunctionDef(self, node):
        """Track current function being analyzed"""
        old_function = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_function
    
    def visit_AugAssign(self, node):
        """Check for string concatenation with +="""
        # Look for string concatenation patterns
        if isinstance(node.op, ast.Add):
            # Check if we're in a loop
            parent = getattr(node, 'parent_loop', False)
            if parent:
                self.issues.append({
                    'line': node.lineno,
                    'type': 'string_concatenation',
                    'severity': 'high',
                    'message': f'String concatenation with += in loop at line {node.lineno}. Use join() instead.',
                    'function': self.current_function
                })
        self.generic_visit(node)
    
    def visit_For(self, node):
        """Check for inefficient loop patterns"""
        # Mark all children as being in a loop
        for child in ast.walk(node):
            child.parent_loop = True
        
        # Check for nested loops
        for child in ast.walk(node.body[0] if node.body else node):
            if isinstance(child, ast.For) and child != node:
                self.issues.append({
                    'line': node.lineno,
                    'type': 'nested_loop',
                    'severity': 'medium',
                    'message': f'Nested loop at line {node.lineno}. Consider using set/dict for O(1) lookups.',
                    'function': self.current_function
                })
                break
        
        self.generic_visit(node)
    
    def visit_Compare(self, node):
        """Check for list membership tests"""
        if isinstance(node.ops[0], ast.In):
            # Check if comparing against a list (potential O(n) operation)
            for comparator in node.comparators:
                if isinstance(comparator, (ast.List, ast.ListComp)):
                    self.issues.append({
                        'line': node.lineno,
                        'type': 'list_membership',
                        'severity': 'medium',
                        'message': f'Membership test on list at line {node.lineno}. Convert to set for O(1) lookup.',
                        'function': self.current_function
                    })
        self.generic_visit(node)
    
    def visit_Call(self, node):
        """Check for repeated function calls in loops"""
        # Check for len() in range()
        if isinstance(node.func, ast.Name) and node.func.id == 'range':
            if node.args:
                arg = node.args[0]
                if isinstance(arg, ast.Call):
                    if isinstance(arg.func, ast.Name) and arg.func.id == 'len':
                        self.issues.append({
                            'line': node.lineno,
                            'type': 'len_in_range',
                            'severity': 'low',
                            'message': f'Using len() in range() at line {node.lineno}. Consider enumerate() or direct iteration.',
                            'function': self.current_function
                        })
        
        self.generic_visit(node)
    
    def analyze(self, code: str, filename: str = '<string>') -> List[dict]:
        """Analyze code and return list of performance issues"""
        try:
            tree = ast.parse(code, filename=filename)
            self.visit(tree)
            return self.issues
        except SyntaxError as e:
            return [{
                'line': e.lineno or 0,
                'type': 'syntax_error',
                'severity': 'error',
                'message': f'Syntax error: {e.msg}',
                'function': None
            }]


def analyze_file(filename: str) -> List[dict]:
    """Analyze a Python file for performance issues"""
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
        analyzer = PerformanceAnalyzer()
        return analyzer.analyze(code, filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error analyzing file: {e}", file=sys.stderr)
        return []


def print_report(issues: List[dict], filename: str):
    """Print a formatted report of issues found"""
    if not issues:
        print(f"✓ No performance issues found in {filename}")
        return
    
    print(f"\n{'=' * 80}")
    print(f"Performance Analysis: {filename}")
    print(f"{'=' * 80}\n")
    
    # Group by severity
    by_severity = {'high': [], 'medium': [], 'low': [], 'error': []}
    for issue in issues:
        by_severity[issue['severity']].append(issue)
    
    for severity in ['error', 'high', 'medium', 'low']:
        if by_severity[severity]:
            severity_symbol = {'error': '✗', 'high': '⚠', 'medium': '!', 'low': 'ℹ'}
            print(f"{severity_symbol[severity]} {severity.upper()} SEVERITY ({len(by_severity[severity])} issues)")
            print("-" * 80)
            
            for issue in by_severity[severity]:
                func_info = f" in {issue['function']}()" if issue['function'] else ""
                print(f"  Line {issue['line']}{func_info}: {issue['message']}")
            print()


def main_cli():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_performance.py <python_file>")
        print("\nExample:")
        print("  python analyze_performance.py examples_inefficient.py")
        sys.exit(1)
    
    filename = sys.argv[1]
    issues = analyze_file(filename)
    print_report(issues, filename)
    
    # Return exit code based on severity
    if any(issue['severity'] in ['error', 'high'] for issue in issues):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main_cli()
