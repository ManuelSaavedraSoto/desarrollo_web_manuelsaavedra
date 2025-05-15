// Form Input Handling Functions
var regionJSON = null;

async function fetchRegions() {
    try {
        const response = await fetch('/api/regiones');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        regionJSON = data;

    }  catch (error) {
        console.error('Error:', error);
    }
}

function handleComuna(event) {
    const comunaSelect = document.getElementById('comuna-select');
    const selectedRegionId = event.target.value;
    
    // Reset and enable comuna select
    comunaSelect.disabled = false;
    comunaSelect.innerHTML = '<option value="" selected disabled>Por favor elija una comuna.</option>';
    
    // Find selected region in fetched JSON
    const selectedRegion = regionJSON.find(region => region.id === parseInt(selectedRegionId));
    
    if (!(selectedRegion === undefined)) {
        comunaSelect.classList.remove('error');
        // Populate comuna select with options
        selectedRegion.comunas.forEach(comuna => {
            const option = document.createElement('option');
            option.value = comuna.id;
            option.textContent = comuna.nombre;
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

function handleEndDateTimeInput(startInput) {
    if (startInput.classList.contains('error')) {
        startInput.classList.remove('error');
    }
    
    const endInput = document.getElementById('end-datetime');
    const errorLabel = document.getElementById('end-datetime-error-label');
    
    if (!startInput.value) {
        endInput.value = '';
        return;
    }

    // Parse start date with timezone
    const hourInMillis = 3600 * 1000;
    let startDate = new Date(startInput.value + ':00.000-04:00');
    
    // Set default end time to start time + 3 hours
    let defaultEndDate = new Date(startDate.getTime() + 3 * hourInMillis);
    
    // Set minimum end time to start time + 1 hour
    let minDate = new Date(startDate.getTime() + hourInMillis);
    
    // "Mask" timezone offset
    defaultEndDate.setHours(defaultEndDate.getHours() - 4);
    minDate.setHours(minDate.getHours() - 4);

    // Format dates for input fields (local timezone)
    endInput.value = defaultEndDate.toISOString().slice(0, -8); // Remove seconds and timezone
    endInput.min = minDate.toISOString().slice(0, -8);
    endInput.disabled = false;

    errorLabel.hidden = true;
}

function handleOptionalPhotoInputs(enable) {
    for (let i = 2; i <= 5; i++) {
        const input = document.getElementById(`foto-input-${i}`);
        input.disabled = !enable;
        if (!enable) {
            input.value = ''; // Clear the input when disabling
        }
    }
}

// Form Validation Functions
function validateName() {
    const nameInput = document.getElementById('name-input');
    let isValid = true;

    if (!nameInput.value || nameInput.value.length > 200) {
        nameInput.classList.add('error');
        isValid = false;
    } else {
        nameInput.classList.remove('error');
    }

    return isValid;
}

function validateRegionComuna() {
    const regionSelect = document.getElementById('region-select');
    const comunaSelect = document.getElementById('comuna-select');
    const regionData = regionJSON.find(region => region.id === parseInt(regionSelect.value));
    
    if (!(regionData === undefined)) {
        const selectedComuna = regionData.comunas.find(comuna => comuna.id === parseInt(comunaSelect.value));
        if (!(selectedComuna === undefined)) {
            regionSelect.classList.remove('error');
            comunaSelect.classList.remove('error');
            return true;
        } else {
            comunaSelect.classList.add('error');
            return false;
        }
    } else {
        regionSelect.classList.add('error');
        comunaSelect.classList.add('error');
        return false;
    }
}

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
    
    // Reset error state
    errorLabel.hidden = true;
    input.classList.remove('error');
    
    if (file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        if (!validTypes.includes(file.type)) {
            errorLabel.hidden = false;
            input.value = '';
            input.classList.add('error');
            return false;
        }
        
        // If this is foto-input-1, enable other photo inputs
        if (fileId === 'foto-input-1') {
            handleOptionalPhotoInputs(true);
        }
        
        return true;
    }
    
    // If this is foto-input-1 being cleared, disable other photo inputs
    if (fileId === 'foto-input-1') {
        handleOptionalPhotoInputs(false);
    }
    
    return true;
}

function validatePhotos() {
    const firstPhoto = document.getElementById('foto-input-1');
    const firstPhotoError = document.getElementById('foto-type-error-label-1');
    
    // Reset error states
    firstPhotoError.hidden = true;
    firstPhoto.classList.remove('error');
    
    if (!firstPhoto.files.length) {
        firstPhoto.classList.add('error');
        firstPhotoError.textContent = 'La primera foto es obligatoria';
        firstPhotoError.hidden = false;
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
        const themes = document.querySelectorAll('#theme-inputs');
        themes.forEach(theme => {
            theme.classList.add('error');
        });
        return false;
    }

    if (otherThemeCheckbox.checked) {
        if (!otherThemeInput.value || otherThemeInput.value.length < 3 || otherThemeInput.value.length > 15) {
            otherThemeInput.classList.add('error');
            return false;
        }
        otherThemeInput.classList.remove('error');
    }

    return true;
}

function validateEndDateTimeInput(endInput) {    
    const startInput = document.getElementById('init-datetime');
    const errorMsg = document.getElementById('end-datetime-error-label');
    
    // If end date is empty, it's valid (will use default)
    if (!endInput.value) {
        endInput.classList.remove('error');
        errorMsg.hidden = true;
        return true;
    }

    let endDate = new Date(endInput.value+':00.000-04:00');
    let startDate = new Date(startInput.value+':00.000-04:00');
    
    // Calculate minimum end time (start time + 1 hour)
    let minEndDate = new Date(startDate.getTime() + 3600000);
    
    // Check if end time is at least 1 hour after start time
    const isValid = endDate >= minEndDate;
    
    if (!isValid) {
        endInput.classList.add('error');
        errorMsg.textContent = 'La fecha de término debe ser al menos 1 hora después del inicio';
    } else {
        endInput.classList.remove('error');
    }
    
    errorMsg.hidden = isValid;

    return isValid;
}

function validateDateTime() {
    const startInput = document.getElementById('init-datetime');
    
    if (!startInput.value) {
        startInput.classList.add('error');
        return false;
    }

    // Start date must be in the future
    let now = new Date();
    let startDate = new Date(startInput.value+':00.000-04:00');

    if (startDate < now) {
        startInput.classList.add('error');
        return false;
    }
    startInput.classList.remove('error');
    
    // For end time validation, if it's empty we'll use default
    const endInput = document.getElementById('end-datetime');
    if (!endInput.value) {
        return true;
    }
    
    return validateEndDateTimeInput(endInput);
}

function validateContacts() {
    const selectedMethods = document.querySelectorAll('#contact-methods input:checked');
    const selectedMethodsArr = Array.from(selectedMethods);
    
    if (selectedMethodsArr.length === 0) {
        const methods = document.querySelectorAll('#contact-methods');
        methods.forEach(method => {
            method.classList.add('error');
        });
        return false;
    }

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
    // Run all validations and track results
    const validations = {
        'Nombre': validateName(),
        'Región/Comuna': validateRegionComuna(),
        'Email': validateEmail(),
        'Teléfono': validateTel(),
        'Fecha/Hora': validateDateTime(),
        'Métodos de contacto': validateContacts(),
        'Temas': validateThemes(),
        'Fotos': validatePhotos()
    };

    // Find all failed validations
    const failures = Object.entries(validations)
        .filter(([_, passed]) => !passed)
        .map(([field, _]) => field);

    if (failures.length > 0) {
        showToast(`Por favor revise: ${failures.join(', ')}`, 'error');
        return false;
    }

    return true;
}

// Form state
let isSubmitting = false;

function setSubmitting(submitting) {
    isSubmitting = submitting;
    const verifyBtn = document.getElementById('verify-btn');
    const submitBtn = document.getElementById('submit-btn');
    
    verifyBtn.disabled = submitting;
    submitBtn.disabled = submitting;
    
    if (submitting) {
        verifyBtn.textContent = 'Subiendo...';
        submitBtn.textContent = 'Subiendo...';
    } else {
        verifyBtn.textContent = 'Subir Actividad';
        submitBtn.textContent = 'Enviar';
    }
}

// Form Submission Functions
function loadForm() {
    const initDateInput = document.getElementById("init-datetime");

    let now = new Date(Date.now());
    now.setTime(now.getTime() - 4 * 3600 * 1000);
    initDateInput.min = now.toISOString().slice(0,-8);
    
    // Initialize photo inputs state
    handleOptionalPhotoInputs(false);
    
    // Initialize region selector
    document.getElementById('region-select').addEventListener("change", handleComuna);

    // Initialize form submission handlers
    document.getElementById('verify-btn').addEventListener('click', () => {
        if (isSubmitting) {
            return;
        }
        
        if (validateForm()) {
            toggleWindow('confirmation');
        }
    });

    // Set up confirm/cancel buttons
    document.getElementById('close-btn').addEventListener('click', () => {
        if (!isSubmitting) {
            toggleWindow('confirmation');
        }
    });
    
    document.getElementById('submit-btn').addEventListener('click', async () => {
        if (!isSubmitting) {
            await submitForm();
            toggleWindow('confirmation');
        }
    });

    // Add form submit handler to prevent default submission
    document.getElementById('actividad-form').addEventListener('submit', (e) => {
        e.preventDefault();
        return false;
    });
}

async function submitForm() {
    // Prevent multiple submissions
    if (isSubmitting) {
        return;
    }
    
    setSubmitting(true);
    const form = document.getElementById('actividad-form');
    const formData = new FormData(form);

    // Add selected themes to form data
    const selectedThemes = document.querySelectorAll('#theme-inputs input[type="checkbox"]:checked');
    selectedThemes.forEach((theme, index) => {
        if (theme.value === 'Otro') {
            const otherThemeValue = document.getElementById('other-theme-text-input').value;
            if (otherThemeValue) {
                formData.append(`theme-${index}`, otherThemeValue);
            }
        } else {
            formData.append(`theme-${index}`, theme.value);
        }
    });

    // Add contact methods to form data
    const selectedContacts = document.querySelectorAll('#contact-methods input[type="checkbox"]:checked');
    selectedContacts.forEach((contact, index) => {
        const method = contact.value;
        const identifier = document.getElementById(`contact-${method}-input`).value;
        formData.append(`contact-method-${index}`, method);
        formData.append(`contact-identifier-${index}`, identifier);
    });

    try {
        const response = await fetch(window.location.href, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        
        if (result.success) {
            // Redirect immediately on success, toast will be shown on index page
            window.location.href = '/?success=true';
        } else {
            showToast(result.error || 'Error al procesar el formulario', 'error');
            // Keep form visible and scroll to any validation messages
            const validationMessages = document.querySelector('.validation-message');
            if (validationMessages) {
                validationMessages.scrollIntoView({ behavior: 'smooth' });
            }
            setSubmitting(false);
        }
    } catch (error) {
        showToast('Error al enviar el formulario', 'error');
        console.error('Error:', error);
        setSubmitting(false);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    fetchRegions().then(() => {
        loadForm();
    })
});