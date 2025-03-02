import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Step 1: Define the sensory inputs and build the network using Functional API
smell_cof = 0.7
taste_cof = 0.7
sight_cof = 0.7
sound_cof = 0.7
senses = ["Coffee Smell", "Cake Taste", "Friend Sight", "Music Hear"]
inputs_data = np.array([
    [1, 1, 1, 1],  # Full café memory
    [1, 0, 0, 0],  # Coffee only
    [0, 1, 0, 0],  # Pie only
    [0, 0, 1, 0],  # Friend only
    [0, 0, 0, 1],  # Song only
    [0, 0, 0, 0]   # No input
])

outputs_data = np.array([
    [1, 1, 1, 1],      # Full recall
    [1, smell_cof, smell_cof, smell_cof], # Coffee triggers partial recall
    [taste_cof, 1, taste_cof, taste_cof], # Pie triggers partial recall
    [sight_cof, sight_cof, 1, sight_cof], # Friend triggers partial recall
    [sound_cof, sound_cof, sound_cof, 1], # Song triggers partial recall
    [0, 0, 0, 0]        # No input, no recall
])

# Define the model with Functional API and two hidden layers
inputs = layers.Input(shape=(4,), name='input_layer')
hidden1 = layers.Dense(8, activation='relu', name='hidden1')(inputs)    # First hidden layer: 8 nodes
hidden2 = layers.Dense(6, activation='relu', name='hidden2')(hidden1)   # Second hidden layer: 6 nodes
outputs = layers.Dense(4, activation='sigmoid', name='output')(hidden2)

# Create the full model
model = models.Model(inputs=inputs, outputs=outputs)

# Compile with MSE loss and a lower learning rate
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
              loss='mean_squared_error', 
              metrics=['mae'])  # Mean Absolute Error as a metric

# Train with more epochs
model.fit(inputs_data, outputs_data, epochs=1000, verbose=0)

# Define sub-models for both hidden layers
hidden1_layer_model = models.Model(inputs=inputs, outputs=hidden1)
hidden2_layer_model = models.Model(inputs=inputs, outputs=hidden2)
print("Training complete. Network has learned the memory patterns.")

# Step 2: Create interactive GUI
root = tk.Tk()
root.title("Neural Network Memory Recall")
root.geometry("1200x800")  # Wider window to fit extra layer

# Function to get activations (output and both hidden layers)
def get_activations(input_data):
    hidden1_activations = hidden1_layer_model.predict(input_data, verbose=0)
    hidden2_activations = hidden2_layer_model.predict(input_data, verbose=0)
    output_activations = model.predict(input_data, verbose=0)
    return hidden1_activations[0], hidden2_activations[0], output_activations[0]

# Function to update the neural network plot
def update_plot(*args):
    # Get slider values
    input_data = np.array([[slider_vars[i].get() for i in range(4)]])  # Shape: (1, 4)

    # Get activations
    hidden1_vals, hidden2_vals, output_vals = get_activations(input_data)

    # Clear previous plot
    ax.clear()

    # Define layer positions
    input_x, hidden1_x, hidden2_x, output_x = 0, 1, 2, 3  # X positions for 4 layers
    layer_spacing = 0.2  # Vertical spacing between nodes

    # Input layer (4 nodes)
    for i in range(4):
        intensity = input_data[0][i]
        ax.scatter(input_x, i * layer_spacing, s=300, c='orange', alpha=intensity, edgecolors='black')
        ax.text(input_x - 0.3, i * layer_spacing, senses[i], ha='right', va='center')

    # Hidden layer 1 (8 nodes)
    for i in range(8):
        intensity = hidden1_vals[i] / max(hidden1_vals) if max(hidden1_vals) > 0 else 0  # Normalize
        ax.scatter(hidden1_x, i * layer_spacing * 0.5, s=300, c='blue', alpha=intensity, edgecolors='black')
        ax.text(hidden1_x + 0.2, i * layer_spacing * 0.5, f"{hidden1_vals[i]:.2f}", va='center')

    # Hidden layer 2 (6 nodes)
    for i in range(6):
        intensity = hidden2_vals[i] / max(hidden2_vals) if max(hidden2_vals) > 0 else 0  # Normalize
        ax.scatter(hidden2_x, i * layer_spacing * 0.6, s=300, c='purple', alpha=intensity, edgecolors='black')
        ax.text(hidden2_x + 0.2, i * layer_spacing * 0.6, f"{hidden2_vals[i]:.2f}", va='center')

    # Output layer (4 nodes)
    for i in range(4):
        intensity = output_vals[i]
        ax.scatter(output_x, i * layer_spacing, s=300, c='green', alpha=intensity, edgecolors='black')
        ax.text(output_x + 0.3, i * layer_spacing, f"{output_vals[i]:.2f}", va='center')
        ax.text(output_x + 0.6, i * layer_spacing, senses[i], ha='left', va='center')

    # Draw connections (simplified)
    for i in range(4):
        for j in range(8):
            ax.plot([input_x, hidden1_x], [i * layer_spacing, j * layer_spacing * 0.5], 'k-', alpha=0.1)
    for i in range(8):
        for j in range(6):
            ax.plot([hidden1_x, hidden2_x], [i * layer_spacing * 0.5, j * layer_spacing * 0.6], 'k-', alpha=0.1)
    for i in range(6):
        for j in range(4):
            ax.plot([hidden2_x, output_x], [i * layer_spacing * 0.6, j * layer_spacing], 'k-', alpha=0.1)

    # Set up plot
    ax.set_xlim(-0.5, 3.8)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title("Neural Network Recall (Adjust Sliders)")
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["Input", "Hidden 1", "Hidden 2", "Output"])
    ax.set_yticks([])
    canvas.draw()

# Step 3: Set up GUI layout
# Sliders frame (at the top)
slider_frame = tk.Frame(root)
slider_frame.pack(side=tk.TOP, pady=20)

# Create sliders for each input
slider_vars = [tk.DoubleVar(value=0.0) for _ in senses]  # Initial values at 0.0
for i, sense in enumerate(senses):
    tk.Label(slider_frame, text=sense, font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    slider = tk.Scale(slider_frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,
                      variable=slider_vars[i], length=150, command=update_plot)
    slider.pack(side=tk.LEFT, padx=5)

# Create a frame for the plot (below sliders)
plot_frame = tk.Frame(root)
plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Matplotlib figure
fig, ax = plt.subplots(figsize=(12, 5))  # Wider figure for extra layer
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Initial plot (all inputs at 0.0)
update_plot()

# Start the GUI loop
root.mainloop()
