LaserUSB
========

Based on Rabbit King Laser 40B (board V 8.1)

Allow to replace the OEM software like NewlyDraw.
This projects aim to allow to use a Rabbit 40B.

Those laser cutters use a HPGL similiar language.
Every command is like HPGL finished by a ';'

Using the NewlyDraw as reference, **1** mm are **10** steps

Open Questions
--------------

* When got the laser activated?
   Do I have to use SP0? 
   or PD?
   or DA0?
   or all of them?

* How to abort the process? - use the stop button

Seen Commands
-------------

SP0 - select pen (HPGL)
DA0 - ?? activate laser?
DW
GZ

PA - plot absolute (HPGL)
PR - plot relative (HPGL)
PD-1912,0 - pen down (HPGL)
PU-1393,1360 - pen up (HPGL)

VJ24  - ?? velocity?
VK100 - ?? velocity?
VP100 - ?? velocity?
VQ15  - ?? velocity?
VS10  - ?? velocity?

ZG1 - ??
ZED - ends a file?
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
