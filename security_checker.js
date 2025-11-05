/**
 * Security Checker Script
 * Kiểm tra các lỗ hổng bảo mật phổ biến
 */

// Danh sách từ khóa nguy hiểm
const DANGEROUS_KEYWORDS = [
    // API Keys
    'client_secret',
    'api_key',
    'private_key',
    'secret_key',
    'access_token',
    'refresh_token',
    
    // PayPal/Stripe
    'sk_live_',
    'pk_live_',
    'sk_test_',
    'pk_test_',
    'client_secret',
    
    // Authentication
    'Basic ',
    'Bearer ',
    'Authorization',
    'password',
    'passwd',
    'pwd',
    
    // Database
    'database_url',
    'db_password',
    'connection_string',
    
    // Cloud Services
    'aws_secret',
    'google_api_key',
    'azure_key',
    
    // Common patterns
    'secret',
    'token',
    'key',
    'credential'
];

// Hàm kiểm tra một đoạn text
function checkTextForSecrets(text, filename) {
    const issues = [];
    
    DANGEROUS_KEYWORDS.forEach(keyword => {
        const regex = new RegExp(keyword, 'gi');
        const matches = text.match(regex);
        
        if (matches) {
            issues.push({
                keyword: keyword,
                count: matches.length,
                filename: filename,
                severity: getSeverity(keyword)
            });
        }
    });
    
    return issues;
}

// Xác định mức độ nguy hiểm
function getSeverity(keyword) {
    const highRisk = ['client_secret', 'sk_live_', 'pk_live_', 'private_key'];
    const mediumRisk = ['api_key', 'password', 'Basic '];
    
    if (highRisk.some(risk => keyword.toLowerCase().includes(risk.toLowerCase()))) {
        return 'HIGH';
    } else if (mediumRisk.some(risk => keyword.toLowerCase().includes(risk.toLowerCase()))) {
        return 'MEDIUM';
    } else {
        return 'LOW';
    }
}

// Hàm quét tất cả scripts trên trang
function scanPageForSecrets() {
    const results = [];
    
    // Lấy tất cả script tags
    const scripts = document.querySelectorAll('script');
    
    scripts.forEach((script, index) => {
        if (script.src) {
            // External script
            console.log(`Checking external script: ${script.src}`);
            // Note: Không thể đọc nội dung external script từ browser
            results.push({
                type: 'external_script',
                src: script.src,
                warning: 'External script - check manually'
            });
        } else {
            // Inline script
            const content = script.innerHTML;
            const issues = checkTextForSecrets(content, `inline_script_${index}`);
            if (issues.length > 0) {
                results.push({
                    type: 'inline_script',
                    issues: issues,
                    content: content.substring(0, 200) + '...'
                });
            }
        }
    });
    
    return results;
}

// Hàm kiểm tra localStorage/sessionStorage
function checkStorageForSecrets() {
    const results = [];
    
    // Kiểm tra localStorage
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        const value = localStorage.getItem(key);
        
        const issues = checkTextForSecrets(value, `localStorage.${key}`);
        if (issues.length > 0) {
            results.push({
                type: 'localStorage',
                key: key,
                issues: issues,
                value: value.substring(0, 100) + '...'
            });
        }
    }
    
    // Kiểm tra sessionStorage
    for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        const value = sessionStorage.getItem(key);
        
        const issues = checkTextForSecrets(value, `sessionStorage.${key}`);
        if (issues.length > 0) {
            results.push({
                type: 'sessionStorage',
                key: key,
                issues: issues,
                value: value.substring(0, 100) + '...'
            });
        }
    }
    
    return results;
}

// Hàm chính để chạy kiểm tra
function runSecurityScan() {
    console.log('🔍 Starting Security Scan...');
    
    const results = {
        scripts: scanPageForSecrets(),
        storage: checkStorageForSecrets(),
        timestamp: new Date().toISOString()
    };
    
    // Hiển thị kết quả
    console.log('📊 Security Scan Results:', results);
    
    // Tạo báo cáo
    generateSecurityReport(results);
    
    return results;
}

// Tạo báo cáo bảo mật
function generateSecurityReport(results) {
    let report = '🚨 SECURITY SCAN REPORT\n';
    report += '=' .repeat(50) + '\n\n';
    
    // Scripts
    if (results.scripts.length > 0) {
        report += '📜 SCRIPTS WITH ISSUES:\n';
        results.scripts.forEach(script => {
            if (script.issues) {
                report += `\nFile: ${script.type}\n`;
                script.issues.forEach(issue => {
                    report += `  ⚠️  ${issue.severity}: ${issue.keyword} (${issue.count} occurrences)\n`;
                });
            }
        });
        report += '\n';
    }
    
    // Storage
    if (results.storage.length > 0) {
        report += '💾 STORAGE WITH ISSUES:\n';
        results.storage.forEach(storage => {
            report += `\n${storage.type}: ${storage.key}\n`;
            storage.issues.forEach(issue => {
                report += `  ⚠️  ${issue.severity}: ${issue.keyword} (${issue.count} occurrences)\n`;
            });
        });
        report += '\n';
    }
    
    // Tổng kết
    const totalIssues = results.scripts.filter(s => s.issues).length + results.storage.length;
    if (totalIssues === 0) {
        report += '✅ No security issues found!\n';
    } else {
        report += `🚨 Total issues found: ${totalIssues}\n`;
        report += '\n🔧 RECOMMENDATIONS:\n';
        report += '1. Remove hardcoded secrets from client-side code\n';
        report += '2. Use environment variables for sensitive data\n';
        report += '3. Implement proper authentication (JWT, OAuth)\n';
        report += '4. Use HTTPS for all communications\n';
        report += '5. Implement proper session management\n';
    }
    
    console.log(report);
    
    // Copy to clipboard (nếu được hỗ trợ)
    if (navigator.clipboard) {
        navigator.clipboard.writeText(report).then(() => {
            console.log('📋 Report copied to clipboard');
        });
    }
    
    return report;
}

// Export functions để sử dụng trong console
window.securityCheck = {
    run: runSecurityScan,
    checkText: checkTextForSecrets,
    checkStorage: checkStorageForSecrets,
    keywords: DANGEROUS_KEYWORDS
};

console.log('🔧 Security Checker loaded!');
console.log('Usage: securityCheck.run()');
