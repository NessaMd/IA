import gymnasium as gym
import numpy as np
import random

env = gym.make('CliffWalking-v0', render_mode="human")

Q = np.zeros((env.observation_space.n, env.action_space.n))

num_episodes = 10000
learning_factor = 0.1
discount_factor = 0.9
epsilon = 0.1

# Q Learning
def q_learning():
    for episode in range(num_episodes):
        state, info = env.reset()
        done = False
        
        print(episode)
        
        while not done:
            # Exploração gananciosa de Epsilon
            if random.uniform(0, 1) > epsilon:
                action = np.argmax(Q[state, :])
            else:
                action = env.action_space.sample()
            
            next_state, reward, done, truncated, info = env.step(action)
            
            max_next_state = np.max(Q[next_state, :])

            # Atualiza tabela Q
            Q[state, action] = Q[state, action] + learning_factor * (reward + discount_factor * max_next_state - Q[state, action])
                                
            state = next_state
            env.render()

# Controle do jogo
def play_game():
    next_state, info = env.reset()
    done = False
    q_learning()

    env.close()

# Execução principal
play_game()
