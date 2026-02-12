from modules.va_module import VAModule
from modules.pt_module import PTModule
from core.severity_analyzer import SeverityAnalyzer
from reports.report_generator import ReportGenerator

class VAPTToolkit:

    def __init__(self, target):
        self.target = target
        self.analyzer = SeverityAnalyzer()
        self.reporter = ReportGenerator()

    def start_scan(self, mode):

        if mode == "VA":
            module = VAModule(self.target)
        else:
            module = PTModule(self.target)

        raw_results = module.execute()

        analyzed = self.analyzer.classify(raw_results)

        report_path = self.reporter.generate(analyzed)

        return analyzed, report_path
