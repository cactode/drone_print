import abc
import logging
import asyncio
from mavsdk.system import System

log = logging.getLogger(__name__)


class PDrone(abc.ABC):
    """
    Abstract Base Class that specifies the functions required for a 3D printing drone.
    3D printing drones should subclass this ABC. 
    """

    @property
    @abc.abstractmethod
    def drone(self) -> System:
        """
        A MAVSDK system object that corresponds to the drone being controlled.
        """
        ...

    @abc.abstractmethod
    async def initialize(self):
        """
        Performs all necessary steps to prepare the drone for printing. 
        """
        ...

    @abc.abstractmethod
    async def deinitialize(self):
        """
        Returns the drone to a safe / desired state.
        """
        ...

    @abc.abstractmethod
    async def extrude(self, state: bool) -> bool:
        """
        Sets the state of the extruder on the drone.

        Args:
            state (bool): Whether the extruder should be activately extruding.
        """
        ...


class GenericPDrone(PDrone):
    def __init__(self):
        # generic initialization code taken from:
        # https://github.com/mavlink/MAVSDK-Python/blob/main/examples/mission.py
        drone = System()
        await drone.connect(system_address="udp://:14540")

        log.info("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                log.info(f"Drone discovered with UUID: {state.uuid}")
                break

        self._drone = drone

    @property
    def drone(self):
        return self.drone

    async def initialize(self):
        log.info("-- Arming")
        await drone.action.arm()

        log.info("-- Taking Off")
        await drone.action.takeoff()

    async def deinitialize(self):
        log.info("-- Landing")
        await drone.action.land()

        log.info("-- Disarming")
        await drone.action.disarm()

    async def extrude(self, state: bool):
        # unimplemented
        log.info(f"Extruder is {("on" if state else "false")}")
