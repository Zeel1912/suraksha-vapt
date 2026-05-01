<?php
// Simple dashboard
session_start();

if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit();
}

$conn = new mysqli("localhost", "root", "", "vulnerable_db");
$conn->select_db("vulnerable_db");

// Update session balance
$result = $conn->query("SELECT balance FROM users WHERE username = '{$_SESSION['user']}'");
if ($result && $row = $result->fetch_assoc()) {
    $_SESSION['balance'] = $row['balance'];
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Vulnerable</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .balance { background: #e8f5e8; padding: 15px; border-radius: 4px; margin-bottom: 20px; text-align: center; }
        .menu { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .menu a { display: block; padding: 15px; background: #1976d2; color: white; text-decoration: none; border-radius: 4px; text-align: center; }
        .menu a:hover { background: #1565c0; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🏠 Dashboard</h2>
        <p>Welcome, <?php echo htmlspecialchars($_SESSION['user']); ?>!</p>

        <div class="balance">
            <strong>Your Balance: $<?php echo number_format($_SESSION['balance'], 2); ?></strong>
        </div>

        <div class="menu">
            <a href="transfer.php">💸 Transfer Money</a>
            <a href="profile.php">👤 Profile</a>
            <a href="comment.php">💬 Comments</a>
            <a href="search.php">🔍 Search</a>
        </div>

        <p style="text-align: center; margin-top: 20px;">
            <a href="logout.php">🚪 Logout</a>
        </p>
    </div>
</body>
</html>