#!/usr/bin/env python3
"""
Quick Start Script
Run this to get started with the performance optimization toolkit.
"""

import sys
import os


def print_banner():
    """Print welcome banner"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║        PERFORMANCE OPTIMIZATION TOOLKIT - QUICK START             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")


def main():
    """Quick start menu"""
    print_banner()
    
    print("""
Welcome! This toolkit helps you identify and fix performance issues.

What would you like to do?

1. 📖 See usage guide and workflow
2. 🏃 Run performance benchmarks
3. 🔍 Analyze code for issues
4. 🎯 Run all demonstrations
5. 📊 See real-world example (log analyzer)
6. 🎓 Learn advanced patterns
7. 🌐 See web/API optimizations
8. ℹ️  Show documentation index

0. Exit

Choose an option (0-8): """)
    
    try:
        choice = input().strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting...")
        return
    
    commands = {
        '1': ('python3 usage_guide.py', 'Usage Guide'),
        '2': ('python3 benchmark.py', 'Benchmarks'),
        '3': ('python3 analyze_performance.py examples_inefficient.py', 'Code Analyzer Demo'),
        '4': ('python3 run_all_demos.py', 'All Demonstrations'),
        '5': ('python3 compare_log_analyzers.py', 'Log Analyzer Comparison'),
        '6': ('python3 advanced_patterns.py', 'Advanced Patterns'),
        '7': ('python3 web_performance.py', 'Web Performance'),
        '8': (None, 'Documentation Index'),
        '0': (None, 'Exit')
    }
    
    if choice == '8':
        show_documentation_index()
        return
    elif choice == '0':
        print("\nGoodbye!")
        return
    elif choice in commands:
        cmd, name = commands[choice]
        print(f"\n{'='*70}")
        print(f"Running: {name}")
        print(f"{'='*70}\n")
        os.system(cmd)
    else:
        print("\nInvalid choice. Please run the script again.")


def show_documentation_index():
    """Show documentation index"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                     DOCUMENTATION INDEX                           ║
╚═══════════════════════════════════════════════════════════════════╝

📚 Getting Started:
   • README.md                  - Start here for overview
   • QUICK_REFERENCE.md         - Quick lookup guide
   • WORKFLOW.md                - Visual workflow diagram

📖 In-Depth Guides:
   • PERFORMANCE_GUIDE.md       - Detailed patterns (8 sections)
   • INEFFICIENCIES_IDENTIFIED.md - All 15 issues cataloged
   • OPTIMIZATION_CHECKLIST.md  - Code review checklist
   • SUMMARY.md                 - Measured results

🔬 Examples:
   • examples_inefficient.py    - What NOT to do (10 patterns)
   • examples_efficient.py      - Best practices (15 patterns)
   • log_analyzer_slow.py       - Real-world before
   • log_analyzer_optimized.py  - Real-world after (2.68x faster)

🛠️  Tools:
   • analyze_performance.py     - Static analyzer
   • benchmark.py               - Performance tests
   • profiling_demo.py          - Profiling guide
   • compare_log_analyzers.py   - Case study
   • advanced_patterns.py       - Advanced techniques
   • web_performance.py         - Web optimizations
   • usage_guide.py             - Complete guide
   • run_all_demos.py           - All demos

Open any file in your editor to learn more!
""")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print(__doc__)
        print("""
Usage:
    python3 quickstart.py              # Interactive menu
    python3 quickstart.py --help       # Show this help
    
Or run any tool directly:
    python3 usage_guide.py
    python3 benchmark.py
    python3 analyze_performance.py <file>
    python3 run_all_demos.py
""")
    else:
        main()
