from datetime import datetime
import json
import os

def generate_report(target, attack, result, severity, scan_type):
    report = {
        "target": target,
        "scan_type": scan_type,
        "attack": attack,
        "severity": severity,
        "details": result,
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    return report


def render_report_text(report):
    header = f"SURAKSHA VAPT PROFESSIONAL REPORT\n{'='*50}\n"
    header += f"Target: {report['target']}\n"
    header += f"Scan Type: {report['scan_type']}\n"
    header += f"Attack Vector: {report['attack']}\n"
    header += f"Risk Level: {report['severity']}\n"
    header += f"Generated: {report['generated_at']}\n\n"

    body = "EXECUTIVE SUMMARY\n" + "="*30 + "\n"

    details = report.get("details", {})

    if isinstance(details, dict):
        # Handle structured results from enhanced modules
        if "status" in details:
            body += f"Assessment Status: {details['status']}\n"
        if "risk_level" in details:
            body += f"Risk Assessment: {details['risk_level']}\n"
        if "vulnerability" in details:
            body += f"Vulnerability Type: {details['vulnerability']}\n\n"

        # Findings section
        if "findings" in details and details["findings"]:
            body += "KEY FINDINGS\n" + "-"*15 + "\n"
            for finding in details["findings"]:
                body += f"• {finding}\n"
            body += "\n"

        # Detailed analysis
        if "details" in details and details["details"]:
            body += "DETAILED ANALYSIS\n" + "-"*20 + "\n"
            if isinstance(details["details"], list):
                for i, item in enumerate(details["details"], 1):
                    if isinstance(item, dict):
                        body += f"Form/Analysis {i}:\n"
                        for key, value in item.items():
                            if key != "issues":
                                body += f"  {key}: {value}\n"
                            else:
                                if value:
                                    body += f"  Issues:\n"
                                    for issue in value:
                                        body += f"    {issue}\n"
                        body += "\n"
                    else:
                        body += f"{i}. {item}\n"
            else:
                body += f"{details['details']}\n\n"

        # Educational notes
        if "educational_notes" in details and details["educational_notes"]:
            body += "EDUCATIONAL INSIGHTS\n" + "-"*25 + "\n"
            for note in details["educational_notes"]:
                body += f"• {note}\n"
            body += "\n"

        # Recommendations
        if "recommendations" in details and details["recommendations"]:
            body += "RECOMMENDATIONS\n" + "-"*18 + "\n"
            for rec in details["recommendations"]:
                body += f"• {rec}\n"
            body += "\n"

        # Additional technical details
        for key, value in details.items():
            if key not in ["findings", "details", "educational_notes", "recommendations", "status", "risk_level", "vulnerability"]:
                if isinstance(value, (dict, list)):
                    body += f"{key.upper()}:\n"
                    body += json.dumps(value, indent=2) + "\n\n"
                else:
                    body += f"{key}: {value}\n\n"

    else:
        # Handle legacy string results
        body += f"Raw Results:\n{str(details)}\n\n"

    return header + body


def generate_report_pdf(report):
    try:
        from weasyprint import HTML, CSS
        from flask import render_template
        import io
    except ImportError as e:
        print(f"PDF generation failed: {e}")
        return None

    try:
        # Render the HTML template with report data
        html_content = render_template('result.html',
                                     target=report['target'],
                                     scan_type=report['scan_type'],
                                     attack=report['attack'],
                                     severity=report['severity'],
                                     result=report.get('details', {}),
                                     report=report,
                                     process_info="Professional vulnerability assessment completed using industry-standard tools and methodologies.")

        # Create PDF from HTML
        base_url = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        html_doc = HTML(string=html_content, base_url=base_url)

        # Add print-specific CSS
        css = CSS(string='''
            @page {
                size: A4;
                margin: 1in;
            }
            .no-print { display: none !important; }
            body { font-family: Arial, sans-serif; }
            .container { max-width: none; margin: 0; padding: 0; }
        ''')

        # Generate PDF
        pdf_bytes = html_doc.write_pdf(stylesheets=[css])

        return pdf_bytes

    except Exception as e:
        print(f"PDF generation error: {e}")
        return None
