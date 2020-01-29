from ControlInput import ControlInput
from ControlOutput import ControlOutput


class ScriptedControlModule():
    
    def __init__(self, train: bool): 
        print("Init")

    def initialize_run(self, episode: int, control_input: ControlInput):       
        print("Initializing run")

    def get_action(self, elpased_time: float) -> ControlOutput:
        outputState = ControlOutput()
        outputState.Wheel1aTargetSpeed = 0.0
        outputState.Wheel2bTargetSpeed = 0.0
        outputState.Wheel3aTargetSpeed = 0.0
        return outputState

    def update_run_results(self, run: int, elapsed_time:float, control_state: ControlInput, control_action: ControlOutput, reward: float, terminated: bool):
        print("Updating run results")

    def finalize_run(self, run: int):       
        print("Finalizing run")






