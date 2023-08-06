function nextStep() {
    console.log("button clicked")
    document.getElementById('order').style.display = 'none';
    document.getElementById('details').style.display = 'block';
    document.getElementById('prevBtn').style.display = 'block';
  }
  
  function prevStep() {
    document.getElementById('details').style.display = 'none';
    document.getElementById('order').style.display = 'block';
    document.getElementById('prevBtn').style.display = 'none';
  }
  
  