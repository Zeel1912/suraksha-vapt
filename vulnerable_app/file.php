<?php
// Vulnerable file viewer with directory traversal
$file = isset($_GET['file']) ? $_GET['file'] : 'readme.txt';

// VULNERABLE: No path validation - directory traversal
$full_path = $file;

$message = "";
$content = "";

if (file_exists($full_path)) {
    $content = file_get_contents($full_path);
} else {
    $message = "File not found: " . htmlspecialchars($file);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>File Viewer - Vulnerable</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .warning { background: #ffebee; border: 1px solid #f44336; color: #c62828; padding: 10px; border-radius: 4px; margin-bottom: 20px; }
        .file-content { background: #f5f5f5; border: 1px solid #ddd; padding: 15px; border-radius: 4px; font-family: monospace; white-space: pre-wrap; }
        .error { color: #d32f2f; text-align: center; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">
            <strong>VULNERABLE:</strong> This file viewer is vulnerable to directory traversal attacks.
        </div>

        <h2>📁 File Viewer</h2>

        <form method="GET" style="margin-bottom: 20px;">
            <input type="text" name="file" value="<?php echo htmlspecialchars($file); ?>" style="width: 70%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            <button type="submit" style="padding: 8px 16px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer;">View File</button>
        </form>

        <?php if ($message): ?>
            <div class="error"><?php echo $message; ?></div>
        <?php endif; ?>

        <?php if ($content): ?>
            <h3>File: <?php echo htmlspecialchars($file); ?></h3>
            <div class="file-content"><?php echo htmlspecialchars($content); ?></div>
        <?php endif; ?>

        <p style="text-align: center; margin-top: 20px;">
            <a href="/">← Back to Home</a>
        </p>

        <div style="margin-top: 20px; font-size: 12px; color: #666;">
            <strong>Test Directory Traversal:</strong><br>
            Try: ../../../etc/passwd<br>
            Try: ../../../../windows/system32/config/sam (on Windows)
        </div>
    </div>
</body>
</html>