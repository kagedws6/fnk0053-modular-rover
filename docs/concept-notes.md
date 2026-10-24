# FNK0053 modular rover concept -- revision A

This is an appearance and packaging study, not a verified printable chassis.

## Proposed arrangement

- Rounded open lower frame with separate replaceable front/rear bumpers.
- Original four motors, wheels and electronics shield retained.
- Rear battery holder accessible from above.
- Removable top deck for the Waveshare ESP32-S3-AUDIO-Board, separate speaker and battery.
- Existing camera/display pan-and-tilt head retained at the front.
- Repeating M3 accessory clearance holes on the deck and side rails.
- Underside line-tracking module retained as a component envelope.

## Explicit assumptions (mm)

| Parameter | Concept value | Status |
|---|---:|---|
| Frame length | 238 | Proposed |
| Frame width | 132 | Proposed |
| Overall tire-to-tire width | 193 | Estimated envelope |
| Wheel diameter / width | 65 / 27 | Unverified |
| Wheelbase | 124 | Unverified |
| Shield envelope | 210 x 124 x 2 | Unverified, simplified outline |
| Top deck | 112 x 120 x 4 | Proposed |
| Audio-board envelope diameter | 70 | Unverified |
| Accessory pitch | 12 | Proposed design interface |
| M3 clearance diameter | 3.4 | Proposed; fit coupon required |

These values establish a coherent concept, not measurements recovered accurately from photos. Perspective and the tape's offset prevent reliable hole coordinates. Do not infer manufacturing accuracy from the displayed numbers.

## Files

- `rover-concept.scad`: editable parametric OpenSCAD concept. Set `part` to assembly, frame, deck, audio_adapter, or bumper. `explode` separates the component groups.
- `concept-model.json`: preview mesh and component metadata.
- `build_preview.py`: regenerates the preview geometry and inline visualization from `viewer-template.html`.

The viewer uses simplified geometry: accessory holes are shown as surface markers. The OpenSCAD source subtracts actual holes. Existing components are simplified envelopes, including the face and battery holders. Colors identify parts and are not required filament colors.

## Still required before printable engineering

Confirm board outline, mounting holes and underside component clearances; motor bracket geometry and shaft position; wheel dimensions and clearances; audio-board holes, microphone positions, connectors and buttons; battery and speaker dimensions; head sweep and ribbon bend space; sensor height. Motor mounting holes and board-specific mounting bosses have deliberately not been invented. The frame tabs are provisional. The audio adapter has no board-specific holes yet.

Frame/board attachment, deck supports, bumper joints, the head mount and the sensor bracket still need engineering. Some assembly hardware and cable routing are omitted in the preview. No load analysis, detailed collision check, OpenSCAD render validation, slicer validation or physical fit check has been completed. No STL is provided to avoid presenting the concept as ready to print.

The initial target printer is a Bambu Lab P1S; initial material is Bambu PLA. Final geometry will need print orientation, reinforcement and tolerances suitable for that setup. Small mounting coupons should precede full-frame prints.

## Sources

Owner-provided assembly photos; Freenove FNK0053 assembly documentation; hardware identification from the ongoing rover project. Exact dimensions above remain assumptions. Original photographs, vendor firmware and vendor documents are not redistributed here.
