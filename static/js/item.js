let itemUUID = location.pathname.split('/')[2]

async function loadItem() {
    let response = await fetch(`/api/items/${itemUUID}`);

    if (response.status !== 200) {
        alert("Error during loading item");
        return;
    }
    let item = await response.json();
    document.getElementById("back_button").innerText = "< Back";
    document.getElementById("back_button").onclick = () => history.back()
    document.getElementById("title").innerText = item["title"];
    document.getElementById("description").innerText = item["description"];
    document.getElementById("price").innerText = `$${item["price"]}`;

    await loadCart()
}

async function loadCart() {
    let response = await fetch(`/api/carts/?item=${itemUUID}`);

    if (response.status !== 200) {
        alert("Error during loading cart");
        return;
    }
    let responseData = await response.json();
    let cart = responseData["results"]

    if (cart.length === 0) {
        updateButtons(null)
    } else {
        updateButtons(cart[0])
    }
}

async function addToCart(count) {
    let response = await fetch(`/api/carts/`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            "item": itemUUID, "count": count
        })
    });

    if (response.status !== 201) {
        alert("Error during updating cart");
    }
    await loadCart()
}

async function clearCart(uuid) {
    let response = await fetch(`/api/carts/${uuid}/`, {
        method: "DELETE",
        credentials: "include",
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    if (response.status !== 204) {
        alert("Error during clearing cart");
    }
    updateButtons(null)
}

function updateButtons(in_cart) {
    if (in_cart === null) {
        document.getElementById("remove_from_cart").innerText = "";
        document.getElementById("in_cart_count").innerText = "";
        document.getElementById("clear_cart").innerText = "";
        document.getElementById("add_to_cart").innerText = "Add to cart";
        document.getElementById("add_to_cart").onclick = () => addToCart(1)
    } else {
        if (in_cart["count"] === 1) {
            document.getElementById("remove_from_cart").innerText = "-";
            document.getElementById("remove_from_cart").onclick = () => clearCart(in_cart["uuid"])
        } else {
            document.getElementById("remove_from_cart").innerText = "-";
            document.getElementById("remove_from_cart").onclick = () => addToCart(in_cart["count"] - 1)
        }
        document.getElementById("in_cart_count").innerText = in_cart["count"];

        document.getElementById("add_to_cart").innerText = "+";
        document.getElementById("add_to_cart").onclick = () => addToCart(in_cart["count"] + 1)

        document.getElementById("clear_cart").innerText = "Remove from cart";
        document.getElementById("clear_cart").onclick = () => clearCart(in_cart["uuid"])
    }
}