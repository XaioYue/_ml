from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 產生隨機的分群資料，共3群、每群100筆資料
X, y_true = make_blobs(n_samples=300, centers=3, cluster_std=0.60, random_state=0)

# 建立 KMeans 模型，指定3群
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(X)

# 取得模型分群結果
labels = kmeans.labels_
centers = kmeans.cluster_centers_

# 畫出聚類結果與中心點
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75, marker='X')  # 中心點
plt.title("KMeans Clustering")
plt.show()
