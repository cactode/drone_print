import abc
import logging
import asyncio
from mavsdk.system import System

log = logging.getLogger(__name__)


class PDrone(abc.ABC):
    """
    Abstract Base Class that specifies the functions required for a 3D printing drone.
    3D printing drones must be quadcopters with a GPS connection and the ability to extrude on command.
    3D printing drones should subclass this ABC.
    """

    @abc.abstractclassmethod
    async def create(cls):
        """
        Creates a new instance of this drone object. Regular initialization should not be used as it does not work well with asyncio
        """
        ...

    @property
    @abc.abstractmethod
    def drone(self) -> System:
        """
        A MAVSDK system object that corresponds to the drone being controlled.
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
    @classmethod
    async def create(cls):
        # generic initialization code taken from:
        # https://github.com/mavlink/MAVSDK-Python/blob/main/examples/mission.py'
        self = GenericPDrone()
        drone = System()
        await drone.connect(system_address="udp://:14540")

        log.info("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                log.info(f"Drone discovered with UUID: {state.uuid}")
                break

        self._drone = drone
        return self

    @property
    def drone(self):
        return self._drone

    async def extrude(self, state: bool):
        # unimplemented for demo
        message = "on" if state else "off"
        log.info(f"Extruder is {message}")
