# Contributing

Issues and pull requests are welcome. This project is currently at the measurement and fit-coupon stage. A polished preview is not evidence of mechanical fit.

## Measurement conventions

- Use millimeters.
- In the model, +X is forward toward the camera head, Y is left/right, and +Z is up from ground level.
- Report the hardware revision, the reference edge or hole, and the direction of every measurement. Label left/right as seen looking forward from behind the rover.
- Report center-to-center hole distances, hole diameter, plate thickness, bracket footprint and available screw clearance separately.
- Mark measurements as confirmed, approximate or inferred. Include the tool used and reasonable uncertainty.
- Photograph parts straight-on with the ruler in the same plane as the feature. Remove location metadata and crop unrelated personal surroundings before posting images.

## Fit-check report

Include printer model, nozzle diameter, layer height, material, any XY/hole compensation, and whether the STL was printed at 100% scale.

For the M3 sample, report the smallest hole that allows the screw to slide freely. For the bracket gauge, include a photo showing both screw centers and the tick scale, the estimated center spacing, and whether the bracket and gauge sat flat.

## CAD changes

- Keep the original kit hardware serviceable, including battery removal and connector access.
- Make accessory adapters replaceable so a different sensor does not require a new full chassis.
- Separate measured component dimensions from proposed design dimensions.
- Include editable source with exported meshes. State what was checked in CAD, in a slicer and on a physical print.
- For changes to the Python generators, rebuild the affected files and include validation results. Do not claim physical validation unless a part was actually printed and tested.
- Avoid adding vendor code, manuals, firmware images or third-party designs without a compatible license and attribution.

Original files in this repository use the MIT license. Contributions should use the same license unless explicitly discussed before submission.
