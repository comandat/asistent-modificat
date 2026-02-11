import argparse
import ast
import os
import sys

def analyze_file(filepath):
    """
    Analyze a Python file for code complexity.
    """
    print(f"Analyzing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check lines of code
        lines = code.split('\n')
        num_lines = len(lines)
        if num_lines > 200:
            print(f"❌ {filepath} too long: {num_lines} lines (max 200)")
            return False, f"**{filepath}** has **{num_lines}** lines. Split it into modules."

        # Check complexity (AST)
        tree = ast.parse(code)
        
        # Check functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Count lines in function
                func_lines = node.end_lineno - node.lineno
                if func_lines > 30:
                    print(f"⚠️ Function '{node.name}' in {filepath} is too long ({func_lines} lines)")
                    return False, f"Function **{node.name}** in {filepath} is too long ({func_lines} lines). Refactor."
                
                # Check arguments
                if len(node.args.args) > 5:
                    print(f"⚠️ Function '{node.name}' in {filepath} has too many args ({len(node.args.args)})")
                    return False, f"Function **{node.name}** in {filepath} has {len(node.args.args)} args. Use an object."
        
        return True, ""
        
    except SyntaxError:
        print(f"❌ Syntax Error in {filepath}")
        return False, f"**{filepath}** has Syntax Error."
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")
        return False, f"Error analyzing {filepath}: {e}"

def analyze_project(root_dir):
    """
    Analyze all Python files in directory.
    """
    print(f"🏗️ Starting Code Analysis in: {root_dir}")
    issues = []
    
    for root, _, files in os.walk(root_dir):
        if "venv" in root or "node_modules" in root or ".git" in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                ok, msg = analyze_file(path)
                if not ok:
                    issues.append(msg)
    
    # Generate Report
    if issues:
        report = "# Code Audit Report 🚨\n\n"
        report += "**CRITICAL ISSUES FOUND:**\n\n"
        for issue in issues:
            report += f"- {issue}\n"
        
        with open("audit_report.md", "w") as f:
            f.write(report)
        print("❌ Issues found. See audit_report.md")
        sys.exit(1) # Fail build
    else:
        print("✅ Code is clean.")
        if os.path.exists("audit_report.md"):
            os.remove("audit_report.md")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nanobot Code Architect Tool")
    parser.add_argument("path", help="Project path to analyze")
    args = parser.parse_args()
    
    analyze_project(args.path)
