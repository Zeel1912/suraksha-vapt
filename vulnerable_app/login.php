<?php
// Vulnerable login page with SQL injection
session_start();

// Database connection (intentionally vulnerable)
$conn = new mysqli("localhost", "root", "", "vulnerable_db");

// Create database and table if not exists
$conn->query("CREATE DATABASE IF NOT EXISTS vulnerable_db");
$conn->select_db("vulnerable_db");
$conn->query("CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    balance DECIMAL(10,2) DEFAULT 1000.00
)");
$conn->query("INSERT IGNORE INTO users (username, password) VALUES ('admin', 'admin123')");
$conn->query("INSERT IGNORE INTO users (username, password) VALUES ('user', 'password')");

$message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // VULNERABLE: Direct SQL injection
    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    $result = $conn->query($query);

    if ($result && $result->num_rows > 0) {
        $user = $result->fetch_assoc();
        $_SESSION['user'] = $user['username'];
        $_SESSION['balance'] = $user['balance'];
        header("Location: dashboard.php");
        exit();
    } else {
        $message = "Invalid credentials!";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login - Vulnerable</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 400px; margin: 50px auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
        button { width: 100%; padding: 10px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #1565c0; }
        .warning { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 10px; border-radius: 4px; margin-bottom: 20px; }
        .message { color: #d32f2f; text-align: center; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">
            <strong>VULNERABLE:</strong> This login form is intentionally vulnerable to SQL injection attacks.
        </div>

        <h2>🔐 Login</h2>

        <?php if ($message): ?>
            <div class="message"><?php echo $message; ?></div>
        <?php endif; ?>

        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>

        <p style="text-align: center; margin-top: 20px;">
            <a href="/">← Back to Home</a>
        </p>

        <div style="margin-top: 20px; font-size: 12px; color: #666;">
            <strong>Test Credentials:</strong><br>
            admin / admin123<br>
            user / password
        </div>
    </div>
</body>
</html>