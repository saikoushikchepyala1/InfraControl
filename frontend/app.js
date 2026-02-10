const scanButton = document.getElementById("scanButton");
const summarySection = document.getElementById("summary");
const regionsSection = document.getElementById("regions");
const issuesSection = document.getElementById("issues");
const inventorySection = document.getElementById("inventory");

scanButton.addEventListener("click", scanAccount);

async function scanAccount() {
    scanButton.disabled = true;
    scanButton.textContent = "Scanning...";

    let data;

    try {
        const response = await fetch("/scan/account");

        if (!response.ok) {
            throw new Error("Server returned " + response.status);
        }

        data = await response.json();

    } catch (err) {
        console.error("Scan failed:", err);

        summarySection.classList.remove("hidden");
        summarySection.innerHTML = `
            <div class="section-title">Error</div>
            <div>Scan failed. Backend not reachable or timeout.</div>
        `;

        scanButton.disabled = false;
        scanButton.textContent = "Scan AWS Account";
        return;
    }

    renderSummary(data);
    renderRegions(data);
    renderIssues(data);
    renderInventory(data);

    scanButton.disabled = false;
    scanButton.textContent = "Scan AWS Account";
}

function renderSummary(data) {
    summarySection.classList.remove("hidden");

    summarySection.innerHTML = `
        <div class="section-title">Summary</div>
        <div class="grid">
            <div class="box">Regions Scanned: ${data.regions_scanned.length}</div>
            <div class="box">Total Issues: ${data.summary.total_issues}</div>
        </div>
    `;
}

function renderRegions(data) {
    regionsSection.classList.remove("hidden");

    const regions = Object.keys(data.inventory || {});

    if (regions.length === 0) {
        regionsSection.innerHTML = `
            <div class="section-title">Regions Detected</div>
            <div>No active regions detected</div>
        `;
        return;
    }

    const regionBoxes = regions
        .map(region => `<div class="box">${region}</div>`)
        .join("");

    regionsSection.innerHTML = `
        <div class="section-title">Regions Detected</div>
        <div class="grid">${regionBoxes}</div>
    `;
}

function renderIssues(data) {
    issuesSection.classList.remove("hidden");

    if (data.issues.length === 0) {
        issuesSection.innerHTML = `
            <div class="section-title">Issues</div>
            <div>No issues detected</div>
        `;
        return;
    }

    const issueCards = data.issues.map(issue => {
        const severity = issue.severity.toLowerCase();
        return `
            <div class="issue ${severity}">
                <div class="issue-title">${issue.service} – ${issue.issue}</div>
                <div class="issue-meta">
                    Resource: ${issue.resource} |
                    Region: ${issue.region || "global"} |
                    Severity: ${issue.severity}
                </div>
                <div class="issue-meta">${issue.why}</div>
                <div class="issue-meta">Fix: ${issue.suggested_fix}</div>
            </div>
        `;
    }).join("");

    issuesSection.innerHTML = `
        <div class="section-title">Issues</div>
        ${issueCards}
    `;
}

function renderInventory(data) {
    inventorySection.classList.remove("hidden");

    const inventory = data.inventory || {};
    const regions = Object.keys(inventory);

    if (regions.length === 0) {
        inventorySection.innerHTML = `
            <div class="section-title">Inventory</div>
            <div>No resources found</div>
        `;
        return;
    }

    const regionBlocks = regions.map(region => {
        const services = inventory[region];

        const serviceRows = Object.entries(services)
            .map(([service, count]) => {
                return `<div class="box">${service}: ${count}</div>`;
            })
            .join("");

        return `
            <div style="margin-bottom: 16px;">
                <strong>${region}</strong>
                <div class="grid" style="margin-top: 8px;">
                    ${serviceRows}
                </div>
            </div>
        `;
    }).join("");

    inventorySection.innerHTML = `
        <div class="section-title">Inventory</div>
        ${regionBlocks}
    `;
}