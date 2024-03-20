document.getElementById("orderForm").addEventListener("submit", function(event) {
    var address_line1 = document.getElementById("address_line1").value.trim();
    var postcode = document.getElementById("postcode").value.trim();
    
    // Reset previous error messages
    document.getElementById("address_line1_error").textContent = "";
    document.getElementById("postcode_error").textContent = "";
    
    // Check if address line 1 is empty or exceeds 100 characters
    if (address_line1 === "" || address_line1.length > 100) {
        event.preventDefault(); // Prevent form submission
        if (address_line1 === "") {
            document.getElementById("address_line1_error").textContent = "Address Line 1 is required.";
        } else {
            document.getElementById("address_line1_error").textContent = "Address Line 1 cannot exceed 100 characters.";
        }
    }
    
    // Check if postcode is empty or does not match the pattern
     if (postcode === "" || !/^((SE|SW|W|EC|WC|E|N|NW)\d)/.test(postcode)) {
        event.preventDefault(); // Prevent form submission
    if (postcode === "") {
        document.getElementById("postcode_error").textContent = "Postcode is required.";
    } else {
        document.getElementById("postcode_error").textContent = "Invalid postcode format. We only deliver in London";
    }
}
});

// Clear error messages when inputs change
document.getElementById("address_line1").addEventListener("input", function() {
    document.getElementById("address_line1_error").textContent = "";
});

document.getElementById("postcode").addEventListener("input", function() {
    document.getElementById("postcode_error").textContent = "";
});