import subprocess
import json

class ToolManager:

    def run_sqlmap(self, target):
        command = ["sqlmap", "-u", target, "--batch", "--output-dir=output/sqlmap"]
        return self.execute(command, "SQL Injection")

    def run_nikto(self, target):
        command = ["nikto", "-h", target, "-o", "output/nikto.txt"]
        return self.execute(command, "Security Misconfiguration / Outdated Software")

    def run_zap(self, target):
        command = ["zap-cli", "quick-scan", "--self-contained", target]
        return self.execute(command, "ZAP Scan")

    def run_hydra(self, target):
        command = ["hydra", "-L", "usernames.txt", "-P", "passwords.txt", target]
        return self.execute(command, "Brute Force")

    def run_sslyze(self, target):
        command = ["sslyze", target]
        return self.execute(command, "SSL/TLS Analysis")

    def execute(self, command, attack_type):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300
            )
            return {
                "attack": attack_type,
                "output": result.stdout,
                "status": "Completed"
            }
        except Exception as e:
            return {
                "attack": attack_type,
                "output": str(e),
                "status": "Failed"
            }
