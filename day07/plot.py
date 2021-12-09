import matplotlib.pyplot as plt

y = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
x = list(range(len(y)))

fig, ax = plt.subplots()
ax.bar(x, y)
ax.set_xticks(x, y)

ax.hlines(y=5, xmin=0, xmax=x[-1], linewidth=2, color='r')

plt.show()
