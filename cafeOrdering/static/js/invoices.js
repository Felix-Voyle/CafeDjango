document.addEventListener("DOMContentLoaded", function() {
    $('.mark-paid-link').on('click', function(event) {
        event.preventDefault();
        var invoiceRef = $(this).data('invoiceRef');
        $('#confirmPaymentBtn').attr('href', invoiceRef);
        $('#confirmationModal').modal('show');
    });

    $('#confirmationModal').on('hidden.bs.modal', function () {
        $('.confirm-payment-btn').attr('href', '');
    });

    $('.delete-btn').on('click', function(event) {
        if ($(this).hasClass('disabled')) {
            event.preventDefault();
        } else {
            var invoiceRef = $(this).data('invoice-ref');
            $('#confirmDeleteBtn').attr('data-invoice-ref', invoiceRef);
        }
    });

    $('#deleteConfirmationModal').on('show.bs.modal', function (event) {
        var invoiceRef = $('#confirmDeleteBtn').attr('data-invoice-ref');
        $('#confirmDeleteBtn').on('click', function() {
            window.location.href = invoiceRef;
        });
    });

    $('#deleteConfirmationModal').on('hidden.bs.modal', function () {
        $('#confirmDeleteBtn').off('click');
    });

});