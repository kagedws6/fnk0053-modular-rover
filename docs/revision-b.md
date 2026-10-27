# Revision B engineering notes

Revision B uses nominal dimensions from the owner-supplied Freenove FNK0053 STEP model. The vendor model itself is not bundled. `data/kit-dimensions.json` records the selected measurements, source hash, coordinate mapping and bracket positions. Values are model-derived, not physically verified dimensions of the owner's kit.

## Geometry

The main board's planar envelope is 233.311883 x 120.337885 mm and its thickness is 1.6 mm. The tire diameter is 64.6 mm and width approximately 30 mm. Stock assembly placement is retained individually, including small asymmetries; tire-to-tire width is approximately 148.823 mm and wheelbase approximately 119.1-119.4 mm.

The 244 x 132 mm carrier narrows to an 82 mm waist around the wheel zones. Its lower mounting plane stays at 43.3 mm above ground, the original bracket/PCB underside elevation. Its base is 4 mm thick. Four bosses raise the PCB underside to 54 mm, a proposed 10.7 mm lift. This keeps motor loads on the carrier, with electronics supported above. The bottom board-fastener head recesses are nominally 6.4 mm diameter and 2.4 mm deep. Their fit and screw lengths remain to be checked.

The pan servo protrudes through the original PCB, so its opening continues through the new carrier. The lower frame opening has 2 mm nominal plan clearance around the simplified 32.8 x 12 mm body envelope. This is a static packaging check, not a servo movement test.

Four bracket pairs reproduce the measured 8 mm chassis attachment spacing at each kit position. The bracket's modeled 2.6 mm holes are not treated as a clearance-hole specification: the new printed carrier uses nominal 3.4 mm clearance holes. Actual screw size and thread engagement must be confirmed. Two motor-side bracket holes are 17 mm apart in the supplied model.

The line-sensor carrier stays at the original underside mounting elevation, so existing 28 mm supports can preserve sensor height despite the electronics-board lift. The proposed upper accessory deck is 110 x 120 x 4 mm at Z=83.6, using the four stock deck-hole positions and 28 mm standoffs above the raised PCB. The rear battery bay remains uncovered.

Separate front/rear bumpers use upper flanges over the carrier end bars and proposed M3 joints. The assembly length including bumpers is 254 mm; the frame itself is 244 mm long. The full frame fits inside the nominal P1S bed envelope before brim/slicer allowances, but no slicer job is supplied.

## Files and reproduction

- `revision-b.scad` is the current OpenSCAD assembly and selectable part source. `rover-concept.scad` includes it as a compatibility entry point.
- `mechanical_layout.py` holds shared planar geometry. Run `python scripts/build_mechanics.py` after changes to regenerate `generated/profiles-b.scad`, the experimental frame/deck STLs and the fixed coupon.
- `build_preview.py` uses the same structural profiles with simplified stock hardware envelopes. Small holes are displayed as surface markers; CAD/STLs contain real cut-through holes.
- `scripts/preview-renderer.js` supplies the depth-buffer renderer used by the interactive preview template.
- `experimental/validation-b.json` records mesh and selected clearance checks.

## Checks completed

Generated meshes reload as closed, consistently wound, positive-volume, single connected components. The lower frame has no plan overlap with any measured tire bounding box; minimum plan distance is over 3.1 mm. All bracket pairs remain 8 mm apart and have enough surrounding pad area for a nominal screw-head envelope. The pan-servo opening has at least 2 mm plan clearance. The carrier profile is connected and within its stated footprint.

The clearance checks use conservative tire boxes and a simplified servo envelope. They are deliberately narrower than a full collision/strength claim. This is still a prototype design.

## Next physical check

Print `fit-checks/motor-bracket-8mm-fit.stl` first. It is a 26 x 20 x 2 mm bench-fit plate with two 3.4 mm holes, 8 mm apart. Check it against a metal bracket and report free screw entry, flush contact and interference. The existing M3 clearance coupon helps select hole compensation.

## Still unresolved

Do not treat the full frame/deck as final print-and-assemble files. Board/frame fastener sizes, access, thread engagement, wire routing, support boss fit, battery retention, head support and motion sweep need physical checks. The actual PCB perimeter is simplified to a bounding outline with wheel/servo cutouts in the preview; detailed PCB components are not reproduced. The source STEP includes small placement discrepancies, and its secondary anomalously scaled wire presentation was excluded from measurement.

The voice board, battery and speaker still use estimated envelopes. Their final adapter holes, microphone openings, USB/button access and retaining features have not been designed. No physical prints, load tests or full assembly collision analysis have been completed.
