document.addEventListener("DOMContentLoaded", function () {
    // document.querySelectorAll(".update-cart").forEach(count);

    // I prefer this method
    document.querySelectorAll(".update-cart").forEach((button) => {
        button.onclick = function () {
            var productID = this.dataset.product;
            var action = this.dataset.action;
            console.log("THIS is " + user);
            if (user == "AnonymousUser") {
                console.log("He is anonymous");
                console.log(cart);
                addCookieItem(productID, action);
            } else {
                // console.log("haha umchaph");
                updateUserOrder(productID, action);
            }
        }
    });

    /**
     * Documentation: Javascript Cookies
     * Code Keys
     * Remember the cookie we set only stores product id's and quantity.
     *  Get Cookies In View
     *  We can retrieve what's in our browsers cookies by using request.COOKIES['cart'] and
     *  json.loads() to parse the data becuase currently it is a string value
     *
     *
     *
     * @param productID
     * @param action
     */
    function addCookieItem(productID, action) {

        console.log(productID);
        console.log(action);
        if (action === 'add') {
            if (cart[productID] === undefined) {
                cart[productID] = {"quantity": 1}
                console.log('Item Added');
            } else {
                cart[productID]['quantity'] += 1;
            }
        }


        if (action === 'remove') {
            cart[productID]['quantity'] -= 1;
            if (cart[productID]['quantity'] <= 0) {
                console.log('Item Deleted')
                delete cart[productID];
            }
        }
        console.log(cart);
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
        location.reload();

    }


    function updateUserOrder(productID, action) {
        var url = "/update_item/"
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken,
            },
            body: JSON.stringify({"productID": productID, "action": action})
        })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                console.log("data", data)
                location.reload()
            })
    }
});

