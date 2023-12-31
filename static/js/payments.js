let nextPaymentsSetUrl = "/api/payments";

async function loadPayments() {
    if (nextPaymentsSetUrl !== null) {
        let response = await fetch(nextPaymentsSetUrl);

        if (response.status !== 200) {
            alert("Error during loading new payments");
            return;
        }

        let responseData = await response.json();
        let newPayments = responseData["results"];

        for (let newPayment of newPayments) {
            await addPayment(newPayment);
        }
        nextPaymentsSetUrl = responseData.next;
        await loadPayments();
    }
}

async function loadItem(uuid) {
    let response = await fetch(`/api/items/${uuid}`);
    if (response.status !== 200) {
        alert("Error during loading item");
        return;
    }
    return await response.json()
}

async function addPayment(newPayment) {
    let totalCost = 0
    let payment_cost = document.createElement("div");
    payment_cost.className = "payment_price";

    let payment = document.createElement("div");
    payment.onclick = () => openPayment(newPayment.uuid);
    payment.className = `payment ${newPayment.status}`

    for (let item of newPayment.items) {
        let item_instance = await loadItem(item.item)
        let payment_item = document.createElement("div");
        let cost = item_instance.price * item.count
        payment_item.innerText = `${item_instance.title} ($${item_instance.price} * ${item.count} = $${cost})`
        payment.appendChild(payment_item)
        totalCost += cost
    }

    payment_cost.innerText = `$${totalCost}`
    payment.appendChild(payment_cost);

    document.getElementById("payments").appendChild(payment);
}

function openPayment(uuid) {
    window.location = `/payments/${uuid}`
}