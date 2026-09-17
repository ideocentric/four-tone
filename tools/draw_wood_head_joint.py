# SPDX-FileCopyrightText: 2026 Matt Comeione
# SPDX-License-Identifier: GPL-3.0-or-later
"""Draw the wooden head joint concept (SVG). All dimensions in mm.

    python3 tools/draw_wood_head_joint.py docs/images/wood-head-joint.svg

The design carries the voicing dimensions of the tested printed head joint
(rev 02) into a five-piece wooden build: four boards and a block, assembled the
way a wooden organ pipe is, with the windway formed as the gap between the block
face and the front board. Edit the constants below to change it.
"""
import sys

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wood_head_joint_spec as SP

OUT, WALL, IN = SP.OUT, SP.WALL, SP.IN
H = SP.BOX_H                              # height of the glued box
BLOCK_H = SP.BLOCK_H
WW_W, WW_D, WW_L = SP.WW_W, SP.WW_D, SP.WW_L
CUTUP, WIN_W, LAB = SP.CUTUP, SP.WIN_W, SP.LAB_ANGLE
INLET = SP.INLET
CH_W, CH_H, CH_D = SP.CH_W, SP.CH_H, SP.CH_D
COLLAR_H, SPIGOT_D, SPIGOT_L, COLLAR_BORE = SP.COLLAR_H, SP.SPIGOT_D, SP.SPIGOT_L, SP.COLLAR_BORE
MOUTH, LABIUM = SP.MOUTH, SP.LABIUM
CH_TOP = BLOCK_H - WW_L
CH_BOT = CH_TOP - CH_H
S = 3.0
out = []
def px(v): return v * S
def rect(x, y, w, h, cls="part"): out.append(f'<rect x="{px(x):.1f}" y="{px(y):.1f}" width="{px(w):.1f}" height="{px(h):.1f}" class="{cls}"/>')
def line(x1, y1, x2, y2, cls="thin"): out.append(f'<line x1="{px(x1):.1f}" y1="{px(y1):.1f}" x2="{px(x2):.1f}" y2="{px(y2):.1f}" class="{cls}"/>')
def poly(pts, cls="part"): out.append('<polygon points="' + " ".join(f"{px(x):.1f},{px(y):.1f}" for x, y in pts) + f'" class="{cls}"/>')
def text(x, y, s, cls="note", anchor="start"): out.append(f'<text x="{px(x):.1f}" y="{px(y):.1f}" class="{cls}" text-anchor="{anchor}">{s}</text>')
def dim_h(x1, x2, y, label):
    line(x1, y, x2, y, "dim")
    for x, d in ((x1, 1), (x2, -1)): poly([(x, y), (x + d * 2.0, y - 1.0), (x + d * 2.0, y + 1.0)], "arrow")
    text((x1 + x2) / 2, y - 1.4, label, "dimtext", "middle")
def dim_v(y1, y2, x, label, side="left"):
    line(x, y1, x, y2, "dim")
    for y, d in ((y1, 1), (y2, -1)): poly([(x, y), (x - 1.0, y + d * 2.0), (x + 1.0, y + d * 2.0)], "arrow")
    text(x + (-1.4 if side == "left" else 1.4), (y1 + y2) / 2 + 1.1, label, "dimtext", "end" if side == "left" else "start")
def group(tx, ty, title, sub=""):
    out.append(f'<g transform="translate({px(tx):.1f},{px(ty):.1f})">')
    if title: text(0, -7, title, "title")
    if sub: text(0, -2.5, sub, "sub")
def endgroup(): out.append("</g>")
Z = lambda z: H - z                     # model z (up) to drawing y (down)

