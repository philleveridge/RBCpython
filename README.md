# RBCpython
RobbuilderController in Python for RPi

This is an attempt to build a robot controller of Robobuilder in Python

Main module
rbcontroller  Main loop

Utilities 
rbcsdb       Simple DB to manage the robot movement seuqences
rbcfaces     Controls LCD face module  (HS1106 module I2C interface)

Libraries:
wckkey       Keyboard lib
wckirc       IR controller lib
wckmodule    Low level RB servo commands
wckplay      Play moves
wckacc       Accelerometrer interfcae  (MPU6050 on I2C interface)

Database
db16.txt     Set of prebuilt moves for 16 servo robot
