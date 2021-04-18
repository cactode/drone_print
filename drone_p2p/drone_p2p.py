import re
from typing import TextIO
from collections import namedtuple
from drone_p2p.pdrone import PDrone
from mavsdk.mission import MissionItem, MissionPlan, MissionProgress

import logging
log = logging.getLogger(__name__)

State = namedtuple('State', ['x', 'y', 'z', 'speed', 'extrude'])

async def drone_p2p(pdrone : PDrone, printcode : TextIO):
    # initialize simple state machine
    max_speed = await pdrone.drone.get_maximum_speed()
    state = State(x = 0, y = 0, z = 0, speed = max_speed, extrude = 0)

    # parse input file
    mission_items = list()
    for line in printcode:
        # pre-formatting
        instruction = line.strip().lower()
        # ignore null lines
        if not instruction: continue
        # some stuff happens

    mission_plan = MissionPlan(mission_items)
    
    await pdrone.drone.mission.set_return_to_launch_after_mission(True)
    log.info("-- Uploading mission")
    await pdrone.drone.mission.upload_mission(mission_plan)
    log.info("-- Calling drone initialization subroutine")
    await pdrone.initialize()
    log.info("-- Starting print mission")
    

    ...