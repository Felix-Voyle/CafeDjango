//Ajax function to update order status on checkbox tick
document.addEventListener('DOMContentLoaded', function() {
    const sentCheckboxes = document.querySelectorAll('.sent-checkbox');

    sentCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const orderId = this.getAttribute('data-order-id');
            const status = this.getAttribute('name');

            updateOrderStatus(orderId, status, this);
        });
    });

    function updateOrderStatus(orderId, status, checkbox) {
        const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

        const data = {
            orderId: orderId,
            status: status,
        }

        fetch('/manage/update_order_status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            checkbox.checked = true;
            checkbox.disabled = true;
            location.reload();
        })
        .catch(error => {
            console.error('Error updating order status:', error);
            location.reload();
        });
    }
});


// Check if user wants to edit order as no reported problem
document.addEventListener('DOMContentLoaded', function() {
    $('#confirmEditBtn').on('click', function(event) {
        event.preventDefault();
        var editLink = $('#editLinkTrigger').attr('href');
        window.location.href = editLink;
    });

    $('#editConfirmationModal').on('hidden.bs.modal', function (event) {
        event.preventDefault();
    });

    $('#editConfirmationModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);
        var hasProblem = button.data('has-problem');
        var modal = $(this);
        if (hasProblem === 'true') {
            modal.find('.modal-body').text("No reported problems with this order. Are you sure you want to edit it?");
        } else {
            modal.find('.modal-body').text("You've already resolved the reported problem. Are you sure you want to edit it?");
        }
    });
});

