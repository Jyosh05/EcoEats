let cartQuantity = 1;

let shoppingCart = [
  {
    productId: 'f1',
    productName: 'Chicken Salad',
    price: 6.60,
    quantity: 1
  },
  // More items to be added
];

function addToCart() {
  // Perform any necessary actions (e.g., add item to a cart object, update UI, etc.)
  const newItem = {
    productId: f1, // Replace with the actual product ID
    productName: 'Poached Chicken Salad', // Replace with the actual product name
    price: 6.60, // Replace with the actual product price
    quantity: 1 // Initial quantity
  };

  // Check if the item is already in the cart
  const existingItem = cart.find(item => item.productId === newItem.productId);

  if (existingItem) {
    // If the item is already in the cart, increment its quantity
    existingItem.quantity++;
  } else {
    // If the item is not in the cart, add it
    cart.push(newItem);
  }

  // Increment the overall cart quantity
  cartQuantity++;

  // Update the UI
  function updateCartQuantityDisplay() {
  document.getElementById('quantity').textContent = `${cartQuantity}`;
}
}

function incrementQuantity() {
  cartQuantity++;
  updateQuantityDisplay();
}

function decrementQuantity() {
  if (cartQuantity > 1) {
    cartQuantity--;
    updateQuantityDisplay();
  }
}

function updateQuantityDisplay() {
  const quantityDisplays = document.getElementsByClassName('quantity-display');
    for (const display of quantityDisplays) {
        display.textContent = `${cartQuantity}`;
    }
}


