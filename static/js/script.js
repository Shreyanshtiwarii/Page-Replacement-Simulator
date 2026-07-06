// ================================
// Page Replacement Simulator - Frontend Logic
// ================================

// --- Element References ---
const framesInput = document.getElementById("frames");
const referenceInput = document.getElementById("referenceString");
const algorithmSelect = document.getElementById("algorithm");
const algoDescription = document.getElementById("algoDescription");

const startBtn = document.getElementById("startBtn");
const sampleBtn = document.getElementById("sampleBtn");
const resetBtn = document.getElementById("resetBtn");

const errorMessage = document.getElementById("errorMessage");
const loadingSpinner = document.getElementById("loadingSpinner");
const resultsCard = document.getElementById("resultsCard");

const totalFaultsEl = document.getElementById("totalFaults");
const totalHitsEl = document.getElementById("totalHits");
const hitRatioEl = document.getElementById("hitRatio");
const faultRatioEl = document.getElementById("faultRatio");
const execTimeEl = document.getElementById("execTime");

const tableHeaderRow = document.getElementById("tableHeaderRow");
const tableBody = document.getElementById("tableBody");

// --- Algorithm Descriptions ---
const ALGO_DESCRIPTIONS = {
  fifo: "FIFO replaces the page that has been in memory the longest, regardless of how recently it was used.",
  lru: "LRU replaces the page that has not been used for the longest period of time.",
  optimal: "Optimal replaces the page that will not be used for the longest time in the future. It requires future knowledge and is mainly used as a benchmark."
};

// Show the description for the default selected algorithm on page load.
algoDescription.textContent = ALGO_DESCRIPTIONS[algorithmSelect.value];

// Update the description whenever the algorithm dropdown changes.
algorithmSelect.addEventListener("change", () => {
  algoDescription.textContent = ALGO_DESCRIPTIONS[algorithmSelect.value];
});

// --- Sample Input Button ---
sampleBtn.addEventListener("click", () => {
  framesInput.value = 3;
  referenceInput.value = "7 0 1 2 0 3 0 4 2 3 0 3 2";
  errorMessage.textContent = "";
});

// --- Reset Button ---
resetBtn.addEventListener("click", () => {
  framesInput.value = "";
  referenceInput.value = "";
  algorithmSelect.value = "fifo";
  algoDescription.textContent = ALGO_DESCRIPTIONS.fifo;
  errorMessage.textContent = "";
  resultsCard.classList.add("hidden");
  loadingSpinner.classList.add("hidden");
  tableBody.innerHTML = "";
  tableHeaderRow.innerHTML = "";
});

// --- Client-side Validation ---
function validateInputs(framesValue, referenceValue) {
  if (framesValue === "" || framesValue === null) {
    return "Please enter the number of frames.";
  }

  const framesNum = Number(framesValue);
  if (!Number.isInteger(framesNum) || framesNum <= 0) {
    return "Number of frames must be a positive whole number.";
  }

  if (!referenceValue || referenceValue.trim() === "") {
    return "Reference string cannot be empty.";
  }

  const tokens = referenceValue.trim().split(/\s+/);
  for (const token of tokens) {
    if (!/^-?\d+$/.test(token)) {
      return `Invalid character '${token}' found. Only whole numbers separated by spaces are allowed.`;
    }
  }

  return null; // No errors
}

// --- Start Simulation Button ---
startBtn.addEventListener("click", async () => {
  errorMessage.textContent = "";
  resultsCard.classList.add("hidden");

  const framesValue = framesInput.value;
  const referenceValue = referenceInput.value;
  const algorithm = algorithmSelect.value;

  const validationError = validateInputs(framesValue, referenceValue);
  if (validationError) {
    errorMessage.textContent = validationError;
    return;
  }

  loadingSpinner.classList.remove("hidden");

  try {
    const response = await fetch("/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        frames: Number(framesValue),
        reference_string: referenceValue.trim(),
        algorithm: algorithm
      })
    });

    const data = await response.json();

    loadingSpinner.classList.add("hidden");

    if (!response.ok) {
      errorMessage.textContent = data.error || "Something went wrong. Please try again.";
      return;
    }

    renderResults(data);
  } catch (err) {
    loadingSpinner.classList.add("hidden");
    errorMessage.textContent = "Could not reach the server. Please check your connection and try again.";
  }
});

// --- Render Results on the Page ---
function renderResults(data) {
  const numFrames = data.frames;

  // --- Update stat boxes ---
  totalFaultsEl.textContent = data.faults;
  totalHitsEl.textContent = data.hits;
  hitRatioEl.textContent = (data.hit_ratio * 100).toFixed(1) + "%";
  faultRatioEl.textContent = (data.fault_ratio * 100).toFixed(1) + "%";
  execTimeEl.textContent = data.execution_time_ms + " ms";

  // --- Build table header dynamically based on number of frames ---
  tableHeaderRow.innerHTML = "";
  const headers = ["Step", "Page"];
  for (let i = 1; i <= numFrames; i++) {
    headers.push(`Frame ${i}`);
  }
  headers.push("Status");

  headers.forEach((headerText) => {
    const th = document.createElement("th");
    th.textContent = headerText;
    tableHeaderRow.appendChild(th);
  });

  // --- Build table body rows dynamically ---
  tableBody.innerHTML = "";

  data.steps.forEach((step, index) => {
    const row = document.createElement("tr");
    row.style.animationDelay = `${index * 0.04}s`;

    // Step number cell
    const stepCell = document.createElement("td");
    stepCell.textContent = index + 1;
    row.appendChild(stepCell);

    // Page cell
    const pageCell = document.createElement("td");
    pageCell.textContent = step.page;
    row.appendChild(pageCell);

    // Frame cells
    step.frames.forEach((frameValue) => {
      const frameCell = document.createElement("td");
      frameCell.textContent = frameValue;
      if (frameValue !== "-") {
        frameCell.classList.add("frame-filled");
      }
      row.appendChild(frameCell);
    });

    // Status cell with colored badge
    const statusCell = document.createElement("td");
    const badge = document.createElement("span");
    badge.textContent = step.status;
    badge.classList.add("status-badge", step.status === "Hit" ? "hit" : "fault");
    statusCell.appendChild(badge);
    row.appendChild(statusCell);

    tableBody.appendChild(row);
  });

  resultsCard.classList.remove("hidden");
}
