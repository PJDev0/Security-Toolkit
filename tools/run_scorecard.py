#!/usr/bin/env python3
"""
Main entry point for Repo Security Scorecard
"""

import os
import sys
import json
import argparse
from scorecard import SecurityScorecard
from badge_generator import generate_score_badge


def main():
    parser = argparse.ArgumentParser(
        description='Generate security scorecard for GitHub repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a repo
  python run_scorecard.py owner/repo
  
  # Generate badge only
  python run_scorecard.py owner/repo --badge-only
  
  # Output as markdown
  python run_scorecard.py owner/repo --format markdown
  
  # Use specific GitHub token
  GITHUB_TOKEN=xxx python run_scorecard.py facebook/react
        """
    )
    
    parser.add_argument('repo', help='Repository in format owner/repo')
    parser.add_argument('--format', choices=['json', 'markdown', 'table'], 
                       default='table', help='Output format')
    parser.add_argument('--badge-only', action='store_true', 
                       help='Only generate badge from existing report')
    parser.add_argument('--output-dir', default='.', 
                       help='Directory to save outputs')
    parser.add_argument('--style', choices=['flat', 'plastic'], default='flat',
                       help='Badge style')
    
    args = parser.parse_args()
    
    # Parse owner/repo
    try:
        owner, repo_name = args.repo.split('/')
    except ValueError:
        print("Error: Repository must be in format 'owner/repo'")
        sys.exit(1)
    
    # Check token
    token = os.environ.get('GITHUB_TOKEN')
    if not token and not args.badge_only:
        print("GITHUB_TOKEN environment variable required")
        print("Get one at: https://github.com/settings/tokens")
        print("Required scopes: repo (for private repos), public_repo")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Run analysis or load existing
    if args.badge_only:
        # Load existing report
        report_file = f"{args.output_dir}/scorecard-{owner}-{repo_name}.json"
        if not os.path.exists(report_file):
            print(f"No existing report found at {report_file}")
            sys.exit(1)
        with open(report_file) as f:
            report = json.load(f)
    else:
        # Run new analysis
        scorecard = SecurityScorecard(token)
        report = scorecard.analyze_repo(owner, repo_name)
        
        # Save JSON report
        json_file = f"{args.output_dir}/scorecard-{owner}-{repo_name}.json"
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
    
    # Generate badge
    badge_file = f"{args.output_dir}/badge-{owner}-{repo_name}.svg"
    generate_score_badge(
        report['score'], 
        report['max_score'], 
        report['grade'], 
        report['color'],
        badge_file
    )
    
    # Output based on format
    if args.format == 'json':
        print(json.dumps(report, indent=2))
    elif args.format == 'markdown':
        print(generate_markdown(report, badge_file))
    else:
        print_table(report, badge_file)
    
    print(f"\nDone. Files saved in {args.output_dir}/")
    print(f"   - Report: scorecard-{owner}-{repo_name}.json")
    print(f"   - Badge: {badge_file}")


def print_table(report, badge_file):
    """Print formatted table to console"""
    print(f"\nSECURITY SCORECARD: {report['repository']}")
    print("=" * 60)
    print(f"Overall Score: {report['score']}/{report['max_score']} ({report['percentage']}%)")
    print(f"Grade: {report['grade']}")
    print(f"Badge: {badge_file}")
    print("-" * 60)
    
    for check_name, check in report['checks'].items():
        status = "[PASS]" if check['passed'] else "[FAIL]"
        points = f"+{check['weight']}" if check['passed'] else "0"
        print(f"{status:<8} {check['description']:<35} ({points} pts)")
    
    print("=" * 60)


def generate_markdown(report, badge_file):
    """Generate markdown summary"""
    lines = [
        f"## Security Scorecard: {report['repository']}",
        "",
        f"![Security Score]({badge_file})",
        "",
        f"**Score:** {report['score']}/{report['max_score']} ({report['percentage']}%)",
        f"**Grade:** {report['grade']}",
        "",
        "### Checks",
        "",
        "| Check | Status | Points |",
        "|-------|--------|--------|"
    ]
    
    for check_name, check in report['checks'].items():
        status = "Pass" if check['passed'] else "Fail"
        points = str(check['weight']) if check['passed'] else "0"
        lines.append(f"| {check['description']} | {status} | +{points} |")
    
    lines.append("")
    lines.append(f"*Generated: {report['timestamp']}*")
    
    return "\n".join(lines)


if __name__ == "__main__":
    main()