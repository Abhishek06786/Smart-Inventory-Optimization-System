import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score


# ---------------------------------
# Load Dataset
# ---------------------------------

df = pd.read_csv("data/sales_data.csv")


# ---------------------------------
# Encode Category
# ---------------------------------

encoder = LabelEncoder()

df["category"] = encoder.fit_transform(df["category"])


# ---------------------------------
# Features & Target
# ---------------------------------

X = df[
    [
        "category",
        "price",
        "stock",
        "daily_sales",
        "lead_time"
    ]
]

y = df["demand"]


# ---------------------------------
# Train Test Split
# ---------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42

)


# ---------------------------------
# Train Model
# ---------------------------------

model = RandomForestRegressor(

    n_estimators=200,

    random_state=42

)

model.fit(X_train, y_train)


# ---------------------------------
# Accuracy
# ---------------------------------

prediction = model.predict(X_test)

score = r2_score(y_test, prediction)

print("\nModel Accuracy :", round(score * 100, 2), "%")


# ---------------------------------
# Save Model
# ---------------------------------

joblib.dump(model, "models/demand_model.pkl")

joblib.dump(encoder, "models/category_encoder.pkl")

print("\nModel Saved Successfully.")