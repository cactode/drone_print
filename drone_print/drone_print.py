import asyncio
from typing import TextIO, List
from collections import namedtuple
from drone_print.pdrone import PDrone
from mavsdk.mission import MissionItem, MissionPlan

import logging

log = logging.getLogger(__name__)
NAN = float("nan")


async def drone_print(pdrone: PDrone, printcode: TextIO):
    """
    Starts drone 3D print.

    Args:
        pdrone: 3D printing quadcopter. At the time of function invocation,
            the drone must be disarmed and landed.
        printcode: Text file (compliant with provided spec)
            that describes the path to be taken by the quadcopter.
    """
    # parse input file
    mission_items = list()
    extrude_state = [False]
    for line in printcode:
        # ignore comments
        if ";" in line:
            continue
        # pre-formatting
        instructions = line.strip().lower().split()
        # ignore null lines
        if not instructions:
            continue
        # convert to floats
        values = [float(instruction) for instruction in instructions]
        # append parsed state
        mission_items.append(
            MissionItem(
                *values[:4], True, NAN, NAN, MissionItem.CameraAction.NONE, NAN, NAN
            )
        )
        extrude_state.append(bool(values[4]))
        log.info(
            f"Added waypoint X={values[0]}, Y={values[1]}, Z={values[2]}, SPD={values[3]}, EXT={values[4]}"
        )
    extrude_state[-1] = False  # ensure extruder is off when path ends
    mission_plan = MissionPlan(mission_items)
    log.info("Clearing past missions")
    await pdrone.drone.mission.clear_mission()
    await pdrone.drone.mission.set_return_to_launch_after_mission(True)
    log.info("Uploading mission")
    await pdrone.drone.mission.upload_mission(mission_plan)
    log.info("Arming")
    await pdrone.drone.action.arm()
    log.info("Taking Off")
    await pdrone.drone.action.takeoff()
    log.info("Starting print mission")
    await pdrone.drone.mission.start_mission()
    set_extruder_task = asyncio.create_task(set_extruder(pdrone, extrude_state))
    running_tasks = [set_extruder_task]
    await asyncio.create_task(observe_is_in_air(pdrone, running_tasks))
    log.info("Drone landed, mission completed")


async def set_extruder(pdrone: PDrone, extrude_state: List[bool]):
    """Task to ensure that the extruder is turned on and off as needed during the mission"""
    extruder_state = False
    async for mission_progress in pdrone.drone.mission.mission_progress():
        log.info(
            f"Executing instruction {mission_progress.current}/{mission_progress.total}"
        )
        if extruder_state != extrude_state[mission_progress.current]:
            extruder_state = extrude_state[mission_progress.current]
            await pdrone.extrude(extruder_state)


async def observe_is_in_air(pdrone: PDrone, running_tasks):
    """Monitors whether the drone is flying or not and
    returns after landing"""
    # taken from:
    # https://github.com/mavlink/MAVSDK-Python/blob/main/examples/mission.py'
    was_in_air = False

    async for is_in_air in pdrone.drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return