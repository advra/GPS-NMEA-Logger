## GPS NMEA Logger

GPS NMEA is a protocol used in many applications like the Pixhawk. The pixhawk is an onboard autonomy aerial system for drones. NMEA messages are transmitted from the onboard pixhawk to a nearby ground base station. This program opens a port on the ground base station, reads the incoming message, verifies the checksum and saves it to a csv. 

Completed:
- Read data from TCP port
- Verify and Compute checksum
- Initial Unit Test

To Do:
 - add to csv
