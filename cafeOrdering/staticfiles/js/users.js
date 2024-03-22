function showEditModal() {
    $('#editCancelModal').modal('show');
}

function reportProblem(orderId) {
    // Set the hidden input value to the orderId
    $('#orderIdInput').val(orderId);
    // Show the modal
    $('#reportProblemModal').modal('show');
}

function submitProblem() {
    // Get the problem description from the textarea
    var problemDescription = $('#problemDescription').val();
    // Get the orderId from the hidden input
    var orderId = $('#orderIdInput').val();

    // Perform validation on the problem description
    if (problemDescription.length < 5 || problemDescription.length > 200) {
        // Update the validation notification with the error message
        $('#validation-notification').html('<strong style="color: red;">Problem description must be between 5 and 200 characters.</strong>');
        return; 
    }

    // AJAX call to submit the problem
    $.ajax({
        type: 'POST',
        url: reportProblemUrl, // Use the URL passed from the template
        data: {
            'order_id': orderId,
            'problem_description': problemDescription,
            'csrfmiddlewaretoken': csrfToken
        },
        success: function (response) {
            // Close the modal
            $('#reportProblemModal').modal('hide');
            // Reload page to display Django messages
            location.reload();
        },
        error: function (xhr, errmsg, err) {
            // Handle errors
            alert('Error reporting problem: ' + errmsg);
        }
    });
}

// remove validation notification on bs modal close
$('#reportProblemModal').on('hidden.bs.modal', function () {
    $('#validation-notification').empty();
});