#!/usr/bin/env python3
import os,datetime,csv,pcbnew,wx
FIELD_LCSC="#LCSC"
FIELD_HEIGHT="#Height"
class CustomCSVExporter(pcbnew.ActionPlugin):
 def defaults(self):
  self.name="Custom PnP CSV Exporter"
  self.category="External Plugins"
  self.description=f"CSV export with {FIELD_LCSC} & {FIELD_HEIGHT} fields"
  self.icon_file_name="custom_icon.svg"
 def Run(self):
  board=pcbnew.GetBoard()
  path=board.GetFileName()
  if not path:
   wx.MessageBox("Save board first","Error",wx.OK|wx.ICON_ERROR)
   return
  origin=board.GetDesignSettings().GetAuxOrigin()
  ox,oy=origin.x,origin.y
  rows=[]
  for m in board.GetFootprints():
   ref=m.GetReference()
   fields=m.GetFieldsShownText()
   val=fields.get(FIELD_LCSC,"").strip()or m.GetValue()
   hgt=fields.get(FIELD_HEIGHT,"").strip()
   pkg=m.GetFPIDAsString()
   pos=m.GetPosition()
   x_mm=pcbnew.ToMM(pos.x-ox)
   y_mm=-pcbnew.ToMM(pos.y-oy)
   rot=m.GetOrientationDegrees()
   side="top"if m.GetLayer()==pcbnew.F_Cu else"bottom"
   rows.append([ref,val,pkg,f"{x_mm:.4f}",f"{y_mm:.4f}",f"{rot:.3f}",side,hgt])
  if not rows:
   wx.MessageBox("No footprints found","Error",wx.OK|wx.ICON_ERROR)
   return
  out_fn=os.path.splitext(path)[0]+"_custom.csv"
  with open(out_fn,"w",newline="",encoding="utf-8")as f:
   f.write(f"# Created {datetime.datetime.now().isoformat()}\n")
   f.write("# Unit=mm, Y inverted\n")
   writer=csv.writer(f)
   writer.writerow(["Ref","Val","Package","X","Y","Rot","Side","Height"])
   writer.writerows(rows)
  wx.MessageBox(f"Saved: {out_fn}","Success",wx.OK|wx.ICON_INFORMATION)
CustomCSVExporter().register()
