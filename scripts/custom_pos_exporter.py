#!/usr/bin/env python3
import os
import datetime
import csv
import pcbnew
import wx

# ← Exact keys of your custom footprint fields
FIELD_LCSC   = "#LCSC"
FIELD_HEIGHT = "#Height"

class CustomCSVExporter(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Custom PnP CSV Exporter"
        self.category = "External Plugins"
        self.description = (
            "Generate a CSV PnP file using your "
            f"'{FIELD_LCSC}' and '{FIELD_HEIGHT}' fields, "
            "with coordinates relative to the board origin (Y axis inverted)."
        )
        # To use a custom icon, place an SVG named 'custom_icon.svg' in the same folder as this script
        # and set its basename here:
        self.icon_file_name = "custom_icon.svg"

    def Run(self):
        board = pcbnew.GetBoard()
        path  = board.GetFileName()
        if not path:
            wx.MessageBox(
                "❌ Please save your board before exporting.",
                "Custom PnP CSV Exporter",
                wx.OK | wx.ICON_ERROR
            )
            return

        # Get the board origin (drill/plot origin) in internal units
        design_settings = board.GetDesignSettings()
        origin = design_settings.GetAuxOrigin()  # wxPoint in internal units
        ox = origin.x
        oy = origin.y

        # 1) Gather all footprints and build a row‐list
        rows = []
        for m in board.GetFootprints():
            ref    = m.GetReference()
            fields = m.GetFieldsShownText()  # dict[str,str]
            val    = fields.get(FIELD_LCSC, "").strip() or m.GetValue()
            hgt    = fields.get(FIELD_HEIGHT, "").strip()
            pkg    = m.GetFPIDAsString()

            pos = m.GetPosition()
            relx = pos.x - ox
            rely = pos.y - oy

            x_mm = pcbnew.ToMM(relx)
            y_mm = -pcbnew.ToMM(rely)  # invert Y axis
            rot  = m.GetOrientationDegrees()
            side = "top" if m.GetLayer() == pcbnew.F_Cu else "bottom"

            rows.append([
                ref,
                val,
                pkg,
                f"{x_mm:.4f}",
                f"{y_mm:.4f}",
                f"{rot:.3f}",
                side,
                hgt
            ])

        if not rows:
            wx.MessageBox(
                "❌ No footprints found on the board!",
                "Custom PnP CSV Exporter",
                wx.OK | wx.ICON_ERROR
            )
            return

        base   = os.path.splitext(path)[0]
        out_fn = base + "_custom.csv"
        now    = datetime.datetime.now().isoformat()

        with open(out_fn, "w", newline="", encoding="utf-8") as f:
            f.write(f"# Created on {now}\n")
            f.write("# Unit = mm, Angle = deg. Coordinates relative to board origin (Y inverted).\n")

            writer = csv.writer(f)
            writer.writerow(["Ref", "Val", "Package", "X (mm)", "Y (mm)", "Rot", "Side", "Height"])
            writer.writerows(rows)

        wx.MessageBox(
            f"✅ Wrote CSV PnP file to:\n{out_fn}",
            "Custom PnP CSV Exporter",
            wx.OK | wx.ICON_INFORMATION
        )

# Register in Tools → External Plugins
CustomCSVExporter().register()




































# #!/usr/bin/env python3
# import os
# import datetime
# import csv
# import pcbnew
# import wx

# # ← Exact keys of your custom footprint fields
# FIELD_LCSC   = "#LCSC"
# FIELD_HEIGHT = "#Height"

# class CustomCSVExporter(pcbnew.ActionPlugin):
#     def defaults(self):
#         self.name = "Custom PnP CSV Exporter"
#         self.category = "External Plugins"
#         self.description = (
#             "Generate a CSV PnP file using your "
#             f"'{FIELD_LCSC}' and '{FIELD_HEIGHT}' fields."
#         )

#     def Run(self):
#         board = pcbnew.GetBoard()
#         path  = board.GetFileName()
#         if not path:
#             wx.MessageBox(
#                 "❌ Please save your board before exporting.",
#                 "Custom PnP CSV Exporter",
#                 wx.OK | wx.ICON_ERROR
#             )
#             return

#         # 1) Gather all footprints and build a row‐list
#         footprints = list(board.GetFootprints())
#         rows = []
#         for m in footprints:
#             ref    = m.GetReference()
#             fields = m.GetFieldsShownText()  # dict[str,str]
#             val    = fields.get(FIELD_LCSC, "").strip() or m.GetValue()
#             hgt    = fields.get(FIELD_HEIGHT, "").strip()
#             pkg    = m.GetFPIDAsString()
#             pos    = m.GetPosition()
#             x_mm   = pcbnew.ToMM(pos.x)
#             y_mm   = pcbnew.ToMM(pos.y)
#             rot    = m.GetOrientationDegrees()
#             side   = "top" if m.GetLayer() == pcbnew.F_Cu else "bottom"
#             # Format numeric values as strings for CSV
#             rows.append([
#                 ref,
#                 val,
#                 pkg,
#                 f"{x_mm:.4f}",
#                 f"{y_mm:.4f}",
#                 f"{rot:.3f}",
#                 side,
#                 hgt
#             ])

#         if not rows:
#             wx.MessageBox(
#                 "❌ No footprints found on the board!",
#                 "Custom PnP CSV Exporter",
#                 wx.OK | wx.ICON_ERROR
#             )
#             return

#         # 2) Open CSV file and write comments + header + rows
#         base   = os.path.splitext(path)[0]
#         out_fn = base + "_custom.csv"
#         now    = datetime.datetime.now().isoformat()

#         with open(out_fn, "w", newline="", encoding="utf-8") as f:
#             # Optional comment lines
#             f.write(f"# Created on {now}\n")
#             f.write("# Unit = mm, Angle = deg.\n")

#             writer = csv.writer(f)
#             # Column titles compliant with OpenPnP CSV importer
#             writer.writerow([
#                 "Ref",
#                 "Val",
#                 "Package",
#                 "X (mm)",
#                 "Y (mm)",
#                 "Rot",
#                 "Side",
#                 "Height"
#             ])
#             # Write each footprint row
#             for row in rows:
#                 writer.writerow(row)

#         wx.MessageBox(
#             f"✅ Wrote CSV PnP file to:\n{out_fn}",
#             "Custom PnP CSV Exporter",
#             wx.OK | wx.ICON_INFORMATION
#         )

# # Register in Tools → External Plugins
# CustomCSVExporter().register()











#############################################################################################################################################################





# #!/usr/bin/env python3
# import os
# import datetime
# import pcbnew
# import wx

# # ← Exact keys of your custom footprint fields
# FIELD_LCSC   = "#LCSC"
# FIELD_HEIGHT = "#Height"

# class CustomPosExporter(pcbnew.ActionPlugin):
#     def defaults(self):
#         self.name = "Custom PnP Exporter"
#         self.category = "External Plugins"
#         self.description = (
#             "Generate a tabular PnP file using your "
#             f"'{FIELD_LCSC}' and '{FIELD_HEIGHT}' fields."
#         )

#     def Run(self):
#         board = pcbnew.GetBoard()
#         path  = board.GetFileName()
#         if not path:
#             wx.MessageBox(
#                 "❌ Please save your board before exporting.",
#                 "Custom PnP Exporter",
#                 wx.OK | wx.ICON_ERROR
#             )
#             return

#         # 1) Gather all footprints and build a row‐list
#         footprints = list(board.GetFootprints())
#         rows = []
#         for m in footprints:
#             ref    = m.GetReference()
#             fields = m.GetFieldsShownText()  # dict[str,str]
#             val    = fields.get(FIELD_LCSC, "").strip() or m.GetValue()
#             hgt    = fields.get(FIELD_HEIGHT, "").strip()
#             pkg    = m.GetFPIDAsString()
#             pos    = m.GetPosition()
#             x_mm   = pcbnew.ToMM(pos.x)
#             y_mm   = pcbnew.ToMM(pos.y)
#             rot    = m.GetOrientationDegrees()
#             side   = "F" if m.GetLayer() == pcbnew.F_Cu else "B"
#             rows.append((ref, val, pkg, x_mm, y_mm, rot, side, hgt))

#         if not rows:
#             wx.MessageBox(
#                 "❌ No footprints found on the board!",
#                 "Custom PnP Exporter",
#                 wx.OK | wx.ICON_ERROR
#             )
#             return

#         # 2) Compute column widths for the three text fields + height
#         w_ref = max(len("Ref"),     max(len(r[0]) for r in rows))
#         w_val = max(len("Val"),     max(len(r[1]) for r in rows))
#         w_pkg = max(len("Package"), max(len(r[2]) for r in rows))
#         w_hgt = max(len("Height"),  max(len(r[7]) for r in rows))

#         # 3) Open file and print header + rows with fixed‐width formatting
#         base   = os.path.splitext(path)[0]
#         out_fn = base + "_custom.pos"
#         now = datetime.datetime.now().isoformat()

#         with open(out_fn, "w", encoding="utf-8") as f:
#             # Header (you can tweak these to match your style)
#             f.write(f"### Created on {now}\n")
#             f.write("## Unit = mm, Angle = deg.\n")

#             # Column titles
#             f.write(
#                 f"{'Ref':<{w_ref}}  "
#                 f"{'Val':<{w_val}}  "
#                 f"{'Package':<{w_pkg}}  "
#                 f"{'PosX':>10}  "
#                 f"{'PosY':>10}  "
#                 f"{'Rot':>8}  "
#                 f"{'Side':<4}  "
#                 f"{'Height':>{w_hgt}}\n"
#             )

#             # Each footprint
#             for ref, val, pkg, x_mm, y_mm, rot, side, hgt in rows:
#                 f.write(
#                     f"{ref:<{w_ref}}  "
#                     f"{val:<{w_val}}  "
#                     f"{pkg:<{w_pkg}}  "
#                     f"{x_mm:>10.4f}  "
#                     f"{y_mm:>10.4f}  "
#                     f"{rot:>8.3f}  "
#                     f"{side:<4}  "
#                     f"{hgt:>{w_hgt}}\n"
#                 )

#         wx.MessageBox(
#             f"✅ Wrote aligned PnP file to:\n{out_fn}",
#             "Custom PnP Exporter",
#             wx.OK | wx.ICON_INFORMATION
#         )

# # Register in Tools → External Plugins
# CustomPosExporter().register()













#############################################################################################################################################################




# #!/usr/bin/env python3
# import os
# import datetime
# import pcbnew
# import wx

# # ← exact keys of your custom footprint fields:
# FIELD_LCSC   = "#LCSC"
# FIELD_HEIGHT = "#Height"

# class CustomPosExporter(pcbnew.ActionPlugin):
#     def defaults(self):
#         self.name = "Custom PnP Exporter"
#         self.category = "External Plugins"
#         self.description = (
#             "Generate a whitespace-delimited PnP file using the "
#             f"'{FIELD_LCSC}' and '{FIELD_HEIGHT}' footprint fields."
#         )

#     def Run(self):
#         board = pcbnew.GetBoard()
#         path  = board.GetFileName()
#         if not path:
#             wx.MessageBox(
#                 "❌ Please save your board before exporting.",
#                 "Custom PnP Exporter",
#                 wx.OK | wx.ICON_ERROR
#             )
#             return

#         base       = os.path.splitext(path)[0]
#         out_fn     = base + "_custom.pos"
#         footprints = list(board.GetFootprints())

#         if not footprints:
#             wx.MessageBox(
#                 "❌ No footprints found on the board!",
#                 "Custom PnP Exporter",
#                 wx.OK | wx.ICON_ERROR
#             )
#             return

#         # write a little header so it's obvious what's what
#         now = datetime.datetime.now().astimezone().isoformat()
#         with open(out_fn, "w", encoding="utf-8") as f:
#             f.write(f"### Created on {now}\n")
#             f.write("## Unit = mm, Angle = deg.\n")
#             f.write("# Ref Val Package PosX PosY Rot Side Height\n")

#             for m in footprints:
#                 ref    = m.GetReference()
#                 pkg    = m.GetFPIDAsString()                 # library-qualified footprint name :contentReference[oaicite:0]{index=0}
#                 pos    = m.GetPosition()
#                 x_mm   = pcbnew.ToMM(pos.x)
#                 y_mm   = pcbnew.ToMM(pos.y)
#                 rot    = m.GetOrientationDegrees()
#                 side   = "F" if m.GetLayer() == pcbnew.F_Cu else "B"

#                 # grab all of your custom fields at once
#                 fields = m.GetFieldsShownText()              # returns dict[str,str] of fields :contentReference[oaicite:1]{index=1}
#                 val     = fields.get(FIELD_LCSC, "").strip() or m.GetValue()
#                 height  = fields.get(FIELD_HEIGHT, "").strip()

#                 f.write(
#                     f"{ref} {val} {pkg} "
#                     f"{x_mm:.4f} {y_mm:.4f} {rot:.4f} {side} {height}\n"
#                 )

#         wx.MessageBox(
#             f"✅ Wrote PnP file with height column:\n{out_fn}",
#             "Custom PnP Exporter",
#             wx.OK | wx.ICON_INFORMATION
#         )

# CustomPosExporter().register()






#############################################################################################################################################################






# #!/usr/bin/env python3
# import os
# import datetime
# import pcbnew
# import wx

# # ← EXACTLY the name of your custom footprint field
# FIELD_NAME = "#LCSC"

# class CustomPosExporter(pcbnew.ActionPlugin):
#     def defaults(self):
#         self.name = "Custom PnP Exporter"
#         self.category = "External Plugins"
#         self.description = (
#             "Generate a whitespace‐delimited PnP file using the "
#             f"'{FIELD_NAME}' footprint field."
#         )

#     def Run(self):
#         board = pcbnew.GetBoard()
#         path  = board.GetFileName()
#         if not path:
#             wx.MessageBox(
#                 "❌ Please save your board before exporting.",
#                 "Custom PnP Exporter",
#                 wx.OK | wx.ICON_ERROR
#             )
#             return

#         base       = os.path.splitext(path)[0]
#         out_fn     = base + "_custom.pos"
#         footprints = list(board.GetFootprints())

#         if not footprints:
#             wx.MessageBox(
#                 "❌ No footprints found on the board!",
#                 "Custom PnP Exporter",
#                 wx.OK | wx.ICON_ERROR
#             )
#             return

#         # build header
#         now = datetime.datetime.now().astimezone().isoformat()
#         try:
#             version = pcbnew.GetBuildVersion()
#         except AttributeError:
#             version = "KiCad " + pcbnew.VERSION

#         with open(out_fn, "w", encoding="utf-8") as f:
#             f.write(f"### Footprint positions - created on {now} ###\n")
#             f.write(f"### Printed by KiCad version {version} ###\n")
#             f.write("## Unit = mm, Angle = deg.\n")
#             f.write("## Side : both\n")
#             f.write("# Ref Val Package PosX PosY Rot Side\n")

#             for m in footprints:
#                 ref    = m.GetReference()
#                 fields = m.GetFieldsShownText()
#                 val    = fields.get(FIELD_NAME, "").strip() or m.GetValue()
#                 pkg    = m.GetFPIDAsString()
#                 pos    = m.GetPosition()
#                 x_mm   = pcbnew.ToMM(pos.x)
#                 y_mm   = pcbnew.ToMM(pos.y)
#                 rot    = m.GetOrientationDegrees()
#                 side   = "F" if m.GetLayer() == pcbnew.F_Cu else "B"

#                 # whitespace-delimited, like KiCad’s own .pos
#                 f.write(
#                     f"{ref} {val} {pkg} "
#                     f"{x_mm:.4f} {y_mm:.4f} {rot:.4f} {side}\n"
#                 )

#         wx.MessageBox(
#             f"✅ Wrote PnP file:\n{out_fn}",
#             "Custom PnP Exporter",
#             wx.OK | wx.ICON_INFORMATION
#         )

# # register it in Tools → External Plugins
# CustomPosExporter().register()
