class SeverityAnalyzer:

    def classify(self, results):

        severity_keywords = {
            "sql injection": "Critical",
            "xss": "High",
            "csrf": "High",
            "authentication": "High",
            "brute": "Critical",
            "ssl": "Medium",
            "tls": "Medium",
            "header": "Low",
            "cookie": "Medium",
            "directory traversal": "High",
            "misconfiguration": "Medium",
        }

        for result in results:
            output = result["output"].lower()
            assigned = "Informational"

            for keyword in severity_keywords:
                if keyword in output:
                    assigned = severity_keywords[keyword]
                    break

            result["severity"] = assigned

        return results
