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
    console.log(price)
    const product = input.name;
    const quantity = parseInt(input.value, 10);

    if (quantity > 0) {
      total += parseFloat(price) * quantity
      const row = document.createElement("tr");

      const productNameCell = document.createElement("td");
      productNameCell.textContent = product;
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

function incQuantity(e) {
  const input = e.target.previousElementSibling;
  let product = input.name;
  let value = parseInt(input.value, 10);
  if (value === 100) {
    return;
  }
  value += 1;
  input.value = value;
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
}
