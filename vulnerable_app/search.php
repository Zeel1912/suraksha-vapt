<?php
// Vulnerable search page with SQL injection and XSS
$conn = new mysqli("localhost", "root", "", "vulnerable_db");
$conn->select_db("vulnerable_db");

// Create sample data
$conn->query("CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price DECIMAL(10,2)
)");
$conn->query("INSERT IGNORE INTO products (name, description, price) VALUES
    ('Laptop', 'High-performance laptop', 999.99),
    ('Phone', 'Smartphone with camera', 599.99),
    ('Tablet', 'Portable tablet device', 299.99)");

$results = [];
$message = "";

if (isset($_GET['query'])) {
    $query = $_GET['query'];

    // VULNERABLE: SQL injection in search
    $sql = "SELECT * FROM products WHERE name LIKE '%$query%' OR description LIKE '%$query%'";
    $result = $conn->query($sql);

    if ($result) {
        while ($row = $result->fetch_assoc()) {
            $results[] = $row;
        }
    }

    $message = "Search results for: " . htmlspecialchars($query);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Search - Vulnerable</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .search-form { margin-bottom: 20px; }
        .search-form input { width: 70%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        .search-form button { padding: 10px 20px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .search-form button:hover { background: #1565c0; }
        .warning { background: #ffebee; border: 1px solid #f44336; color: #c62828; padding: 10px; border-radius: 4px; margin-bottom: 20px; }
        .result { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 4px; background: #fafafa; }
        .result h3 { margin-top: 0; color: #1976d2; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">
            <strong>VULNERABLE:</strong> This search is vulnerable to SQL injection and XSS attacks.
        </div>

        <h2>🔍 Product Search</h2>

        <form class="search-form" method="GET">
            <input type="text" name="query" placeholder="Search products..." value="<?php echo isset($_GET['query']) ? htmlspecialchars($_GET['query']) : ''; ?>" required>
            <button type="submit">Search</button>
        </form>

        <?php if ($message): ?>
            <h3><?php echo $message; ?></h3>
        <?php endif; ?>

        <?php if (!empty($results)): ?>
            <h3>Results:</h3>
            <?php foreach ($results as $product): ?>
                <div class="result">
                    <h3><?php echo htmlspecialchars($product['name']); ?></h3>
                    <p><?php echo htmlspecialchars($product['description']); ?></p>
                    <p><strong>Price: $<?php echo $product['price']; ?></strong></p>
                </div>
            <?php endforeach; ?>
        <?php elseif (isset($_GET['query'])): ?>
            <p>No results found.</p>
        <?php endif; ?>

        <p style="text-align: center; margin-top: 20px;">
            <a href="/">← Back to Home</a>
        </p>

        <div style="margin-top: 20px; font-size: 12px; color: #666;">
            <strong>Test Searches:</strong><br>
            Try: ' OR '1'='1 (SQL injection)<br>
            Try: &lt;script&gt;alert('XSS')&lt;/script&gt; (XSS)
        </div>
    </div>
</body>
</html>