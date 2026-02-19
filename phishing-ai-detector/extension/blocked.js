// blocked.js - Direct API Version
document.addEventListener('DOMContentLoaded', () => {
    console.log("0Scam Blocker: Initializing...");

    const params = new URLSearchParams(window.location.search);
    const originalUrl = params.get('url');
    const risk = params.get('risk');
    const conf = params.get('conf');

    const urlBanner = document.getElementById('blocked-url');
    const riskLevel = document.getElementById('risk-level');
    const confidence = document.getElementById('confidence');
    const btnBack = document.getElementById('btn-back');
    const btnBypass = document.getElementById('btn-bypass');

    // Populate UI
    if (originalUrl) urlBanner.textContent = decodeURIComponent(originalUrl);
    if (risk) riskLevel.textContent = risk.toUpperCase();
    if (conf) confidence.textContent = (parseFloat(conf) * 100).toFixed(1) + "%";

    // GO TO SAFETY
    if (btnBack) {
        btnBack.addEventListener('click', async (e) => {
            e.preventDefault();
            btnBack.textContent = "NAVIGATING...";
            chrome.runtime.sendMessage({ action: "goBack" });
        });
    }

    // UNBLOCK SITE
    if (btnBypass) {
        btnBypass.addEventListener('click', async (e) => {
            e.preventDefault();
            const decodedUrl = decodeURIComponent(originalUrl);
            
            if (confirm("WARNING: Bypassing this shield may expose your passwords. Are you sure?")) {
                btnBypass.textContent = "UNBLOCKING...";
                
                // 1. Send Whitelist Message
                chrome.runtime.sendMessage({ action: "whitelist", url: decodedUrl }, (response) => {
                    // 2. ONLY AFTER whitelist is confirmed, navigate the tab back
                    if (response && response.success) {
                        chrome.tabs.getCurrent((tab) => {
                            if (tab && tab.id) {
                                // Redirect tab back to original malicious page
                                chrome.tabs.update(tab.id, { url: decodedUrl });
                            } else {
                                window.location.href = decodedUrl;
                            }
                        });
                    } else {
                        console.error("[0Scam] Whitelist failed.");
                        alert("Error whitelisting URL.");
                    }
                });
            }
        });
    }
});
