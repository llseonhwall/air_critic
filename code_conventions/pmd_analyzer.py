import subprocess
import json

class PMDAnalyzer:
    def __init__(self, pmd_path, convention_rules, code, java_save_path):
        self.pmd_path = pmd_path
        self.convention_rules = convention_rules
        self.code = code
        self.java_save_path = java_save_path
        
        
    def save_java_file_from_text(self):
        with open(self.java_save_path, "w") as java_file:
            java_file.write(self.code)
    
    def run_pmd_analysis(self):
        try:
            # run pmd command
            command = [
                self.pmd_path,
                "-d", self.java_save_path, 
                "-R", self.convention_rules,
                "-f", "json"
                ]
            pmd_results = subprocess.run(command, capture_output=True, text=True, check=True)
            self.pmd_results = json.loads(pmd_results.stdout)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            print(f"Error output: {e.stderr}")  # 오류 메시지 출력
            self.pmd_results = {"violations": []}
        return self.pmd_results

    def analyze_convention_violations(self):
        violations = self.pmd_results.get("violations", [])
        total_violations = len(violations)

        # 규칙별 위반사항 분류
        rule_violations = {}
        for violation in violations:
            rule = violation.get("rule", "Unknown Rule")
            if rule not in rule_violations:
                rule_violations[rule] = 0
            rule_violations[rule] += 1

        # 정량화된 결과 계산
        compliance_score = max(0, 100 - (total_violations * 2))  # 위반 하나당 -2점
        evaluate_score = {
            "total_violations": total_violations,
            "violations_by_rule": rule_violations,
            "compliance_score": compliance_score
        }

        return evaluate_score
