import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

print("🛠️ Fixing mental health model files...")

X_dummy = np.array([[7.5, 20, 3, 2], [8.0, 22, 4, 1], [6.0, 19, 2, 5], [9.0, 21, 5, 1], [5.5, 23, 1, 4]])
y_dummy = np.array([0, 0, 1, 0, 1])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_dummy)

model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_scaled, y_dummy)

with open('mental.model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('mental.scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("🎉 Success! mental model files fixed!")