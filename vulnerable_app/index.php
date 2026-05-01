<!DOCTYPE html>
<html>
<head>
    <title>SURAKSHA Vulnerable Test Environment</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .warning { background: #ffebee; border: 1px solid #f44336; color: #c62828; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .vulnerability-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
        .vuln-card { border: 1px solid #ddd; padding: 15px; border-radius: 5px; background: #fafafa; }
        .vuln-card h3 { margin-top: 0; color: #d32f2f; }
        .vuln-card a { display: inline-block; background: #1976d2; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; margin: 5px 0; }
        .vuln-card a:hover { background: #1565c0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">
            <h2>⚠️ WARNING: Educational Test Environment</h2>
            <p><strong>This is a deliberately vulnerable web application created for educational purposes only.</strong></p>
            <p>It contains intentional security vulnerabilities to demonstrate common attack types. This application should NEVER be exposed to the internet or used in production environments.</p>
            <p><strong>Use only for learning cybersecurity concepts with the SURAKSHA VAPT platform.</strong></p>
        </div>

        <h1>🎯 SURAKSHA Vulnerable Test Environment</h1>
        <p>This environment provides safe, controlled targets for testing various security vulnerabilities. Each vulnerability is intentionally implemented for educational demonstration.</p>

        <div class="vulnerability-list">
            <div class="vuln-card">
                <h3>💉 SQL Injection</h3>
                <p>Test SQL injection attacks on login forms and search functionality.</p>
                <a href="login.php">Login Form (SQLi)</a><br>
                <a href="search.php">Search (SQLi)</a>
            </div>

            <div class="vuln-card">
                <h3>🎭 Cross-Site Scripting (XSS)</h3>
                <p>Test reflected and stored XSS vulnerabilities.</p>
                <a href="comment.php">Comment System (Stored XSS)</a><br>
                <a href="search.php?query=<script>alert('XSS')</script>">Search (Reflected XSS)</a>
            </div>

            <div class="vuln-card">
                <h3>🔄 Cross-Site Request Forgery (CSRF)</h3>
                <p>Test CSRF attacks on form submissions.</p>
                <a href="transfer.php">Money Transfer (CSRF)</a><br>
                <a href="profile.php">Profile Update (CSRF)</a>
            </div>

            <div class="vuln-card">
                <h3>🔨 Brute Force Attacks</h3>
                <p>Test brute force attacks on authentication.</p>
                <a href="login.php">Login Form (Brute Force)</a>
            </div>

            <div class="vuln-card">
                <h3>🔓 Broken Authentication</h3>
                <p>Test weak session management and authentication bypass.</p>
                <a href="admin.php">Admin Panel (Broken Auth)</a><br>
                <a href="forgot.php">Password Reset (Broken)</a>
            </div>

            <div class="vuln-card">
                <h3>🍪 Insecure Cookies</h3>
                <p>Test insecure cookie configurations.</p>
                <a href="login.php">Login (Check Cookies)</a>
            </div>

            <div class="vuln-card">
                <h3>📁 Directory Traversal</h3>
                <p>Test path traversal attacks.</p>
                <a href="file.php?file=readme.txt">File Viewer (Traversal)</a>
            </div>

            <div class="vuln-card">
                <h3>🔒 SSL/TLS Issues</h3>
                <p>Test SSL/TLS configurations (requires HTTPS).</p>
                <a href="https://localhost:8443/">HTTPS Test</a>
            </div>

            <div class="vuln-card">
                <h3>⚙️ Security Misconfiguration</h3>
                <p>Test common misconfiguration issues.</p>
                <a href="config.php">Config Exposure</a><br>
                <a href="backup.sql">Backup File</a>
            </div>

            <div class="vuln-card">
                <h3>📅 Outdated Components</h3>
                <p>Test vulnerabilities in outdated software.</p>
                <a href="info.php">PHP Info (Outdated)</a>
            </div>
        </div>

        <div style="margin-top: 30px; padding: 20px; background: #e3f2fd; border-radius: 5px;">
            <h3>📚 How to Use This Environment</h3>
            <ol>
                <li>Use the SURAKSHA VAPT platform to scan this environment</li>
                <li>Try different attack types against the vulnerable endpoints</li>
                <li>Observe how attacks succeed and learn from the results</li>
                <li>Study the source code to understand the vulnerabilities</li>
                <li>Apply the mitigation strategies learned in the platform</li>
            </ol>
        </div>
    </div>
</body>
</html>