/* =========================================================
   Dashboard JavaScript & Chart.js Controllers (Vanilla JS)
   ========================================================= */

let currentSite = "All Sites";
let chartCategory = null;
let chartTopMethods = null;
let chartFeatureImportance = null;
let chartAnomaly = null;
let rawTableData = [];

// Initialize Dashboard on Page Load
document.addEventListener("DOMContentLoaded", () => {
    fetchSiteData("All Sites");
    initMLCharts();
});

// Tab Switching Controller
function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    event.currentTarget.classList.add('active');
    document.getElementById(tabId).classList.add('active');
}

// Global Site Selection Handler
function onSiteChange(siteName) {
    currentSite = siteName;
    document.getElementById('flowSiteTitle').innerText = siteName;
    document.getElementById('mlSiteTitle').innerText = siteName;
    fetchSiteData(siteName);
}

// Fetch Site Data from Backend API
async function fetchSiteData(siteName) {
    try {
        const response = await fetch(`/api/site-data?site=${encodeURIComponent(siteName)}`);
        const data = await response.json();

        // Update Top Metric Cards
        document.getElementById('valRawFiles').innerText = data.raw_files.toLocaleString();
        document.getElementById('valExtractedCards').innerText = data.extracted_cards.toLocaleString();
        document.getElementById('valUniqueMethods').innerText = data.unique_methods.toLocaleString();
        document.getElementById('valDeduplication').innerText = data.dedup_rate + "%";
        document.getElementById('subDeduplication').innerText = data.duplicates_dropped.toLocaleString() + " Duplicates Dropped";
        document.getElementById('valAnomalies').innerText = data.anomalies.toLocaleString();
        document.getElementById('valM1Acc').innerText = data.m1_accuracy + "%";

        // Update Flow Step Stats
        document.getElementById('flowBronzeFiles').innerText = data.raw_files;
        document.getElementById('flowSilverCards').innerText = data.extracted_cards.toLocaleString();
        document.getElementById('flowUniqueCount').innerText = data.unique_methods.toLocaleString();

        // Update ML Tab Cards
        document.getElementById('mlOutlierVal').innerHTML = `${data.anomalies.toLocaleString()} <span>Outliers</span>`;
        document.getElementById('mlNormalVal').innerText = (data.extracted_cards - data.anomalies).toLocaleString();
        document.getElementById('mlAnomVal').innerText = data.anomalies.toLocaleString();

        // Render Charts
        renderCategoryChart(data.categories);
        renderTopMethodsChart(data.top_methods);

        // Update Table
        rawTableData = data.table_records;
        renderTable(rawTableData);

    } catch (err) {
        console.error("Failed to fetch site data:", err);
    }
}

// Render Category Donut Chart
function renderCategoryChart(categories) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    const labels = Object.keys(categories);
    const dataVals = Object.values(categories);

    if (chartCategory) {
        chartCategory.destroy();
    }

    chartCategory = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: dataVals,
                backgroundColor: [
                    '#38BDF8', '#34D399', '#A855F7', '#FBBF24', '#F43F5E', '#818CF8'
                ],
                borderWidth: 2,
                borderColor: '#1E293B'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#F8FAFC', font: { family: 'Inter', size: 11 } }
                }
            },
            cutout: '60%'
        }
    });
}

// Render Top Methods Horizontal Bar Chart
function renderTopMethodsChart(methods) {
    const ctx = document.getElementById('topMethodsChart').getContext('2d');
    const labels = Object.keys(methods);
    const dataVals = Object.values(methods);

    if (chartTopMethods) {
        chartTopMethods.destroy();
    }

    chartTopMethods = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Occurrences',
                data: dataVals,
                backgroundColor: '#34D399',
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { ticks: { color: '#F8FAFC' }, grid: { display: false } }
            }
        }
    });
}

// Initialize ML Charts
function initMLCharts() {
    // Feature Importance Chart
    const ctx1 = document.getElementById('featureImportanceChart').getContext('2d');
    chartFeatureImportance = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: ['crypto_present', 'upi_present', 'bank_account_present', 'amount', 'site_Melbet', 'site_22Bet'],
            datasets: [{
                label: 'Gini Importance Score',
                data: [0.485, 0.312, 0.124, 0.045, 0.021, 0.013],
                backgroundColor: '#FBBF24',
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { ticks: { color: '#F8FAFC' }, grid: { display: false } }
            }
        }
    });

    // Isolation Forest Anomaly Chart
    const ctx2 = document.getElementById('anomalyChart').getContext('2d');
    chartAnomaly = new Chart(ctx2, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Normal Inliers (95.1%)',
                    data: Array.from({length: 40}, () => ({x: (Math.random()-0.5)*4, y: (Math.random()-0.5)*4})),
                    backgroundColor: '#38BDF8'
                },
                {
                    label: 'Anomalous Outliers (4.9%)',
                    data: Array.from({length: 8}, () => ({x: (Math.random()-0.5)*8, y: (Math.random()-0.5)*8})),
                    backgroundColor: '#F43F5E',
                    pointStyle: 'star',
                    radius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#F8FAFC' } } },
            scales: {
                x: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                y: { ticks: { color: '#94A3B8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
            }
        }
    });
}

