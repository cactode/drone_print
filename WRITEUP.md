# Drone Print Spec
## File Format
Each line of the file corresponds to a location that the drone should fly to / speed at which it should fly / whether the extruder should turn on or off once it reaches that point.
Each line of the file should express the following info:
- LAT: Latitude in degrees, between -90 and 90
- LON: Longitude in degrees, between -180 and 180
- ALT: Altitude in m, relative to takeoff height
- SPD: Speed, in m/s. Must be under the max speed of the drone
- EXT: Whether or not the extruder should turn on / remain on after reaching this point. "0" for off, "1" for on

Each line of the file should be formatted as follows (shown in quasi-regex):
line ::= LAT " "+ LONG " "+ ALT " "+ SPD " "+ EXT

All of (LAT, LON, ALT, SPD, EXT) should be expressed as decimal floating point numbers.

Lines that are blank / start with ; are ignored. The file should not contain non-ASCII characters.

This module expects the input file to be formatted correctly. Its behavior is not defined for malformed files.

## Structure and Usage
3D printing drones are defined as quadcopters that have the ability to "extrude" something. To use this module, the user must subclass `drone_print.PDrone` and implement the missing functions. `drone_print.GenericPDrone` is provided for simulations and attempts to connect with a simulated drone on udp://:14540.

To use this library, one must call `drone_print.drone_print`. This function takes in a PDrone object & a TextIO object. The function parses the text file and uses it to generate a MAV mission. It starts this mission on the quadcopter and monitors the mission's progress. As each step in the mission executes, an asynchronous generator makes sure that the extruder is on at the correct times. 

## Design Considerations
This module was intended to be implemented in a larger system / was not meant to be interfaced with by a human operator; it therefore does not implement sytax checking / bounds checking on the input file. It is expected that a "slicer" would manage higher-level tasks like coordinate mapping, speed management, etc. This module tries to rely mostly on high level MAVSDK functions; by doing this, it keeps some of the safety guarantees made by the MAVSDK interface. 

Before testing this on a real aircraft, I'd like to add proper unit tests / implement the other components in this system. I would also like to add input sanity checks to ensure that malformed inputs do not cause undefined behavior. Additional utility features (built in coordinate transformations from global to local, buffered file loading for large file support, etc) would also be helpful.