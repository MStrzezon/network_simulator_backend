from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceDTO:
    id: str
    name: str
    path: []


@dataclass(frozen=True)
class CoordinatesDTO:
    latitude: str
    longitude: str
    height: str


@dataclass(frozen=True)
class SimulationParamsDTO:
    simulation_timeframe: int
    simulation_timestep: int