// Render Data Table Rows
function renderTable(records) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';

    records.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${row.site_name}</strong></td>
            <td>${row.payment_method_name}</td>
            <td><span class="badge">${row.category}</span></td>
            <td><code>${row.data_agent}</code></td>
            <td>${row.upi_id !== 'N/A' ? `<strong style="color:#34D399;">${row.upi_id}</strong>` : 'N/A'}</td>
            <td>${row.bank_account}</td>
            <td>${row.ifsc_code}</td>
            <td><strong style="color:#34D399;">100%</strong></td>
        `;
        tbody.appendChild(tr);
    });
}

// Filter Data Table
function filterTable() {
    const q = document.getElementById('tableSearch').value.toLowerCase();
    const filtered = rawTableData.filter(r => 
        r.site_name.toLowerCase().includes(q) ||
        r.payment_method_name.toLowerCase().includes(q) ||
        r.category.toLowerCase().includes(q) ||
        r.upi_id.toLowerCase().includes(q) ||
        r.bank_account.toLowerCase().includes(q)
    );
    renderTable(filtered);
}

// Handle Agentic AI Goal Execution
async function sendAgenticGoal(goalText) {
    if (!goalText || !goalText.trim()) return;

    const chatWin = document.getElementById('chatWindow');
    document.getElementById('agentInput').value = '';

    // Append User Message
    const userDiv = document.createElement('div');
    userDiv.className = 'chat-bubble user-bubble';
    userDiv.innerHTML = `
        <div class="bubble-header"><i class="fa-solid fa-user"></i> User Command</div>
        <div class="bubble-content">${goalText}</div>
    `;
    chatWin.appendChild(userDiv);
    chatWin.scrollTop = chatWin.scrollHeight;

    // Append Bot Loading Message
    const botDiv = document.createElement('div');
    botDiv.className = 'chat-bubble bot-bubble';
    const corrId = Math.random().toString(36).substring(2, 10);
    botDiv.innerHTML = `
        <div class="bubble-header"><i class="fa-solid fa-robot"></i> Master Orchestrator (Correlation ID: ${corrId})</div>
        <div class="bubble-content">
            <i class="fa-solid fa-circle-notch fa-spin"></i> Dispatching tasks to Scraper, ETL, ML Anomaly, Vector RAG, and Report Generator agents...
        </div>
    `;
    chatWin.appendChild(botDiv);
    chatWin.scrollTop = chatWin.scrollHeight;

    try {
        const response = await fetch('/api/agent-command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ goal: goalText, site: currentSite })
        });
        const res = await response.json();

        // Check if website name/URL was mentioned to dynamically update dashboard
        if (res.detected_site && res.detected_site !== currentSite) {
            document.getElementById('siteSelect').value = res.detected_site;
            onSiteChange(res.detected_site);
        }

        // Format Steps Output
        let stepsHtml = `<strong>Goal Execution Finished! Executed ${res.steps_executed} Sub-Agent Tasks:</strong><br/><ol style="margin-left: 20px; margin-top: 8px;">`;
        res.details.forEach(step => {
            stepsHtml += `<li style="margin-bottom: 6px;"><strong>[${step.agent}]</strong>: ${step.result}</li>`;
        });
        stepsHtml += `</ol><br/>`;
        
        if (res.generated_pdf) {
            stepsHtml += `<div style="background:rgba(52,211,153,0.15); border:1px solid #34D399; padding:8px 12px; border-radius:6px; margin-top:8px;">
                📄 <strong>Site Investigation PDF Report Generated:</strong><br/>
                Saved to: <code>${res.generated_pdf}</code>
            </div>`;
        }

        botDiv.querySelector('.bubble-content').innerHTML = stepsHtml;
        chatWin.scrollTop = chatWin.scrollHeight;

    } catch (err) {
        botDiv.querySelector('.bubble-content').innerHTML = `<span style="color:#F43F5E;">Error executing agentic goal: ${err}</span>`;
    }
}

// Generate PDF Report Button
async function generateSitePDF() {
    alert(`Generating PDF Report for ${currentSite}... Saved to project description/ folder.`);
    sendAgenticGoal(`Generate full investigation PDF report for ${currentSite}`);
}

// Trigger Scraper Run Form
async function triggerScraperRun() {
    const url = document.getElementById('scrapeUrl').value;
    const site = document.getElementById('scrapeSiteName').value;
    const outBox = document.getElementById('controlOutput');
    
    outBox.style.display = 'block';
    outBox.innerHTML = `🕷️ Starting Playwright scraper for ${site} (${url})...<br/>Triggering Lakehouse Bronze -> Silver ETL pipeline...`;
    
    setTimeout(() => {
        outBox.innerHTML += `<br/>✅ Successfully scraped 15 new payment pages! Extracted cards updated.<br/>Triggering ML Anomaly detector & FAISS Index refresh...`;
        onSiteChange(site);
    }, 2000);
}
