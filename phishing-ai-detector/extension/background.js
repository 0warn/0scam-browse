// background.js - Ultimate Protection Version

const API_URL = "http://127.0.0.1:5000/scan";

// High-Authority Domains that should NEVER be blocked
const SYSTEM_WHITELIST = [
    "google.com", "facebook.com", "youtube.com", "instagram.com", 
    "twitter.com", "linkedin.com", "github.com", "wikipedia.org", 
    "microsoft.com", "apple.com", "amazon.com", "netflix.com",
    "bing.com", "yahoo.com", "reddit.com", "twitch.tv", "fb.com", "googlevideo.com"
];

const sessionWhitelist = new Set();
const resultCache = new Map();
const redirectTracker = new Map();

chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.local.set({ isEnabled: true });
});

function isSafeUrl(url) {
    if (!url) return true;
    try {
        const urlObj = new URL(url);
        const hostname = urlObj.hostname.toLowerCase();
        
        // Comprehensive check for system whitelist (including subdomains)
        if (SYSTEM_WHITELIST.some(domain => hostname === domain || hostname.endsWith("." + domain))) {
            return true;
        }
        
        const safeProtocols = ["chrome:", "edge:", "about:", "moz-extension:", "chrome-extension:"];
        if (safeProtocols.includes(urlObj.protocol)) return true;
        
        if (hostname === "localhost" || hostname === "127.0.0.1") return true;
    } catch(e) {
        return true; 
    }
    return false;
}

// Redirect Monitoring
chrome.webRequest.onBeforeRedirect.addListener((details) => {
    if (details.tabId === -1 || details.frameId !== 0) return;
    let count = redirectTracker.get(details.tabId) || 0;
    count++;
    redirectTracker.set(details.tabId, count);
}, { urls: ["<all_urls>"], types: ["main_frame"] });

// Navigation Commit
chrome.webNavigation.onCommitted.addListener((details) => {
    if (details.frameId === 0) {
        let count = redirectTracker.get(details.tabId) || 0;
        redirectTracker.set(details.tabId, 0); 
        scanUrl(details.url, details.tabId, count);
    }
});

async function scanUrl(url, tabId, redirectCount = 0) {
    try {
        const { isEnabled } = await chrome.storage.local.get("isEnabled");
        if (isEnabled === false) return;

        // Skip scanning for white-listed sites entirely
        if (isSafeUrl(url)) {
            handleResult({ classification: "LEGITIMATE", risk_level: "LOW", confidence: 1.0, url: url }, url, tabId);
            return;
        }

        if (sessionWhitelist.has(url)) {
            handleResult({ classification: "LEGITIMATE", risk_level: "LOW", confidence: 1.0, url: url }, url, tabId);
            return;
        }

        if (redirectCount > 3) {
            handleResult({
                url: url, classification: "SUSPICIOUS", risk_level: "HIGH",
                confidence: 0.9, reason: "Excessive Redirects"
            }, url, tabId);
            return;
        }

        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) return;
        const data = await response.json();
        handleResult(data, url, tabId);

    } catch (error) {
        console.error("Scan Error:", error);
    }
}

function handleResult(data, url, tabId) {
    if (!tabId || tabId === -1) return;
    updateIcon(data.classification, tabId);
    chrome.storage.local.set({ [tabId]: data });
    chrome.runtime.sendMessage({ action: "updateUI", tabId: tabId, data: data }).catch(() => {});

    if (data.classification === "PHISHING" || (data.classification === "SUSPICIOUS" && data.risk_level === "HIGH")) {
        const blockedUrl = chrome.runtime.getURL("blocked.html") + 
                           `?url=${encodeURIComponent(url)}&risk=${data.risk_level}&conf=${data.confidence}`;
        chrome.tabs.update(tabId, { url: blockedUrl });
    }
}

function updateIcon(status, tabId) {
    let text = "";
    let color = "";
    switch (status) {
        case "PHISHING": text = "BLK"; color = "#D32F2F"; break;
        case "SUSPICIOUS": text = "BLK"; color = "#F57C00"; break;
        case "LEGITIMATE": text = "OK"; color = "#388E3C"; break;
        default: text = ""; color = "#CCCCCC";
    }
    chrome.action.setBadgeText({ text: text, tabId: tabId });
    chrome.action.setBadgeBackgroundColor({ color: color, tabId: tabId });
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "whitelist" && message.url) {
        sessionWhitelist.add(message.url);
        sendResponse({ success: true });
    } else if (message.action === "goBack") {
        if (sender.tab && sender.tab.id) {
            chrome.tabs.update(sender.tab.id, { url: "https://www.google.com" });
        }
        sendResponse({ success: true });
    }
    return true;
});
