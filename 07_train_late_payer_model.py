import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# 1. Load Data from your SQL View
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Alfagamma1991',
    'database': 'edz_operations_db'
}

def train_model():
    try:
        conn = mysql.connector.connect(**config)
        # We pull everything from the view we just created
        query = "SELECT * FROM view_customer_analytics"
        df = pd.read_sql(query, conn)
        conn.close()

        print(f"Loaded {len(df)} records for AI training.")

        # 2. Preprocessing
        # Convert categorical data (Neighborhood, Connection Type) into numbers
        df_encoded = pd.get_dummies(df, columns=['neighborhood_name', 'connection_type'])

        # Features (X): What the AI looks at to make a guess
        # We drop IDs, payment_status (text), and our target
        X = df_encoded.drop(['customer_id', 'neighborhood_id', 'payment_status', 'is_late_payer'], axis=1)
        
        # Target (y): What we want to predict (1 = Late Payer, 0 = Paid)
        y = df_encoded['is_late_payer']

        # 3. Split data (80% for training, 20% for testing to see if it's accurate)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 4. Build the Random Forest
        print("Training Random Forest model...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # 5. Evaluate
        y_pred = model.predict(X_test)
        print("\n--- Model Performance Report ---")
        print(classification_report(y_test, y_pred))

        # 6. Save the model for later use in Power BI or Apps
        joblib.dump(model, 'edz_late_payer_model.pkl')
        print("Model saved as 'edz_late_payer_model.pkl'")

        # 7. Show Feature Importance
        importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
        print("\n--- What factors matter most to the AI? ---")
        print(importances.head(5))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    train_model()