# RBCpython
RobbuilderController in Python for RPi

This is an attempt to build a robot controller of Robobuilder in Python. It requires RPI connected with an extension board to interface to the Robobuilder Huno huimanoid robot.

<b>Main module</b>
<li>rbcontroller  Main loop


<b>Utilities</b> 
<li>rbcsdb       Simple DB to manage the robot movement seuqences
<li>rbcfaces     Controls LCD face module  (HS1106 module I2C interface)


<b>Libraries:</b>
<li>wckkey       Keyboard lib
<li>wckirc       IR controller lib
<li>wckmodule    Low level RB servo commands
<li>wckplay      Play moves
<li>wckacc       Accelerometrer interfcae  (MPU6050 on I2C interface)


<b>Database</b>
<li>db16.txt     Set of prebuilt moves for 16 servo robot
