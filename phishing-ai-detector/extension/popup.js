document.addEventListener('DOMContentLoaded', async () => {
    const statusText = document.getElementById('status-text');
    const classificationVal = document.getElementById('classification-val');
    const riskVal = document.getElementById('risk-level');
    const confVal = document.getElementById('conf-val');
    const urlDisplay = document.getElementById('url-display');
    const pulse = document.getElementById('pulse');
    const toggle = document.getElementById('protection-toggle');
    const refreshBtn = document.getElementById('refresh-btn');
    const toolbarBadge = document.getElementById('toolbar-badge');

    let currentTabId = null;

    function updateUI(data) {
        if (!data) return;

        const classification = (data.classification || "Unknown").toUpperCase();
        const risk = (data.risk_level || "Low").toUpperCase();
        const confidence = data.confidence ? (data.confidence * 100).toFixed(1) + "%" : "-";
        
        classificationVal.textContent = data.classification || "Unknown";
        riskVal.textContent = data.risk_level || "-";
        confVal.textContent = confidence;
        urlDisplay.textContent = data.url || "Unknown";

        // Reset classes
        statusText.className = "status-text";
        pulse.className = "status-pulse";
        classificationVal.className = "value";
        toolbarBadge.className = "toolbar-badge";

        if (classification === "PHISHING" || (classification === "SUSPICIOUS" && risk === "HIGH")) {
            statusText.textContent = "THREAT BLOCKED";
            statusText.classList.add("phishing");
            pulse.classList.add("pulse-danger");
            classificationVal.classList.add("phishing");
            
            // Set Menu Badge [BLK]
            toolbarBadge.textContent = "BLK";
            toolbarBadge.classList.add("badge-blk");

        } else if (classification === "SUSPICIOUS") {
            statusText.textContent = "UNSAFE CONTENT";
            statusText.classList.add("suspicious");
            pulse.classList.add("pulse-warn");
            classificationVal.classList.add("suspicious");
            
            // Set Menu Badge [BLK]
            toolbarBadge.textContent = "BLK";
            toolbarBadge.classList.add("badge-warn");

        } else {
            statusText.textContent = "SYSTEM SECURE";
            statusText.classList.add("safe");
            pulse.classList.add("pulse-safe");
            classificationVal.classList.add("safe");
            
            // Set Menu Badge [OK]
            toolbarBadge.textContent = "OK";
            toolbarBadge.classList.add("badge-ok");
        }
    }

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) {
        currentTabId = tab.id;
        
        if (tab.url.includes("blocked.html")) {
            const urlParams = new URL(tab.url).searchParams;
            const originalUrl = urlParams.get('url');
            const risk = urlParams.get('risk');
            const conf = urlParams.get('conf');

            if (originalUrl) {
                updateUI({
                    url: decodeURIComponent(originalUrl),
                    classification: "PHISHING",
                    risk_level: risk || "HIGH",
                    confidence: parseFloat(conf || 1.0)
                });
                return;
            }
        }

        urlDisplay.textContent = tab.url;
        chrome.storage.local.get(currentTabId.toString(), (result) => {
            if (result[currentTabId]) {
                updateUI(result[currentTabId]);
            } else {
                statusText.textContent = "SCANNING...";
                statusText.className = "status-text suspicious";
                pulse.className = "status-pulse pulse-warn";
                toolbarBadge.textContent = "...";
            }
        });
    }

    chrome.runtime.onMessage.addListener((message) => {
        if (message.action === "updateUI" && message.tabId === currentTabId) {
            updateUI(message.data);
        }
    });

    chrome.storage.local.get(['isEnabled'], (result) => {
        toggle.checked = result.isEnabled !== false; 
    });

    toggle.addEventListener('change', () => {
        chrome.storage.local.set({ isEnabled: toggle.checked });
        if (currentTabId) chrome.tabs.reload(currentTabId);
    });

    refreshBtn.addEventListener('click', () => {
        if (currentTabId) {
            chrome.tabs.reload(currentTabId);
            window.close();
        }
    });
});
