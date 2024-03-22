    // Check if the resolution message textarea exists
    if ($('#resolution_message').length) {
        // Listen for form submission
        $('#editOrderForm').submit(function(event) {
            // Get the value of the resolution message textarea
            var resolutionMessage = $('#resolution_message').val().trim();

           // Check if the resolution message is empty
           if (resolutionMessage === '') {
                    // Update the error message
                    $('#resolution_message_error').text('Resolution message is required.');
                    // Prevent form submission
                    event.preventDefault();
                } else if (resolutionMessage.length < 5 || resolutionMessage.length > 200) {
                    // Check if the length of the resolution message is within the specified range
                    // Update the error message
                    $('#resolution_message_error').text('Resolution message must be between 5 and 200 characters.');
                    // Prevent form submission
                    event.preventDefault();
                } else {
                    // Clear the error message if the resolution message is valid
                    $('#resolution_message_error').text('');
                }
        });
    }

    $(document).ready(function() {
        // Check if the resolution message textarea exists
        if ($('#resolution_message').length) {
            // Listen for input event on the resolution message textarea
            $('#resolution_message').on('input', function() {
                // Clear the error message
                $('#resolution_message_error').text('');
            });
        }
    });