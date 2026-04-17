from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from io import BytesIO
from core_engine.scan_orchestrator import ScanOrchestrator
from reporting.report_generator import generate_report, generate_report_pdf
from reporting.severity_analyzer import analyze_severity

app = Flask(__name__)
app.secret_key = "change_this_secret_in_production"

scanner = ScanOrchestrator()

# User storage (in-memory for demo; use database for production)
VALID_USERS = {
    "admin": "Admin@123",
    "pentester": "Pentest@2026"
}


def validate_signup_input(username, password, confirm_password):
    """Validate signup form input"""
    errors = []
    
    if not username or len(username) < 3:
        errors.append("Username must be at least 3 characters long")
    
    if username.lower() in VALID_USERS:
        errors.append("Username already exists")
    
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters long")
    
    if password != confirm_password:
        errors.append("Passwords do not match")
    
    return errors


def login_required(func):
    def wrapper(*args, **kwargs):
        if session.get("logged_in"):
            return func(*args, **kwargs)
        flash("Please login to access the VAPT toolkit.", "warning")
        return redirect(url_for("login"))
    wrapper.__name__ = func.__name__
    return wrapper


def explain_process(module, attack):
    details = {
        "sqli": "SQL Injection: Tests if unsanitized inputs can manipulate database queries. Read results for database output/error messages. Fix by using prepared statements and input validation.",
        "xss": "Cross Site Scripting: Checks if user input is reflected in HTML/JS. Read results for payload reflection. Remove by escaping output and enforcing CSP.",
        "dir": "Directory Traversal: Tests path traversal to access restricted files. Fix by normalizing paths and forbidding '..' patterns.",
        "misconfig": "Security Misconfiguration: Checks for unsafe server settings. Fix by hardening config and minimal permissions.",
        "outdated": "Outdated Software: Detects old versions with known vulnerabilities. Fix by updating to latest secure versions.",
        "sensitive": "Sensitive Data Exposure: Scans for leaked secrets or confidential files.",
        "headers": "Security Headers: Ensures secure HTTP header policies are enforced.",
        "csrf": "CSRF: Verifies token-based protections. Fix by implementing anti-CSRF tokens and SameSite cookies.",
        "clickjacking": "Clickjacking: Checks X-Frame-Options/CSP to prevent framing attacks.",
        "bruteforce": "Brute Force: Simulates credential guessing attacks. Mitigate with rate limiting and account lockouts.",
        "broken_auth": "Broken Authentication: Assesses weak login flows and session management.",
        "insecure_cookies": "Insecure Cookies: Verifies Secure/HttpOnly/SameSite flags on cookies.",
        "ssl_scan": "SSL/TLS: Tests encryption strength and protocol support. Fix by enforcing TLS1.2+ and strong ciphers."
    }
    return details.get(attack, "Process explanation unavailable.")


@app.route("/")
def home():
    if session.get("logged_in"):
        return render_template("index.html", user=session.get("user"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        if username in VALID_USERS and VALID_USERS[username] == password:
            session["logged_in"] = True
            session["user"] = username
            flash(f"Welcome, {username}.", "success")
            return redirect(url_for("home"))

        flash("Invalid credentials.", "danger")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        errors = validate_signup_input(username, password, confirm_password)
        
        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            # Register new user
            VALID_USERS[username] = password
            flash(f"Account created successfully! You can now login.", "success")
            return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("login"))


@app.route("/vulnscan")
@login_required
def vulnscan():
    return render_template("vulnscan.html")


@app.route("/pentest")
@login_required
def pentest():
    return render_template("pentest.html")


@app.route("/learning")
@login_required
def learning():
    topics = [
        {"attack": "SQL Injection", "objective": "Extract data via malicious queries", "mitigation": "Use parameterized queries"},
        {"attack": "XSS", "objective": "Execute scripts in client browser", "mitigation": "Escape output, enforce CSP"},
        {"attack": "Directory Traversal", "objective": "Read restricted files", "mitigation": "Normalize paths, block .."},
        {"attack": "CSRF", "objective": "Force unwanted authenticated actions", "mitigation": "Anti-CSRF tokens"},
        {"attack": "Brute Force", "objective": "Guess credentials via loop attacks", "mitigation": "Rate limiting, lockouts"},
        {"attack": "Broken Auth", "objective": "Exploit weak session/login logic", "mitigation": "Secure login flows"},
        {"attack": "Insecure Cookies", "objective": "Hijack session tokens", "mitigation": "HttpOnly, Secure, SameSite"},
        {"attack": "SSL/TLS", "objective": "Encrypt data in transit securely", "mitigation": "TLS1.2+, strong ciphers"},
        {"attack": "Misconfig", "objective": "Find unsafe settings/defaults", "mitigation": "Harden config"},
        {"attack": "Outdated Software", "objective": "Exploit known CVEs", "mitigation": "Update dependencies"},
    ]
    return render_template("learning.html", topics=topics)


@app.route("/scan", methods=["POST"])
@login_required
def scan():
    target = request.form.get("target")
    module = request.form.get("module")
    attack = request.form.get("attack")

    scan_type = "Vulnerability Scan" if module == "vulnerability" else "Penetration Test"
    result = scanner.execute_scan(module, attack, target)
    severity = analyze_severity(result)
    report = generate_report(target, attack, result, severity, scan_type)

    session["last_report"] = report

    return render_template(
        "result.html",
        target=target,
        scan_type=scan_type,
        attack=attack,
        severity=severity,
        result=result,
        report=report,
        process_info=explain_process(module, attack),
        user=session.get("user")
    )


@app.route("/download_report")
@login_required
def download_report():
    report = session.get("last_report")
    if not report:
        flash("No report to download. Run a scan first.", "warning")
        return redirect(url_for("home"))

    pdf_bytes = generate_report_pdf(report)
    if not pdf_bytes:
        flash("PDF export requires fpdf (pip install fpdf).", "danger")
        return redirect(url_for("home"))

    filename = f"vapt_{report['attack']}_{report['generated_at'].replace(' ', '_').replace(':','-')}.pdf"
    return send_file(BytesIO(pdf_bytes), as_attachment=True, download_name=filename, mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=True)
