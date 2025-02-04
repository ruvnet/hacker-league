#!/usr/bin/env python3
"""
Test Runner Script for Oncology System

This script runs all tests and generates comprehensive reports.
"""

import os
import sys
import time
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
import pytest
import coverage

def setup_directories():
    """Setup necessary directories for test outputs."""
    base_dir = Path(__file__).parent
    dirs = {
        'reports': base_dir / 'reports',
        'coverage': base_dir / 'reports' / 'coverage',
        'junit': base_dir / 'reports' / 'junit',
        'logs': base_dir / 'reports' / 'logs'
    }
    
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return dirs

def run_tests(args):
    """Run pytest with specified arguments."""
    test_args = [
        '-v',
        '--strict-markers',
        f'--junitxml={args.report_dir}/junit/junit.xml',
        '--cov=src/oncology',
        f'--cov-report=html:{args.report_dir}/coverage',
        '--cov-report=term-missing'
    ]
    
    # Add custom markers based on args
    if args.skip_slow:
        test_args.append('-m not slow')
    if args.skip_integration:
        test_args.append('-m not integration')
    
    # Run tests
    return pytest.main(test_args)

def generate_summary(dirs, start_time, end_time, result):
    """Generate test execution summary."""
    duration = end_time - start_time
    
    # Read coverage data
    coverage_file = dirs['coverage'] / 'index.html'
    coverage_data = "Coverage report available at: " + str(coverage_file)
    
    # Read junit results
    junit_file = dirs['junit'] / 'junit.xml'
    junit_data = "JUnit report available at: " + str(junit_file)
    
    summary = {
        'timestamp': datetime.now().isoformat(),
        'duration_seconds': duration,
        'result_code': result,
        'coverage_info': coverage_data,
        'junit_info': junit_data,
        'environment': {
            'python_version': sys.version,
            'platform': sys.platform,
            'pytest_version': pytest.__version__
        }
    }
    
    # Write summary
    summary_file = dirs['reports'] / 'test_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary

def print_summary(summary):
    """Print formatted test summary."""
    print("\n" + "="*80)
    print("TEST EXECUTION SUMMARY")
    print("="*80)
    
    print(f"\nTimestamp: {summary['timestamp']}")
    print(f"Duration: {summary['duration_seconds']:.2f} seconds")
    print(f"Result Code: {summary['result_code']}")
    
    print("\nReports:")
    print(f"- {summary['coverage_info']}")
    print(f"- {summary['junit_info']}")
    
    print("\nEnvironment:")
    for key, value in summary['environment'].items():
        print(f"- {key}: {value}")
    
    print("\n" + "="*80)

def setup_logging(log_dir):
    """Setup logging configuration."""
    import logging
    
    log_file = log_dir / f"test_run_{datetime.now():%Y%m%d_%H%M%S}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Oncology System Test Runner")
    
    parser.add_argument(
        '--skip-slow',
        action='store_true',
        help="Skip slow tests"
    )
    parser.add_argument(
        '--skip-integration',
        action='store_true',
        help="Skip integration tests"
    )
    parser.add_argument(
        '--report-dir',
        type=str,
        default=None,
        help="Custom directory for test reports"
    )
    
    args = parser.parse_args()
    
    try:
        # Setup
        dirs = setup_directories()
        if args.report_dir:
            dirs['reports'] = Path(args.report_dir)
        args.report_dir = dirs['reports']
        
        logger = setup_logging(dirs['logs'])
        logger.info("Starting test execution")
        
        # Run tests
        start_time = time.time()
        result = run_tests(args)
        end_time = time.time()
        
        # Generate and print summary
        summary = generate_summary(dirs, start_time, end_time, result)
        print_summary(summary)
        
        # Log completion
        logger.info("Test execution completed")
        
        return result
        
    except Exception as e:
        logger.error(f"Error during test execution: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())