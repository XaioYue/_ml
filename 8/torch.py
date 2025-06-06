import torch

x = torch.tensor(0.0, requires_grad=True)
y = torch.tensor(0.0, requires_grad=True)
z = torch.tensor(0.0, requires_grad=True)

learning_rate = 0.1
num_epochs = 100

for epoch in range(num_epochs):

    loss = x**2 + y**2 + z**2 - 2*x - 4*y - 6*z + 8

    loss.backward()

    with torch.no_grad():
        x -= learning_rate * x.grad
        y -= learning_rate * y.grad
        z -= learning_rate * z.grad

        # 重置梯度
        x.grad.zero_()
        y.grad.zero_()
        z.grad.zero_()

    # 每 10 次輸出一次結果(查看過程)
    if epoch % 10 == 0:
        print(f'Epoch {epoch}: Loss = {loss.item():.4f}, x = {x.item():.4f}, y = {y.item():.4f}, z = {z.item():.4f}')

# 最終結果
print(f'Optimized values: x = {x.item():.4f}, y = {y.item():.4f}, z = {z.item():.4f}')
