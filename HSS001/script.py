import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt



input = [] # 나이, 가격, 식사 만족도, 이동거리, 식사시간
output = [] # 스트레스 지수

with open('/content/kaistdb.txt', 'r', encoding = 'cp949') as f:
  next(f)

  for line in f:
    data = line.split('\t')

    data[2] = (int(data[2]) - 18) / (26 - 18)

    data[10] = (int(data[10]) - 0) / (130000 - 0)

    if data[11]=='만족':
      data[11] = 5
    if data[11]=='약간 만족':
      data[11] = 5  
    if data[11]=='약간만족':
      data[11] = 5  
    if data[11]=='불만족':
      data[11]= 1
    if data[11]=='약간 불만족':
      data[11] = 2
    if data[11]=='약간불만족':
      data[11] = 2

    if data[13]=='없음':
      data[13]=0
    if data[13]=='15분이내':
      data[13]=1
    if data[13]=='10분이내':
      data[13]=1
    if data[13]=='30분이내':
      data[13]=2
    if data[13]=='30분이상':
      data[13]=3

    if data[14]=='없음':
      data[14]=0
    if data[14]=='15분이내':
      data[14]=1
    if data[14]=='10분이내':
      data[14]=1
    if data[14]=='30분이내':
      data[14]=2
    if data[14]=='30분이상':
      data[14]=3

    data[6] = int(data[6])

    input_data = [data[2], data[10], data[11], data[13], data[14]]
    output_data = data[6]

    input.append(input_data)
    output.append(output_data)
    


print(input)
input = input[0:3000]
output = output[0:3000]



# Convert input data to TensorFlow tensors
input_array = np.array(input, dtype=np.float32)
input_tensor = tf.convert_to_tensor(input_array, dtype=tf.float32)

output_array = np.array(output, dtype=np.float32)
output_tensor = tf.convert_to_tensor(output_array, dtype=tf.float32)

# Define the deep learning model
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(5, 1)),  # Flatten the input to a 1D tensor
    tf.keras.layers.Dense(128, activation='sigmoid'),  # Add a fully connected layer with ReLU activation
    tf.keras.layers.Dense(64, activation='sigmoid'),
    tf.keras.layers.Dense(32, activation='sigmoid'),  # Add another fully connected layer with ReLU activation
    tf.keras.layers.Dense(1)  # Output layer with a single unit
])

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Train the model
history = model.fit(input_tensor, output_tensor, epochs=20, batch_size=32)  # Replace 'output_tensor' with your desired target/output data

# Make predictions
predictions = model.predict(input_tensor)

# Get training and test loss histories
training_loss = history.history['loss']

# Create count of the number of epochs
epoch_count = range(1, len(training_loss) + 1)

# Visualize loss history
plt.plot(epoch_count, training_loss, 'r--')
plt.legend(['Training Loss'])
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show();

# Convert predictions to a list of real numbers
output_data = predictions.flatten().tolist()
plt.scatter(output[1000:2000], output_data[1000:2000])
plt.show()
