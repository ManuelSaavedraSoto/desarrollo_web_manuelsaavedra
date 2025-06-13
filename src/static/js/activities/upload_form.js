// Form Input Handling Functions
var regionJSON = null;

async function fetchRegions() {
    try {
        const response = await fetch(apiURL);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        regionJSON = data;

    }  catch (error) {
        console.error('Error:', error);
    }
}

function handleRegionSelection(event) {
    const comunaSelect = document.getElementById(inputId.comuna);
    const selectedRegionId = event.target.value;
    
    if (!(selectedRegionId === undefined)) {
        removeErrorLabel(inputId.region);
    }

    // Reset and enable comuna select
    comunaSelect.disabled = false;
    comunaSelect.value = '';
    Array.from(comunaSelect).forEach(comuna => {
        let comunaRegionId = comuna.getAttribute("data-region-id")
        comuna.hidden = comunaRegionId !== selectedRegionId;
    });
}

function handleComunaSelection(event) {
    const selectedComunaId = event.target.value;
    
    if (!(selectedComunaId === undefined)) {
        removeErrorLabel(inputId.comuna);
    }
}

function handleThemeSelection(checkbox) {
    if (checkbox.checked) {
        removeErrorLabel('themes');
    }

    if (checkbox.id === inputId.temaOtro.checkbox) {
        const otherThemeTextInput = document.getElementById(inputId.temaOtro.text);

        otherThemeTextInput.required = checkbox.checked;
        otherThemeTextInput.disabled = !checkbox.checked;

        if (!checkbox.checked) {
            otherThemeTextInput.value = "";
        }
    }
}

function handleContactSelection(selectedOption) {
    const selectedOptions = Array.from(document.querySelectorAll('#rrss input[type=checkbox]:checked'));
    const options = Array.from(document.querySelectorAll('#rrss input[type=checkbox]'));
    let contactInt = parseInt(selectedOption.id.match(/\d/));
    const selectedOptionInput = document.getElementById(inputId.rrss[contactInt].textId);

    selectedOptionInput.required = selectedOption.checked;
    selectedOptionInput.disabled = !selectedOption.checked;
    if (!selectedOption.checked) {
        selectedOptionInput.value = "";
    }

    if (selectedOptions.length > 0) {
        const methods = document.querySelectorAll('#rrss .input-group');
        methods.forEach(method => {
            method.classList.remove('error');
        });
    }

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
    
    const endInput = document.getElementById(inputId.dateEnd);
    
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

    removeErrorLabel(inputId.dateEnd);
}

function handleOptionalPhotoInputs(enable) {
    for (let i = 1; i <= 4; i++) {
        const input = document.getElementById(inputId.photos[i]);
        input.disabled = !enable;
        if (!enable) {
            input.value = ''; // Clear the input when disabling
        }
    }
}

// Form Validation Functions
function validateName() {
    const nameInput = document.getElementById(inputId.nombre);
    let isValid = true;

    if (!nameInput.value || nameInput.value.length > 200) {
        addErrorLabel(inputId.nombre, 'Nombre inválido. Máximo 200 caracteres');
        isValid = false;
    } else {
        removeErrorLabel(inputId.nombre);
    }

    return isValid;
}

function validateRegionComuna() {
    const regionSelect = document.getElementById(inputId.region);
    const comunaSelect = document.getElementById(inputId.comuna)
    const selectedRegionId = parseInt(regionSelect.options[regionSelect.selectedIndex].value);
    const selectedComunaId = parseInt(comunaSelect.options[comunaSelect.selectedIndex].value);
    const selectedComunaRegionId = parseInt(comunaSelect.options[comunaSelect.selectedIndex].getAttribute('data-region-id'));
    const regionData = regionJSON.find(region => region.id === parseInt(selectedRegionId));

    if ( regionData !== undefined) {
        if (selectedComunaRegionId !== regionData.id) {
            addErrorLabel(inputId.comuna, "Comuna Invalida.");
            return false;
        }
        comunaData = regionData.comunas.find(comuna => comuna.id === selectedComunaId)
        if ( comunaData !== undefined ) {
            removeErrorLabel(inputId.comuna);
            return true;
        }
    } else {
        addErrorLabel(inputId.region, "Región Invalida.");
        addErrorClass(inputId.comuna);
        return false;
    }
}

function validateEmail() {
    const emailInput = document.getElementById(inputId.email);
    let isValid = true;
    let email_pattern = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

    if (!email_pattern.test(emailInput.value)) {
        addErrorLabel(inputId.email, 'Email invalido.');
        isValid = false;
    } else {
        removeErrorLabel(inputId.email);
    }

    return isValid;
}

function validateTel() {
    const telInput = document.getElementById(inputId.tel);
    let tel_pattern = /\+[0-9]{3}\.[0-9]{8}/;
    let isValid = true;

    if (!tel_pattern.test(telInput.value)) {
        addErrorLabel(inputId.tel, 'Teléfono inválido. Formato esperado: +56.12345678');
        isValid = false;
    } else {
        removeErrorLabel(inputId.tel);
    }

    return isValid;
}

