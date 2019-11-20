# AdjustTCXDistance
Allows you to adjust distances in a TCX file (Training Center XML, Garmin e.g.)

Say for example you ran on a treadmill for 6 miles, but your fitness devices recorded 5.5 miles. This program will load in your exported TCX file, it will read the distance (5.5 miles), ask you your real distance (6 miles) and will then scale each distance mark accordingly.

Note even in cases where a Garmin device calibrates your treadmill run, the orginal un-calibrated metrics are what's recorded in TCX and also what's reported to Strava. So this allows you to correct Strava data (export TCX, run this program, import file into Strava).
