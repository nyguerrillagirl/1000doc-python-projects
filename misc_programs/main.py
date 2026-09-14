import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Simulation setup ---
n_flips = 100
flips = np.random.choice(['H', 'T'], size=n_flips)

# --- Figure and axes ---
fig, (ax_bar, ax_line) = plt.subplots(1, 2, figsize=(10, 4))
ax_bar.set_ylim(0, 1)
ax_line.set_xlim(0, n_flips)
ax_line.set_ylim(0, 1)

# --- Initialize plots ---
bars = ax_bar.bar(['H', 'T'], [0, 0], color='blue')
(line,) = ax_line.plot([], [], 'b-')
ax_line.axhline(0.5, color='green', linestyle='--', linewidth=0.8)


# --- Animation function ---
def update(frame):
    current_flips = flips[:frame + 1]
    heads = np.sum(current_flips == 'H')
    tails = frame + 1 - heads
    p_heads = heads / (frame + 1)

    # Update bar chart
    bars[0].set_height(heads / (frame + 1))
    bars[1].set_height(tails / (frame + 1))

    # Update line chart
    line.set_data(np.arange(frame + 1), np.cumsum(current_flips == 'H') / np.arange(1, frame + 2))
    return bars, line


# --- Animate ---
ani = FuncAnimation(fig, update, frames=n_flips, interval=100, blit=False)
plt.show()
