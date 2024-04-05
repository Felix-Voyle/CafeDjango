document.addEventListener('DOMContentLoaded', function () {
    
    function displayError(input, msg) {
        var errorMessage = document.createElement('span');
        errorMessage.className = 'input-error-msg';
        errorMessage.textContent = msg;

        var existingErrorMessage = input.parentElement.querySelector('.input-error-msg');
        if (existingErrorMessage) {
            existingErrorMessage.textContent = msg;
        } else {
            input.insertAdjacentElement('afterend', errorMessage);
        }
    }

    function removeError(input) {
        var parentElement = input.parentElement;
        if (parentElement) {
            var existingErrorMessage = parentElement.querySelector('.input-error-msg');
            if (existingErrorMessage) {
                existingErrorMessage.textContent = "";
            }
        }
    }

    function resetForm() {
        var form = document.getElementById('deliveryForm');
        form.innerHTML = originalFormHTML;
        addInputEventListeners();
    }

    $('#deliveryModal').on('hidden.bs.modal', function (e) {
        resetForm();
    });


    function validateInvoiceDetail() {
    var invoiceDetail = document.getElementById('invoiceDetails');
    var invoiceDetailLen = invoiceDetail.value.trim().length;

    if (invoiceDetailLen < 6 || invoiceDetailLen > 100) {
        displayError(invoiceDetail, "Description should be between 6 and 100 characters");
        return false;
    }
    return true;
    }

    function validateServicesAndPrices() {
        var serviceDescriptions = document.getElementsByName('serviceDescription');
        var servicePrices = document.getElementsByName('servicePrice');
        var lastServicePriceInput = servicePrices[servicePrices.length - 1];
    
        for (var i = 0; i < serviceDescriptions.length; i++) {
            var description = serviceDescriptions[i].value;
            var price = servicePrices[i].value;
    
            if (description && !price) {
                displayError(lastServicePriceInput, "Input a price for your service");
                return false;
            }
            if (price && !description) {
                displayError(serviceDescriptions[i], "Input a service for the price");
                return false;
            } 
            var isValid = /^(\d{1,5}(\.\d{1,2})?)?$/.test(price);
            if (!isValid) {
                displayError(lastServicePriceInput, "Invalid input. Can be 7 digits including up to two decimal places.");
                return false;
            }
        }
        return true;
    }        

    document.getElementById('deliveryForm').addEventListener('submit', function (event) {
        event.preventDefault(); 

        if (!this.checkValidity()) {
            event.stopPropagation();
        }

        if (!validateInvoiceDetail()) {
            event.stopPropagation();
            return;
        }

        if (!validateServicesAndPrices()) {
            event.stopPropagation();
            return;
        }

        this.submit()
    });

    var inputs = document.querySelectorAll('input[type="text"], input[type="number"], textarea');
    inputs.forEach(function (input) {
        input.addEventListener('input', function () {
            removeError(input);
        });
    });

    $('#addServiceBtn').on('click', function () {
        let serviceCount = 1;
        var serviceDescriptionInputs = document.querySelectorAll('[name="serviceDescription"]');
        var servicePriceInputs = document.querySelectorAll('[name="servicePrice"]');

        if ([...serviceDescriptionInputs].some(input => !input.value) ||
            [...servicePriceInputs].some(input => !input.value)) {
            var lastServicePriceInput = servicePriceInputs[servicePriceInputs.length - 1];
            displayError(lastServicePriceInput, "Please fill in all current services before adding more.");
        } else {
            var newServiceFields = $('#serviceFields').clone();
            newServiceFields.find('input, textarea').each(function () {
                var oldId = $(this).attr('id');
                var newId = oldId + serviceCount;
                $(this).attr('id', newId).val('').removeAttr('required');
            });
            $('#deliveryForm').append(newServiceFields);
            serviceCount++;
            addInputEventListeners(newServiceFields.find('input[type="text"], input[type="number"], textarea'));
        }
    });

    var originalFormHTML = document.getElementById('deliveryForm').innerHTML;

    function addInputEventListeners() {
        var inputs = document.querySelectorAll('input[type="text"], input[type="number"], textarea');
        inputs.forEach(function (input) {
            input.addEventListener('input', function () {
                removeError(input);
            });
        });
    }
    addInputEventListeners();

});