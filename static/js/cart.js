var updateBtns = document.getElementsByClassName('update-cart');



for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        var price = document.getElementById("product_price").value;
        var link = document.getElementById("link").value;

        console.log(link);

        console.log("product:", productId, 'action:', action, "price:", price, "link:", link);
        console.log(typeof(productId));
        console.log(typeof(action));
        console.log(typeof(price));

        updateUserOrder(productId, action, price, link);
    })
}

function updateUserOrder(productId, action, price, link){
    console.log("user authenticated");

    var url = '/update_item/';
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId, 'action': action, 'price': price, 'link': link
        })
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}