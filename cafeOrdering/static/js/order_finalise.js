document.addEventListener('click', function (event) {
    if (event.target && event.target.id === 'deliveryFormTrigger') {
        const anchor = event.target;
        const orderId = anchor.getAttribute('data-order-id');
        const url = anchor.getAttribute('href');
        const form = document.getElementById('deliveryForm');

        form.setAttribute('action', url);
    }
});

document.getElementById('deliveryForm').addEventListener('submit', function (event) {
    if (!this.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
    }
});

document.addEventListener('click', function (event) {
    if (event.target && event.target.id === 'deliveryFormTrigger') {
        event.preventDefault();
        $('#deliveryModal').modal('show');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    var serviceCount = 1;
    $('#addServiceBtn').on('click', function () {
        var newServiceFields = $('#serviceFields').clone();
        newServiceFields.find('input, textarea').each(function () {
            var oldId = $(this).attr('id');
            var newId = oldId + serviceCount;
            $(this).attr('id', newId).val('').removeAttr('required');
        });
        $('#deliveryForm').append(newServiceFields);
        serviceCount++;
    });
});