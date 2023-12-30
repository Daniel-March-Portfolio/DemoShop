let categoryUUID = location.pathname.split('/')[2]
let nextItemsSetUrl = `/api/items/?category=${categoryUUID}`;
async function loadCategory(){
    let response = await fetch(`/api/categories/${categoryUUID}`);

    if (response.status !== 200) {
        alert("Error during loading category");
        return;
    }
    let category = await response.json();
    document.getElementById("category_title").innerText = category["title"];
}
async function loadItems() {
    if (nextItemsSetUrl !== null) {
        let response = await fetch(nextItemsSetUrl);

        if (response.status !== 200) {
            alert("Error during loading new items");
            return;
        }

        let responseData = await response.json();
        let newItems = responseData["results"];

        for (let newItem of newItems) {
            addItem(newItem["uuid"], newItem["title"], newItem["price"]);
        }
        nextItemsSetUrl = responseData.next;
        await loadItems();
    }
}

function addItem(uuid, title, price) {
    let item_title = document.createElement("div");
    item_title.innerText = title;
    item_title.className = "item-title";

    let item_price = document.createElement("div");
    item_title.className = "item-price";
    item_price.innerText = `$${price}`;

    let item = document.createElement("div");
    item.onclick = () => openItem(uuid);
    item.className = "item"

    item.appendChild(item_title);
    item.appendChild(item_price);

    document.getElementById("items").appendChild(item);
}

function openItem(uuid) {
    window.location = `/items/${uuid}`
}