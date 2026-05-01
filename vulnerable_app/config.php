<?php
// Vulnerable config file that exposes sensitive information

// VULNERABLE: Exposing database credentials
$config = array(
    'database' => array(
        'host' => 'localhost',
        'username' => 'root',
        'password' => '',
        'database' => 'vulnerable_db'
    ),
    'api_keys' => array(
        'stripe_secret' => 'sk_test_1234567890abcdef',
        'aws_access_key' => 'AKIA1234567890ABCDEF',
        'aws_secret_key' => 'supersecretkey123456789',
        'github_token' => 'ghp_1234567890abcdef1234567890abcdef12345678'
    ),
    'email' => array(
        'smtp_host' => 'smtp.gmail.com',
        'smtp_port' => '587',
        'username' => 'admin@example.com',
        'password' => 'adminpassword123'
    ),
    'debug' => true,
    'environment' => 'development'
);

// VULNERABLE: Printing sensitive information
echo "<h2>⚠️ Configuration Exposed</h2>";
echo "<pre>";
print_r($config);
echo "</pre>";

echo "<h3>🔑 API Keys</h3>";
echo "<ul>";
foreach ($config['api_keys'] as $key => $value) {
    echo "<li><strong>$key:</strong> $value</li>";
}
echo "</ul>";

echo "<p><strong>This information should never be visible to users!</strong></p>";
?>