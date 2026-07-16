// ==============================
// Smart Inventory App
// ==============================

window.addEventListener("DOMContentLoaded", async () => {

    await loadCategories();
    await loadProducts();

    document.getElementById("prevBtn")?.addEventListener("click", previousPage);
    document.getElementById("nextBtn")?.addEventListener("click", nextPage);

});

const form = document.getElementById("productForm");

// ==============================
// Toast Notification
// ==============================

function showToast(message, type = "success") {

    const toast = document.getElementById("toast");

    if (!toast) {
        alert(message);
        return;
    }

    toast.innerText = message;

    toast.className = "";
    toast.classList.add(type);
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);

}

let allProducts = [];
let currentPage = 1;
const limit = 100;
let totalProducts = 0;
let totalPages = 1;
let currentSearch = "";
let currentCategory = "All";
let currentSortBy = "id";
let currentSortOrder = "desc";
let currentStockFilter = "All";

// Delete Modal
let deleteProductId = null;

const deleteModal = document.getElementById("deleteModal");
const confirmDeleteBtn = document.getElementById("confirmDelete");
const cancelDeleteBtn = document.getElementById("cancelDelete");


// ==============================
// Add / Update Product
// ==============================

if (form) {

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        const id = document.getElementById("product_id").value;

        const product = {

            product_name: document.getElementById("product_name").value.trim(),
            category: document.getElementById("category").value.trim(),
            stock: Number(document.getElementById("stock").value),
            price: Number(document.getElementById("price").value)

        };

        if (id) {

            if (!confirm("Update this product?")) {
                return;
            }

        }

        try {

            const url = id
                ? `/api/products/${id}`
                : "/api/products";

            const method = id ? "PUT" : "POST";

            const response = await fetch(url, {

                method,

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(product)

            });

            const result = await response.json();

            if (!response.ok) {

                showToast(result.message || "Something went wrong", "error");
                return;

            }

            if (result.message === "Product Already Exists") {

                showToast("Product Already Exists", "warning");
                return;

            }

            showToast(

                id
                    ? "Product Updated Successfully"
                    : "Product Added Successfully",

                "success"

            );

            resetForm();

            if (!id) {

                currentPage = 1;

            }

            await loadCategories();
            await loadProducts();

        }

        catch (error) {

            console.error(error);

            showToast("Something went wrong", "error");

        }

    });

}
// ==============================
// Load Products
// ==============================

async function loadProducts() {

    try {

       const response = await fetch(
         `/api/products?page=${currentPage}&limit=${limit}&search=${encodeURIComponent(currentSearch)}&category=${encodeURIComponent(currentCategory)}&stock_filter=${currentStockFilter}&sort_by=${currentSortBy}&sort_order=${currentSortOrder}`
        );

        if (!response.ok)
            throw new Error();

        const data = await response.json();

        allProducts = data.products || [];

        totalProducts = data.total || 0;

        totalPages = Math.max(
            1,
            Math.ceil(totalProducts / limit)
        );

        displayProducts(allProducts);

        updatePagination();

    }

    catch (error) {

        console.error(error);

        showToast("Unable to load products", "error");

    }

}
// ==============================
// Pagination
// ==============================

function updatePagination() {

    const pageInfo = document.getElementById("pageInfo");

    const prevBtn = document.getElementById("prevBtn");

    const nextBtn = document.getElementById("nextBtn");

    if (pageInfo) {

        pageInfo.innerText =
            `Page ${currentPage} of ${totalPages}`;

    }

    if (prevBtn) {

        prevBtn.disabled = currentPage === 1;

    }

    if (nextBtn) {

        nextBtn.disabled = currentPage >= totalPages;

    }

}

function previousPage() {

    if (currentPage > 1) {

        currentPage--;

        loadProducts();

    }

}

function nextPage() {

    if (currentPage < totalPages) {

        currentPage++;

        loadProducts();

    }

}


// ==============================
// Display Products
// ==============================

function displayProducts(products) {

    const table = document.getElementById("productTable");

    if (!table) return;

    if (products.length === 0) {

        table.innerHTML = `
            <tr>
                <td colspan="6">
                    No Products Found
                </td>
            </tr>
        `;

        return;

    }

    table.innerHTML = products.map(product => `

        <tr>

            <td>${product.id}</td>

            <td>${product.product_name}</td>

            <td>${product.category}</td>

            <td>
                ${
                    product.stock === 0
                        ? `<span style="color:red;font-weight:bold;">Out of Stock</span>`
                        : product.stock < 10
                            ? `<span style="color:orange;font-weight:bold;">${product.stock}</span>`
                            : `<span style="color:green;font-weight:bold;">${product.stock}</span>`
                }
            </td>

            <td>₹${Number(product.price).toFixed(2)}</td>

            <td>

                <button
                  class="action-btn edit-btn"
                  onclick='editProduct(
                  ${product.id},
                  ${JSON.stringify(product.product_name)},
                  ${JSON.stringify(product.category)},
                  ${product.stock},
                  ${product.price}
                  )'>
                  Edit
                </button>

                <button
                    class="action-btn delete-btn"
                    onclick="deleteProduct(${product.id})">

                    Delete

                </button>

            </td>

        </tr>

    `).join("");

}

