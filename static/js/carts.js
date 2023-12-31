let nextCartsSetUrl = `/api/carts/`;
let totalPrice = 0
let itemsList = []
let cartUUIDs = []

async function loadCarts() {
    if (nextCartsSetUrl !== null) {
        let response = await fetch(nextCartsSetUrl);

        if (response.status !== 200) {
            alert("Error during loading new carts");
            return;
        }

        let responseData = await response.json();
        let newCarts = responseData["results"];

        for (let newCart of newCarts) {
            let item = await loadItem(newCart["item"]);
            addCart(newCart["uuid"], item["uuid"], item["title"], item["price"], newCart["count"])
            itemsList.push({"item": item["uuid"], "count": newCart["count"]})
            cartUUIDs.push(newCart["uuid"])
            totalPrice += item["price"] * newCart["count"]
        }
        nextCartsSetUrl = responseData.next;
        await loadCarts();
    } else {
        document.getElementById("total_price").innerText = `Total price: $${totalPrice}`
        document.getElementById("buy").innerText = "Buy all"
        document.getElementById("buy").onclick = () => buy()
    }
}

async function loadItem(uuid) {
    let response = await fetch(`/api/items/${uuid}`);

    if (response.status !== 200) {
        alert("Error during item loading");
        return;
    }
    return await response.json()
}

async function loadCart(uuid) {
    let response = await fetch(`/api/carts/${uuid}/`);

    if (response.status !== 200) {
        alert("Error during cart loading");
        return;
    }
    return await response.json()
}

function addCart(cart_uuid, item_uuid, item_title, item_price, count) {
    let cart_title = document.createElement("div");
    cart_title.innerText = item_title;
    cart_title.className = "item-title";

    let cart_price = document.createElement("div");
    cart_title.className = "item-price";
    cart_price.innerText = `$${item_price * count} ($${item_price} * ${count})`;

    let cart = document.createElement("div");
    cart.onclick = () => openItem(item_uuid);
    cart.className = "cart"
    cart.appendChild(cart_title);
    cart.appendChild(cart_price);

    document.getElementById("carts").appendChild(cart);
}

function openItem(uuid) {
    window.location = `/items/${uuid}`
}

async function buy() {
    let response = await fetch(`/api/payments/`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            "items": itemsList
        })
    });

    if (response.status !== 201) {
        alert("Error during updating cart");
    }
    let responseData = await response.json()
    for (let cartUUID of cartUUIDs) {
        fetch(`/api/carts/${cartUUID}/`, {
            method: "DELETE",
            credentials: "include",
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
    }
    window.location = `/payments/${responseData["uuid"]}`
}