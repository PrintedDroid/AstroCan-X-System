AstroCan X - Saber Mini Remote
==============================
www.printed-droid.com

The AstroCan X Mini Remote (two stacked PCBs) built directly into a Ø42 mm lightsaber hilt.
Front = emitter (the joystick points to the emitter), back = pommel.
The rear grip tube unscrews for USB charging.


PARTS (folder STL/)
-------------------
Pick ONE version folder - it contains everything you need to print, already in print orientation:

  STL/1_Right_Island   right-hand Mini Remote, raised joystick island
  STL/2_Right_Cutout   right-hand Mini Remote, flat lid with joystick cutout
  STL/3_Left_Island    left-hand Mini Remote, raised joystick island
  STL/4_Left_Cutout    left-hand Mini Remote, flat lid with joystick cutout
  STL/5_Modular_Ends_Grips  mix-and-match emitter heads/sleeves, grip bodies (4 grip styles) and pommel heads
  STL/0_Options        alternatives: short emitter, support-free grip tubes (PommelDown, OpenDown)

  R / L = Mini Remote version (lower PCB mirrored for the left version: side buttons,
  slide switch, antenna notch and screws swap sides).

Each version folder contains:

  TopShell / BottomShell                 the two housing halves
  BottomShell_*_Grenade/_Ribs/_Panels  bottom shell with grip pattern (option)
  *_NoScrews shells                      option without side screws (lock rings hold the shells)
  SaberMiniRemote_LockRing.stl           print 2x - lock rings, one in front of each end
  SaberMiniRemote_EmitterRing_Long.stl   emitter (standard; short one in 0_Options)
  SaberMiniRemote_GripTube.stl           grip tube with pommel, print pommel down
                                         (needs supports in the grooves; support-free in 0_Options:
                                          GripTube_PommelDown or GripTube_OpenDown, all overhangs 45 deg)
  SaberMiniRemote_NavCap.stl             cap for the navigation button
  Preview_Assembly.png                   what it looks like assembled
  Preview_Section.png                    cut view (threads, lock rings, emitter cone)
  Preview_PrintParts.png                 all parts as they go on the print bed, with heights

Hardware: 4x M2 countersunk screws, approx. 6-8 mm (side screws, top shell into bottom shell).


ASSEMBLY
--------
1. Place the Mini Remote (both PCBs) into the bottom shell, USB side towards the grip end.
2. Put the NavCap on the navigation button, close with the top shell.
3. Screw the shells together with the 4 side M2 screws.
4. Screw one LockRing onto each threaded stub, all the way to the shoulder.
   The rings hold the two shell halves together whenever an end piece is removed.
5. Screw on the emitter (front, joystick side) and the grip tube (back, USB side).
6. Charging: unscrew the grip tube only - the LockRing stays in place.

Threads: right-hand (clockwise = tight), pitch 2.5 mm, both ends identical.


PRINTING (no supports unless noted)
-----------------------------------
  TopShell        split face down; supports needed under the lid / openings
  BottomShell     supports needed (round underside)
  EmitterRing*    standing, thread opening down (inside: 45 deg cone roof)
  GripTube        standing, pommel down (supports in the grooves)
  GripTube_OpenDown  standing, thread opening down
  GripTube_PommelDown standing on the flat pommel
  LockRing        flat
  NavCap          as for the Mini Remote


DIMENSIONS
----------
  Hilt diameter   42 mm (emitter flare 49 mm, pommel 47 mm)
  Total length    approx. 280 mm with EmitterRing_Long, approx. 260 mm with EmitterRing


SOURCE
------
  build_saber_miniremote.py   parametric Blender script (VARIANTE = RECHTS/LINKS,
                              JOY_STYLE = INSEL/AUSSCHNITT, GRIP_LEN, EM_LONG, LOCK_L, TRANS)
  Saber_MiniRemote.blend      all variants as Blender collections