# ------------------------------------------------------------------ A section
group(42, 106, "", "")
text(0, -58, "A  SECTION THROUGH THE CENTRE", "title")
text(0, -53, "assembled; the mouth faces left. Shaded = wood, white = air.", "sub")
rect(0, Z(H), WALL, H)                                         # front board
rect(OUT - WALL, Z(H), WALL, H)                                # back board
rect(WALL, Z(H), IN, H - BLOCK_H, "void")                      # interior above the block
rect(WALL + WW_D, Z(BLOCK_H), IN - WW_D, BLOCK_H)              # block
rect(WALL, Z(MOUTH), WW_D, WW_L, "void")                       # windway gap
rect(WALL + WW_D, Z(CH_TOP), CH_D, CH_H, "void")               # wind chamber
BX = WALL + WW_D + (IN - WW_D) / 2 - INLET / 2
rect(BX, Z(CH_BOT), INLET, CH_BOT, "void")                     # inlet bore
rect(0, Z(LABIUM), WALL, CUTUP, "void")                        # window
line(WALL, Z(LABIUM), 0, Z(LABIUM) - 4.2, "thin")              # labium bevel
# collar and spigot, drawn above the box
CT = -COLLAR_H
rect(0, CT, OUT, COLLAR_H)                                     # collar body
rect((OUT - COLLAR_BORE) / 2, CT, COLLAR_BORE, COLLAR_H, "void")
rect((OUT - SPIGOT_D) / 2, CT - SPIGOT_L, SPIGOT_D, SPIGOT_L)  # spigot
rect((OUT - COLLAR_BORE) / 2, CT - SPIGOT_L, COLLAR_BORE, SPIGOT_L, "void")
line(0, CT, OUT, CT, "thin")
text(OUT + 4, CT - SPIGOT_L + 6, f"spigot \u00f8{SPIGOT_D:g} x {SPIGOT_L:g}, turned on the collar;")
text(OUT + 4, CT - SPIGOT_L + 10, "the PVC pipe slides over it and rests")
text(OUT + 4, CT - SPIGOT_L + 14, "on the collar shoulder")
text(OUT + 4, CT + COLLAR_H / 2, f"collar {OUT:g} x {OUT:g} x {COLLAR_H:g}, bore \u00f8{COLLAR_BORE:g}")
text(OUT + 4, Z(LABIUM) - 1.5, f"labium: {LAB:g}\u00b0 bevel, {WIN_W:g} mm wide")
text(OUT + 4, Z(MOUTH) - 1.5, "mouth line = top face of the block")
text(OUT + 4, Z(MOUTH) + 6, f"windway: {WW_W:g} mm wide x {WW_D:g} mm gap,")
text(OUT + 4, Z(MOUTH) + 10, f"{WW_L:g} mm long, formed by the gap between")
text(OUT + 4, Z(MOUTH) + 14, "the block face and the front board")
text(OUT + 4, Z(CH_TOP) + 9, f"wind chamber {CH_W:g} x {CH_H:g} x {CH_D:g} deep")
text(OUT + 4, Z(0) - 5, f"\u00f8{INLET:g} inlet bore, fan caddy nozzle")
dim_v(CT - SPIGOT_L, H, -10, f"{H + COLLAR_H + SPIGOT_L:g} overall")
dim_v(CT, H, -4.5, f"{H + COLLAR_H:g} to the shoulder")
dim_v(Z(BLOCK_H), H, OUT + 1.5, f"{BLOCK_H:g}", "right")
dim_v(Z(LABIUM), Z(MOUTH), OUT + 8, f"cut-up {CUTUP:g}", "right")
dim_h(0, OUT, H + 8, f"{OUT:g}")
dim_h(WALL, OUT - WALL, H + 15, f"{IN:g} inside")
endgroup()

# ------------------------------------------------------------- B front board
group(192, 106, "B  FRONT BOARD", f"{OUT:g} x {H:g} x {WALL:g}, one off, dense hardwood")
rect(0, 0, OUT, H)
rect((OUT - WIN_W) / 2, Z(LABIUM), WIN_W, CUTUP, "void")
dim_h((OUT - WIN_W) / 2, (OUT + WIN_W) / 2, Z(LABIUM) - 5, f"{WIN_W:g}")
dim_v(Z(LABIUM), Z(MOUTH), (OUT + WIN_W) / 2 + 3, f"{CUTUP:g}", "right")
dim_v(Z(MOUTH), H, (OUT + WIN_W) / 2 + 3, f"{MOUTH:g}", "right")
dim_h(0, OUT, H + 8, f"{OUT:g}")
dim_v(0, H, -6, f"{H:g}")
text(0, H + 16, "Window cut through. Bevel its top edge")
text(0, H + 20, f"at {LAB:g}° on the inside face: that edge")
text(0, H + 24, "is the labium and must stay crisp.")
endgroup()

