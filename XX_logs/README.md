this is the folder for the log files.
the log files will not be pushed onto github due to the size.
the log files will be saved in folder "logs" in this directory.


NO BARO Measurements on the Seawatch 4 logs
Seawatch 4 logs are the ones with the 9 in front!

# logs of interest:
- AETR
- AHR2
- IMU (größe checken)
- GPS (?)


# Logtypes:
## AETR
- Aileron
- Elevon
- Thrust
- Rudder
- FLap
- SS (?)

## AHR2
- Roll
- Pitch
- Yaw
- Alt
- Lat
- Lng
- Q1-4 (?)

## AOA
- AOA (Angle of attack)
- SSA (Sideslipangle)

## ARM
- ArmState
- ArmChecks
- Forced
- Method

## ATT
- DesRoll
- Roll
- DesPitch
- Pitch
- DesYaw
- Yaw
- ErrRp
- ErrYaw
- AEKF

## AUXF
- 31 (?)

## BARO
- 0
    - Alt
    - Press
    - Temp
    - CRt
    - SMS
    - Offset
    - GndTemp
    - Health

## BAT
- 0
    - Volt
    - VoltR
    - Curr
    - CurrTot
    - Enrg Tot
    - Temp
    - Res
    - RemPct

## CMD
- not relevant I think

## CTUN
- Control tuning information

## DSF
- Onboard logging statistics

## EV
- event indentifier

## FILE
- idk

## FMT
- FMT not necessary

## FMTU
- not neccessary

## FTN
- FTN filter tuning message

## GPA
- GPS accuracy

## GPS
- GPS data

## IMU
- hat 2 imus
- inertia measurement unit

## LAND
- slope landing data

## MAG
- data from compass

## MAV
- GCS mavlink statistics

## MAVC
- MAvlink command

## MODE
- vehicle control information

## MSG
- Textual message

## MULT 
- message mapping from single character to numeric multiplier

## NTON
- navigation tuning information

## ORGN
- vehicle navigation origin or other notable position

## PARM
- parameter value

## PID - PRSY pid values for controllers

## PM autopilot system performance and general data dumping ground

## POS
- canonical vehicle position

## POWR
- sytem power information

## RAD
- telemetry radio statistics

## RCI2 
- rcinput channels to vehicle

## RCIN
- rcinput channels again

## RCOU
- servo channel output values

## STAK
- stack information

## STAT
- current status of the aircraft
- isflying, armed, safety, crash

## TEC TEC2 energy control system

## TERR rattin database information

## TSYN time syncronisation info

## UBX1, UBX2 ublock specific information

## UNIT message mapping from single character to SI unit

## VIBE vibrations

## VER vibrations wieder

## *KF Kalman filter constants