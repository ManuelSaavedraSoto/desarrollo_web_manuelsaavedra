// UI/Window Management Functions
function toggleWindow(windowId) {
    const window = document.getElementById(`window-${windowId}`);
    const overlay = document.getElementById('overlay');
    if (window.style.display === 'none' || window.style.display === '') {
        window.style.display = 'block';
        overlay.style.display = 'block';
    } else {
        window.style.display = 'none';
        overlay.style.display = 'none';
    }
}

function showImage(src) {
    const imageWindow = document.getElementById('image-window');
    const overlay = document.getElementById('overlay');
    const enlargedImage = document.getElementById('enlarged-image');
    enlargedImage.src = src;
    imageWindow.style.display = 'block';
    overlay.style.display = 'block';
}

function closeImage() {
    const imageWindow = document.getElementById('image-window');
    const overlay = document.getElementById('overlay');
    imageWindow.style.display = 'none';
    overlay.style.display = 'none';
}

function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    const toast = document.createElement('div');
    const id = `toast-${Date.now()}`;
    
    toast.className = `toast ${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');
    toast.setAttribute('aria-atomic', 'true');
    toast.id = id;
    toast.textContent = message;
    
    // Add close button for keyboard accessibility
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '×';
    closeBtn.setAttribute('aria-label', 'Close notification');
    closeBtn.style.marginLeft = '10px';
    closeBtn.style.background = 'none';
    closeBtn.style.border = 'none';
    closeBtn.style.color = 'white';
    closeBtn.style.fontSize = '20px';
    closeBtn.style.cursor = 'pointer';
    closeBtn.onclick = () => toast.remove();
    
    toast.appendChild(closeBtn);
    toastContainer.appendChild(toast);
    
    // Focus management
    closeBtn.focus();
    
    // Remove the toast after animation ends
    setTimeout(() => {
        if (document.getElementById(id)) {
            toast.remove();
        }
    }, 3000);
}
