import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 產生模擬資料
np.random.seed(0)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)  # y = 4 + 3x + 一點噪音

# 建立線性回歸模型
model = LinearRegression()
model.fit(X, y)

# 模型參數
print(f"截距 (intercept): {model.intercept_[0]:.2f}")
print(f"係數 (slope): {model.coef_[0][0]:.2f}")

# 預測
X_new = np.array([[0], [2]])
y_pred = model.predict(X_new)

# 畫圖
plt.scatter(X, y, color='blue', label='訓練資料')
plt.plot(X_new, y_pred, color='red', linewidth=2, label='預測線')
plt.xlabel("X")
plt.ylabel("y")
plt.title("線性回歸示範")
plt.legend()
plt.show()
