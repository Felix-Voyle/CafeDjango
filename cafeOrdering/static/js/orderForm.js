function nextStep() {
  document.getElementById("order").style.display = "none";
  document.getElementById("details").style.display = "block";
  document.getElementById("prevBtn").style.display = "block";
  document.getElementById("nextBtn").style.display = "none";
  document.getElementById("formTitles").style.display = "none";

  const inputs = document.querySelectorAll("input.qty-input");
  const tableBody = document.querySelector("#orderTable tbody");
  const showTotal = document.getElementById('total');
  
  tableBody.innerHTML = '';
  let total = 0

  inputs.forEach((input) => {
    const price = input.parentElement.previousElementSibling.querySelector('span').textContent;
    const product = input.parentElement.parentElement.querySelector('label').textContent;
    const quantity = parseInt(input.value, 10);

    if (quantity > 0) {
      total += parseFloat(price) * quantity
      const row = document.createElement("tr");

      const productNameCell = document.createElement("td");
      productNameCell.textContent = product;
      productNameCell.classList.add("text-center");
      row.appendChild(productNameCell);

      const priceCell = document.createElement("td");
      priceCell.textContent = price
      priceCell.classList.add("text-center");
      row.appendChild(priceCell);

      const quantityCell = document.createElement("td");
      quantityCell.textContent = quantity;
      quantityCell.classList.add("text-center");
      row.appendChild(quantityCell);

      tableBody.appendChild(row);
    }
  });
  showTotal.innerHTML = total.toFixed(2)
}



function prevStep() {
  document.getElementById("details").style.display = "none";
  document.getElementById("order").style.display = "block";
  document.getElementById("prevBtn").style.display = "none";
  document.getElementById("nextBtn").style.display = "block";
  document.getElementById("formTitles").style.display = "flex";
}

function minSpend(minSpendValue) {
  const inputs = document.querySelectorAll("input.qty-input");
  const nextBtn = document.getElementById("nextBtn");
  let total = 0;

  inputs.forEach((input) => {
    const price = parseFloat(input.parentElement.previousElementSibling.querySelector('span').textContent);
    const quantity = parseInt(input.value, 10);
    if (quantity > 0) {
      total += price * quantity;
    }
  });

  total = parseFloat(total.toFixed(2));

  if (total >= minSpendValue) {
    nextBtn.removeAttribute("disabled");
  } else {
    nextBtn.setAttribute("disabled", "disabled");
  }

  console.log(total, minSpendValue);
}

function incQuantity(e) {
  const input = e.target.previousElementSibling;
  let product = input.name;
  let value = parseInt(input.value, 10);
  if (value === 100) {
    return;
  }
  value += 1;
  input.value = value;
  minSpend(20)
}

function decQuantity(e) {
  const input = e.target.nextElementSibling;
  let product = input.name;
  let value = parseInt(input.value, 10);
  if (value === 0) {
    return;
  }
  value -= 1;
  input.value = value;
  minSpend(20)
}

$(document).ready(function() {
  $("#futureDate").datepicker({
    dateFormat: "dd/mm/yy",
    beforeShowDay: function(date) {
      var now = new Date();
      var day = date.getDay();
      var timeDifference = date - now;

      if (day === 0 || day === 6 || timeDifference < 0 || timeDifference <= 1000 * 60 * 60 * 48) {
        return [false, ""];
      }
      return [true, ""];
    },
    onSelect: function(dateText, inst) {
      var selectedDate = $.datepicker.formatDate("yy-mm-dd", $(this).datepicker("getDate"));
      $("#futureDateFormatted").val(selectedDate);
      console.log($("#futureDateFormatted").val())
    }
  });
  $('#timepicker').timepicker({
    timeFormat: 'HH:mm', 
    interval: 15,
    minTime: '7:30am',
    maxTime: '5:30pm',         
    dynamic: false,       
    dropdown: true,       
});

});
