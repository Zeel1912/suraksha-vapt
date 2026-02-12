from datetime import datetime
import os

class ReportGenerator:

    def generate(self, analyzed_results):

        if not os.path.exists("reports/output"):
            os.makedirs("reports/output")

        filename = f"reports/output/report_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

        with open(filename, "w") as f:

            f.write("SURAKSHA-VAPT Security Report\n")
            f.write("="*60 + "\n\n")

            for result in analyzed_results:
                f.write(f"Attack: {result['attack']}\n")
                f.write(f"Status: {result['status']}\n")
                f.write(f"Severity: {result['severity']}\n")
                f.write("-"*50 + "\n")

        return filename
