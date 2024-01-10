from typing import Dict, List, Tuple, Union


Coordinates = List[int]
Command = Dict[str, Union[str, int]]
CommandsList = List[Command]
ExecutionResult = Dict[str, Union[float, int, int]]
Trajectory = List[Union[List[int], int, str]]
