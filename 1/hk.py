import random

def f(x: int, y: int, z: int) -> int:
    return x**2 + y**2 + z**2 - 2*x - 4*y - 6*z + 8

x, y, z = 1, 1, 1
lr = 0.0001
fail = 0
while fail < 100000:
    lr_x = random.uniform(-lr, lr)
    lr_y = random.uniform(-lr, lr)
    lr_z = random.uniform(-lr, lr)
    if f(x + lr_x, y + lr_y, z + lr_z) < f(x, y, z):
        x, y, z = x + lr_x, y + lr_y, z + lr_z
    else:
        fail += 1

print("x:", x, "y:", y, "z:", z)