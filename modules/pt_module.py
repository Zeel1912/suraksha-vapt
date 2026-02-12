from core.tool_manager import ToolManager

class PTModule:

    def __init__(self, target):
        self.target = target
        self.tool_manager = ToolManager()

    def execute(self):

        results = []

        # ZAP for CSRF, Auth, Clickjacking, Cookies
        results.append(self.tool_manager.run_zap(self.target))

        # Brute Force
        results.append(self.tool_manager.run_hydra(self.target))

        # SSL/TLS
        results.append(self.tool_manager.run_sslyze(self.target))

        return results
