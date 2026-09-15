# Artwork

## `enso-oro.svg`

The house mark (ensō). Original work by Matt Comeione, drawn in Adobe
Illustrator, and used across the instrument projects. This file is a byte-for-byte
copy of `hardware/art/enso-oro.svg` from
[caryatid](https://github.com/ideocentric/caryatid), where its provenance is
recorded. Being first party, it places no constraint on how this design is
licensed.

It is committed as source because the silkscreen logo on the six fan driver is
generated from it: the board carries 153 derived polygons, which are an output.
CERN-OHL-S defines Complete Source as the editable design files, so the SVG has
to travel with the board.

On the six fan driver, rev A, the mark is 11.9 x 12.0 mm on F.SilkS, centred at
(66.5, 10.0) mm from the board's top-left corner, right of the title block. The
polygons are grouped as `enso logo` in the board file. They were converted with
the same method as caryatid's `tools/svg_to_silk.py` (even-odd hole detection,
holes keyholed into their parent contour, since silkscreen polygons cannot hold
holes), giving the same 153 polygons and 12,255 points.
