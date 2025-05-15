// Activity List Management
let currentPage = 1;
let totalPages = 1;

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('es-CL', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function createTableRow(activity) {
    return `
        <tr onclick="window.location.href='/actividades/${activity.id}'" class="btn-row">
            <td>${formatDate(activity.inicio)}</td>
            <td>${activity.termino || 'No especificado'}</td>
            <td>${activity.comuna}</td>
            <td>${activity.sector || 'No especificado'}</td>
            <td>${activity.temas.join(', ')}</td>
            <td>${activity.nombre}</td>
            <td>${activity.num_fotos || 0}</td>
        </tr>
    `;
}

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
    try {
        const response = await fetch(`/api/actividades?page=${page}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        
        // Update table body
        const tableBody = document.getElementById('activities-table-body');
        tableBody.innerHTML = data.activities.map(activity => createTableRow(activity)).join('');
        
        // Update pagination state
        currentPage = data.current_page;
        totalPages = data.total_pages;
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
