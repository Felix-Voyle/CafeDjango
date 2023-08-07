function accountPopUp() {
    var toggleCard = document.getElementById("toggleCard");
    var isDisplayed = toggleCard.style.display === "block";

    if (isDisplayed) {
        toggleCard.style.display = "none";
        document.removeEventListener("click", clickOutsideToggleCard);
    } else {
        toggleCard.style.display = "block";
        document.addEventListener("click", clickOutsideToggleCard);
    }
}

function clickOutsideToggleCard(event) {
    var toggleCard = document.getElementById("toggleCard");
    var toggleButton = document.getElementById("toggleButton");
    
    if (!toggleCard.contains(event.target) && event.target !== toggleButton) {
        toggleCard.style.display = "none";
    
        document.removeEventListener("click", clickOutsideToggleCard);
    }
}