// ==============================
// Search
// ==============================

function searchProducts() {

    filterProducts();

}

function filterProducts() {

    currentSearch =
        document.getElementById("searchInput").value.trim();

    currentCategory =
        document.getElementById("categoryFilter").value;

    currentStockFilter =
        document.getElementById("stockFilter").value;

    currentPage = 1;

    loadProducts();

}
// ==============================
// Categories
// ==============================

async function loadCategories() {

    const dropdown = document.getElementById("categoryFilter");

    if (!dropdown) return;

    try {

        const response = await fetch("/api/categories");

        if (!response.ok)
            throw new Error();

        const categories = await response.json();

        dropdown.innerHTML =
            `<option value="All">All Categories</option>`;

        categories.forEach(category => {

            dropdown.innerHTML +=
                `<option value="${category}">
                    ${category}
                </option>`;

        });

        if ([...dropdown.options].some(option => option.value === currentCategory)) {

            dropdown.value = currentCategory;

        } else {

            currentCategory = "All";
            dropdown.value = "All";

        }

    }

    catch (error) {

     console.error(error);

     showToast("Unable to load categories", "error");

    }

}


// ==============================
// Edit Product
// ==============================

function editProduct(id, name, category, stock, price) {

    document.getElementById("product_id").value = id;

    document.getElementById("product_name").value = name;

    document.getElementById("category").value = category;

    document.getElementById("stock").value = stock;

    document.getElementById("price").value = price;

    document.getElementById("formTitle").innerText =
        "Edit Product";

    document.getElementById("submitBtn").innerText =
        "Update Product";

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}
// ==============================
// Delete Product
// ==============================

function deleteProduct(id) {

    deleteProductId = id;

    deleteModal.style.display = "flex";


}


// ==============================
// Reset Form
// ==============================

function resetForm() {

    if (form) {

        form.reset();

    }

    document.getElementById("product_id").value = "";

    document.getElementById("formTitle").innerText =
        "Add Product";

    document.getElementById("submitBtn").innerText =
        "Add Product";

}


// ==============================
// Refresh Current Page
// ==============================

function refreshPage() {

    loadProducts();

}

// ==============================
// Export Products
// ==============================

function exportProducts() {

    window.location.href = "/api/export";

}

// ==============================
// Import Products
// ==============================


async function importProducts() {

    const fileInput = document.getElementById("excelFile");

    if (!fileInput.files.length) {

        showToast("Please select an Excel file", "warning");
        return;

    }

    const formData = new FormData();

    formData.append("file", fileInput.files[0]);

    try {

        const response = await fetch("/api/import", {

            method: "POST",
            body: formData

        });

        const result = await response.json();

        if (!response.ok) {

            showToast(result.message || "Import Failed", "error");
            return;

        }

        showToast(

            `${result.message}\nImported : ${result.imported}\nSkipped : ${result.skipped}`,

            "success"

        );

        fileInput.value = "";

        currentPage = 1;

        await loadCategories();
        await loadProducts();

    }

    catch (error) {

        console.error(error);

        showToast("Import Failed", "error");

    }

}

if (cancelDeleteBtn) {

    cancelDeleteBtn.onclick = () => {

        deleteModal.style.display = "none";
        deleteProductId = null;

    };

}

if (confirmDeleteBtn) {

    confirmDeleteBtn.onclick = async () => {

        if (!deleteProductId) return;

        try {

            const response = await fetch(`/api/products/${deleteProductId}`, {

                method: "DELETE"

            });

            const result = await response.json();

            if (!response.ok) {

                showToast(result.message || "Unable to delete product", "error");
                return;

            }

            showToast("Product Deleted Successfully", "success");

            deleteModal.style.display = "none";

            deleteProductId = null;

            if (currentPage > 1 && allProducts.length === 1) {

                currentPage--;

            }

            await loadCategories();
            await loadProducts();

        }

        catch (err) {

            console.error(err);

            showToast("Unable to delete product", "error");

        }

    };

}

window.onclick = function(e){

    if(e.target === deleteModal){

        deleteModal.style.display = "none";
        deleteProductId = null;

    }

};
// ==============================
// Sorting
// ==============================

function sortTable(column){

    if(currentSortBy === column){

        currentSortOrder =
            currentSortOrder === "asc"
            ? "desc"
            : "asc";

    }
    else{

        currentSortBy = column;
        currentSortOrder = "asc";

    }

    currentPage = 1;

    loadProducts();

}