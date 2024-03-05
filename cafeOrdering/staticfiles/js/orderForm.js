// Display the next step in the order process
function nextStep() {
  document.getElementById("order").style.display = "none";
  document.getElementById("details").style.display = "block";
  document.getElementById("prevBtn").style.display = "block";
  document.getElementById("nextBtn").style.display = "none";
  document.getElementById("formTitles").style.display = "none";

  const inputs = document.querySelectorAll("input.qty-input");
  const tableBody = document.querySelector("#orderTable tbody");
  const showTotal = document.getElementById("total");

  tableBody.innerHTML = "";
  let total = 0;

  disableFilterProduct(true)
  showOrderSummary(total, tableBody);
}

function disableFilterProduct(bool) {
  const selectElements = document.querySelectorAll("select[name='category']");
  selectElements.forEach(function(select) {
    select.disabled = bool;
  });

  const productSearchForm = document.querySelector(".category-form");
  productSearchForm.disabled = bool;

  const inputField = document.getElementById("productSearch");
  inputField.disabled = bool;

  const productSearchBtn = document.getElementById("productSearchBtn");
  productSearchBtn.disabled = bool;
}

function showOrderSummary(total, tableBody) {
  // Get the current cart data from Session Storage
  const cart = JSON.parse(sessionStorage.getItem('cart')) || {};

  for (const productId in cart) {
    const { quantity, price, name } = cart[productId];

    if (quantity > 0) {
      const row = document.createElement('tr');

      const productNameCell = document.createElement('td');
      productNameCell.classList.add('text-center', 'col-6')

      // Create a label element
      const productNameLabel = document.createElement('label');
      productNameLabel.textContent = name; // Set the label text to the product name
      productNameLabel.classList.add('text-center');
      productNameCell.appendChild(productNameLabel);

      // Create a hidden input element
      const productNameInput = document.createElement('input');
      productNameInput.type = 'hidden';
      productNameInput.name = `confirmed-product`;
      productNameInput.value = productId;
      productNameInput.classList.add('text-center');
      productNameCell.appendChild(productNameInput);

      row.appendChild(productNameCell);

      const priceCell = document.createElement('td');
      priceCell.textContent = `£${price}`;
      priceCell.classList.add('text-center');
      row.appendChild(priceCell);

      const quantityCell = document.createElement('td');
      quantityCell.classList.add('text-center')
      const quantityInput = document.createElement('input');
      quantityInput.type = 'number';
      quantityInput.name = `confirmed-qty`;
      quantityInput.value = quantity;
      quantityInput.classList.add('text-center', 'plain-input');
      quantityInput.readOnly = true;
      quantityCell.appendChild(quantityInput);
      row.appendChild(quantityCell);

      tableBody.appendChild(row);
    }
  }

  const showTotal = document.getElementById('total');
  let totalAmount = 0;

  for (const productId in cart) {
    const { quantity, price } = cart[productId];
    totalAmount += parseFloat(price) * quantity;
  }

  showTotal.innerHTML = `${totalAmount.toFixed(2)}`;
}


// Go back to the previous step in the order process
function prevStep() {
  document.getElementById("details").style.display = "none";
  document.getElementById("order").style.display = "block";
  document.getElementById("prevBtn").style.display = "none";
  document.getElementById("nextBtn").style.display = "block";
  document.getElementById("formTitles").style.display = "flex";

  disableFilterProduct(false)
}

// Check if the total order amount meets a minimum spending requirement
function minSpend(minSpendValue) {
  const cart = JSON.parse(sessionStorage.getItem('cart')) || {};
  const nextBtn = document.getElementById('nextBtn');
  let total = 0;

  for (const productId in cart) {
    const { quantity, price } = cart[productId];

    if (quantity > 0) {
      total += price * quantity;
    }
  }

  total = parseFloat(total.toFixed(2));

  if (total >= minSpendValue) {
    nextBtn.removeAttribute('disabled');
  } else {
    nextBtn.setAttribute('disabled', 'disabled');
  }
}


// Increment the quantity of a product
function incQuantity(e) {
  const input = e.target.previousElementSibling;
  let id = input.name;
  let name = input.getAttribute('data-product-name')
  let price = input.getAttribute('data-product-price')
  let value = parseInt(input.value, 10);
  if (value === 100) {
    return;
  }
  value += 1;
  input.value = value;
  updateCart(id, value, name, price);
  minSpend(20);
}

// Decrement the quantity of a product
function decQuantity(e) {
  const input = e.target.nextElementSibling;
  let id = input.name;
  let name = input.getAttribute('data-product-name')
  let price = input.getAttribute('data-product-price')
  let value = parseInt(input.value, 10);
  if (value === 0) {
    return;
  }
  value -= 1;
  input.value = value;
  updateCart(id, value, name, price);
  minSpend(20);
}

function updateCart(productId, quantity, name, price) {
  // Get the current cart data from Session Storage
  const cart = JSON.parse(sessionStorage.getItem('cart')) || {};

  // Update the quantity for the given product ID
  cart[productId] = {
    name,
    quantity,
    price
  }

  // Store the updated cart data back in Session Storage
  sessionStorage.setItem('cart', JSON.stringify(cart));
}

function onLoadInputs() {
  const cart = JSON.parse(sessionStorage.getItem('cart')) || {};

  for (const productId in cart) {
    const quantity = cart[productId].quantity;
    const input = document.querySelector(`input[name="${productId}"]`);
    if (input) {
      input.value = quantity;
    }
  }
  minSpend(20)
}

// jQuery code for date and time picker
$(document).ready(function () {
  // Datepicker configuration
  $("#futureDate").datepicker({
    dateFormat: "dd/mm/yy",
    beforeShowDay: function (date) {
      var now = new Date();
      var day = date.getDay();
      var timeDifference = date - now;

      if (
        day === 0 ||
        day === 6 ||
        timeDifference < 0 ||
        timeDifference <= 1000 * 60 * 60 * 48
      ) {
        return [false, ""];
      }
      return [true, ""];
    },
    onSelect: function (dateText, inst) {
      var selectedDate = $.datepicker.formatDate(
        "yy-mm-dd",
        $(this).datepicker("getDate")
      );
      $("#futureDateFormatted").val(selectedDate);
    },
  });
  // Timepicker configuration
  $("#timepicker").timepicker({
    timeFormat: "HH:mm",
    interval: 15,
    minTime: "7:30am",
    maxTime: "5:30pm",
    dynamic: false,
    dropdown: true,
  });
});

function clearCart() {
  sessionStorage.removeItem('cart');
}

window.addEventListener('load', onLoadInputs);