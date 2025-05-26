// Scripts for activity_detail.html

let isSubmitting = false;

function validateForm() {
    const nameInput = document.getElementById('name');
    const textInput = document.getElementById('text');
    let isValid = true;
    removeErrorLabel('name');
    removeErrorLabel('text');

    // Validate name (required, max 80 chars, min 3 chars)
    if (!nameInput.value || nameInput.value.length > 80 || nameInput.value.length < 3) {
        addErrorLabel('name', 'Nombre inválido. Máximo 80 caracteres y mínimo 3 caracteres.');
        isValid = false;
    }

    // Validate comment text (required, min 5 chars)
    if (!textInput.value || textInput.value.length < 5) {
        addErrorLabel('text', 'Comentario inválido. Mínimo 5 caracteres.');
        isValid = false;
    }

    return isValid;
}

function setSubmitting(submitting) {
    isSubmitting = submitting;
    const submitBtn = document.getElementById('submit-btn');
    
    submitBtn.disabled = submitting;
    
    if (submitting) {
        submitBtn.textContent = 'Enviando...';
    } else {
        submitBtn.textContent = 'Subir comentario';
    }
}

async function submitForm() {
    if (isSubmitting) {
        return;
    }

    isSubmitting = true;
    const form = document.getElementById('comment-form');
    const formData = new FormData(form);

    try {
        const response = await fetch(window.location.href, {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();
        
        if (result.success) {
            // Refresh page to show new comment
            window.location.href = window.location.href;
            return;
        } else {
            showToast('Por favor corrija los errores indicados', 'error');
            // Show specific error messages by category
            if (result) {
                // Clear previous error states
                document.querySelectorAll('.error').forEach(el => 
                    el.classList.contains('toast') ? {} : el.classList.remove('error')
                );
                document.querySelectorAll('.error-label').forEach(el => el.remove());

                // Handle each category of errors
                for (const category in result) {
                    for (const error_type in result[category]) {
                        addErrorLabel(result[category][error_type].id, 
                                    result[category][error_type].msg);
                    }
                }
            }
        }
    } catch (error) {
        showToast('Error al enviar el comentario', 'error');
        console.error('Error:', error);
    } finally {
        setSubmitting(false);
    }
}

function loadForm() {
    // Prevent default form submission
    document.getElementById('comment-form').addEventListener('submit', (e) => {
        e.preventDefault();
        return false;
    });

    // Link new submit function
    document.getElementById('submit-btn').addEventListener('click', async () => {
        if (!isSubmitting && validateForm()) {
            await submitForm();
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    loadForm();
});