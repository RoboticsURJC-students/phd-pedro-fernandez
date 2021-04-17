'''
https://pythonprogramming.net/q-learning-reinforcement-learning-python-tutorial/

'''


import gym
import numpy as np


env = gym.make("MountainCar-v0")
# print(env.action_space.n)
# print(env.action_space.n)
# print(env.observation_space.high)
# print(env.observation_space.low)


env.reset()

LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 1000

SHOW_EVERY = 200
#print(EPISODES//2)

DISCRETE_OS_SIZE = [20, 20]
discrete_os_win_size = (env.observation_space.high -
                        env.observation_space.low)/DISCRETE_OS_SIZE


# Exploration settings
epsilon = 1  # not a constant, qoing to be decayed
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES//2
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)


q_table = np.random.uniform(
    low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))

# print(discrete_os_win_size)
# print(q_table.shape)


def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low) / discrete_os_win_size
    return tuple(discrete_state.astype(int))





for episode in range(EPISODES):

    if episode % SHOW_EVERY == 0:
        print("episode:", episode)
        render = True
    else:
        render = False    

    discrete_state = get_discrete_state(env.reset())
    #print(env.reset())
    #print(discrete_state)   

    done = False
    while not done:

        #action = np.argmax(q_table[discrete_state])
        
        if np.random.random() > epsilon:
            # Get action from Q table
            action = np.argmax(q_table[discrete_state])
        else:
            # Get random action
            action = np.random.randint(0, env.action_space.n)


        new_state, reward, done, _ = env.step(action)

        new_discrete_state = get_discrete_state(new_state)

        #env.render() #si dejo esta funciona la visualziacion
        #if render: #no esta funcionando bien del todo la visualazion
        #    env.render()
    #new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

    # If simulation did not end yet after last step - update Q table
        if not done:

        # Maximum possible Q value in next step (for new state)
            max_future_q = np.max(q_table[new_discrete_state])
        #print("np.max(q_table[new_discrete_state]", np.max(q_table[new_discrete_state]))
            #print("q_table[new_discrete_state]:", q_table[new_discrete_state])
        #print("new_discrete_state:", new_discrete_state)

        # Current Q value (for current state and performed action)
            current_q = q_table[discrete_state + (action,)]
            #print("discrete_state:", discrete_state)
            #print("action:", action)
            #print("discrete_state + (action,):", discrete_state + (action,))
            #print("current_q", current_q)

        # And here's our equation for a new Q value for current state and action
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * \
                (reward + DISCOUNT * max_future_q)
            #print("new_q:", new_q)

        # Update Q table with new Q value
            q_table[discrete_state + (action,)] = new_q

    # Simulation ended (for any reason) - if goal position is achived - update Q value with reward directly
        elif new_state[0] >= env.goal_position:
            print(f"finish in episode {episode}")
            #q_table[discrete_state + (action,)] = reward
            print(f"discrete_state (initial): {discrete_state} and q_table[discrete_state + (action,)]: {q_table[discrete_state + (action,)]}, and new_discrete_state: {new_discrete_state}")

            q_table[discrete_state + (action,)] = 0
            #if episode > 600:
            #    env.render()

        
        discrete_state = new_discrete_state


    # Decaying is being done every episode if episode number is within decaying range
    if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
        epsilon -= epsilon_decay_value


env.close()
