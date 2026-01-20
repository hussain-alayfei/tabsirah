import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os

def train_model():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_FILE = os.path.join(BASE_DIR, 'data_processed', 'data_arabic.pickle')
    MODEL_FILE = os.path.join(BASE_DIR, 'models', 'model_arabic.p')

    print(f"🔄 Loading data from {DATA_FILE}...")
    
    if not os.path.exists(DATA_FILE):
        print("❌ Data file not found! Run processing first.")
        return

    data_dict = pickle.load(open(DATA_FILE, 'rb'))
    data = np.asarray(data_dict['data'])
    labels = np.asarray(data_dict['labels'])
    
    # Verify shape
    print(f"   Samples: {data.shape[0]}")
    print(f"   Features: {data.shape[1]} (Expected 42)")
    
    # Split
    print("✂️ Splitting data (80% Train, 20% Test)...")
    x_train, x_test, y_train, y_test = train_test_split(
        data, labels, test_size=0.2, shuffle=True, stratify=labels
    )
    
    # Train
    print("🧠 Training Random Forest (Using ALL CPUs)...")
    # n_jobs=-1 uses all processors
    model = RandomForestClassifier(n_estimators=200, n_jobs=-1, verbose=1) 
    model.fit(x_train, y_train)
    
    # Evaluate
    print("🧪 Testing model...")
    y_predict = model.predict(x_test)
    acc = accuracy_score(y_test, y_predict)
    
    print(f"\n🏆 Accuracy: {acc*100:.2f}%")
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_predict))
    
    # Save
    f = open(MODEL_FILE, 'wb')
    pickle.dump({'model': model}, f)
    f.close()
    print(f"💾 Model saved to {MODEL_FILE}")

if __name__ == "__main__":
    train_model()
