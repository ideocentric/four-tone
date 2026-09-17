# SPDX-FileCopyrightText: 2026 Matt Comeione
# SPDX-License-Identifier: GPL-3.0-or-later
"""Dimensions of the wooden head joint, in mm.

One source of truth for the drawing (draw_wood_head_joint.py), the CAD model
(model_wood_head_joint.py) and the flat profiles (wood_dxf.py), so they cannot
drift apart. Edit here, then re-run all three.

Coordinates: Z up from the bottom of the box, X toward the mouth (the mouth faces
-X), origin on the axis.
"""

OUT = 71.0          # outside of the square tube
WALL = 12.0         # board thickness
IN = OUT - 2 * WALL  # 47, interior and the width of the side boards
BOX_H = 125.0       # height of the glued box

BLOCK_H = 53.0      # block height; its top face is the windway exit and mouth line
WW_W = 30.0         # windway width
WW_D = 1.5          # windway gap: the rabbet depth in the block face
WW_L = 10.0         # windway length
CH_W, CH_H, CH_D = 30.0, 15.0, 30.0   # wind chamber pocket in the block face
INLET = 10.25       # airway inlet bore, takes the fan caddy nozzle

CUTUP = 17.0        # windway exit to labium
WIN_W = 32.0        # window width
LAB_ANGLE = 19.3    # labium bevel, degrees above horizontal, rising outward
MOUTH = BLOCK_H             # z of the mouth line
LABIUM = MOUTH + CUTUP      # z of the labium edge

COLLAR_H = 25.0     # collar body, glued to the top of the box
SPIGOT_D = 52.3     # turned spigot: the PVC pipe slides over it
SPIGOT_L = 25.0
COLLAR_BORE = 47.0  # through bore in the collar, matching the interior

TOTAL_H = BOX_H + COLLAR_H            # 150 to the shoulder the pipe rests on
PIPE_ID = 52.5      # 2" schedule 40 PVC inside diameter, for reference
PIPE_OD = 60.3
