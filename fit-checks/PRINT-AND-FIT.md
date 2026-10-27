# First PLA fit-check prints

These are small measuring/clearance tools, not load-bearing rover parts. Neither tool assumes an actual Freenove motor-bracket spacing.

## Revision B: print the fixed coupon first

Freenove's STEP confirms **8.00 mm center spacing** on all four metal brackets. The new `motor-bracket-8mm-fit.stl` is a 26 x 20 x 2 mm plate with two nominal 3.4 mm holes at that spacing. Print it flat, at 100% scale, 0.20 mm layers, with your normal matching Bambu PLA profile and no supports. Try the screw-clearance sample as well.

When convenient, remove the rover batteries and detach one bracket from the PCB. Keep the motor on its bracket if practical. Hold the coupon against the bracket's chassis attachment face and check that two loose M3 screws line up without bending or forcing the parts. Keep this a bench fit check, not a replacement mount. Send a straight-on photo and report whether it sits flat and both screws enter freely.

The fixed coupon supersedes the broad spacing gauge for the next fit check. The older gauge remains useful; its first tick is 8 mm. The full revision B frame/deck STLs in `experimental/` still need mechanical and fastener verification before a full assembly print.

## Print

Import `motor-bracket-spacing-gauge.stl` and `m3-clearance-sample.stl` into Bambu Studio. STL dimensions are in millimeters. Select your P1S, installed nozzle and matching Bambu PLA profile. Lay both pieces flat with raised labels facing up, keep scale at 100%, and use a 0.20 mm layer height. Supports are unnecessary; a brim should normally be unnecessary. The main plates are 2 mm thick and total height is 2.4 mm. Start with normal profile settings; no special high-strength settings are needed for these tools.

This guidance assumes standard PLA printing. No slicer-generated print time or material estimate has been verified, and no physical print has been tested yet.

## 1. Check screw clearance

Try an existing M3 screw in the three holes marked 3.2, 3.4 and 3.6. These are nominal modeled diameters; the printed holes may be smaller. Record the smallest hole the screw slides through freely, without driving its threads into the plastic. Tell me if none works. Do not use the gauge as a tap or force a tight screw.

## 2. Check one motor bracket

When convenient, remove the rover batteries before loosening mounting hardware. Detach one metal motor bracket from the circuit board, leaving the motor attached if practical. Preserve its screws and nuts.

Hold the flat underside of the spacing gauge against the bracket's chassis mounting face, with the labels facing outward. Align one bracket hole with the single round hole at the gauge's zero point. Align the other bracket hole with the long slot. Two loosely inserted M3 screws can help locate the centers; do not tighten them or use the gauge as a permanent motor mount. Use appropriate screw length for the extra 2 mm plate and avoid protruding screws against electronics.

Read the second screw's center against the ticks beside the slot. Numbers 10, 20 and 30 show center-to-center spacing in mm from the fixed round hole. Intermediate ticks are every 2 mm. The usable center range is 8-36 mm. The leftmost unlabeled tick is 8 mm. The round hole and slot are both nominally 3.6 mm wide.

The slot is intentionally loose. Treat the reading as a rough spacing check, not caliper accuracy. If the bracket cannot sit flat, the holes do not fall in the range, or the motor blocks access, stop the fit check and photograph the interference. That tells us what to change.

## Send back

- Which clearance hole fits the M3 screw freely.
- A photo looking straight at the gauge and bracket, showing the screw centers and ticks.
- Whether the gauge sits flat, and any interference.

This establishes bracket screw spacing only. We will still need the bracket footprint, board mounting locations, and motor/wheel clearances before generating the final chassis. A successful gauge fit does not validate the concept chassis dimensions.

## File validation

The generation script reloads each STL and checks for a closed watertight mesh, consistent face winding, positive volume and one connected component. Results are in `mesh-validation.json`. These are mesh checks, not a physical fit or print test. `fit-gauges.scad` is the editable source equivalent; its font may look different from the generated STL's block lettering.
