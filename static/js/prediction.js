// ===================================
// Prediction Form
// ===================================

const form = document.getElementById("predictionForm");

if (form) {

    form.addEventListener("submit", async function (e) {

        e.preventDefault();

        const button = form.querySelector("button");

        button.disabled = true;
        button.innerText = "Predicting...";

        const predictionData = {

            product_name: document.getElementById("product").value.trim(),

            category: document.getElementById("category").value.trim(),

            price: parseFloat(document.getElementById("price").value),

            stock: parseInt(document.getElementById("stock").value),

            daily_sales: parseInt(document.getElementById("sales").value),

            lead_time: parseInt(document.getElementById("lead").value)

        };

        try {

            const response = await fetch("/api/predict", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(predictionData)

            });

            if (!response.ok) {

                throw new Error("Prediction API Failed");

            }

            const data = await response.json();

            // ===========================
            // Predicted Demand
            // ===========================

            document.getElementById("predictedDemand").innerText =
                `${data.predicted_demand} Units`;

            // ===========================
            // Recommended Stock
            // ===========================

            document.getElementById("recommendedStock").innerText =
                `${data.recommended_stock} Units`;

            // ===========================
            // Restock Status
            // ===========================

            const restock =
                document.getElementById("restockStatus");

            restock.className = "";

            if (data.restock_status === "Required") {

                restock.innerHTML =
                    "⚠️ Required";

                restock.classList.add("danger");

            }

            else {

                restock.innerHTML =
                    "✅ Not Required";

                restock.classList.add("good");

            }

            // ===========================
            // Demand Level
            // ===========================

            const level =
                document.getElementById("demandLevel");

            level.className = "";

            if (data.demand_level === "High") {

                level.innerHTML =
                    "🔴 High";

                level.classList.add("danger");

            }

            else if (data.demand_level === "Medium") {

                level.innerHTML =
                    "🟠 Medium";

                level.classList.add("warning");

            }

            else {

                level.innerHTML =
                    "🟢 Low";

                level.classList.add("good");

            }

        }

        catch (error) {

            console.error(error);

            alert("Prediction Failed!");

        }

        finally {

            button.disabled = false;
            button.innerText = "Predict Demand";

        }

    });

}