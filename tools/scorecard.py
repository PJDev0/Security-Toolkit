#!/usr/bin/env python3
"""
Repository Security Scorecard
Checks GitHub repos for security best practices
"""

import os
import sys
from github import Github
from github.GithubException import GithubException
from typing import Dict
import json


class SecurityScorecard:
    CHECKS = {
        'has_license': {'weight': 15, 'description': 'Has LICENSE file'},
        'has_codeowners': {'weight': 20, 'description': 'Has CODEOWNERS file'},
        'has_readme': {'weight': 10, 'description': 'Has README.md'},
        'has_security_md': {'weight': 15, 'description': 'Has SECURITY.md'},
        'branch_protection_main': {'weight': 25, 'description': 'Main branch protected'},
        'requires_pr_reviews': {'weight': 10, 'description': 'Requires PR reviews'},
        'signed_commits': {'weight': 5, 'description': 'Requires signed commits'},
    }
    
    def __init__(self, token: str):
        self.github = Github(token)
        self.results = {}
        self.score = 0
        self.max_score = sum(c['weight'] for c in self.CHECKS.values())
    
    def analyze_repo(self, owner: str, repo_name: str) -> Dict:
        """Run all security checks on a repository"""
        try:
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            print(f"Analyzing {owner}/{repo_name}...")
            
            # Check 1: License
            self.results['has_license'] = self._check_license(repo)
            
            # Check 2: CODEOWNERS
            self.results['has_codeowners'] = self._check_codeowners(repo)
            
            # Check 3: README
            self.results['has_readme'] = self._check_file_exists(repo, "README.md")
            
            # Check 4: Security policy
            self.results['has_security_md'] = self._check_security_policy(repo)
            
            # Check 5-7: Branch protection (requires admin access)
            branch_checks = self._check_branch_protection(repo)
            self.results.update(branch_checks)
            
            # Calculate final score
            self._calculate_score()
            
            return self._generate_report(owner, repo_name)
            
        except GithubException as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def _check_license(self, repo) -> bool:
        """Check if repo has a license file"""
        try:
            license_file = repo.get_license()
            return license_file is not None
        except:
            # Fallback: check common license filenames
            for filename in ['LICENSE', 'LICENSE.md', 'LICENSE.txt', 'LICENSE.rst']:
                if self._check_file_exists(repo, filename):
                    return True
            return False
    
    def _check_codeowners(self, repo) -> bool:
        """Check for CODEOWNERS in .github/ or root"""
        locations = [
            'CODEOWNERS',
            '.github/CODEOWNERS',
            'docs/CODEOWNERS'
        ]
        return any(self._check_file_exists(repo, loc) for loc in locations)
    
    def _check_file_exists(self, repo, path: str) -> bool:
        """Check if a file exists in the repo"""
        try:
            repo.get_contents(path)
            return True
        except:
            return False
    
    def _check_security_policy(self, repo) -> bool:
        """Check for SECURITY.md"""
        try:
            repo.get_security_md()
            return True
        except:
            # Manual check
            for path in ['SECURITY.md', '.github/SECURITY.md', 'docs/SECURITY.md']:
                if self._check_file_exists(repo, path):
                    return True
            return False
    
    def _check_branch_protection(self, repo) -> Dict[str, bool]:
        """Check branch protection rules"""
        results = {
            'branch_protection_main': False,
            'requires_pr_reviews': False,
            'signed_commits': False
        }
        
        try:
            # Try main branch first, then master
            for branch_name in ['main', 'master']:
                try:
                    branch = repo.get_branch(branch_name)
                    protection = branch.get_protection()
                    
                    results['branch_protection_main'] = True
                    results['requires_pr_reviews'] = (
                        protection.required_pull_request_reviews is not None
                    )
                    results['signed_commits'] = (
                        protection.required_signatures_enabled 
                        if hasattr(protection, 'required_signatures_enabled') 
                        else False
                    )
                    break
                except:
                    continue
                    
        except Exception as e:
            print(f"Warning: Could not check branch protection (needs admin access): {e}")
        
        return results
    
    def _calculate_score(self):
        """Calculate weighted score"""
        self.score = 0
        for check, passed in self.results.items():
            if passed and check in self.CHECKS:
                self.score += self.CHECKS[check]['weight']
    
    def _generate_report(self, owner: str, repo_name: str) -> Dict:
        """Generate detailed report"""
        percentage = round((self.score / self.max_score) * 100)
        
        # Determine grade
        if percentage >= 90:
            grade = 'A'
            color = 'brightgreen'
        elif percentage >= 75:
            grade = 'B'
            color = 'green'
        elif percentage >= 60:
            grade = 'C'
            color = 'yellow'
        elif percentage >= 40:
            grade = 'D'
            color = 'orange'
        else:
            grade = 'F'
            color = 'red'
        
        return {
            'repository': f"{owner}/{repo_name}",
            'score': self.score,
            'max_score': self.max_score,
            'percentage': percentage,
            'grade': grade,
            'color': color,
            'checks': {
                name: {
                    'passed': self.results.get(name, False),
                    'weight': info['weight'],
                    'description': info['description']
                }
                for name, info in self.CHECKS.items()
            },
            'timestamp': self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat()


def main():
    # Get GitHub token
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Please set GITHUB_TOKEN environment variable")
        print("   export GITHUB_TOKEN='your_token_here'")
        sys.exit(1)
    
    if len(sys.argv) < 3:
        print("Usage: python scorecard.py <owner> <repo>")
        print("Example: python scorecard.py facebook react")
        sys.exit(1)
    
    owner, repo = sys.argv[1], sys.argv[2]
    
    # Run analysis
    scorecard = SecurityScorecard(token)
    report = scorecard.analyze_repo(owner, repo)
    
    # Print results
    print("\n" + "="*50)
    print(f"SECURITY SCORECARD: {report['repository']}")
    print("="*50)
    print(f"Score: {report['score']}/{report['max_score']} ({report['percentage']}%)")
    print(f"Grade: {report['grade']}")
    print("-"*50)
    
    for check_name, check_data in report['checks'].items():
        status = "[PASS]" if check_data['passed'] else "[FAIL]"
        print(f"{status} {check_data['description']} (+{check_data['weight']} pts)")
    
    # Save report
    filename = f"scorecard-{owner}-{repo}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved to {filename}")
    
    return report


if __name__ == "__main__":
    main()