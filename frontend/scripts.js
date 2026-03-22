/* ============================================================
   AI RESUME ANALYZER — scripts.js
   ============================================================ */

const API_URL = "http://127.0.0.1:8000/analyze-pdf";

// ── DOM refs ──────────────────────────────────────────────
const form        = document.getElementById("uploadForm");
const fileInput   = document.getElementById("resumeFile");
const dropZone    = document.getElementById("dropZone");
const dropContent = document.getElementById("dropContent");
const fileSelected = document.getElementById("fileSelected");
const fileNameEl  = document.getElementById("fileName");
const fileRemove  = document.getElementById("fileRemove");
const analyzeBtn  = document.getElementById("analyzeBtn");
const btnText     = analyzeBtn.querySelector(".btn-text");
const btnIcon     = analyzeBtn.querySelector(".btn-icon");
const btnLoader   = document.getElementById("btnLoader");
const resultsSection = document.getElementById("resultsSection");
const scoreValue  = document.getElementById("scoreValue");
const scoreGrade  = document.getElementById("scoreGrade");
const ringProgress = document.getElementById("ringProgress");
const skillsFound  = document.getElementById("skillsFound");
const skillsMissing = document.getElementById("skillsMissing");
const foundCount  = document.getElementById("foundCount");
const missingCount = document.getElementById("missingCount");
const recoText    = document.getElementById("recoText");
const errorBar    = document.getElementById("errorBar");
const errorMsg    = document.getElementById("errorMsg");
const errorClose  = document.getElementById("errorClose");

// ── Drag & Drop ───────────────────────────────────────────

["dragenter", "dragover"].forEach(ev =>
    dropZone.addEventListener(ev, e => {
        e.preventDefault();
        dropZone.classList.add("drag-over");
    })
);

["dragleave", "drop"].forEach(ev =>
    dropZone.addEventListener(ev, e => {
        e.preventDefault();
        dropZone.classList.remove("drag-over");
    })
);

dropZone.addEventListener("drop", e => {
    const file = e.dataTransfer.files[0];
    if (file && file.type === "application/pdf") {
        setFile(file);
    } else {
        showError("Please drop a PDF file.");
    }
});

fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) setFile(fileInput.files[0]);
});

fileRemove.addEventListener("click", e => {
    e.stopPropagation();
    clearFile();
});

function setFile(file) {
    fileNameEl.textContent = file.name;
    dropContent.style.display = "none";
    fileSelected.style.display = "flex";
    // Sync DataTransfer so FormData picks up drag-dropped file
    if (!fileInput.files[0] || fileInput.files[0] !== file) {
        const dt = new DataTransfer();
        dt.items.add(file);
        fileInput.files = dt.files;
    }
}

function clearFile() {
    fileInput.value = "";
    fileNameEl.textContent = "";
    fileSelected.style.display = "none";
    dropContent.style.display = "";
}

// ── Error bar ─────────────────────────────────────────────

errorClose.addEventListener("click", () => {
    errorBar.style.display = "none";
});

function showError(msg) {
    errorMsg.textContent = msg;
    errorBar.style.display = "flex";
    resultsSection.style.display = "none";
}

function hideError() {
    errorBar.style.display = "none";
}

// ── Loading state ─────────────────────────────────────────

function setLoading(on) {
    analyzeBtn.disabled = on;
    btnText.style.display = on ? "none" : "";
    btnIcon.style.display = on ? "none" : "";
    btnLoader.style.display = on ? "flex" : "none";
}

// ── Score ring animation ──────────────────────────────────

const CIRCUMFERENCE = 2 * Math.PI * 50; // r=50 → 314.16

function animateScore(score) {
    // Clamp 0–100
    const pct = Math.min(100, Math.max(0, score));
    const offset = CIRCUMFERENCE * (1 - pct / 100);

    // Color the ring based on score
    if (pct >= 75)      ringProgress.style.stroke = "var(--green)";
    else if (pct >= 50) ringProgress.style.stroke = "var(--gold)";
    else if (pct >= 30) ringProgress.style.stroke = "#e8a04b";
    else                ringProgress.style.stroke = "var(--red)";

    ringProgress.style.strokeDashoffset = offset;

    // Count-up animation
    let current = 0;
    const duration = 1200;
    const start = performance.now();
    function tick(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
        current = pct * eased;
        scoreValue.textContent = current.toFixed(1) + "%";
        if (progress < 1) requestAnimationFrame(tick);
        else scoreValue.textContent = pct.toFixed(2) + "%";
    }
    requestAnimationFrame(tick);

    // Grade label
    scoreGrade.className = "score-grade";
    if (pct >= 75) {
        scoreGrade.textContent = "Excellent Match";
        scoreGrade.classList.add("excellent");
    } else if (pct >= 50) {
        scoreGrade.textContent = "Good Match";
        scoreGrade.classList.add("good");
    } else if (pct >= 30) {
        scoreGrade.textContent = "Fair Match";
        scoreGrade.classList.add("fair");
    } else {
        scoreGrade.textContent = "Needs Work";
        scoreGrade.classList.add("poor");
    }
}

// ── Render results ────────────────────────────────────────

function renderResults(data) {
    // Score
    animateScore(data.score);

    // Skills found
    skillsFound.innerHTML = "";
    (data.skills || []).forEach((skill, i) => {
        const tag = document.createElement("span");
        tag.className = "skill-tag found";
        tag.textContent = skill;
        tag.style.animationDelay = `${i * 0.05}s`;
        skillsFound.appendChild(tag);
    });
    foundCount.textContent = (data.skills || []).length;

    // Missing skills
    skillsMissing.innerHTML = "";
    (data.missing || []).forEach((skill, i) => {
        const tag = document.createElement("span");
        tag.className = "skill-tag missing";
        tag.textContent = skill;
        tag.style.animationDelay = `${i * 0.05}s`;
        skillsMissing.appendChild(tag);
    });
    missingCount.textContent = (data.missing || []).length;

    // Recommendation
    recoText.textContent = data.recommendation || "No recommendation available.";

    // Show section
    resultsSection.style.display = "";
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

// ── Form submit ───────────────────────────────────────────

form.addEventListener("submit", async function (e) {
    e.preventDefault();
    hideError();

    if (!fileInput.files[0]) {
        showError("Please select a PDF resume before analyzing.");
        return;
    }

    const jobRole = document.getElementById("jobRole").value;

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("job_role", jobRole);

    setLoading(true);
    resultsSection.style.display = "none";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.error || `Server error: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        renderResults(data);

    } catch (err) {
        console.error(err);
        showError(err.message || "Error connecting to API. Make sure your server is running on port 8000.");
    } finally {
        setLoading(false);
    }
});
