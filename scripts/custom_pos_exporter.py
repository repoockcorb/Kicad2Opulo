#!/usr/bin/env python3
import os
import datetime
import csv
import pcbnew
import wx

FIELD_LCSC = "#LCSC"
FIELD_HEIGHT = "#Height"

class CustomCSVExporter(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Custom PnP CSV Exporter"
        self.category = "External Plugins"
        self.description = f"Generate CSV PnP file using '{FIELD_LCSC}' and '{FIELD_HEIGHT}' fields, Y axis inverted."
        self.icon_file_name = "custom_icon.svg"

    def Run(self):
        board = pcbnew.GetBoard()
        path = board.GetFileName()
        if not path:
            wx.MessageBox("❌ Please save your board before exporting.", "Custom PnP CSV Exporter", wx.OK | wx.ICON_ERROR)
            return

        design_settings = board.GetDesignSettings()
        origin = design_settings.GetAuxOrigin()
        ox, oy = origin.x, origin.y

        rows = []
        for m in board.GetFootprints():
            ref = m.GetReference()
            fields = m.GetFieldsShownText()
            val = fields.get(FIELD_LCSC, "").strip() or m.GetValue()
            hgt = fields.get(FIELD_HEIGHT, "").strip()
            pkg = m.GetFPIDAsString()

            pos = m.GetPosition()
            relx, rely = pos.x - ox, pos.y - oy
            x_mm = pcbnew.ToMM(relx)
            y_mm = -pcbnew.ToMM(rely)
            rot = m.GetOrientationDegrees()
            side = "top" if m.GetLayer() == pcbnew.F_Cu else "bottom"

            rows.append([ref, val, pkg, f"{x_mm:.4f}", f"{y_mm:.4f}", f"{rot:.3f}", side, hgt])

        if not rows:
            wx.MessageBox("❌ No footprints found on the board!", "Custom PnP CSV Exporter", wx.OK | wx.ICON_ERROR)
            return

        base = os.path.splitext(path)[0]
        out_fn = base + "_custom.csv"
        now = datetime.datetime.now().isoformat()

        with open(out_fn, "w", newline="", encoding="utf-8") as f:
            f.write(f"# Created on {now}\n")
            f.write("# Unit = mm, Angle = deg. Coordinates relative to board origin (Y inverted).\n")
            writer = csv.writer(f)
            writer.writerow(["Ref", "Val", "Package", "X (mm)", "Y (mm)", "Rot", "Side", "Height"])
            writer.writerows(rows)

        wx.MessageBox(f"✅ Wrote CSV PnP file to:\n{out_fn}", "Custom PnP CSV Exporter", wx.OK | wx.ICON_INFORMATION)

CustomCSVExporter().register()
