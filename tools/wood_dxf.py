#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Matt Comeione
# SPDX-License-Identifier: GPL-3.0-or-later
"""Write flat DXF profiles of the wooden head joint pieces, for sheet cutting.

    pip install ezdxf
    python3 tools/wood_dxf.py

Each file has a CUT layer with the profile to cut through, and a REFERENCE layer
showing features that are machined later (rabbet, pocket, bore, spigot) so a shop
can see what else the piece needs. Units are millimetres.
"""
import os
import sys

import ezdxf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wood_head_joint_spec as S

OUTDIR = "mechanical/wood/dxf"
os.makedirs(OUTDIR, exist_ok=True)


def new_doc():
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4                      # millimetres
    doc.layers.add("CUT", color=7)
    doc.layers.add("REFERENCE", color=1, linetype="DASHED")
    return doc, doc.modelspace()


def rect(msp, x0, y0, x1, y1, layer="CUT"):
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": layer})


def note(msp, x, y, s, h=3.0):
    msp.add_text(s, height=h, dxfattribs={"layer": "REFERENCE"}).set_placement((x, y))


def save(doc, name):
    path = os.path.join(OUTDIR, name)
    doc.saveas(path)
    print("wrote", path)


# ---- front board ------------------------------------------------------------
doc, msp = new_doc()
rect(msp, 0, 0, S.OUT, S.BOX_H)
rect(msp, (S.OUT - S.WIN_W) / 2, S.MOUTH, (S.OUT + S.WIN_W) / 2, S.LABIUM)
note(msp, 2, S.BOX_H + 4, f"FRONT BOARD  {S.OUT:g} x {S.BOX_H:g} x {S.WALL:g}  1 off")
note(msp, 2, S.BOX_H + 10, f"window cut through; bevel its top edge {S.LAB_ANGLE:g} deg on the inside face (labium)")
save(doc, "front-board.dxf")

# ---- back board -------------------------------------------------------------
doc, msp = new_doc()
rect(msp, 0, 0, S.OUT, S.BOX_H)
note(msp, 2, S.BOX_H + 4, f"BACK BOARD  {S.OUT:g} x {S.BOX_H:g} x {S.WALL:g}  1 off")
save(doc, "back-board.dxf")

# ---- side board -------------------------------------------------------------
doc, msp = new_doc()
rect(msp, 0, 0, S.IN, S.BOX_H)
note(msp, 2, S.BOX_H + 4, f"SIDE BOARD  {S.IN:g} x {S.BOX_H:g} x {S.WALL:g}  2 off")
save(doc, "side-board.dxf")

# ---- block ------------------------------------------------------------------
doc, msp = new_doc()
rect(msp, 0, 0, S.IN, S.IN)
msp.add_circle((S.IN / 2, S.IN / 2), S.INLET / 2, dxfattribs={"layer": "REFERENCE"})
rect(msp, (S.IN - S.WW_W) / 2, 0, (S.IN + S.WW_W) / 2, S.WW_D, "REFERENCE")
rect(msp, (S.IN - S.CH_W) / 2, 0, (S.IN + S.CH_W) / 2, S.CH_D, "REFERENCE")
note(msp, 2, S.IN + 4, f"BLOCK BLANK  {S.IN:g} x {S.IN:g} x {S.BLOCK_H:g} tall  1 off  (plan view)")
note(msp, 2, S.IN + 10, f"dashed: %%c{S.INLET:g} bore through from the bottom;")
note(msp, 2, S.IN + 16, f"windway rabbet {S.WW_W:g} wide x {S.WW_D:g} deep over the top {S.WW_L:g} of the front face;")
note(msp, 2, S.IN + 22, f"wind chamber pocket {S.CH_W:g} wide x {S.CH_D:g} deep x {S.CH_H:g} tall below it")
save(doc, "block.dxf")

# ---- collar -----------------------------------------------------------------
doc, msp = new_doc()
rect(msp, 0, 0, S.OUT, S.OUT)
msp.add_circle((S.OUT / 2, S.OUT / 2), S.COLLAR_BORE / 2)
msp.add_circle((S.OUT / 2, S.OUT / 2), S.SPIGOT_D / 2, dxfattribs={"layer": "REFERENCE"})
note(msp, 2, S.OUT + 4, f"COLLAR  {S.OUT:g} x {S.OUT:g} x {S.COLLAR_H:g}  1 off  (plan view)")
note(msp, 2, S.OUT + 10, f"%%c{S.COLLAR_BORE:g} bore through; turn a spigot %%c{S.SPIGOT_D:g} x {S.SPIGOT_L:g} long on the top face")
note(msp, 2, S.OUT + 16, f"(dashed circle) so the 2 inch PVC pipe slides over it")
save(doc, "collar.dxf")
