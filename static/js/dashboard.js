// ===================================
// Dashboard Start
// ===================================

window.onload = () => {

    console.log("Dashboard Loaded");

    loadUser();
    loadDashboard();
    loadRecentProducts();
    loadLowStockProducts();

    updateTime();

    setInterval(updateTime, 1000);

    // Auto Refresh Every 30 Seconds
    setInterval(() => {

        loadDashboard();
        loadRecentProducts();
        loadLowStockProducts();

    }, 30000);

};

// ===================================
// Load Logged In User
// ===================================

async function loadUser() {

    try {

        const response = await fetch("/api/user");

        if (response.status === 401) {

            window.location.href = "/";
            return;

        }

        const user = await response.json();

        const userName = document.getElementById("userName");

        if (userName) {

            userName.textContent = user.name;

        }

    }

    catch (err) {

        console.error("User Error :", err);

    }

}

// ===================================
// Last Updated Time
// ===================================

function updateTime() {

    const now = new Date();

    document.getElementById("lastUpdated").textContent =
        now.toLocaleString("en-IN");

}

// ===================================
// Dashboard Cards
// ===================================

async function loadDashboard() {

    try {

        const response = await fetch("/api/dashboard");

        if (response.status === 401) {

            window.location.href = "/";
            return;

        }

        const data = await response.json();

        document.getElementById("totalProducts").textContent =
            data.total_products || 0;

        document.getElementById("lowStock").textContent =
            data.low_stock || 0;

        document.getElementById("outOfStock").textContent =
            data.out_of_stock || 0;

        document.getElementById("inventoryValue").textContent =
            "₹" +
            Math.round(Number(data.inventory_value || 0))
            .toLocaleString("en-IN");

    }

    catch (err) {

        console.error("Dashboard Error :", err);

    }

}
// ===================================
// Recent Products
// ===================================

async function loadRecentProducts() {

    try {

        const response = await fetch("/api/products?page=1&limit=5");

        if (response.status === 401) {

            window.location.href = "/";
            return;

        }

        const data = await response.json();

        const tbody = document.getElementById("recentProducts");

        tbody.innerHTML = "";

        if (!data.products || data.products.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="5">
                        No Products Available
                    </td>
                </tr>
            `;

            return;

        }

        data.products.forEach(product => {

            let stockBadge = "";

            if (product.stock == 0) {

                stockBadge =
                `<span class="badge-danger">
                    Out Of Stock
                </span>`;

            }

            else if (product.stock <= 10) {

                stockBadge =
                `<span class="badge-warning">
                    Low Stock
                </span>`;

            }

            else {

                stockBadge =
                `<span class="badge-success">
                    In Stock
                </span>`;

            }

            tbody.innerHTML += `

                <tr>

                    <td>${product.id}</td>

                    <td>${product.product_name}</td>

                    <td>${product.category}</td>

                    <td>${stockBadge}</td>

                    <td>
                        ₹${Math.round(Number(product.price))
                        .toLocaleString("en-IN")}
                    </td>

                </tr>

            `;

        });

        // Recent Activity Update
        loadRecentActivity(data.products);

    }

    catch (err) {

        console.error("Recent Products Error :", err);

    }

}
// ===================================
// Low Stock Products
// ===================================

async function loadLowStockProducts() {

    try {

        const response = await fetch("/api/low-stock");

        if (response.status === 401) {

            window.location.href = "/";
            return;

        }

        const products = await response.json();

        const tbody = document.getElementById("lowStockList");

        const stockAlert = document.getElementById("stockAlert");

        tbody.innerHTML = "";

        // No Low Stock Products

        if (products.length === 0) {

            tbody.innerHTML = `
                <tr>
                    <td colspan="2">
                        <span class="badge-success">
                            ✔ All Products In Stock
                        </span>
                    </td>
                </tr>
            `;

            if (stockAlert) {

                stockAlert.innerHTML = `
                    <p style="color:#16a34a;font-weight:600;">
                        ✔ Inventory is Healthy
                    </p>
                `;

            }

            return;

        }

        // Stock Alert

        if (stockAlert) {

            stockAlert.innerHTML = `
                <p style="color:#dc2626;font-weight:600;">
                    ⚠ ${products.length} Product(s) Need Restocking
                </p>
            `;

        }

        // Low Stock List

        products.forEach(product => {

            tbody.innerHTML += `

                <tr>

                    <td>${product.product_name}</td>

                    <td>

                        <span class="badge-warning">

                            ${product.stock} Left

                        </span>

                    </td>

                </tr>

            `;

        });

    }

    catch (err) {

        console.error("Low Stock Error :", err);

    }

}
// ===================================
// Recent Activity
// ===================================

function loadRecentActivity(products) {

    const activity = document.getElementById("recentActivity");

    if (!activity) return;

    activity.innerHTML = "";

    if (products.length === 0) {

        activity.innerHTML = `
            <tr>
                <td>No Recent Activity</td>
            </tr>
        `;

        return;

    }

    products.slice(0, 5).forEach(product => {

        activity.innerHTML += `

            <tr>

                <td>

                    <i class="bi bi-box-seam-fill"></i>

                    <strong>${product.product_name}</strong>

                    <br>

                    <small>

                        Category :
                        ${product.category}

                    </small>

                </td>

            </tr>

        `;

    });

}



// ===================================
// Helper Function
// ===================================

function formatCurrency(value) {

    return "₹" + Math.round(Number(value || 0))
        .toLocaleString("en-IN");

}



// ===================================
// Refresh Dashboard
// ===================================

function refreshDashboard() {

    loadDashboard();

    loadRecentProducts();

    loadLowStockProducts();

}



// ===================================
// End
// ===================================

console.log("Smart Inventory Dashboard Ready");