# -------------------------------------------------------------- C back board
group(288, 106, "C  BACK BOARD", f"{OUT:g} x {H:g} x {WALL:g}, one off")
rect(0, 0, OUT, H)
dim_h(0, OUT, H + 8, f"{OUT:g}")
dim_v(0, H, -6, f"{H:g}")
endgroup()

# ------------------------------------------------------------- D side boards
group(374, 106, "D  SIDE BOARDS", f"{IN:g} x {H:g} x {WALL:g}, two off")
rect(0, 0, IN, H)
text(IN / 2, H / 2, "2 off", "note", "middle")
dim_h(0, IN, H + 8, f"{IN:g}")
dim_v(0, H, -6, f"{H:g}")
endgroup()

# -------------------------------------------------------------------- E block
group(22, 268, "E  BLOCK", f"front face. {IN:g} x {IN:g} x {BLOCK_H:g}, one off, hardwood")
rect(0, 0, IN, BLOCK_H)
rect((IN - WW_W) / 2, 0, WW_W, WW_L, "void")
rect((IN - CH_W) / 2, WW_L, CH_W, CH_H, "void")
rect(IN / 2 - INLET / 2, WW_L + CH_H, INLET, BLOCK_H - WW_L - CH_H, "hidden")
text(IN + 3, WW_L / 2 + 1, f"windway rabbet, {WW_W:g} wide")
text(IN + 3, WW_L + CH_H / 2 + 1, f"wind chamber, {CH_W:g} wide")
text(IN + 3, BLOCK_H - 5, f"ø{INLET:g} bore (hidden)")
dim_h(0, IN, BLOCK_H + 8, f"{IN:g}")
dim_v(0, WW_L, -5, f"{WW_L:g}")
dim_v(WW_L, WW_L + CH_H, -5, f"{CH_H:g}")
dim_v(0, BLOCK_H, -12, f"{BLOCK_H:g}")
text(0, BLOCK_H + 17, f"Windway rabbet {WW_W:g} wide x {WW_D:g} deep x {WW_L:g} long across the front")
text(0, BLOCK_H + 21, f"face, open at the top. Wind chamber pocket {CH_W:g} x {CH_H:g} x {CH_D:g} deep")
text(0, BLOCK_H + 25, f"below it. ø{INLET:g} bore from the bottom face into the chamber.")
endgroup()

group(150, 268, "", "block, side face")
rect(0, 0, IN, BLOCK_H)
rect(0, 0, WW_D, WW_L, "void")
rect(0, WW_L, CH_D, CH_H, "void")
dim_h(0, CH_D, WW_L + CH_H + 6, f"{CH_D:g} deep")
dim_h(0, IN, BLOCK_H + 8, f"{IN:g}")
dim_v(0, WW_L, IN + 4, f"{WW_L:g}", "right")
endgroup()

# ------------------------------------------------------------------- G collar
group(238, 268, "G  COLLAR", f"{OUT:g} x {OUT:g} x {COLLAR_H:g} plus a turned spigot, one off, hardwood")
rect(0, SPIGOT_L, OUT, COLLAR_H)
rect((OUT - SPIGOT_D) / 2, 0, SPIGOT_D, SPIGOT_L)
rect((OUT - COLLAR_BORE) / 2, 0, COLLAR_BORE, COLLAR_H + SPIGOT_L, "void")
text(OUT + 3, SPIGOT_L / 2, f"spigot \u00f8{SPIGOT_D:g} x {SPIGOT_L:g}, turned")
text(OUT + 3, SPIGOT_L + COLLAR_H / 2, f"bore \u00f8{COLLAR_BORE:g} through")
dim_h((OUT - SPIGOT_D) / 2, (OUT + SPIGOT_D) / 2, -5, f"\u00f8{SPIGOT_D:g}")
dim_h(0, OUT, COLLAR_H + SPIGOT_L + 8, f"{OUT:g}")
dim_v(0, SPIGOT_L, -5, f"{SPIGOT_L:g}")
dim_v(SPIGOT_L, SPIGOT_L + COLLAR_H, -5, f"{COLLAR_H:g}")
text(0, COLLAR_H + SPIGOT_L + 17, "The spigot cannot be turned on the glued box:")
text(0, COLLAR_H + SPIGOT_L + 21, f"at \u00f8{SPIGOT_D:g} the cut would break through the")
text(0, COLLAR_H + SPIGOT_L + 25, "corners of the 47 mm square interior. Turning")
text(0, COLLAR_H + SPIGOT_L + 29, "this one small piece instead avoids that.")
endgroup()

