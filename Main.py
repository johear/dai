import Performances
from ControlInput import ControlInput
from ControlOutput import ControlOutput 
from ScriptedControlModule import ScriptedControlModule
from AiControlModule import AiControlModule
from SafetyControlModule import SafetyControlModule
from ssh import ssh
from DaiBody import DaiBody
from Simulation import Simulation
import sys
import time
import os 
#import ptvsd

print("Setting up controllers")

#ptvsd.enable_attach('172a62dc-4551-43d9-9aaa-71af1d5def35')
#print("Waiting for debugger")
#ptvsd.wait_for_attach()

train_controller = True
training_runs = 10

performance = Performances.CourtyardPerformance
# control_module = ScriptedControlModule(train_controller)
control_module = AiControlModule(train_controller)
safety_module = SafetyControlModule(performance)


def main():
    simulation = Simulation()
    
    print("Setting up controllers")
    dai_body = DaiBody(performance, safety_module, simulation)

    print("Intializing system")
    dai_body.initialize()

    total_runs = training_runs if train_controller else 0

    for run in range(total_runs) :
        print("Run", run, "of", total_runs)
        dai_body.reset()
        # initialize control module with the current body observtion
        control_input = dai_body.observe_control_inputs()
        control_module.initialize_run(run, control_input)

        start_time = time.time()
        last_time = start_time

        print("Running controllers")
        key = 0
        try:
            while ((time.time() < start_time + performance.duration) or key == chr(27)):
                timer_start = time.time()
                elapsed_time = time.time() - start_time
                # get the current recommended action based on the current body state)
                control_output = control_module.get_action(elapsed_time)
                timer_lap1 = time.time()
                print("get Control output duration: ", timer_lap1-timer_start)
                # sanitize the actions for safety
                safe_control_output = safety_module.sanitize_output(control_input, control_output)
                timer_lap2 = time.time()
                print("safe Control output duration: ", timer_lap2-timer_lap1)
				# apply the new action to the body
                dai_body.apply_control_outputs(safe_control_output, time.time() - last_time)
                last_time = time.time()
                timer_lap3 = time.time()
                print("apply Control output duration: ", timer_lap3-timer_lap2)
                # wait for action to effect body
                # time.sleep(1)
                
                # observe the resulting body state and reward status
                control_input = dai_body.observe_control_inputs()
                timer_lap4 = time.time()
                print("observe Control input duration: ", timer_lap4-timer_lap3)
                status = dai_body.get_status(elapsed_time)
                timer_lap5 = time.time()
                print("get status duration: ", timer_lap5-timer_lap4)
                # Update control module with results
                control_module.update_run_results(run, elapsed_time, control_input, safe_control_output, status[0] + safety_module.get_positional_safety_punishment(), status[1])
                timer_lap6 = time.time()
                print("update Control module duration: ", timer_lap6-timer_lap5)
			   # key = sys.stdin.read(1)[0]
                timer_end = time.time()
                print("Performance loop duration: ", timer_end-timer_start)
                simulation.stepSimulation()
                if status[1]:
                    break
        except Exception as e: 
            print("Crashed:", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        control_module.finalize_run(run)
        if key == chr(27):
            break

    print("Finalizing system")
    dai_body.finalize()
    simulation.disconnect()
    print("Finished")
    
    # try:           
        # connection1 = ssh("192.168.1.101", "pi", "slave2ai")
        # connection1.sendCommand("sudo halt > /dev/null 2>&1 &")
        # print("101 off")
    # except:
        # pass
    # try:
        # connection2 = ssh("192.168.1.102", "pi", "slave2ai")
        # connection2.sendCommand("sudo halt > /dev/null 2>&1 &")
        # print("102 off")
    # except:
        # pass
    # try:
        # connection3 = ssh("192.168.1.103", "pi", "slave2ai")
        # connection3.sendCommand("sudo halt > /dev/null 2>&1 &")
        # print("103 off")
    # except:
        # pass
    # try:
        # connection4 = ssh("192.168.1.104", "pi", "slave2ai")
        # connection4.sendCommand("sudo halt > /dev/null 2>&1 &")
        # print("104 off")
    # except:
        # pass
    # try:
        # connection5 = ssh("192.168.1.105", "pi", "slave2ai")
        # connection5.sendCommand("sudo halt > /dev/null 2>&1 &")
        # print("105 off")
    # except:
        # pass
    # try:
        # connection6 = ssh("192.168.1.106", "pi", "slave2ai")
        # connection6.sendCommand("sudo halt > /dev/null 2>&1 &")
        # print("106 off")
    # except:
        # pass
    # try:
        # print("Goodbye world")
        # connection7 = ssh("192.168.1.100", "pi", "slave2ai")
        # connection7.sendCommand("sudo halt > /dev/null 2>&1 &")
    # except:
        # pass

if __name__ == '__main__':
    main()