from vulnerability_module.sql_injection import run_sqlmap_scan
from vulnerability_module.xss_scanner import run_xss_scan
from vulnerability_module.directory_traversal import run_directory_scan
from vulnerability_module.security_misconfig import run_nikto_scan
from vulnerability_module.outdated_software import detect_outdated_server
from vulnerability_module.sensitive_data import detect_sensitive_data
from vulnerability_module.security_header import check_security_headers
from vulnerability_module.ssl_tls import run_ssl_scan

from pentest_module.brute_force import run_hydra_scan
from pentest_module.csrf import detect_csrf
from pentest_module.clickjacking import detect_clickjacking
from pentest_module.broken_auth import detect_broken_auth
from pentest_module.insecure_cookies import detect_insecure_cookie


class ScanOrchestrator:

    def execute_scan(self, module, attack, target):

        try:

            if module == "vulnerability":
                if attack == "sqli":
                    return run_sqlmap_scan(target)
                elif attack == "xss":
                    return run_xss_scan(target)
                elif attack == "dir":
                    return run_directory_scan(target)
                elif attack == "misconfig":
                    return run_nikto_scan(target)
                elif attack == "outdated":
                    return detect_outdated_server(target)
                elif attack == "sensitive":
                    return detect_sensitive_data(target)
                elif attack == "headers":
                    return check_security_headers(target)

            elif module == "pentest":
                if attack == "csrf":
                    return detect_csrf(target)
                elif attack == "clickjacking":
                    return detect_clickjacking(target)
                elif attack == "bruteforce":
                    return run_hydra_scan(target)
                elif attack == "broken_auth":
                    return detect_broken_auth(target)
                elif attack == "insecure_cookies":
                    return detect_insecure_cookie(target)
                elif attack == "ssl_scan":
                    return run_ssl_scan(target)

            return {
                "vulnerability": "Scan Error",
                "status": "Error",
                "details": "Invalid module or attack selected"
            }

        except Exception as e:
            return {
                "vulnerability": "System Error",
                "status": "Error",
                "details": str(e)
            }
