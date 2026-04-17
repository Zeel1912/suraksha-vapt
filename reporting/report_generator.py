from datetime import datetime
import json

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
        from fpdf import FPDF
    except ImportError:
        return None

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SURAKSHA VAPT PROFESSIONAL REPORT", ln=True, align="C")
    pdf.ln(8)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Target: {report['target']}", ln=True)
    pdf.cell(0, 8, f"Scan Type: {report['scan_type']}", ln=True)
    pdf.cell(0, 8, f"Attack Vector: {report['attack']}", ln=True)
    pdf.cell(0, 8, f"Risk Level: {report['severity']}", ln=True)
    pdf.cell(0, 8, f"Generated: {report['generated_at']}", ln=True)
    pdf.ln(4)

    details = report.get("details", {})

    if isinstance(details, dict):
        # Executive Summary
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 8, "Executive Summary", ln=True)
        pdf.set_font("Arial", "", 11)

        if "status" in details:
            pdf.cell(0, 6, f"Assessment Status: {details['status']}", ln=True)
        if "risk_level" in details:
            pdf.cell(0, 6, f"Risk Assessment: {details['risk_level']}", ln=True)
        if "vulnerability" in details:
            pdf.cell(0, 6, f"Vulnerability Type: {details['vulnerability']}", ln=True)

        pdf.ln(4)

        # Key Findings
        if "findings" in details and details["findings"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Key Findings", ln=True)
            pdf.set_font("Arial", "", 11)
            for finding in details["findings"]:
                pdf.multi_cell(0, 6, f"• {finding}")
            pdf.ln(4)

        # Educational Insights
        if "educational_notes" in details and details["educational_notes"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Educational Insights", ln=True)
            pdf.set_font("Arial", "", 11)
            for note in details["educational_notes"]:
                pdf.multi_cell(0, 6, f"• {note}")
            pdf.ln(4)

        # Recommendations
        if "recommendations" in details and details["recommendations"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Recommendations", ln=True)
            pdf.set_font("Arial", "", 11)
            for rec in details["recommendations"]:
                pdf.multi_cell(0, 6, f"• {rec}")
            pdf.ln(4)

        # Technical Details
        if "details" in details and details["details"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Technical Details", ln=True)
            pdf.set_font("Arial", "", 10)

            if isinstance(details["details"], list):
                for i, item in enumerate(details["details"], 1):
                    pdf.cell(0, 6, f"Analysis {i}:", ln=True)
                    if isinstance(item, dict):
                        for key, value in item.items():
                            if key != "issues":
                                pdf.cell(0, 5, f"  {key}: {value}", ln=True)
                            else:
                                if value:
                                    pdf.cell(0, 5, "  Issues:", ln=True)
                                    for issue in value:
                                        pdf.multi_cell(0, 5, f"    {issue}")
                    else:
                        pdf.multi_cell(0, 5, f"  {item}")
                    pdf.ln(2)
            else:
                pdf.multi_cell(0, 6, str(details["details"]))

    else:
        # Legacy string results
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 8, "Details:", ln=True)
        pdf.set_font("Arial", "", 11)

        details_str = str(details)
        for line in details_str.splitlines():
            pdf.multi_cell(0, 6, line)

    return pdf.output(dest="S").encode("latin-1")
