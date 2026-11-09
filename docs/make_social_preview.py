"""Render docs/social-preview.png (1280 x 640): the four layers and the one-line principle.

    python docs/make_social_preview.py      # needs matplotlib
Upload the result under Settings -> General -> Social preview.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG, INK, MUTED = "#12151b", "#e6e9ef", "#9aa3b2"
LAYERS = [("Orchestration", "/agora brackets every session · /plaza runs improvement rounds", "#7aa2ff"),
          ("Skills", "packaged workflows, levelled draft → used → hardened → reference", "#45c08a"),
          ("Policies", "rules every skill applies, mirrored verbatim into CLAUDE.md", "#e3b341"),
          ("Tools and state", "seven checks with exit codes · one file per session", "#ff8f6b")]

fig = plt.figure(figsize=(12.8, 6.4), dpi=100, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1280)
ax.set_ylim(0, 640)
ax.axis("off")
ax.text(64, 560, "agora-method", color=INK, fontsize=40, fontweight="bold", va="center")
ax.text(64, 505, "A working method for building software with an AI agent", color=MUTED, fontsize=18,
        va="center")
for i, (name, desc, colour) in enumerate(LAYERS):
    y = 380 - i * 86
    ax.add_patch(FancyBboxPatch((64, y), 1152, 66, boxstyle="round,pad=0,rounding_size=10",
                                facecolor="#1b2029", edgecolor=colour, linewidth=2.5))
    ax.text(92, y + 33, name, color=colour, fontsize=19, fontweight="bold", va="center")
    ax.text(380, y + 33, desc, color=INK, fontsize=15, va="center")
ax.text(64, 40, "A mechanism the system calls survives; a mechanism a human must remember does not.",
        color=MUTED, fontsize=15, style="italic", va="center")
out = Path(__file__).with_name("social-preview.png")
fig.savefig(out, facecolor=BG)
print(out)
