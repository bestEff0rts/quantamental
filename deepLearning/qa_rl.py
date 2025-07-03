#double deep q-network agent rl
import numpy as np
import matplotlib.pyplot as plt
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam


class DDQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size  = state_size
        self.action_size = action_size
        self.memory  = []      # For experience replay
        self.gamma   = 0.9     # Discount factor
        self.epsilon = 0.01   # Exploration rate
        self.epsilon_min   = 0.001 # Minimum value of epsilon
        self.epsilon_decay = 0.9   # Gradually reducing the exploration factor
        self.model = self.build_model()
        self.target_model = self.build_model()

    def build_model(self):
      model = Sequential()
      model.add(Dense(64, input_shape=(self.state_size,), activation='relu'))  
      model.add(Dense(64, activation='relu'))
      model.add(Dense(self.action_size, activation='linear'))
      model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
      return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        act_values = self.model.predict(state)
        
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        indices = np.random.choice(len(self.memory), batch_size, replace=False)
        minibatch = [self.memory[idx] for idx in indices]
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                action_next = np.argmax(self.model.predict(next_state)[0])
                target = reward + self.gamma * self.target_model.predict(next_state)[0][action_next]
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

# Generate the Sinewave time series
time_steps = 100 # Length of the series
data = np.sin(np.arange(0, 10 * np.pi, 10 * np.pi / time_steps))        
data

# Preprocess the data
window_size = 3
X = []
Y = []
for i in range(len(data) - window_size):
    X.append(data[i:i + window_size])
    Y.append(data[i + window_size])
X = np.array(X)
Y = np.array(Y)

# Set up the DDQN agent
state_size = window_size
action_size = 1
agent = DDQNAgent(state_size, action_size)

# Train the DDQN agent
batch_size = 64
epochs = 10
update_target_freq = 10
for epoch in range(epochs):
    for i in range(len(X) - 1):
        state = np.reshape(X[i], [1, state_size])
        action = agent.act(state)
        next_state = np.reshape(X[i + 1], [1, state_size])
        reward = Y[i]
        done = False
        agent.remember(state, action, reward, next_state, done)

    if len(agent.memory) > batch_size:
        agent.replay(batch_size)

    if epoch % update_target_freq == 0:
        agent.update_target_model()

# Test the trained model
test_data = np.sin(np.arange(0, 12 * np.pi, 10 * np.pi / 5000))
test_X = []

for i in range(len(test_data) - window_size):
    test_X.append(test_data[i:i + window_size])
test_X = np.array(test_X)
predictions = []

for i in range(len(test_X)):
    state = np.reshape(test_X[i], [1, state_size])
    prediction = agent.model.predict(state)[0][0]
    predictions.append(prediction)

# Plot the results
plt.plot(np.arange(len(test_data)), test_data, label = 'Actual')

