LaserUSB
========

Based on Rabbit King Laser 40B (board V 8.1)

Allow to replace the OEM software like NewlyDraw.
This projects aim to allow to use a Rabbit 40B.

Those laser cutters use a HPGL similiar language.
Every command is like HPGL finished by a ';'

Using the NewlyDraw as reference, **1** mm are **10** steps

Open and Answered Questions
---------------------------

* When got the laser activated?
   when using SP1 + PD it's activating the laser.

* How to abort the process? - use the software stop button
   Really dangerous, it's not direct responsive meaning the Laser cutter
   will continue it's work until the command (or multiple?) are executed before
   evaluating the command buffer.

Seen Commands
-------------

SP0 - select pen (HPGL)
DA0 - ?? activate laser?
DW
GZ - Go Zero. Seems to reset the coordination for a particular PEN to this position.
I *think* every pen has it's own coordination system. And every pen must initilize this to
a decent 0,0 coordination. I *think* the hardware is only doing this for the default moving PEN.
Meaning this must be called for every other pen by our self.
I **would** recommend always setting it.

PA - plot absolute (HPGL)
PR - plot relative (HPGL)
PD-1912,0 - pen down (HPGL)
PU-1393,1360 - pen up (HPGL)

VJ24  - acceleration (at least for move, when changing the acceleration it changes this value)
VK100 - ?? velocity?
VP100 - ?? velocity?
VQ15  - initial velocity (at least for move, but think it's also used by any other command)
VS10  - ?? velocity?

ZG1 - ??
ZED - ends a file?
ZQ - used by the stop command
ZZZFile[0-9] - selects which file to work on

Examples
--------

Manual step
^^^^^^^^^^^

On 10mm step, press manual step button once

.. code::

  ZZZFile0;VP100;VK100;SP2;SP2;VQ15;VJ24;VS10;PR;PU400,0;ZED;


Move around the Frame
^^^^^^^^^^^^^^^^^^^^^

Use schwein.dxf as input.

.. code::

  ZZZFile0;VP100;VK100;SP2;SP2;VQ15;VJ24;VS10;PR;PU-1912,0;PU0,1378;PU1912,0;PU0,-1378;ZED;


Stop button
^^^^^^^^^^^

When pressing the stop button on the panel. It sends:

.. code::

  ZZZFile0;ZQ;ZED

Cut a line
^^^^^^^^^^

Engrave something.
.. code::

  ZZZFile0;VP100;VK100;SP1;VQ15;VJ24;VS10;SP1;GZ;PR;PD00,-800;ZED

Test blog
^^^^^^^^^

- Closing the application doesn't generate traffic on the laser.
- Where does it save the orientation? on the usb dongle?
- Change the "Move Speed0" (Properties->Advanced) to 14 changes "VQ15" -> "VQ14"
