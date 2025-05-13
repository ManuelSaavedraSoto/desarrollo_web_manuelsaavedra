// Form Input Handling Functions
function enableComuna(event) {
    const comunaSelect = document.getElementById('comuna-select');
    const selectedRegionId = event.target.value;
    
    // Reset and enable comuna select
    comunaSelect.disabled = false;
    comunaSelect.innerHTML = '<option value="" selected disabled>Por favor elija una comuna.</option>';
    
    // Get comunas for the selected region from hidden container
    const regionContainer = document.querySelector(`.region-comunas[data-region-id="${selectedRegionId}"]`);
    if (regionContainer) {
        const comunaItems = regionContainer.querySelectorAll('.comuna-item');
        comunaItems.forEach(comuna => {
            const option = document.createElement('option');
            option.value = comuna.dataset.comunaId;
            option.textContent = comuna.dataset.comunaName;
            comunaSelect.appendChild(option);
        });
    }
}

function handleThemeSelection(checkbox) {
    const otherThemeInputDiv = document.getElementById('other-theme-input');
    const otherThemeTextInput = document.getElementById('other-theme-text-input');

    if (checkbox.checked) {
        otherThemeInputDiv.hidden = false;
        otherThemeTextInput.required = true;
    } else {
        otherThemeInputDiv.hidden = true;
        otherThemeTextInput.required = false;
        otherThemeTextInput.value = "";
    }
}

function handleContactSelection(selectedOption) {
    const selectedOptions = Array.from(document.querySelectorAll('#contact-methods input:checked'));
    const options = Array.from(document.querySelectorAll('#contact-methods input'));

    const selectedOptionDiv = document.getElementById(`contact-${selectedOption.value}`);
    const selectedOptionInput = document.getElementById(`contact-${selectedOption.value}-input`);

    selectedOptionDiv.hidden = !selectedOption.checked;
    selectedOptionInput.required = selectedOption.checked;
    if (!selectedOption.checked) selectedOptionInput.value = "";

    options.forEach(option => {
        option.disabled = false;
        if (!option.checked && selectedOptions.length == 5) {
            option.disabled = true;
        }
    });
}

function updateEndDateTimeInput(startInput) {
    if (startInput.classList.contains('error'))
        startInput.classList.remove('error');
    
    const endInput = document.getElementById('end-datetime');
    const hourInMillis = 3600 * 1000;
    let startDate = new Date(startInput.value+':00.000-04:00');
    let endDate = new Date();
    let minDate = new Date();

    endDate.setTime(startDate.getTime() + 3*hourInMillis);
    endDate.setTime(endDate.getTime() - 4 * hourInMillis); // "masking" timezone
    endInput.value = endDate.toISOString().slice(0,-8);
    
    minDate.setTime(startDate.getTime() + 60 * 1000);
    minDate.setTime(minDate.getTime() - 4 * hourInMillis); // "masking" timezone
    endInput.min = minDate.toISOString().slice(0,-8);
}

// Form Validation Functions
function validateEmail() {
    const emailInput = document.getElementById('email-input');
    let isValid = true;
    let email_pattern = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

    if (!email_pattern.test(emailInput.value)) {
        emailInput.classList.add('error');
        isValid = false;
    } else {
        emailInput.classList.remove('error');
    }

    return isValid;
}

function validateTel() {
    const telInput = document.getElementById('tel-input');
    let tel_pattern = /\+[0-9]{3}\.[0-9]{8}/;
    let isValid = true;

    if (!tel_pattern.test(telInput.value)) {
        telInput.classList.add('error');
        isValid = false;
    } else {
        telInput.classList.remove('error');
    }

    return isValid;
}

function validateFoto(input) {
    const fileId = input.id;
    const errorLabel = document.getElementById(`foto-type-error-label-${fileId.split('-')[2]}`);
    const file = input.files[0];
    
    if (file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        if (!validTypes.includes(file.type)) {
            errorLabel.hidden = false;
            input.value = '';
            return false;
        }
        errorLabel.hidden = true;
        return true;
    }
    errorLabel.hidden = true;
    return true;
}

