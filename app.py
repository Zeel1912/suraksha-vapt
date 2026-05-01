from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from io import BytesIO
from core_engine.scan_orchestrator import ScanOrchestrator
from reporting.report_generator import generate_report, generate_report_pdf
from reporting.severity_analyzer import analyze_severity
import subprocess
import os

app = Flask(__name__)
app.secret_key = "change_this_secret_in_production"

scanner = ScanOrchestrator()

# User storage (in-memory for demo; use database for production)
VALID_USERS = {
    "admin": "Admin@123",
    "pentester": "Pentest@2026"
}

# Sandbox server process
sandbox_process = None


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
        {
            "attack": "SQL Injection",
            "objective": "Extract, modify, or delete database data by injecting malicious SQL code",
            "identification": "Look for SQL syntax errors in responses, unexpected data leakage, or successful injection payloads like ' OR 1=1 --",
            "mitigation": "Use parameterized queries/prepared statements, input validation, stored procedures, and ORM frameworks. Never concatenate user input directly into SQL queries."
        },
        {
            "attack": "XSS",
            "objective": "Execute malicious scripts in users' browsers to steal cookies, session tokens, or perform actions on behalf of users",
            "identification": "Check if script payloads like <script>alert(1)</script> appear in page output, or if JavaScript executes when injected into forms/URLs",
            "mitigation": "Escape all user input before outputting to HTML, use Content Security Policy (CSP), validate and sanitize input, use safe encoding functions"
        },
        {
            "attack": "Directory Traversal",
            "objective": "Access files and directories outside the web root by manipulating path traversal sequences",
            "identification": "Monitor for payloads like ../../../etc/passwd or ..\\..\\windows\\system32\\config\\sam in file access attempts",
            "mitigation": "Normalize all file paths, validate input against whitelist, use chroot/jails, avoid direct file system access, implement proper path validation"
        },
        {
            "attack": "CSRF",
            "objective": "Trick authenticated users into performing unwanted actions on web applications they're logged into",
            "identification": "Check if state-changing operations can be performed via GET requests or without proper token validation",
            "mitigation": "Implement anti-CSRF tokens in all forms, use SameSite cookie attribute, require re-authentication for sensitive operations, validate Origin/Referer headers"
        },
        {
            "attack": "Brute Force",
            "objective": "Systematically try all possible combinations of credentials until finding valid ones",
            "identification": "Monitor for multiple failed login attempts from same IP, unusual login patterns, or successful logins with weak passwords",
            "mitigation": "Implement account lockouts after failed attempts, use CAPTCHA, enforce strong password policies, implement rate limiting, use multi-factor authentication"
        },
        {
            "attack": "Broken Authentication",
            "objective": "Exploit flaws in authentication mechanisms to impersonate users or bypass login controls",
            "identification": "Check for predictable session IDs, missing logout functionality, weak password recovery, or session fixation vulnerabilities",
            "mitigation": "Use secure session management, implement proper logout, enforce password complexity, use secure password recovery, implement account lockouts"
        },
        {
            "attack": "Insecure Cookies",
            "objective": "Intercept or manipulate session cookies to hijack user sessions or steal sensitive information",
            "identification": "Check cookie attributes (Secure, HttpOnly, SameSite), verify if cookies are transmitted over HTTP, test for cookie manipulation",
            "mitigation": "Set Secure flag for HTTPS-only cookies, use HttpOnly to prevent JavaScript access, implement SameSite attribute, use secure random session IDs"
        },
        {
            "attack": "SSL/TLS Vulnerabilities",
            "objective": "Intercept encrypted communications or exploit weak cryptographic implementations",
            "identification": "Check for SSLv2/SSLv3 usage, weak ciphers, certificate validation issues, or protocol downgrade attacks",
            "mitigation": "Use TLS 1.2 or higher, disable weak ciphers, implement HSTS headers, regular certificate renewal, use strong key sizes"
        },
        {
            "attack": "Security Misconfiguration",
            "objective": "Exploit improperly configured security settings, default credentials, or exposed sensitive information",
            "identification": "Check for default passwords, unnecessary services running, verbose error messages, directory listings, exposed configuration files",
            "mitigation": "Regular security audits, remove default accounts, disable unnecessary features, use minimal privilege principle, implement proper error handling"
        },
        {
            "attack": "Outdated Software",
            "objective": "Exploit known vulnerabilities in unpatched software, libraries, or frameworks",
            "identification": "Check software versions against CVE databases, monitor for known vulnerable components, scan for outdated libraries",
            "mitigation": "Regular patch management, dependency scanning, use vulnerability management tools, implement automated updates where possible"
        }
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
        flash("PDF export requires weasyprint (pip install weasyprint). Please install it and try again.", "danger")
        return redirect(url_for("home"))

    # Clean filename
    timestamp = report['generated_at'].replace(' ', '_').replace(':', '-').replace('.', '-')
    filename = f"SURAKSHA_VAPT_{report['attack']}_{timestamp}.pdf"

    return send_file(BytesIO(pdf_bytes), as_attachment=True, download_name=filename, mimetype="application/pdf")


@app.route("/sandbox/start")
@login_required
def start_sandbox():
    """Start the vulnerable test environment"""
    global sandbox_process

    try:
        if sandbox_process is None or sandbox_process.poll() is not None:
            # Start the vulnerable app server
            vulnerable_app_dir = os.path.join(os.path.dirname(__file__), "vulnerable_app")
            sandbox_process = subprocess.Popen(
                ["python3", "server.py"],
                cwd=vulnerable_app_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            flash("🎯 Sandbox environment started! Access at http://localhost:8080", "success")
        else:
            flash("⚠️ Sandbox environment is already running", "warning")
    except Exception as e:
        flash(f"❌ Failed to start sandbox: {str(e)}", "danger")

    return redirect(url_for("home"))


@app.route("/sandbox/stop")
@login_required
def stop_sandbox():
    """Stop the vulnerable test environment"""
    global sandbox_process

    try:
        if sandbox_process and sandbox_process.poll() is None:
            sandbox_process.terminate()
            sandbox_process.wait(timeout=5)
            sandbox_process = None
            flash("🛑 Sandbox environment stopped", "info")
        else:
            flash("⚠️ Sandbox environment is not running", "warning")
    except Exception as e:
        flash(f"❌ Failed to stop sandbox: {str(e)}", "danger")

    return redirect(url_for("home"))


@app.route("/sandbox/status")
@login_required
def sandbox_status():
    """Check sandbox status"""
    global sandbox_process

    if sandbox_process and sandbox_process.poll() is None:
        return {"status": "running", "url": "http://localhost:8080"}
    else:
        return {"status": "stopped"}


if __name__ == "__main__":
    app.run(debug=True)
