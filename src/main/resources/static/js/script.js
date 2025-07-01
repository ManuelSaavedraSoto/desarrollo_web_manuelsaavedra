// Activity List Management
let currentPage = 1;
let totalPages = 1;

function updatePagination() {
    const paginationDiv = document.getElementById('pagination');
    let paginationHtml = '';

    if (totalPages > 1) {
        // Previous button
        if (currentPage > 1) {
            paginationHtml += `
                <button onclick="changePage(${currentPage - 1})">
                    &laquo; Anterior
                </button>
            `;
        }

        // Page numbers
        for (let i = 1; i <= totalPages; i++) {
            paginationHtml += `
                <button onclick="changePage(${i})" 
                        class="${i === currentPage ? 'active' : ''}">
                    ${i}
                </button>
            `;
        }

        // Next button
        if (currentPage < totalPages) {
            paginationHtml += `
                <button onclick="changePage(${currentPage + 1})">
                    Siguiente &raquo;
                </button>
            `;
        }
    }

    paginationDiv.innerHTML = paginationHtml;
}

async function fetchActivities(page) {
    let formData = new FormData();
    formData.append("page", page)
    try {
        const response = await fetch(apiURL, {
            "method": "POST",
            "body": formData,
        });
        const data = await response.json();

        totalPages = data.totalPages;
        currentPage = data.currentPage;
        document.getElementById("activities-table-body").innerHTML = data.html;

        updatePagination();
                
    } catch (error) {
        console.error('Error:', error);
        showToast('Error al cargar las actividades', 'error');
    }
}

function changePage(newPage) {
    if (newPage >= 1 && newPage <= totalPages) {
        fetchActivities(newPage);
    }
}

// --- Star Rating Tooltip and Evaluation ---
let tooltip = null;
let tooltipTarget = null;

function showStarTooltip(target, activityId) {
    if (!tooltip) tooltip = document.getElementById('star-tooltip');
    tooltipTarget = target;
    tooltip.style.display = 'block';
    // Position tooltip below the button
    const rect = target.getBoundingClientRect();
    tooltip.style.left = (rect.left + window.scrollX) + 'px';
    tooltip.style.top = (rect.bottom + window.scrollY + 5) + 'px';
    tooltip.setAttribute('data-activity-id', activityId);
}

function hideStarTooltip() {
    if (tooltip) tooltip.style.display = 'none';
    tooltipTarget = null;
}

function handleStarHover(e) {
    if (!e.target.classList.contains('star')) return;
    const val = parseInt(e.target.getAttribute('data-value'));
    Array.from(tooltip.querySelectorAll('.star')).forEach((star, idx) => {
        star.style.color = idx < val ? '#FFD700' : '#ccc';
    });
}

function handleStarOut() {
    Array.from(tooltip.querySelectorAll('.star')).forEach(star => {
        star.style.color = '#ccc';
    });
}

function handleStarClick(e) {
    if (!e.target.classList.contains('star')) return;
    const val = parseInt(e.target.getAttribute('data-value'));
    const activityId = tooltip.getAttribute('data-activity-id');
    evaluateActivity(activityId, val);
    hideStarTooltip();
}

function showTooltipError(msg) {
    let tooltip = document.getElementById('star-tooltip');
    if (tooltip) {
        tooltip.innerHTML = `<span style='color:red;'>${msg}</span>`;
        tooltip.style.display = 'block';
        setTimeout(() => {
            tooltip.style.display = 'none';
            tooltip.innerHTML = `<span class="star" data-value="1">&#9733;</span>
<span class="star" data-value="2">&#9733;</span>
<span class="star" data-value="3">&#9733;</span>
<span class="star" data-value="4">&#9733;</span>
<span class="star" data-value="5">&#9733;</span>
<span class="star" data-value="6">&#9733;</span>
<span class="star" data-value="7">&#9733;</span>`;
        }, 2000);
    }
}

function isValidScore(val) {
    return Number.isInteger(val) && val >= 1 && val <= 7;
}

async function evaluateActivity(activityId, score) {
    score = parseInt(score);
    if (!isValidScore(score)) {
        showTooltipError('El puntaje debe ser un entero entre 1 y 7');
        return;
    }
    let formData = new FormData();
    formData.append('id', activityId);
    formData.append('score', score);
    try {
        const response = await fetch(scoreURL, {
            method: 'POST',
            body: formData
        });
        if (response.ok) {
            const data = await response.json();
            // Update score in table
            const scoreCell = document.querySelector(`.activity-score[data-id='${activityId}']`);
            if (scoreCell) {
                scoreCell.textContent = data.score;
                scoreCell.classList.remove('star-added'); // Remove flag so addScoreStars can re-add
                addScoreStars(); // Add the star after updating
            }
            showToast('¡Actividad evaluada!', 'success');
        } else {
            const errMsg = await response.text();
            showTooltipError(errMsg || 'Error al evaluar');
        }
    } catch (err) {
        showTooltipError('Error al evaluar');
    }
}

// Attach event listeners after activities are loaded
function attachEvaluateListeners() {
    document.querySelectorAll('.evaluate-btn').forEach(btn => {
        btn.onclick = function(e) {
            showStarTooltip(btn, btn.getAttribute('data-id'));
        };
    });
}

// Hide tooltip on click outside
window.addEventListener('mousedown', function(e) {
    if (tooltip && tooltip.style.display === 'block' && !tooltip.contains(e.target) && (!tooltipTarget || !tooltipTarget.contains(e.target))) {
        hideStarTooltip();
    }
});

// Tooltip star events
if (!window._starTooltipSetup) {
    window._starTooltipSetup = true;
    document.addEventListener('DOMContentLoaded', () => {
        tooltip = document.getElementById('star-tooltip');
        if (tooltip) {
            tooltip.style.display = 'none'; // Hide tooltip on page load
            tooltip.addEventListener('mouseover', handleStarHover);
            tooltip.addEventListener('mouseout', handleStarOut);
            tooltip.addEventListener('click', handleStarClick);
        }
        addScoreStars();
        attachEvaluateListeners();
    });
}

// Add a star next to the score dynamically after table loads
function addScoreStars() {
    document.querySelectorAll('.activity-score').forEach(cell => {
        if (!cell.classList.contains('star-added')) {
            let score = cell.textContent.trim();
            if (score && score !== '-') {
                cell.innerHTML = score + ' <span class="star score-star">&#9733;</span>';
            }
            cell.classList.add('star-added');
        }
    });
}
// Patch fetchActivities to also add the star
const origFetchActivities2 = fetchActivities;
fetchActivities = async function(page) {
    await origFetchActivities2(page);
    attachEvaluateListeners();
    addScoreStars();
};
document.addEventListener('DOMContentLoaded', () => {
    addScoreStars();
    attachEvaluateListeners();
});

// --- Toast utility (simple) ---
function showToast(msg, type) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'toast ' + (type || '');
    toast.textContent = msg;
    container.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 2500);
}