function validateFoto(input) {
    const fileId = input.id;
    const file = input.files[0];
    
    // Reset error state
    input.classList.remove('error');
    
    if (file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        if (!validTypes.includes(file.type)) {
            input.value = '';
            input.classList.add('error');
            return false;
        }
        
        // If this is foto-input-1, enable other photo inputs
        if (fileId === inputId.photos[0]) {
            handleOptionalPhotoInputs(true);
        }
        
        removeErrorLabel('photo-inputs');
        removeErrorLabel(fileId);

        return true;
    }
    
    // If this is foto-input-1 being cleared, disable other photo inputs
    if (fileId === inputId.photos[0]) {
        handleOptionalPhotoInputs(false);
    }
    
    return true;
}

function validatePhotos() {
    const firstPhoto = document.getElementById(inputId.photos[0]);
    
    // Reset error states
    removeErrorLabel(inputId.photos[0]);
    
    if (!firstPhoto.files.length) {
        addErrorLabel(inputId.photos[0], 'Primera foto es obligatoria');
        return false;
    }
    
    // Validate all photo inputs
    for (let i = 0; i < 5; i++) {
        const input = document.getElementById(inputId.photos[i]);
        if (input.files.length && !validateFoto(input)) {
            return false;
        }
    }
    return true;
}

function validateThemes() {
    const themeInputs = document.querySelectorAll('#themes input[type="checkbox"]');
    const selectedThemes = Array.from(themeInputs).filter(input => input.checked);
    const otherThemeCheckbox = document.getElementById(inputId.temaOtro.checkbox);
    const otherThemeInput = document.getElementById(inputId.temaOtro.text);

    if (selectedThemes.length === 0) {
        const themes = document.querySelectorAll('#themes');
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
    const startInput = document.getElementById(inputId.dateStart);
    
    // If end date is empty, it's valid (will use default)
    if (!endInput.value) {
        endInput.classList.remove('error');
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
    } else {
        endInput.classList.remove('error');
    }
    
    return isValid;
}

function validateDateTime() {
    const startInput = document.getElementById(inputId.dateStart);
    
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
    const endInput = document.getElementById(inputId.dateEnd);
    if (!endInput.value) {
        return true;
    }
    
    return validateEndDateTimeInput(endInput);
}

function validateContactText(input) {
    const value = input.value;
    let isValid = true;
    if (!input.value || input.value.length < 4 || input.value.length > 50) {
        input.classList.add('error');
        isValid = false;
    } else {
        input.classList.remove('error');
    }
    return isValid;
}

function validateContacts() {
    const selectedMethods = document.querySelectorAll('#rrss input:checked');
    const selectedMethodsArr = Array.from(selectedMethods);
    let isValid = true;
    if (selectedMethodsArr.length === 0) {
        const methods = document.querySelectorAll('#rrss .input-group');
        methods.forEach(method => {
            method.classList.add('error');
        });
        return false;
    }

    for (let method of selectedMethodsArr) {
        let contactInt = parseInt(method.id.match(/\d/));
        const input = document.getElementById(inputId.rrss[contactInt].textId);
        isValid = validateContactText(input);
    }
    
    return isValid;
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
    const initDateInput = document.getElementById(inputId.dateStart);
    const regionSelect = document.getElementById(inputId.region);
    const comunaSelect = document.getElementById(inputId.comuna);

    let now = new Date(Date.now());
    now.setTime(now.getTime() - 4 * 3600 * 1000);
    initDateInput.min = now.toISOString().slice(0,-8);
    
    // Initialize photo inputs state
    handleOptionalPhotoInputs(false);
    
    // Initialize name input
    document.getElementById(inputId.nombre).addEventListener('change', validateName);

    // Initialize telephone input
    document.getElementById(inputId.tel).addEventListener('change', validateTel);

    // Initialize region selector
    regionSelect.addEventListener("change", handleRegionSelection);
    regionSelect.value = '';

    // Initialize comuna selector
    comunaSelect.addEventListener("change", handleComunaSelection);
    comunaSelect.value = '';
    comunaSelect.disabled = true;

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
        if (!isSubmitting && validateForm()) {
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

    // Validate form before submission
    /* Commented for testing purposes
    if (!validateForm()) {
        return;
    }
    */
    
    setSubmitting(true);
    const form = document.getElementById('actividad-form');
    const formData = new FormData(form);

    try {
        const response = await fetch(window.location.href, {
            method: 'POST',
            body: formData,
            enctype: 'multipart/form-data',
        });
        const result = await response.json();
        console.log(result);
        
        if (result.success) {
            // Redirect immediately on success, toast will be shown on index page
            window.location.href = '/?success=true';
        } else {
            showToast('Por favor corrija los errores indicados', 'error');
            // Show specific error messages by category
            if (result) {
                // Clear previous error states
                document.querySelectorAll('.error').forEach(el => el.classList.contains('toast') ? {} : el.classList.remove('error'));
                document.querySelectorAll('.error-label').forEach(el => el.remove());

                // Handle each category of errors
                for (const category in result) {
                    for (const error_type in result[category]) {
                        addErrorLabel(result[category][error_type].id, result[category][error_type].msg);
                    }
                }
            }
            // Reset form state
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