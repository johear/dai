import numpy as np
import random
import argparse
from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
import tensorflow as tf
import json

from ReplayBuffer import ReplayBuffer
from ActorNetwork import ActorNetwork
from CriticNetwork import CriticNetwork
from OU import OU
import timeit

from ControlInput import ControlInput
from ControlOutput import ControlOutput
import time #added for code timers

OU = OU()       #Ornstein-Uhlenbeck Process


class AiControlModule():
    
    BUFFER_SIZE = 100000
    BATCH_SIZE = 1200
    GAMMA = 0.99
    TAU = 0.001     #Target Network HyperParameters
    LRA = 0.0001    #Learning rate for Actor
    LRC = 0.001     #Lerning rate for Critic

    np.random.seed(1337)

    EXPLORE = 100000.
    epsilon = 1 # used for reducing exploration rate over time

    current_state = None
    reward = 0

    def __init__(self, train: bool): 
        self._train_indicator = train

        #Tensorflow GPU optimization
        print("Starting TensorFlow")
        config = tf.ConfigProto()
        #config.gpu_options.allow_growth = True
        print("Get TensorFlow Session")
        sess = tf.Session(config=config)
        from keras import backend as K
        print("Starting session")
        K.set_session(sess) 

        print("Initializing networks")
        self.actor = ActorNetwork(sess, ControlInput.state_dim, ControlOutput.action_dim, self.BATCH_SIZE, self.TAU, self.LRA)
        self.critic = CriticNetwork(sess, ControlInput.state_dim, ControlOutput.action_dim, self.BATCH_SIZE, self.TAU, self.LRC)
        self.buff = ReplayBuffer(self.BUFFER_SIZE)    #Create replay buffer

        #Now load the weight
        print("Now we load the weight")
        try:
            self.actor.model.load_weights("actormodel.h5")
            self.critic.model.load_weights("criticmodel.h5")
            self.actor.target_model.load_weights("actormodel.h5")
            self.critic.target_model.load_weights("criticmodel.h5")
            print("Weight load successfully")
        except:
            print("Cannot find the weight")
 

    def initialize_run(self, run: int, control_input: ControlInput):       
        self.current_state = np.hstack(control_input.get_states_array())
        self.total_reward = 0.0


    def get_action(self, elapsed_time: float) -> ControlOutput:

        action = np.zeros([1, ControlOutput.action_dim])
        action_noise = np.zeros([1, ControlOutput.action_dim])
            
        original_action = self.actor.model.predict(self.current_state.reshape(1, self.current_state.shape[0]))

        # Gradually decrease epsilon from 1 to 0 over EXPLORE iterations to reduce exploration rate over time
        self.epsilon -= 1.0 / self.EXPLORE

        # OU function call
        # mu represents the mean value should be 0 as both wheels and sliders vary -1...1
        # theta was defined to have any average speed of reversal to mean
        # sigma volatility is low for wheels (to discourarge sudden acceleration) but high for sliders to encourage exploration
        action_noise[0][0] = self._train_indicator * max(self.epsilon, 0) * OU.function(original_action[0][0],  0.0 , 0.50, 0.30)
        action_noise[0][1] = self._train_indicator * max(self.epsilon, 0) * OU.function(original_action[0][1],  0.0 , 0.50, 0.30)
        action_noise[0][2] = self._train_indicator * max(self.epsilon, 0) * OU.function(original_action[0][2],  0.0 , 0.50, 0.30)
        action_noise[0][3] = self._train_indicator * max(self.epsilon, 0) * OU.function(original_action[0][3],  0.0 , 0.50, 0.30)
        action_noise[0][4] = self._train_indicator * max(self.epsilon, 0) * OU.function(original_action[0][4],  0.0 , 0.50, 0.30)
        action_noise[0][5] = self._train_indicator * max(self.epsilon, 0) * OU.function(original_action[0][5],  0.0 , 0.50, 0.30)
        action_noise[0][6] = self._train_indicator * max(self.epsilon, 0) * OU.function(original_action[0][6],  0.0 , 0.50, 0.80)
        action_noise[0][7] = self._train_indicator * max(self.epsilon, 0) * OU.function(original_action[0][7],  0.0 , 0.50, 0.80)
        action_noise[0][8] = self._train_indicator * max(self.epsilon, 0) * OU.function(original_action[0][8],  0.0 , 0.50, 0.80)

        action[0][0] = original_action[0][0] + action_noise[0][0]
        action[0][1] = original_action[0][1] + action_noise[0][1]
        action[0][2] = original_action[0][2] + action_noise[0][2]
        action[0][3] = original_action[0][3] + action_noise[0][3]
        action[0][4] = original_action[0][4] + action_noise[0][4]
        action[0][5] = original_action[0][5] + action_noise[0][5]
        action[0][6] = original_action[0][6] + action_noise[0][6]
        action[0][7] = original_action[0][7] + action_noise[0][7]
        action[0][8] = original_action[0][8] + action_noise[0][8]

        output = ControlOutput()
        output.set_actions_array(action)
        return output

    def update_run_results(self, run: int, elapsed_time:float, new_control_state: ControlInput, control_action: ControlOutput, reward: float, terminated: bool):    
        #print("updating run results...")
        action = control_action.get_actions_array()
        new_state = np.hstack(new_control_state.get_states_array())
        # previous observation, actions, reward, current observation and whether terminated to buffer
        self.buff.add(self.current_state, action[0], reward, new_state, terminated)      #Add replay buffer
        # set the current state to the new state
        self.current_state = new_state
        # get a random batch of experiences from the buffer, this is a fairly small number
        batch = self.buff.getBatch(self.BATCH_SIZE)
        states = np.asarray([e[0] for e in batch])
        actions = np.asarray([e[1] for e in batch])
        rewards = np.asarray([e[2] for e in batch])
        new_states = np.asarray([e[3] for e in batch])
        dones = np.asarray([e[4] for e in batch])
        # actions from the batch again, this just seeoms to be a cheap trick to initialize array
        corrected_rewards = np.asarray([e[1] for e in batch]) 

        # get the q values (or rewards) for the batch from the target critic network
        target_q_values = self.critic.target_model.predict([new_states, self.actor.target_model.predict(new_states)])  
        for k in range(len(batch)):
            if dones[k]:
                corrected_rewards[k] = rewards[k]
            else:
                # update the corrected_rewards array with the predicted rewards
                # not clear to me why we're adding rewards here rather than some kind of ponderation
                corrected_rewards[k] = rewards[k] + self.GAMMA*target_q_values[k]
        loss = 0        
        if (self._train_indicator):
            # train the actual critic model using the updated rewards from the critic target
            # returns the loss = the global error of the critic training, ideally this should
            # be as small as possible
            loss += self.critic.model.train_on_batch([states,actions], corrected_rewards)
 
            # ask the current actor method for the actions he'd predict for the states 
            action_for_grad = self.actor.model.predict(states)
 
            # get the gradients from the critic 
            grads = self.critic.gradients(states, action_for_grad)
 
            # train the actor using the critic gradients
            self.actor.train(states, grads)
        
             
            # train the actor and critic target networks
            self.actor.target_train()
           
            self.critic.target_train()
            

        # update the total reward, this isn't actually used for anything per se
        self.total_reward += reward
        
        #print("Run", run, "Action", action, "Reward", reward, "Loss", loss)

        
    def finalize_run(self, run: int):       
        if np.mod(run, 3) == 0 :
            if (self._train_indicator):
                print("Now we save model")
                self.actor.model.save_weights("actormodel.h5", overwrite=True)
                with open("actormodel.json", "w") as outfile:
                    json.dump(self.actor.model.to_json(), outfile)

                self.critic.model.save_weights("criticmodel.h5", overwrite=True)
                with open("criticmodel.json", "w") as outfile:
                    json.dump(self.critic.model.to_json(), outfile)

        print("TOTAL REWARD @ " + str(run) +"-th Run  : Reward " + str(self.total_reward))
        print("")