document.addEventListener("DOMContentLoaded", function() {
    var addButton = document.getElementById("add-product");
    var productSelect = document.getElementById("product");
    var quantityInput = document.getElementById("quantity");
    var addedProductsTable = document.getElementById("added-products-table");
    var invoiceForm = document.getElementById("invoice-products");
    var invoiceDetail = document.getElementById("invoice-detail");

    addButton.addEventListener("click", function() {
        var productId = productSelect.value;
        var productName = productSelect.options[productSelect.selectedIndex].text;
        var quantity = quantityInput.value;

        if (productId && quantity > 0) {
            // Check if the table header is already added
            if (addedProductsTable.getElementsByTagName('thead').length === 0) {
                // Create the table header row
                var thead = document.createElement('thead');
                var headerRow = document.createElement('tr');
                var productHeader = document.createElement('th');
                var quantityHeader = document.createElement('th');
                var deleteHeader = document.createElement('th');

                // Add classes to the table header cells
                productHeader.classList.add('invoice-th', 'text-center');
                quantityHeader.classList.add('invoice-th', 'text-center');
                deleteHeader.classList.add('invoice-th', 'text-center');

                // Set the innerHTML of the header cells
                productHeader.textContent = "Product";
                quantityHeader.textContent = "Qty";

                // Append the header cells to the header row
                headerRow.appendChild(productHeader);
                headerRow.appendChild(quantityHeader);
                headerRow.appendChild(deleteHeader); // Assuming this is the delete button header

                // Append the header row to the thead
                thead.appendChild(headerRow);

                // Append the thead to the table
                addedProductsTable.appendChild(thead);
            }

            // Create a new table row
            var newRow = addedProductsTable.insertRow();

            // Insert cells for Product, Quantity, and Delete button
            var productCell = newRow.insertCell();
            var quantityCell = newRow.insertCell();
            var deleteCell = newRow.insertCell();

            // Set the content of the cells
            productCell.textContent = productName;
            quantityCell.textContent = quantity;

            // Add classes to table row and cells
            newRow.classList.add("invoice-row");
            productCell.classList.add("invoice-table");
            quantityCell.classList.add("invoice-table");
            deleteCell.classList.add("invoice-table");

            // Create hidden input fields for product and quantity
            var productInput = document.createElement("input");
            productInput.type = "hidden";
            productInput.name = "products";
            productInput.value = productId;
            productCell.appendChild(productInput);

            var quantityInputHidden = document.createElement("input");
            quantityInputHidden.type = "hidden";
            quantityInputHidden.name = "quantities";
            quantityInputHidden.value = quantity;
            quantityCell.appendChild(quantityInputHidden);

            invoiceDetail.classList.remove("d-none");

            // Create a delete button
            var deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";
            deleteButton.className = "btn btn-danger";
            deleteButton.onclick = function() {
                addedProductsTable.deleteRow(newRow.rowIndex);
                if (addedProductsTable.rows.length === 1) {
                    // If there are no more rows, remove the table header
                    addedProductsTable.deleteTHead();
                    invoiceDetail.classList.add("d-none");
                }
            };
            deleteCell.appendChild(deleteButton);
        } else {
            alert("Please select a product and enter a valid quantity.");
        }
    });
});