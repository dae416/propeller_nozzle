"""Convert the STL meshes to STEP.

--brep sews every triangle into a planar-faceted B-rep solid
(~52 MB/file). Universally importable as a solid. This is what ships in
STEP/ — CATIA and SpaceClaim reject tessellated AP242 with "No B-Rep data
in input file", so the heavy form is the one committed.

Default (no flag) writes AP242 *tessellated* STEP instead (~1.7 MB/file):
the exact mesh in a standard STEP container, for CAD packages that read it.

Requires: pip install cadquery-ocp
Usage:    python stl_to_step.py STL/ STEP/ [--brep]
"""
import sys
import pathlib

from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.Interface import Interface_Static
from OCP.IFSelect import IFSelect_RetDone
from OCP.RWStl import RWStl
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Face, TopoDS_Shell


def write_step(shape, path):
    writer = STEPControl_Writer()  # must exist before Interface_Static calls
    Interface_Static.SetCVal_s("write.step.schema", "AP242DIS")
    Interface_Static.SetIVal_s("write.step.tessellated", 1)
    Interface_Static.SetCVal_s("write.step.unit", "MM")
    writer.Transfer(shape, STEPControl_AsIs)
    if writer.Write(str(path)) != IFSelect_RetDone:
        raise RuntimeError(f"STEP write failed: {path}")


def tessellated_shape(tri):
    face = TopoDS_Face()
    b = BRep_Builder()
    b.MakeFace(face)
    b.UpdateFace(face, tri)
    shell = TopoDS_Shell()
    b.MakeShell(shell)
    b.Add(shell, face)
    return shell


def brep_shape(tri):
    from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakePolygon,
                                    BRepBuilderAPI_MakeFace,
                                    BRepBuilderAPI_Sewing,
                                    BRepBuilderAPI_MakeSolid)
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_SHELL
    from OCP.TopoDS import TopoDS
    sew = BRepBuilderAPI_Sewing(1e-6)
    for i in range(1, tri.NbTriangles() + 1):
        i1, i2, i3 = tri.Triangle(i).Get()
        poly = BRepBuilderAPI_MakePolygon(tri.Node(i1), tri.Node(i2), tri.Node(i3), True)
        face = BRepBuilderAPI_MakeFace(poly.Wire())
        if face.IsDone():
            sew.Add(face.Face())
    sew.Perform()
    shape = sew.SewedShape()
    exp = TopExp_Explorer(shape, TopAbs_SHELL)
    if exp.More():
        shell = TopoDS.Shell_s(exp.Current())
        if shell.Closed():
            mk = BRepBuilderAPI_MakeSolid(shell)
            if mk.IsDone():
                shape = mk.Solid()
    return shape


if __name__ == "__main__":
    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    brep = "--brep" in sys.argv
    dst.mkdir(exist_ok=True)
    for stl in sorted(src.glob("*.stl")):
        tri = RWStl.ReadFile_s(str(stl))
        if tri is None:
            raise RuntimeError(f"cannot read {stl}")
        out = dst / (stl.stem + ".step")
        write_step(brep_shape(tri) if brep else tessellated_shape(tri), out)
        print(f"{stl.name} -> {out.name} ({out.stat().st_size // 1024} KB)")