function validatePhotos() {
    // Validate required first photo
    const firstPhoto = document.getElementById('foto-input-1');
    if (!firstPhoto.files.length) {
        document.getElementById('foto-type-error-label-1').hidden = false;
        return false;
    }
    
    // Validate all photo inputs
    for (let i = 1; i <= 5; i++) {
        const input = document.getElementById(`foto-input-${i}`);
        if (input.files.length && !validateFoto(input)) {
            return false;
        }
    }
    return true;
}

function validateThemes() {
    const themeInputs = document.querySelectorAll('#theme-inputs input[type="checkbox"]');
    const selectedThemes = Array.from(themeInputs).filter(input => input.checked);
    const otherThemeCheckbox = document.querySelector('#theme-inputs input[value="Otro"]');
    const otherThemeInput = document.getElementById('other-theme-text-input');

    if (selectedThemes.length === 0) {
        return false;
    }

    if (otherThemeCheckbox.checked && (!otherThemeInput.value || otherThemeInput.value.length < 3)) {
        otherThemeInput.classList.add('error');
        return false;
    }

    return true;
}

function validateEndDateTimeInput(endInput) {    
    const startInput = document.getElementById('init-datetime');
    const errorMsg = document.getElementById('end-datetime-error-label');    
    
    if (endInput.value == "" || endInput.value == startInput.value)
        return true;

    let endDate = new Date(endInput.value+':00.000-04:00');
    let startDate = new Date(startInput.value+':00.000-04:00');

    if (endDate <= startDate) {
        endInput.classList.add('error');
    } else {
        endInput.classList.remove('error');
    }
    
    errorMsg.hidden = (endDate > startDate);

    return (endDate > startDate);
}

function validateDateTime() {
    const startInput = document.getElementById('init-datetime');
    const endInput = document.getElementById('end-datetime');
    
    if (endInput.value === "") return true;
    
    return validateEndDateTimeInput(endInput);
}

function validateContacts() {
    const selectedMethods = document.querySelectorAll('#contact-methods input:checked');
    const selectedMethodsArr = Array.from(selectedMethods);
    
    if (selectedMethodsArr.length === 0) return false;
    
    for (let method of selectedMethodsArr) {
        const input = document.getElementById(`contact-${method.value}-input`);
        if (!input.value || input.value.length < 4) {
            input.classList.add('error');
            return false;
        }
    }
    
    return true;
}

function validateForm() {
    const isValid = (
        validateEmail() &&
        validateTel() &&
        validateDateTime() &&
        validateContacts() &&
        validateThemes() &&
        validatePhotos()
    );

    if (!isValid) {
        alert('Por favor, complete todos los campos requeridos correctamente.');
    }

    return isValid;
}

// UI/Window Management Functions
function toggleWindow(rowId) {
    const window = document.getElementById(`window-${rowId}`);
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

// Form Submission and Confirmation Functions
function showConfirmationWindow() {
    const confirmationWindow = document.getElementById('confirmation-window');
    const overlay = document.getElementById('overlay');

    confirmationWindow.style.display = 'block';
    overlay.style.display = 'block';

    document.getElementById('close-btn').addEventListener('click', closeConfirmationWindow);
    document.getElementById('submit-btn').addEventListener('click', submitForm);
}

function closeConfirmationWindow() {
    const confirmationWindow = document.getElementById('confirmation-window');
    const overlay = document.getElementById('overlay');

    confirmationWindow.style.display = 'none';
    overlay.style.display = 'none';
}

function loadForm() {
    const initDateInput = document.getElementById("init-datetime");

    let now = new Date(Date.now());
    now.setTime(now.getTime() - 4 * 3600 * 1000);
    initDateInput.min = now.toISOString().slice(0,-8);
    
    document.getElementById('region-select').addEventListener("change", enableComuna);

    document.getElementById('verify-btn').addEventListener('click', () => {
        if (validateForm()) {
            showConfirmationWindow();
        } else {
            alert('Por favor, complete todos los campos requeridos.');
        }
    });
}

function submitForm() {
    const form = document.getElementById('actividad-form');
    form.submit();
}