# ----------------------------------------------------------------- F assembly
group(360, 268, "F  ASSEMBLY", "")
for i, n in enumerate([
    "1. Cut the four boards, the block and the collar blank.",
    "2. Front board: cut the window, then bevel its top edge",
    f"   at {LAB:g}\u00b0 on the inside face to form the labium.",
    "3. Block: bore the inlet, cut the wind chamber pocket,",
    f"   then the {WW_D:g} mm windway rabbet across the front face.",
    f"4. Collar: bore \u00f8{COLLAR_BORE:g} through, then turn the",
    f"   \u00f8{SPIGOT_D:g} x {SPIGOT_L:g} spigot on one face.",
    "5. Glue the block between the two side boards, flush at",
    "   the bottom ends, block front face toward the mouth.",
    "6. Glue on the front and back boards. The gap between the",
    "   block face and the front board is the windway.",
    "7. Glue the collar on top, bore concentric with the",
    "   interior.",
    "8. Seal the inside with shellac. Keep it out of the windway.",
    "",
    "The PVC pipe slides over the spigot and rests on the",
    "collar shoulder, so the pipe's weight is carried in",
    "compression, not by a socket in bending.",
    "",
    "Wood movement changes the windway gap, so use quartersawn",
    "stock or void-free ply, and seal it.",
]):
    text(0, i * 5.4, n)
endgroup()

W_PX, H_PX = 1700, 1180
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W_PX}" height="{H_PX}" viewBox="0 0 {W_PX} {H_PX}">
<style>
  text {{ font-family: "DejaVu Sans", Helvetica, Arial, sans-serif; fill: #111; }}
  .title {{ font-size: 13px; font-weight: bold; letter-spacing: 0.3px; }}
  .sub {{ font-size: 9.5px; fill: #555; }}
  .note {{ font-size: 9.5px; fill: #222; }}
  .dimtext {{ font-size: 8.5px; fill: #b3261e; }}
  .part {{ fill: #efe7d7; stroke: #111; stroke-width: 1.2; }}
  .void {{ fill: #ffffff; stroke: #111; stroke-width: 1; }}
  .hidden {{ fill: none; stroke: #999; stroke-width: 0.9; stroke-dasharray: 4 3; }}
  .thin {{ stroke: #111; stroke-width: 1; fill: none; }}
  .dim {{ stroke: #b3261e; stroke-width: 0.7; fill: none; }}
  .arrow {{ fill: #b3261e; stroke: none; }}
</style>
<rect width="{W_PX}" height="{H_PX}" fill="#ffffff"/>
<text x="60" y="42" style="font-size:20px;font-weight:bold">four-tone: wooden head joint, concept for quoting</text>
<text x="60" y="62" style="font-size:11px;fill:#444">Six pieces: four boards and a block glued up, plus a turned collar. Built like a wooden organ pipe: the windway is the gap between the block and the front board. All dimensions in mm.</text>
{chr(10).join(out)}
<text x="60" y="{H_PX-50}" style="font-size:10px;fill:#444">Critical for voicing, carried over from the tested printed head joint: windway {WW_W:g} x {WW_D:g} mm and {WW_L:g} mm long, cut-up {CUTUP:g} mm, labium {LAB:g}° and {WIN_W:g} mm wide, inlet ø{INLET:g} mm. Other dimensions may suit stock and tooling.</text>
<text x="60" y="{H_PX-34}" style="font-size:10px;fill:#444">Material: quartersawn hardwood or void-free Baltic birch ply, {WALL:g} mm; front board and block in dense hardwood (maple, cherry or pear). This design has not been built or voiced.</text>
<text x="60" y="{H_PX-18}" style="font-size:10px;fill:#444">Source: github.com/ideocentric/four-tone  |  generated by tools/draw_wood_head_joint.py  |  CC BY-SA 4.0</text>
</svg>
"""
open(sys.argv[1], "w").write(svg)
print("wrote", sys.argv[1])
