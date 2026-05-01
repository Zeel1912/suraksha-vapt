<?php
// Vulnerable comment system with stored XSS
$conn = new mysqli("localhost", "root", "", "vulnerable_db");
$conn->select_db("vulnerable_db");

// Create comments table
$conn->query("CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author VARCHAR(50),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)");

$message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $author = $_POST['author'];
    $comment = $_POST['comment'];

    // VULNERABLE: No input sanitization - stored XSS
    $sql = "INSERT INTO comments (author, comment) VALUES ('$author', '$comment')";
    if ($conn->query($sql)) {
        $message = "Comment added successfully!";
    } else {
        $message = "Error adding comment.";
    }
}

// Get all comments
$comments = [];
$result = $conn->query("SELECT * FROM comments ORDER BY created_at DESC");
if ($result) {
    while ($row = $result->fetch_assoc()) {
        $comments[] = $row;
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Comments - Vulnerable</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .comment-form { margin-bottom: 30px; }
        .comment-form input, .comment-form textarea { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
        .comment-form button { padding: 10px 20px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .comment-form button:hover { background: #1565c0; }
        .warning { background: #ffebee; border: 1px solid #f44336; color: #c62828; padding: 10px; border-radius: 4px; margin-bottom: 20px; }
        .comment { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 4px; background: #fafafa; }
        .comment .author { font-weight: bold; color: #1976d2; }
        .comment .date { color: #666; font-size: 12px; }
        .message { color: #4caf50; text-align: center; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">
            <strong>VULNERABLE:</strong> This comment system is vulnerable to stored XSS attacks. Any JavaScript in comments will execute for all visitors.
        </div>

        <h2>💬 Comments</h2>

        <?php if ($message): ?>
            <div class="message"><?php echo $message; ?></div>
        <?php endif; ?>

        <form class="comment-form" method="POST">
            <input type="text" name="author" placeholder="Your name" required>
            <textarea name="comment" rows="4" placeholder="Leave a comment..." required></textarea>
            <button type="submit">Post Comment</button>
        </form>

        <h3>Recent Comments:</h3>
        <?php if (empty($comments)): ?>
            <p>No comments yet. Be the first to comment!</p>
        <?php else: ?>
            <?php foreach ($comments as $comment): ?>
                <div class="comment">
                    <div class="author"><?php echo htmlspecialchars($comment['author']); ?></div>
                    <div class="date"><?php echo $comment['created_at']; ?></div>
                    <div><?php echo $comment['comment']; // VULNERABLE: No output escaping ?></div>
                </div>
            <?php endforeach; ?>
        <?php endif; ?>

        <p style="text-align: center; margin-top: 20px;">
            <a href="/">← Back to Home</a>
        </p>

        <div style="margin-top: 20px; font-size: 12px; color: #666;">
            <strong>Test XSS Payloads:</strong><br>
            &lt;script&gt;alert('Stored XSS!')&lt;/script&gt;<br>
            &lt;img src=x onerror=alert('XSS')&gt;
        </div>
    </div>
</body>
</html>