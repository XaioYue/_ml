from sklearn.ensemble import IsolationForest
import numpy as np
import matplotlib.pyplot as plt

# 建立簡單資料（含異常點）
rng = np.random.RandomState(42)
X = 0.3 * rng.randn(100, 2)
X_outliers = rng.uniform(low=-4, high=4, size=(10, 2))
X = np.r_[X + 2, X - 2, X_outliers]

# 建立並訓練模型
model = IsolationForest(contamination=0.1, random_state=rng)
model.fit(X)

# 預測（1=正常，-1=異常）
pred = model.predict(X)

# 畫圖
colors = np.array(['#377eb8', '#ff7f00'])  # 正常藍，異常橘
plt.scatter(X[:, 0], X[:, 1], s=30, color=colors[(pred + 1) // 2])
plt.title("Isolation Forest: Normal (blue) vs Anomaly (orange)")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.grid(True)
plt.show()
