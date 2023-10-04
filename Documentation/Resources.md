# Resources/Documentation

## Telemetry Team Details

3.3.1 Telemetry

Upon power up, the Cansat shall collect the required telemetry at a one (1) Hz sample rate and transmit the telemetry data to the ground station. The ASCII format of the telemetry packets are described below. Each telemetry field is delimited by a comma, and each telemetry packet is terminated by a single carriage return character. No comma (`,`) characters should be part of the data fields -- commas are delimiters only.

### 3.3.1.1 Telemetry Formats

The Cansat telemetry packet format to be transmitted at one (1) Hz is as follows:
TEAM_ID, MISSION_TIME, PACKET_COUNT, MODE, STATE, ALTITUDE, AIR_SPEED, HS_DEPLOYED, PC_DEPLOYED, TEMPERATURE, VOLTAGE, PRESSURE, GPS_TIME, GPS_ALTITUDE, GPS_LATITUDE, GPS_LONGITUDE, GPS_SATS, TILT_X, TILT_Y, ROT_Z, CMD_ECHO [,,OPTIONAL_DATA]

The telemetry data fields are to be formatted as follows:
1. `TEAM_ID` is the assigned four-digit team identification number. E.g., imaginary team '1000'.
2. `MISSION_TIME` is UTC time in format hh:mm:ss, where hh is hours, mm is minutes, and ss is seconds. E.g., '13:14:02' indicates 1:14:02 PM.
3. `PACKET_COUNT` is the total count of transmitted packets since turn on, which is to be reset to zero by command when the Cansat is installed in the rocket on the launch pad at the beginning of the mission and maintained through processor reset.
4. `MODE` = 'F' for flight mode and 'S' for simulation mode.
5. `STATE` is the operating state of the software (e.g., LAUNCH_WAIT, ASCENT, ROCKET_SEPARATION, DESCENT, HS_RELEASE, LANDED, etc.). Teams may define their own states. This should be a human-readable description as the judges will review it after the launch in the .csv files.
6. `ALTITUDE` is the altitude in units of meters and must be relative to ground level at the launch site. The resolution must be 0.1 meters.
7. `AIR_SPEED` is the airspeed in meters per second measured with the pitot tube during both ascent and descent.
8. `HS_DEPLOYED` = 'P' indicates the heat shield is deployed, 'N' otherwise.
9. `PC_DEPLOYED` = 'C' indicates the parachute is deployed (at 100 m), 'N' otherwise.
10. `TEMPERATURE` is the temperature in degrees Celsius with a resolution of 0.1 degrees.
11. `PRESSURE` is the air pressure of the sensor used. Value must be in kPa with a resolution of 0.1 kPa.
12. `VOLTAGE` is the voltage of the Cansat power bus with a resolution of 0.1 volts.
13. `GPS_TIME` is the time from the GPS receiver. The time must be reported in UTC and have a resolution of a second.
14. `GPS_ALTITUDE` is the altitude from the GPS receiver in meters above mean sea level with a resolution of 0.1 meters.
15. `GPS_LATITUDE` is the latitude from the GPS receiver in decimal degrees with a resolution of 0.0001 degrees North.
16. `GPS_LONGITUDE` is the longitude from the GPS receiver in decimal degrees with a resolution of 0.0001 degrees West.
17. `GPS_SATS` is the number of GPS satellites being tracked by the GPS receiver. This must be an integer.
18. `TILT_X`, `TILT_Y` are the angles of the Cansat X and Y axes in degrees, with a resolution of 0.01 degrees, where zero degrees is defined as when the axes are perpendicular to the Z axis which is defined as towards the center of gravity of the Earth.
19. `ROT_Z` is the rotation rate of the Cansat in degrees per second with a resolution of 0.1 degrees per second.
20. `CMD_ECHO` is the text of the last command received and processed by the Cansat. For example, CXON or SP101325. See the command section for details of command formats. Do not include commas characters.
21. `[,,OPTIONAL_DATA]` are zero or more additional fields the team considers important following two commas, which indicate a blank field. This data must follow the same format rules (including the use of comma characters ',') to facilitate review of the CSV files by the judges after the mission.

### 3.3.1.2 Telemetry Data Files

The received telemetry for the entire mission shall be saved on the ground station computer as comma-separated value (.csv) files that will be examined by the competition judges in Excel. The CSV format should be the same as used by export from Excel. Teams shall provide the CSV file to the judges immediately after the launch operations via USB drive.

The CSV files shall include a header specifying the name of each field/column of data in the file. The telemetry data files shall be named as follows:
- `Flight_<TEAM_ID>.csv` where the team_id is the four-digit team id number. For example: `Flight_100

## Agile Workflow using Continuous Delivery/Integration Techniques

To understand the development flow for making changes to the project, refer to the following link. It describes the model you will follow for continuous development:

[GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)

## Useful Links for Understanding Project Dependencies

### Pandas Help Links

- [Pandas Tutorial on GeeksforGeeks](https://www.geeksforgeeks.org/pandas-tutorial/)
