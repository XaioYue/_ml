import torch
import matplotlib.pyplot as plt

x = torch.tensor([0, 1, 2, 3, 4], dtype=torch.float32)
y = torch.tensor([1.9, 3.1, 3.9, 5.0, 6.2], dtype=torch.float32)

a0 = torch.tensor(0.0, requires_grad=True)
a1 = torch.tensor(0.0, requires_grad=True)

learning_rate = 0.01
num_epochs = 3000

for epoch in range(num_epochs):

    y_pred = a0 + a1 * x

    
    loss = torch.mean((y - y_pred) ** 2)

    
    loss.backward()

    
    with torch.no_grad():
        a0 -= learning_rate * a0.grad
        a1 -= learning_rate * a1.grad

        a0.grad.zero_()
        a1.grad.zero_()

    
    if epoch % 500 == 0:
        print(f'Epoch {epoch}: Loss = {loss.item():.4f}, a0 = {a0.item():.4f}, a1 = {a1.item():.4f}')


print(f'Final Parameters: a0 = {a0.item():.4f}, a1 = {a1.item():.4f}')

y_predicted = a0.item() + a1.item() * x.numpy()
plt.plot(x.numpy(), y.numpy(), 'ro', label='Original data')
plt.plot(x.numpy(), y_predicted, label='Fitted line')
plt.legend()
plt.show()
