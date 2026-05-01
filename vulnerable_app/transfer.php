<?php
// Vulnerable money transfer page with CSRF
session_start();

if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit();
}

$conn = new mysqli("localhost", "root", "", "vulnerable_db");
$conn->select_db("vulnerable_db");

$message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $to_user = $_POST['to_user'];
    $amount = (float)$_POST['amount'];

    // VULNERABLE: No CSRF protection
    if ($amount > 0 && $amount <= $_SESSION['balance']) {
        // Update balances (simplified - no real transaction safety)
        $conn->query("UPDATE users SET balance = balance - $amount WHERE username = '{$_SESSION['user']}'");
        $conn->query("UPDATE users SET balance = balance + $amount WHERE username = '$to_user'");

        $_SESSION['balance'] -= $amount;
        $message = "Transfer of $$amount to $to_user completed!";
    } else {
        $message = "Invalid transfer amount or insufficient balance.";
    }
}

// Get all users for transfer options
$users = [];
$result = $conn->query("SELECT username FROM users WHERE username != '{$_SESSION['user']}'");
if ($result) {
    while ($row = $result->fetch_assoc()) {
        $users[] = $row['username'];
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Money Transfer - Vulnerable</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .balance { background: #e8f5e8; padding: 10px; border-radius: 4px; margin-bottom: 20px; text-align: center; }
        .transfer-form { margin-bottom: 20px; }
        .transfer-form select, .transfer-form input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
        .transfer-form button { width: 100%; padding: 10px; background: #4caf50; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .transfer-form button:hover { background: #45a049; }
        .warning { background: #ffebee; border: 1px solid #f44336; color: #c62828; padding: 10px; border-radius: 4px; margin-bottom: 20px; }
        .message { text-align: center; margin: 10px 0; padding: 10px; border-radius: 4px; }
        .success { background: #e8f5e8; color: #2e7d32; }
        .error { background: #ffebee; color: #c62828; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">
            <strong>VULNERABLE:</strong> This transfer form has no CSRF protection. It can be exploited by malicious websites.
        </div>

        <h2>💸 Money Transfer</h2>
        <p>Welcome, <?php echo htmlspecialchars($_SESSION['user']); ?>!</p>

        <div class="balance">
            <strong>Your Balance: $<?php echo number_format($_SESSION['balance'], 2); ?></strong>
        </div>

        <?php if ($message): ?>
            <div class="message <?php echo strpos($message, 'completed') !== false ? 'success' : 'error'; ?>">
                <?php echo $message; ?>
            </div>
        <?php endif; ?>

        <form class="transfer-form" method="POST">
            <select name="to_user" required>
                <option value="">Select recipient</option>
                <?php foreach ($users as $user): ?>
                    <option value="<?php echo $user; ?>"><?php echo $user; ?></option>
                <?php endforeach; ?>
            </select>

            <input type="number" name="amount" step="0.01" min="0.01" placeholder="Amount to transfer" required>

            <button type="submit">Transfer Money</button>
        </form>

        <p style="text-align: center; margin-top: 20px;">
            <a href="dashboard.php">← Back to Dashboard</a> | <a href="logout.php">Logout</a>
        </p>

        <div style="margin-top: 20px; font-size: 12px; color: #666;">
            <strong>CSRF Test:</strong> This form can be submitted from external sites without your knowledge.
        </div>
    </div>
</body>
</html>