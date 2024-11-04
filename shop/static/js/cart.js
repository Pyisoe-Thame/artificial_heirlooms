var updateButtons = document.getElementsByClassName('update-cart')

for( var i = 0; i < updateButtons.length; i++)
{
    updateButtons[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        var stock = parseInt(this.dataset.stock);  // get the stock level from data-stock
        var currentQuantity = parseInt(this.dataset.quantity); // Get current OrderItem quantity

        console.log('productId:', productId, 'action:', action)
        console.log('User:', user)
        
        if(action === 'add' && currentQuantity >= stock) {
            alert("The item count cannot exceed the stock limit.");
            return;  // stop further execution if the stock limit is reached
        }
        if(user != "AnonymousUser")
            updateCart(productId, action)
        else
            console.log("User is not authenticated.")
    })
}

function updateCart(productId, action){
    // console.log("User is authenticated.")

    var url = '/update_item/'
    console.log('URL:', url)

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()  /* refresh the page */
    })
}

