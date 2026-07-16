window.onload = async function () {

    try {

        const response = await fetch("/api/analytics");

        if (!response.ok) {
            throw new Error("Failed to fetch analytics data");
        }

        const data = await response.json();

        console.log("Analytics:", data);

        // ==========================
        // Dashboard Cards
        // ==========================

        document.getElementById("totalProducts").textContent =
            data.dashboard.total_products ?? 0;

        document.getElementById("lowStock").textContent =
            data.dashboard.low_stock ?? 0;

        document.getElementById("outOfStock").textContent =
            data.dashboard.out_of_stock ?? 0;

        document.getElementById("inventoryValue").textContent =
            "₹" + Number(data.dashboard.inventory_value || 0).toLocaleString(
                "en-IN",
                {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                }
            );

        // ==========================
        // Common Data
        // ==========================

        const categoryLabels =
            data.category_data.map(item => item.category);

        const categoryCounts =
            data.category_data.map(item => item.total_products);

        const stockValues =
            data.stock_data.map(item => item.total_stock);

        const inventoryValues =
            data.inventory_value_data.map(item => item.inventory_value);

        const colors = [
            "#36A2EB",
            "#FF6384",
            "#FF9F40",
            "#FFCD56",
            "#4BC0C0",
            "#9966FF",
            "#C9CBCF"
        ];

        // ==========================
        // Products by Category
        // ==========================

        new Chart(document.getElementById("categoryChart"), {

            type: "bar",

            data: {

                labels: categoryLabels,

                datasets: [

                    {
                        label: "Products",
                        data: categoryCounts,
                        backgroundColor: "#8EC9F3",
                        borderColor: "#1E88E5",
                        borderWidth: 1
                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: true
                    }

                },

                scales: {

                    y: {

                        beginAtZero: true

                    }

                }

            }

        });

        // ==========================
        // Stock by Category
        // ==========================

        new Chart(document.getElementById("stockChart"), {

            type: "pie",

            data: {

                labels: categoryLabels,

                datasets: [

                    {
                        data: stockValues,
                        backgroundColor: colors
                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "top"

                    }

                }

            }

        });

        // ==========================
        // Inventory Value
        // ==========================

        new Chart(document.getElementById("valueChart"), {

            type: "doughnut",

            data: {

                labels: categoryLabels,

                datasets: [

                    {
                        data: inventoryValues,
                        backgroundColor: colors
                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "top"

                    },

                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                return (
                                    context.label +
                                    " : ₹" +
                                    Number(context.raw).toLocaleString("en-IN")
                                );

                            }

                        }

                    }

                }

            }

        });

    }

    catch (error) {

        console.error("Analytics Error:", error);

    }

};