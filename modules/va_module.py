from core.tool_manager import ToolManager

class VAModule:

    def __init__(self, target):
        self.target = target
        self.tool_manager = ToolManager()

    def execute(self):

        results = []

        # 1 SQL Injection
        results.append(self.tool_manager.run_sqlmap(self.target))

        # 2 Security Misconfiguration & Outdated
        results.append(self.tool_manager.run_nikto(self.target))

        # 3 ZAP scan for headers, sensitive data
        results.append(self.tool_manager.run_zap(self.target))

        return results
