#!/usr/bin/env python3
"""
Test runner with visualization and automatic saving
"""

import os
import sys
import json
import datetime
import subprocess
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List, Any


class TestRunner:
    """Test runner with visualization capabilities."""
    
    def __init__(self):
        self.results_dir = Path("test_results")
        self.results_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def run_tests(self, test_path: str = "tests") -> Dict[str, Any]:
        """Run tests and return results."""
        print(f"Running tests from: {test_path}")
        
        # Run pytest with JSON output
        cmd = [
            sys.executable, "-m", "pytest",
            test_path,
            "--json-report",
            "--json-report-file=none",
            "-v"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            # Parse test results
            test_results = self._parse_test_output(result.stdout, result.stderr, result.returncode)
            
            return test_results
            
        except Exception as e:
            print(f"Error running tests: {e}")
            return {
                "success": False,
                "error": str(e),
                "tests": [],
                "summary": {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "skipped": 0
                }
            }
    
    def _parse_test_output(self, stdout: str, stderr: str, return_code: int) -> Dict[str, Any]:
        """Parse pytest output and extract test results."""
        lines = stdout.split('\n')
        tests = []
        current_test = None
        
        for line in lines:
            if line.startswith('tests/'):
                # Test result line
                parts = line.split()
                if len(parts) >= 2:
                    test_name = parts[0]
                    status = parts[1]
                    
                    test_info = {
                        "name": test_name,
                        "status": status,
                        "duration": None
                    }
                    
                    # Extract duration if available
                    for part in parts[2:]:
                        if part.startswith('[') and part.endswith('s]'):
                            test_info["duration"] = float(part[1:-2])
                    
                    tests.append(test_info)
        
        # Calculate summary
        total = len(tests)
        passed = len([t for t in tests if t["status"] == "PASSED"])
        failed = len([t for t in tests if t["status"] == "FAILED"])
        skipped = len([t for t in tests if t["status"] == "SKIPPED"])
        
        return {
            "success": return_code == 0,
            "tests": tests,
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped
            },
            "stdout": stdout,
            "stderr": stderr,
            "return_code": return_code
        }
    
    def save_results(self, results: Dict[str, Any]) -> str:
        """Save test results to file."""
        filename = f"test_results_{self.timestamp}.json"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to: {filepath}")
        return str(filepath)
    
    def create_visualization(self, results: Dict[str, Any]) -> str:
        """Create visualization of test results."""
        summary = results["summary"]
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Test Results - {self.timestamp}', fontsize=16)
        
        # 1. Pie chart of test status
        labels = ['Passed', 'Failed', 'Skipped']
        sizes = [summary['passed'], summary['failed'], summary['skipped']]
        colors = ['#2ecc71', '#e74c3c', '#f39c12']
        
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Test Status Distribution')
        
        # 2. Bar chart of test counts
        categories = ['Total', 'Passed', 'Failed', 'Skipped']
        values = [summary['total'], summary['passed'], summary['failed'], summary['skipped']]
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
        
        bars = ax2.bar(categories, values, color=colors)
        ax2.set_title('Test Counts')
        ax2.set_ylabel('Number of Tests')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{value}', ha='center', va='bottom')
        
        # 3. Test duration histogram (if available)
        durations = [t.get('duration', 0) for t in results['tests'] if t.get('duration')]
        if durations:
            ax3.hist(durations, bins=10, color='#9b59b6', alpha=0.7)
            ax3.set_title('Test Duration Distribution')
            ax3.set_xlabel('Duration (seconds)')
            ax3.set_ylabel('Number of Tests')
        else:
            ax3.text(0.5, 0.5, 'No duration data available', 
                    ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Test Duration Distribution')
        
        # 4. Success rate over time (mock data for now)
        success_rate = (summary['passed'] / summary['total'] * 100) if summary['total'] > 0 else 0
        ax4.bar(['Success Rate'], [success_rate], color='#2ecc71')
        ax4.set_title('Overall Success Rate')
        ax4.set_ylabel('Percentage (%)')
        ax4.set_ylim(0, 100)
        ax4.text(0, success_rate + 1, f'{success_rate:.1f}%', 
                ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save visualization
        viz_filename = f"test_visualization_{self.timestamp}.png"
        viz_filepath = self.results_dir / viz_filename
        plt.savefig(viz_filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Visualization saved to: {viz_filepath}")
        return str(viz_filepath)
    
    def generate_report(self, results: Dict[str, Any], results_file: str, viz_file: str) -> str:
        """Generate a comprehensive test report."""
        report_filename = f"test_report_{self.timestamp}.md"
        report_filepath = self.results_dir / report_filename
        
        summary = results["summary"]
        success_rate = (summary['passed'] / summary['total'] * 100) if summary['total'] > 0 else 0
        
        with open(report_filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Test Report - {self.timestamp}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Tests**: {summary['total']}\n")
            f.write(f"- **Passed**: {summary['passed']}\n")
            f.write(f"- **Failed**: {summary['failed']}\n")
            f.write(f"- **Skipped**: {summary['skipped']}\n")
            f.write(f"- **Success Rate**: {success_rate:.1f}%\n\n")
            
            f.write("## Test Results\n\n")
            for test in results['tests']:
                status_emoji = "✅" if test['status'] == 'PASSED' else "❌" if test['status'] == 'FAILED' else "⏭️"
                duration_str = f" ({test['duration']:.2f}s)" if test['duration'] else ""
                f.write(f"- {status_emoji} {test['name']}{duration_str}\n")
            
            f.write(f"\n## Files\n\n")
            f.write(f"- **Results JSON**: `{results_file}`\n")
            f.write(f"- **Visualization**: `{viz_file}`\n")
            f.write(f"- **Report**: `{report_filepath}`\n")
            
            if results.get('stderr'):
                f.write(f"\n## Error Output\n\n")
                f.write(f"```\n{results['stderr']}\n```\n")
        
        print(f"Report saved to: {report_filepath}")
        return str(report_filepath)


def main():
    """Main function to run tests with visualization."""
    runner = TestRunner()
    
    print("🚀 Starting test execution...")
    
    # Run tests
    results = runner.run_tests()
    
    # Save results
    results_file = runner.save_results(results)
    
    # Create visualization
    viz_file = runner.create_visualization(results)
    
    # Generate report
    report_file = runner.generate_report(results, results_file, viz_file)
    
    # Print summary
    summary = results["summary"]
    print(f"\n📊 Test Summary:")
    print(f"   Total: {summary['total']}")
    print(f"   Passed: {summary['passed']}")
    print(f"   Failed: {summary['failed']}")
    print(f"   Skipped: {summary['skipped']}")
    
    if summary['total'] > 0:
        success_rate = (summary['passed'] / summary['total'] * 100)
        print(f"   Success Rate: {success_rate:.1f}%")
    
    print(f"\n📁 Files generated:")
    print(f"   Results: {results_file}")
    print(f"   Visualization: {viz_file}")
    print(f"   Report: {report_file}")
    
    if not results["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main() 