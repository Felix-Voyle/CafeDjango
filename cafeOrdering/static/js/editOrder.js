// Access cart data from the context and store it in session storage
const cartData = JSON.parse("{{ cart_data|escapejs }}");
console.log(cartData)
sessionStorage.setItem('cart', JSON.stringify(cartData));

// Add event listener to remove cart data from session storage beforeunload
window.addEventListener('beforeunload', function (event) {
    sessionStorage.removeItem('cart');
});


