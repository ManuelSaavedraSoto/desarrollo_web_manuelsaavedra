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

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    fetchActivities(1);
});
