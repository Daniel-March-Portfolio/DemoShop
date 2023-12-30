let nextCategoriesSetUrl = "/api/categories";

async function loadCategories() {
    if (nextCategoriesSetUrl !== null) {
        let response = await fetch(nextCategoriesSetUrl);

        if (response.status !== 200) {
            alert("Error during loading new categories");
            return;
        }

        let responseData = await response.json();
        let newCategories = responseData["results"];

        for (let newCategory of newCategories) {
            addCategory(newCategory["uuid"], newCategory["title"]);
        }
        nextCategoriesSetUrl = responseData.next;
        await loadCategories();
    }
}

function addCategory(uuid, title) {
    let category_title = document.createElement("div");
    category_title.innerText = title;

    let category = document.createElement("div");
    category.onclick = () => openCategory(uuid);
    category.className = "category"
    category.appendChild(category_title);

    document.getElementById("categories").appendChild(category);
}

function openCategory(uuid) {
    window.location = `/categories/${uuid}`
}