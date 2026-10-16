# Lightsaber Remote - Aussenhuelle (generisches Design, Halbschalen), rechte Hand
# Achse = Z, Pommel unten (z=0), Emitter oben. Vorne = +Y (Daumen/Stick), +X = von vorne gesehen links (Zeigefinger).
# Ausfuehren in Blender:  exec(open(r"...\build_lightsaber.py").read())   mit globals FORM_CTRL = "KASTEN" | "DICK"
import bpy, bmesh, math, mathutils

FORM_CTRL = globals().get("FORM_CTRL", "KASTEN")   # KASTEN = aufgesetzte Bedienplatte, DICK = verdickter Griff mit flacher Front

# ---------------- Parameter ----------------
R = 21.0                 # Griffradius (Ø 42)
R_BORE = 18.0            # Innenradius
SEG = 128                # Rundheit
WALL = 2.0

# Abschnitte (z von unten nach oben)
Z_POMMEL = (0.0, 34.0)
Z_GRIP_RIBS = (36.0, 64.0)       # umlaufende Grip-Rillen + T-Tracks
Z_CONTROL = (66.0, 168.0)        # Bedienbereich
Z_FLUTES = (172.0, 212.0)        # Laengsrillen
Z_NECK = (212.0, 222.0)
Z_EMITTER = (222.0, 270.0)

RIB_PITCH, RIB_GROOVE, RIB_DEPTH = 5.0, 2.0, 1.2
FLUTES, FLUTE_W, FLUTE_DEPTH = 10, 3.0, 2.0
VENTS, VENT_W, VENT_Z, VENT_DEPTH = 6, 4.0, (231.0, 258.0), 2.6
POMMEL_R, POMMEL_FLATS = 23.5, 6
POMMEL_NOTCH, POMMEL_NOTCH_W, POMMEL_NOTCH_H = 8, 4.0, 4.0
RAILS, RAIL_W, RAIL_H = 8, 3.0, 1.6
CROWN, CROWN_W, CROWN_H = 8, 4.5, 5.0
EMITTER_CUT = 14.0

# Bedienplatte vorne
PLATE_Z, PLATE_W = (68.0, 164.0), 30.0
PRINT_VERT = globals().get("PRINT_VERT", False)  # Schalen stehend drucken (Pommel unten): alle Ueberhaenge <= 45 Grad
SEGMENTED = globals().get("SEGMENTED", False)     # Schalen oberhalb des Bedienbereichs geteilt, Emitter-Rohr aufgeschraubt (kuerzere Schalen)
Z_JOINT, JOINT_L = 186.0, 14.0                    # SEGMENTED: Schulter + Gewindestutzen (voll Gewinde) fuer das Emitter-Rohr
GRIP_STYLE = globals().get("GRIP_STYLE", "")   # "" (glatt), "GRENADE", "RIBS", "PANELS": Griff-Alternative im Bedienbereich
KASTEN_DROP = globals().get("KASTEN_DROP", 0.0)      # Alternative: Kasten (samt Front-Modulen) um x mm abgesenkt
PLATE_Y = (23.5 - KASTEN_DROP) if FORM_CTRL == "KASTEN" else 19.5    # Oberflaeche der flachen Front
R_CTRL = 24.0                                         # nur DICK: Radius im Bedienbereich (Ø 48)
JZ, JOY_X, JOY_HOLE = 124.0, -0.5, 17.0               # Joystick
DISP_C, DISP_WIN = (0.0, 149.6), (10.0, 7.0)          # Display-Fenster Mitte (x, z), Groesse
BTN23 = [(x, z) for x in (-3.0, 3.0) for z in (79.5, 88.0, 96.5)]
BTN_HOLE, BTN_SINK_D, BTN_SINK_T = 3.2, 6.5, 1.0
# Seitliche Leiste (modular 1x3/1x4/1x5), Seite +X
SIDE_Z0, SIDE_N, SIDE_PITCH, SIDE_SLOT = 85.5, 5, 6.0, 0.5   # unterster Taster 1x5/1x4, 1x3 sitzt +0.5
# Gewinde + Kraenze (Deko-Ringe halten die Schalen an den Enden zusammen)
TH_PITCH, TH_DEPTH, TH_CLEAR = 2.5, 1.2, 0.3
TH_MAJ = 20.5                          # Aussengewinde der Schalen (Spitzen), Kern = TH_MAJ - TH_DEPTH
Z_TH_BOT = (2.3, 30.2)                 # Gewindestutzen unten (Pommel)
Z_TH_TOP = (236.3, 267.7)              # Gewindestutzen oben (Emitter)
R_CORE_END = 16.0                      # Innenradius in den Gewindezonen (Wand bleibt stabil)
TH_FRAC = 0.5                          # nur die aeussere Haelfte jedes Stutzens hat Gewinde, Rest = Fuehrungsbund
USB_HOLE = 24.0                        # rundes Loch fuer USB-C (Pommel-Kranz dreht sich)
# Schalen-Schrauben M2 Senkkopf von hinten (x, z)
SCREWS = [(-14.5, 95.0), (14.5, 125.0), (-14.5, 160.0), (14.5, 160.0)]   # frei von Hauptplatine und Seitenleiste (bis 1x5)
# PAIR-Loch (Hauptplatine: Taster bei Platine x3.7 / y47; Platine links bei x=-12.75, unten bei z=4.5)
PAIR_XZ, PAIR_HOLE = (12.75 - 3.7, 4.5 + 47.0), 2.0   # von vorne gesehen: Platinen-links = +X
DOWELS = [(-15.5, 45.0), (15.5, 45.0), (-15.5, 232.0), (15.5, 232.0)]   # Passstifte statt Falz (Trennflaechen bleiben flach)
DOWEL_D, DOWEL_L = 3.0, 8.5
DOWEL_DOME = 6.0
SIZE = globals().get("SIZE", "STANDARD")         # "STANDARD" (Ø42, 270) oder "SLIM" (Ø38, ~244)
GY_Z0_SET = 164.0
# Ein/Aus-Schiebeschalter (wie Mini Remote): Gehaeuse 8.6 x 4.4 x ~4.5, Hebel 5 mm, Schlitz 6 mm Weg
SW_Z, SW_L, SW_W, SW_H = 85.0, 8.6, 4.4, 4.5
SW_SLOT_L, SW_SLOT_W, SW_CL = 6.0, 3.0, 0.2
BAT_TYPE = globals().get("BAT_TYPE", "902540")   # Akku unter der Hauptplatine: "902540" (25 breit) oder "902040" (20 breit)
MB_Y_SET = 1.5                                   # Hauptplatine: Unterseite auf der Achse (Akku passt darunter)
PAIR_TUBE_Y0 = MB_Y_SET + 1.6 + 3.7              # PAIR-Fuehrung endet 3.7 ueber der Platine
# Hauptplatine gedreht (nur STANDARD): Bauteile nach hinten (Rueckschale = Montagedeckel), Akku vor der Platine
MB_FLIP = globals().get("MB_FLIP", SIZE != "SLIM")
if MB_FLIP:
    MB_Y_SET = 1.4                               # Platine y 1.4..3.0, Bauteilseite (1.4) zeigt nach hinten
USB_YC = MB_Y_SET - 1.0 - 1.6                    # MB_FLIP: Mitte USB-C (XIAO auf der Rueckseite)
USB_RECT = (12.5, 7.0)                           # MB_FLIP: kleines USB-Loch im Schalen-Ende
if SIZE == "SLIM":
    R, R_BORE = 19.0, 16.0
    Z_FLUTES, Z_NECK, Z_EMITTER = (172.0, 186.0), (186.0, 196.0), (196.0, 244.0)
    VENT_Z = (205.0, 232.0)
    POMMEL_R = 21.5
    PLATE_Y = 21.5
    TH_MAJ = 18.5
    Z_TH_TOP = (Z_EMITTER[0] + 14.3, Z_EMITTER[1] - 2.3)
    R_CORE_END = 14.0
    DOWELS = [(-14.2, 45.0), (14.2, 45.0), (-14.2, Z_TH_TOP[0] - 4.0), (14.2, Z_TH_TOP[0] - 4.0)]
    DOWEL_DOME = 5.0
SPLIT_Y = -8.03         # gerade Teilung parallel zur Front, 8 mm hinter der Achse (Vorderschale nimmt alle Module auf)

# ---------------- Helfer ----------------
COL = "Lightsaber_" + FORM_CTRL + ("_LOW%g" % KASTEN_DROP if KASTEN_DROP else "") + ("_VERT" if PRINT_VERT else "") + ("_SEG" if SEGMENTED else "") + ("_SLIM" if SIZE == "SLIM" else "") + ("" if BAT_TYPE == "902540" else "_" + BAT_TYPE) + ("_" + GRIP_STYLE if GRIP_STYLE else "")
col = bpy.data.collections.get(COL)
if col is None:
    col = bpy.data.collections.new(COL); bpy.context.scene.collection.children.link(col)
for o in list(col.objects):
    bpy.data.objects.remove(o, do_unlink=True)
col.hide_viewport = False                       # ausgeblendete Sammlung -> Booleans greifen nicht!
def _lc(lc):
    if lc.collection == col: return lc
    for c in lc.children:
        r = _lc(c)
        if r: return r
_l = _lc(bpy.context.view_layer.layer_collection)
if _l: _l.exclude = False; _l.hide_viewport = False

def mkobj(name, bm):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); col.objects.link(o); return o

def revolve(name, prof, seg=SEG):
    bm = bmesh.new(); rings = []
    for r, z in prof:
        rings.append([bm.verts.new((r*math.cos(2*math.pi*i/seg), r*math.sin(2*math.pi*i/seg), z)) for i in range(seg)])
    for a, b in zip(rings, rings[1:]):
        for i in range(seg):
            j = (i + 1) % seg; bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(rings[0][::-1]); bm.faces.new(rings[-1])
    return mkobj(name, bm)

def obox(name, cx, cy, ln, wd, z0, z1, ang):
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); vx, vy = -uy, ux
    pts = [(cx + sx*ln/2*ux + sy*wd/2*vx, cy + sx*ln/2*uy + sy*wd/2*vy) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    bm = bmesh.new()
    b = [bm.verts.new((x, y, z0)) for x, y in pts]; t = [bm.verts.new((x, y, z1)) for x, y in pts]
    bm.faces.new(b[::-1]); bm.faces.new(t)
    for i in range(4):
        j = (i+1) % 4; bm.faces.new((b[i], b[j], t[j], t[i]))
    return mkobj(name, bm)

def box(name, x0, x1, y0, y1, z0, z1):
    return obox(name, (x0+x1)/2, (y0+y1)/2, x1-x0, y1-y0, z0, z1, 0)

def cyl_axis(name, axis, a0, a1, p, q, d0, d1=None, seg=48):
    """liegender Zylinder/Kegel entlang X oder Y von a0 (d0) bis a1 (d1); (p, q) = die anderen Koordinaten (x|y, z)"""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=d0/2, radius2=(d1 if d1 else d0)/2, depth=a1-a0)
    rot = mathutils.Matrix.Rotation(math.pi/2, 4, 'Y') if axis == "X" else mathutils.Matrix.Rotation(-math.pi/2, 4, 'X')
    bmesh.ops.transform(bm, matrix=rot, verts=bm.verts)
    c = (a0 + a1) / 2
    bmesh.ops.translate(bm, verts=bm.verts, vec=(c, p, q) if axis == "X" else (p, c, q))
    return mkobj(name, bm)

def bevel_all(obj, r, seg=4):
    bm = bmesh.new(); bm.from_mesh(obj.data)
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=r, offset_type='OFFSET', segments=seg, profile=0.5, affect='EDGES', clamp_overlap=True)
    bm.to_mesh(obj.data); bm.free()

def boolean(target, tool, op='DIFFERENCE'):
    m = target.modifiers.new("b", 'BOOLEAN'); m.operation = op; m.object = tool; m.solver = 'EXACT'
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(target.evaluated_get(dg))
    target.modifiers.remove(m); old = target.data; target.data = me; bpy.data.meshes.remove(old)
    bpy.data.objects.remove(tool, do_unlink=True)

def ring_of(n, offset, fn):
    for i in range(n):
        fn(360 * i / n + offset)

# ---------------- Profil (Schalen) ----------------
TH_MIN = TH_MAJ - TH_DEPTH
# Teilungs-Gewinde (SEGMENTED) kleiner als die End-Gewinde: sonst bleibt am Emitter-Rohr ueber dem Innengewinde
# nur 0.2 mm Wand (Fehler bis 2026-10-15: Rohr unten nur noch Gewindegang -> leere Schichten)
TH_J_MAJ = globals().get("TH_J_MAJ", R - 3.5)
TH_J_MIN = TH_J_MAJ - TH_DEPTH
RI_J = TH_J_MAJ + TH_CLEAR
R_CORE_J = TH_J_MIN - 2.0                  # Innenradius im Teilungszapfen (Wand 2 mm)
R_CORE_TOP = R_CORE_J if SEGMENTED else R_CORE_END
ZM_BOT = Z_TH_BOT[0] + (Z_TH_BOT[1] - Z_TH_BOT[0]) * TH_FRAC
ZM_TOP = Z_TH_TOP[1] - (Z_TH_TOP[1] - Z_TH_TOP[0]) * TH_FRAC
P = [(TH_MIN, Z_TH_BOT[0]), (TH_MIN, ZM_BOT), (TH_MAJ, ZM_BOT), (TH_MAJ, Z_TH_BOT[1]), (R + 1.0, Z_TH_BOT[1]), (R + 1.0, Z_POMMEL[1] - 1.0),
     (R - 1.5, Z_POMMEL[1]), (R - 1.5, Z_GRIP_RIBS[0] - (1.5 if PRINT_VERT else 0.0)), (R, Z_GRIP_RIBS[0])]
z = Z_GRIP_RIBS[0] + RIB_PITCH - RIB_GROOVE
while z + RIB_GROOVE <= Z_GRIP_RIBS[1]:
    if PRINT_VERT:   # obere Flanke 45 Grad (stehend ohne Ueberhang)
        P += [(R, z), (R - RIB_DEPTH, z + 0.4), (R - RIB_DEPTH, z + RIB_GROOVE - RIB_DEPTH), (R, z + RIB_GROOVE)]
    else:
        P += [(R, z), (R - RIB_DEPTH, z + 0.4), (R - RIB_DEPTH, z + RIB_GROOVE - 0.4), (R, z + RIB_GROOVE)]
    z += RIB_PITCH
P += [(R, Z_GRIP_RIBS[1]), (R - 1.5, Z_GRIP_RIBS[1]), (R - 1.5, Z_CONTROL[0] - (1.5 if PRINT_VERT else 0.0)), (R, Z_CONTROL[0])]
if FORM_CTRL == "DICK":
    P += [(R_CTRL, Z_CONTROL[0] + 4), (R_CTRL, Z_CONTROL[1] - 4), (R, Z_CONTROL[1])]
_v = 1.0 if PRINT_VERT else 0.0                # stehend: nach aussen gehende Stufen als 45-Grad-Schraege
P += [(R, Z_CONTROL[1]), (R - 1.5, Z_CONTROL[1]), (R - 1.5, Z_CONTROL[1] + 2 - 2.0*_v), (R + 0.6, Z_CONTROL[1] + 2 + 0.1*_v),
      (R + 0.6, Z_FLUTES[0]), (R, Z_FLUTES[0])]
# oberer Teil (Laengsrillen, Hals, Emitter, Stutzen fuer den Emitter-Kranz) - bei SEGMENTED als eigenes Emitter-Rohr
P_TOP = [(R, Z_FLUTES[1]),
      (R - 1.5, Z_NECK[0]), (R - 1.5, Z_NECK[0] + 2 - 1.8*_v), (R + 0.3, Z_NECK[0] + 2), (R + 0.3, Z_NECK[0] + 5),
      (R - 1.5, Z_NECK[0] + 5), (R - 1.5, Z_NECK[1] - 0.5*_v),
      (R, Z_EMITTER[0] + 1), (R + 1.5, Z_EMITTER[0] + 8), (R + 1.5, Z_TH_TOP[0]), (TH_MAJ, Z_TH_TOP[0]), (TH_MAJ, ZM_TOP), (TH_MIN, ZM_TOP), (TH_MIN, Z_TH_TOP[1])]
if SEGMENTED:   # Schalen enden mit Schulter + vollem Gewindestutzen
    P += [(R, Z_JOINT), (TH_J_MIN, Z_JOINT), (TH_J_MIN, Z_JOINT + JOINT_L)]
else:
    P += P_TOP
shell = revolve("Huelle", P)
Z_TOPZONE = (Z_JOINT - 6.0) if SEGMENTED else (Z_TH_TOP[0] - 8.0)     # ab hier enger (Gewindestutzen oben)
Z_TOP_END = (Z_JOINT + JOINT_L) if SEGMENTED else Z_TH_TOP[1]
if SEGMENTED:   # obere Passstifte unter die Teilung
    DOWELS = [(x, (Z_JOINT - 8.0 if z > Z_JOINT else z)) for x, z in DOWELS]

def thread_ridge(name, r_base, r_tip, z0, z1, pitch, w_base, w_tip, seg=48):
    """schraubenfoermiger Gewindegang (Trapezprofil) von r_base nach r_tip, z0..z1"""
    bm = bmesh.new(); prof = []
    turns = (z1 - z0 - w_base) / pitch
    n = max(2, int(turns * seg))
    for i in range(n + 1):
        a = 2 * math.pi * i / seg; zc = z0 + w_base/2 + pitch * i / seg
        ca, sa = math.cos(a), math.sin(a)
        pts = [(r_base, zc - w_base/2), (r_tip, zc - w_tip/2), (r_tip, zc + w_tip/2), (r_base, zc + w_base/2)]
        prof.append([bm.verts.new((r*ca, r*sa, zz)) for r, zz in pts])
    for a_, b_ in zip(prof, prof[1:]):
        for k in range(4):
            l = (k + 1) % 4; bm.faces.new((a_[k], a_[l], b_[l], b_[k]))
    bm.faces.new(prof[0][::-1]); bm.faces.new(prof[-1])
    return mkobj(name, bm)

# Aussengewinde an den Schalen
for z0, z1, rb, rt in ((Z_TH_BOT[0] + 0.6, ZM_BOT - 0.3, TH_MIN, TH_MAJ),
                       ((Z_JOINT + 0.3, Z_JOINT + JOINT_L - 0.6, TH_J_MIN, TH_J_MAJ) if SEGMENTED else (ZM_TOP + 0.3, Z_TH_TOP[1] - 0.6, TH_MIN, TH_MAJ))):
    boolean(shell, thread_ridge("t", rb - 0.1, rt, z0, z1, TH_PITCH, 1.9, 0.5), 'UNION')

# ---------------- Deko an den Schalen ----------------
def radial_prism(name, a, poly, w):
    """Prisma: Profil poly in (r, z) bei Winkel a, Breite w tangential"""
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); tx, ty = -sa, ca
    bm = bmesh.new()
    A = [bm.verts.new((r*ca - tx*w/2, r*sa - ty*w/2, z)) for r, z in poly]
    B = [bm.verts.new((r*ca + tx*w/2, r*sa + ty*w/2, z)) for r, z in poly]
    bm.faces.new(A); bm.faces.new(B[::-1]); n = len(poly)
    for i in range(n):
        j = (i + 1) % n; bm.faces.new((A[j], A[i], B[i], B[j]))
    return mkobj(name, bm)
def rail(a):
    if PRINT_VERT:   # Unterkante 45 Grad angeschraegt
        z0, z1, ri, ro = Z_GRIP_RIBS[0] + 2, Z_GRIP_RIBS[1] - 2, R - 1.0, R + RAIL_H
        rl = radial_prism("t", a, [(ri, z0), (ro - 0.4, z0 + RAIL_H + 1.0 - 0.4), (ro, z0 + RAIL_H + 1.0), (ro, z1 - 0.5), (ro - 0.5, z1), (ri, z1)], RAIL_W)
        boolean(shell, rl, 'UNION'); return
    d = R + RAIL_H / 2 - 1.0
    rl = obox("t", d*math.cos(math.radians(a)), d*math.sin(math.radians(a)), RAIL_H + 2.0, RAIL_W, Z_GRIP_RIBS[0] + 2, Z_GRIP_RIBS[1] - 2, a)
    bevel_all(rl, 0.5, 2); boolean(shell, rl, 'UNION')
ring_of(RAILS, 180 / RAILS, rail)
def flute(a):
    if PRINT_VERT:   # Rillen-Ende oben 45 Grad (keine haengende Decke)
        z0, z1 = Z_FLUTES[0] + 4, Z_FLUTES[1] - 4
        boolean(shell, radial_prism("t", a, [(R - FLUTE_DEPTH, z0), (R + 5, z0), (R + 5, z1), (R, z1), (R - FLUTE_DEPTH, z1 - FLUTE_DEPTH)], FLUTE_W)); return
    d = R - FLUTE_DEPTH + 5
    boolean(shell, obox("t", d*math.cos(math.radians(a)), d*math.sin(math.radians(a)), 10, FLUTE_W, Z_FLUTES[0] + 4, Z_FLUTES[1] - 4, a))
if not SEGMENTED or Z_FLUTES[1] <= Z_JOINT: ring_of(FLUTES, 180 / FLUTES, flute)   # SLIM: Rillen bleiben an der Schale

# ---------------- Griff-Alternativen im Bedienbereich (GRIP_STYLE, 2026-10-15) ----------------
# erhabene Elemente (Pyramidenstumpf, alle Flanken 45 Grad -> flach und stehend stuetzfrei) auf Rueckseite + Seiten,
# frei bleiben: Bedienkasten (vorne), Seitentasten (+X), Ein/Aus-Schalter (-X), Schraubensenkungen (hinten), Teilungsebene
if GRIP_STYLE:
    GS = {"GRENADE": dict(phis=[157.5 + 22.5*k for k in range(11)], w=6.0, h=1.2, seg=6.0, gap=2.5),
          "RIBS":    dict(phis=[157.5 + 15.0*k for k in range(16)], w=4.0, h=1.0, seg=999.0, gap=0.0),
          "PANELS":  dict(phis=[156.0 + 24.0*k for k in range(10)], w=7.5, h=1.0, seg=26.0, gap=3.0)}[GRIP_STYLE]
    GZ0, GZ1 = Z_CONTROL[0] + 6.0, Z_CONTROL[1] - 6.0
    phis_split = [180.0 + math.degrees(math.asin(-SPLIT_Y / R)), 360.0 - math.degrees(math.asin(-SPLIT_Y / R))]
    def _adist(a, b): return abs((a - b + 180.0) % 360.0 - 180.0)
    ZONES = [(0.0, 14.0, SIDE_Z0 - 6.5, SIDE_Z0 + (SIDE_N - 1) * SIDE_PITCH + SIDE_SLOT + 6.5),     # Seitentasten
             (180.0, 12.0, SW_Z - 9.0, SW_Z + 9.0)]                                                 # Schalter
    for x_, z_ in SCREWS:
        ZONES.append((math.degrees(math.atan2(-math.sqrt(R**2 - x_**2), x_)) % 360.0, math.degrees(5.5 / R), z_ - 5.5, z_ + 5.5))
    gbm = bmesh.new()
    def g_block(phi, z0, z1, w, h):
        ca, sa = math.cos(math.radians(phi)), math.sin(math.radians(phi)); n = (ca, sa); t = (-sa, ca)
        bw = w / 2; r0 = math.sqrt(R**2 - bw**2) - 0.4; d = R + h - r0; tw = max(bw - d, 0.3); tz0, tz1 = z0 + d, z1 - d
        if tz1 - tz0 < 0.6: tz0, tz1 = (z0 + z1) / 2 - 0.3, (z0 + z1) / 2 + 0.3
        def P(r, s, z): return gbm.verts.new((r*n[0] + s*t[0], r*n[1] + s*t[1], z))
        B = [P(r0, -bw, z0), P(r0, bw, z0), P(r0, bw, z1), P(r0, -bw, z1)]
        T = [P(R + h, -tw, tz0), P(R + h, tw, tz0), P(R + h, tw, tz1), P(R + h, -tw, tz1)]
        gbm.faces.new(B[::-1]); gbm.faces.new(T)
        for i in range(4):
            j = (i + 1) % 4; gbm.faces.new((B[i], B[j], T[j], T[i]))
    for phi in [ph + globals().get("GRIP_PHI_OFF", 0.0) for ph in GS["phis"]]:   # GRIP_PHI_OFF: Versatz falls ein Boolean zickt
        aw = math.degrees(GS["w"] / 2 / R)
        if any(_adist(phi, ps) < aw + 1.5 for ps in phis_split): continue          # keine Elemente ueber der Teilung
        if _adist(phi, 90.0) < aw + 50.0: continue                                  # Bedienkasten
        zs = [GZ0 + 0.5 * i for i in range(int((GZ1 - GZ0) / 0.5) + 1)]
        ok = [not any(_adist(phi, za) < aw + zw and zl <= z <= zh for za, zw, zl, zh in ZONES) for z in zs]
        runs, cur = [], None
        for z, o in zip(zs, ok):
            if o: cur = [cur[0], z] if cur else [z, z]
            elif cur: runs.append(cur); cur = None
        if cur: runs.append(cur)
        for z0, z1 in runs:
            if z1 - z0 < min(GS["seg"], 6.0): continue
            n_ = max(1, int((z1 - z0 + GS["gap"]) // (GS["seg"] + GS["gap"]))) if GS["seg"] < 900 else 1
            L = (z1 - z0 - (n_ - 1) * GS["gap"]) / n_ if GS["seg"] < 900 else z1 - z0
            if GS["seg"] < 900 and GRIP_STYLE == "GRENADE": L = GS["seg"]; n_ = int((z1 - z0 + GS["gap"]) // (L + GS["gap"]))
            off = (z1 - z0 - (n_ * L + (n_ - 1) * GS["gap"])) / 2
            for k in range(n_):
                za = z0 + off + k * (L + GS["gap"]); g_block(phi, za, za + L, GS["w"], GS["h"])
    gob = mkobj("t", gbm)
    boolean(shell, gob, 'UNION')

# ---------------- Bedienplatte ----------------
if FORM_CTRL == "KASTEN":
    if PLATE_Y < R + 0.5:   # abgesenkt: Rohr ragt sonst ueber die Platte -> im Plattenbereich flach abschneiden
        boolean(shell, box("t", -PLATE_W/2 + 0.5, PLATE_W/2 - 0.5, PLATE_Y - 0.5, 60, PLATE_Z[0] + 0.5, PLATE_Z[1] - 0.5))
    cb = box("t", -PLATE_W/2, PLATE_W/2, R - 8, PLATE_Y, PLATE_Z[0], PLATE_Z[1])
    bevel_all(cb, 2.0); boolean(shell, cb, 'UNION')
    # (stehend: Unterkante des Kastens wird mit Support gedruckt - keine Rampe, Wunsch)
else:
    boolean(shell, box("t", -40, 40, PLATE_Y, 60, PLATE_Z[0], PLATE_Z[1]))

# ---------------- Hohlraum ----------------
boolean(shell, revolve("t", [(R_CORE_END, Z_TH_BOT[0] + 2.0), (R_CORE_END, Z_TH_BOT[1] + 0.5), (R_BORE, Z_TH_BOT[1] + 2.0),
                             (R_BORE, Z_TOPZONE), (R_CORE_TOP, Z_TOPZONE + (R_BORE - R_CORE_TOP)), (R_CORE_TOP, Z_TOP_END + 5.0)]))
boolean(shell, box("t", -PLATE_W/2 + WALL, PLATE_W/2 - WALL, 0, PLATE_Y - WALL, PLATE_Z[0] + WALL, PLATE_Z[1] - WALL))
if FORM_CTRL == "DICK":
    inner = revolve("t", [(R_CTRL - WALL, Z_CONTROL[0] + 6), (R_CTRL - WALL, Z_CONTROL[1] - 6)])
    boolean(inner, box("t", -60, 60, -60, PLATE_Y - WALL, -10, 400), 'INTERSECT')
    boolean(shell, inner)
if MB_FLIP:   # kleines USB-Loch genau an der Buchse (Schalen drehen sich nicht)
    boolean(shell, box("t", -USB_RECT[0] / 2, USB_RECT[0] / 2, USB_YC - USB_RECT[1] / 2, USB_YC + USB_RECT[1] / 2, Z_TH_BOT[0] - 1, Z_TH_BOT[0] + 3))
else:
    boolean(shell, revolve("t", [(USB_HOLE / 2, Z_TH_BOT[0] - 1), (USB_HOLE / 2, Z_TH_BOT[0] + 3)]))     # USB-Durchgang unten

# ---------------- Oeffnungen vorne / seitlich ----------------
boolean(shell, cyl_axis("t", "Y", 0, PLATE_Y + 5, JOY_X, JZ, JOY_HOLE, seg=96))
boolean(shell, box("t", DISP_C[0] - DISP_WIN[0]/2, DISP_C[0] + DISP_WIN[0]/2, 0, PLATE_Y + 5, DISP_C[1] - DISP_WIN[1]/2, DISP_C[1] + DISP_WIN[1]/2))
for x, z in BTN23:
    boolean(shell, cyl_axis("t", "Y", 0, PLATE_Y + 5, x, z, BTN_HOLE))
    boolean(shell, cyl_axis("t", "Y", PLATE_Y - BTN_SINK_T, PLATE_Y + 0.01, x, z, BTN_HOLE + 1.0, BTN_SINK_D))
r_side = (R_CTRL if FORM_CTRL == "DICK" else R)
for k in range(SIDE_N):
    zc = SIDE_Z0 + k * SIDE_PITCH
    for zz in (zc, zc + SIDE_SLOT):
        boolean(shell, cyl_axis("t", "X", 0, r_side + 5, 0.0, zz, BTN_HOLE))
    boolean(shell, box("t", 0, r_side + 5, -BTN_HOLE/2, BTN_HOLE/2, zc, zc + SIDE_SLOT))
# PAIR: Fuehrungsroehrchen + 2-mm-Loch
yo = math.sqrt(max(R**2 - PAIR_XZ[0]**2, 0)) + 1
if not MB_FLIP:
    boolean(shell, cyl_axis("t", "Y", PAIR_TUBE_Y0, yo - 1.5, PAIR_XZ[0], PAIR_XZ[1], 4.5), 'UNION')
    boolean(shell, cyl_axis("t", "Y", 0.0, yo + 3, PAIR_XZ[0], PAIR_XZ[1], PAIR_HOLE))
PAIR_RIB = (PAIR_XZ[0] + 2.25, PAIR_TUBE_Y0, PAIR_XZ[1])     # 45-Grad-Rippe, wird nach den Hilfsfunktionen gesetzt

# ---------------- Innenleben: Halter fuer die Module (alles in der Vorderschale) ----------------
# Platinen-Oberseite der Front-Module (Joystick, Display, 2x3) liegt einheitlich bei y = BOARD_TOP
BOARD_TOP = PLATE_Y - WALL - 5.3
BTN23_TOP = BOARD_TOP + 1.5                # 2x3-Taster 1.5 mm naeher an die Front (Drucktest)
POST_D, PILOT_D, PILOT_T = 4.5, 1.8, 5.0

def inner_front_y(x, z):
    """y der Innenwand vorne an Stelle (x, z)"""
    if PLATE_Z[0] + WALL <= z <= PLATE_Z[1] - WALL and abs(x) <= PLATE_W / 2 - WALL:
        return PLATE_Y - WALL
    r = (R_CORE_END if z < Z_TH_BOT[1] + 2.0 else R_CORE_TOP) if (z < Z_TH_BOT[1] + 2.0 or z > Z_TOPZONE) else R_BORE
    return math.sqrt(max(r*r - x*x, 0.0))

def in_cavity(x, y, z):
    if PLATE_Z[0] + WALL < z < PLATE_Z[1] - WALL and abs(x) < PLATE_W / 2 - WALL and 0 < y < PLATE_Y - WALL:
        return True
    r = (R_CORE_END if z < Z_TH_BOT[1] + 2.0 else R_CORE_TOP) if (z < Z_TH_BOT[1] + 2.0 or z > Z_TOPZONE) else R_BORE
    return x*x + y*y < r*r

def gusset(x_e, y_b, z, sx, th=1.6):
    """45-Grad-Rippe von der Unterkante einer haengenden Stuetze (x_e = Aussenkante, y_b = Unterkante) schraeg runter in die Wand.
    Druckrichtung +Y: die Unterseite der Rippe ist 45 Grad, die Stuetze waechst damit ohne Support."""
    t = 0.0
    while in_cavity(x_e + sx*t, y_b - t, z) and t < 40: t += 0.25
    t += 1.0
    pts = [(x_e - sx*0.6, y_b + 3.0), (x_e - sx*0.6, y_b), (x_e + sx*t, y_b - t)]
    bm = bmesh.new()
    a = [bm.verts.new((x, y, z - th/2)) for x, y in pts]; b = [bm.verts.new((x, y, z + th/2)) for x, y in pts]
    bm.faces.new(a); bm.faces.new(b[::-1])
    for i in range(3):
        j = (i + 1) % 3; bm.faces.new((a[i], a[j], b[j], b[i]))
    boolean(shell, mkobj("t", bm), 'UNION')

def vwedge(x, y, z, hx, hy, w, extra=1.0):
    """Stehend-Druck: 45-Grad-Stuetzrippe unter einem waagerecht auskragenden Teil.
    Startet bei (x, y, z) (Unterkante), laeuft in Richtung (hx, hy) zur Wand und faellt dabei 1:1 ab."""
    t = 0.0
    while in_cavity(x + hx*t, y + hy*t, z - t) and t < 40: t += 0.25
    t += extra
    px, py = -hy, hx
    pts = [(x, y, z + 0.5), (x + hx*t, y + hy*t, z + 0.5), (x + hx*t, y + hy*t, z - t)]
    bm = bmesh.new()
    a = [bm.verts.new((X - px*w/2, Y - py*w/2, Z)) for X, Y, Z in pts]
    b = [bm.verts.new((X + px*w/2, Y + py*w/2, Z)) for X, Y, Z in pts]
    bm.faces.new(a); bm.faces.new(b[::-1])
    for i in range(3):
        j = (i + 1) % 3; bm.faces.new((a[j], a[i], b[i], b[j]))
    boolean(shell, mkobj("t", bm), 'UNION')

def post_y(x, z, y_board, d=POST_D, pilot=True, rib=True, rib_lift=0.0):
    """Stuetze von der Platinen-Oberseite (y_board) nach vorne bis in die Wand, mit Kernloch"""
    y1 = inner_front_y(x, z) + 1.0
    boolean(shell, cyl_axis("t", "Y", y_board, y1, x, z, d), 'UNION')
    if rib and PRINT_VERT:   # stehend: Rippe unter der Stuetze (aussen am Rand der Stuetze) zur Frontwand
        sx = 1.0 if x >= 0 else -1.0
        vwedge(x + sx*d/2, y_board + 0.3, z - d/2 + 0.3, 0.0, 1.0, 1.6)   # halb ausserhalb -> frei von Glas/Tastern
    elif rib:
        sx = 1.0 if x >= 0 else -1.0
        gusset(x + sx*d/2, y_board + rib_lift, z, sx)
    if pilot:
        boolean(shell, cyl_axis("t", "Y", y_board - 0.5, y_board + PILOT_T, x, z, PILOT_D))

if not MB_FLIP: gusset(PAIR_RIB[0], PAIR_RIB[1], PAIR_RIB[2], 1.0)

# Joystick (Platine 23x25, Stick bei 11/14; zugaengliche Loecher oben rechts 21.5/23.5, unten links 1.5/1.5)
def joy_xz(u, v): return (JOY_X - (u - 11.0), JZ + (v - 14.0))
for u, v in ((21.5, 23.5), (1.5, 1.5)):
    post_y(*joy_xz(u, v), BOARD_TOP)

# Display (Traeger 14x20.5, aktive Mitte bei 7/9.6; Schraubloecher oben 1.5/19 und 12.5/19)
DISP_Z0 = DISP_C[1] - 9.6
def disp_xz(u, v): return (DISP_C[0] - (u - 7.0), DISP_Z0 + v)
for u, v in ((1.5, 19.0), (12.5, 19.0)):
    post_y(*disp_xz(u, v), BOARD_TOP)
boolean(shell, box("t", -PLATE_W/2 + WALL - 0.5, PLATE_W/2 - WALL + 0.5, BOARD_TOP - 1.6, PLATE_Y - WALL + 0.5, DISP_Z0 - 3.0, DISP_Z0 - 1.0), 'UNION')   # Auflage 1 mm Richtung USB (Drucktest)   # Auflage Unterkante

# 2x3-Taster (Platine 14x34, unten bei z=72; Loecher 2/32, 12/32, 1.5/1.5, 12.5/1.5)
BTN23_Z0 = 72.0
for u, v in ((2.0, 32.0), (12.0, 32.0), (1.5, 1.5), (12.5, 1.5)):
    post_y(-(u - 7.0), BTN23_Z0 + v, BTN23_TOP)

# Seitliche Leiste (+X): Platinen-Oberseite bei x = SIDE_TOP, Taster ragen ~1 mm aus der Wand
SIDE_TOP = R + 1.75 - 7.0                   # Seitenleiste 0.75 mm weiter nach aussen (Drucktest)
SIDE_Z_BOARD = SIDE_Z0 - 6.0               # Unterkante der Leiste (gemeinsam fuer 1x3/1x4/1x5)
SIDE_LEN = 37.0                            # laengste Leiste (1x5)
for yy in (-4.0, 4.0):                     # untere Loecher 1.5/1.5 und 9.5/1.5
    x1 = math.sqrt(R_BORE**2 - yy**2) + 1.0
    boolean(shell, cyl_axis("t", "X", SIDE_TOP, x1, yy, SIDE_Z_BOARD + 1.5, POST_D), 'UNION')
    boolean(shell, cyl_axis("t", "X", SIDE_TOP - 0.5, SIDE_TOP + PILOT_T, yy, SIDE_Z_BOARD + 1.5, PILOT_D))
for y0, y1 in ((-5.3, -4.1), (4.1, 5.3)):  # Fuehrungsrippen an den freien Raendern der Leiste
    boolean(shell, box("t", SIDE_TOP, math.sqrt(R_BORE**2 - 5.3**2) + 1.0, y0, y1, SIDE_Z_BOARD + 4.0, SIDE_Z_BOARD + SIDE_LEN), 'UNION')

# Hauptplatine (25.5x73.5, Bauteile nach vorne, USB-C unten; Akku liegt unter der Platine)
MB_Y, MB_Z0, MB_T = MB_Y_SET, 4.5, 1.6         # Unterseite, Unterkante (USB-Ende)
MB_TOP = MB_Y + MB_T
for u, v in ((2.5, 24.0), (23.0, 24.0), (2.0, 70.5), (23.5, 70.5)):
    post_y(12.75 - u, MB_Z0 + v, MB_TOP, d=(5.2 if v > 60 else POST_D), rib_lift=0.3, rib=not (PRINT_VERT and v > 60))   # oben: steht stehend auf dem Akku-Anschlag

# Gyro (22x17.5, flach, Bauteil nach vorne; Loecher oben 1.5/16)
GY_Y, GY_Z0 = -1.0, GY_Z0_SET
for u in (1.5, 20.5):
    post_y(11.0 - u, GY_Z0 + 16.0, GY_Y + 1.6)

# Akku unter der Hauptplatine (Kabel nur 4-8.5 cm): seitliche Schienen, oberer Anschlag, unten nur Ecken (Kabel frei)
BAT = ((25.0 if BAT_TYPE == "902540" else 20.0), 9.0, 40.0); BAT_CL = 0.4
BAT_Z0 = Z_TH_BOT[1] + (2.0 if MB_FLIP else 3.0)                           # oberhalb der Gewindezone (dort ist die Bohrung enger)
BAT_YC = (MB_TOP + 0.3 + BAT[1] / 2) if MB_FLIP else (MB_Y - 0.3 - BAT[1] / 2)   # MB_FLIP: vor der Platine, sonst darunter
bx, by = BAT[0] / 2 + BAT_CL, BAT[1] / 2 + BAT_CL
if MB_FLIP:   # Akku zwischen Platine und Front: Schienen vom Bett bis zur Wand, Anschlaege an beiden Enden
    yw = inner_front_y(bx + 0.8, BAT_Z0 + 20) + 1.0
    for sx in (-1, 1):
        boolean(shell, box("t", *sorted((sx * bx, sx * (bx + 1.6))), SPLIT_Y - 1.0, yw, BAT_Z0 - 1.6, BAT_Z0 + BAT[2]), 'UNION')
        boolean(shell, box("t", *sorted((sx * (bx - 4.0), sx * (bx + 0.8))), MB_TOP + 0.3, yw, BAT_Z0 - 1.6, BAT_Z0), 'UNION')
    boolean(shell, box("t", -bx - 0.8, bx + 0.8, MB_TOP + 0.3, yw, BAT_Z0 + BAT[2], BAT_Z0 + BAT[2] + 1.6), 'UNION')
    if PRINT_VERT:   # Unterkante der Schienen haengt sonst frei ueber der Stutzenbohrung
        for sx in (-1, 1):
            vwedge(sx * (bx + 0.8), SPLIT_Y, BAT_Z0 - 1.6 + 0.3, 0.0, 1.0, 1.6)
else:
    for sx in (-1, 1):
        x0, x1 = sorted((sx * bx, sx * (bx + 1.6)))
        boolean(shell, box("t", x0, x1, SPLIT_Y - 1.0, MB_Y - 0.3, BAT_Z0 - 1.6, BAT_Z0 + BAT[2]), 'UNION')
        boolean(shell, box("t", *sorted((sx * (bx - 4.0), sx * (bx + 0.8))), SPLIT_Y - 1.0, MB_Y - 0.3, BAT_Z0 - 1.6, BAT_Z0), 'UNION')   # unten nur Ecken
    boolean(shell, box("t", -bx - 0.8, bx + 0.8, SPLIT_Y - 1.0, MB_Y - 0.3, BAT_Z0 + BAT[2], BAT_Z0 + BAT[2] + 1.6), 'UNION')

# Ein/Aus-Schalter links (-X): Tasche an der Innenwand, waechst von der Trennebene, oben kleine Lippen
xw = -R_BORE                                         # Innenwand bei y ~ 0
xi = xw + SW_H + 0.3                                 # Innenkante Schalterkoerper
hz, hy = SW_L / 2 + SW_CL, SW_W / 2 + SW_CL
boolean(shell, box("t", xw - 1.0, xi + 0.6, SPLIT_Y - 1.0, -hy, SW_Z - hz - 1.6, SW_Z + hz + 1.6), 'UNION')        # Auflage (vom Bett)
for sz in (-1, 1):
    z0, z1 = sorted((SW_Z + sz * hz, SW_Z + sz * (hz + 1.6)))
    boolean(shell, box("t", xw - 1.0, xi + 0.6, SPLIT_Y - 1.0, hy + 1.2, z0, z1), 'UNION')                       # Seitenwaende
    l0, l1 = sorted((SW_Z + sz * (hz - 0.8), SW_Z + sz * hz))
    boolean(shell, box("t", xi - 1.0, xi + 0.6, hy, hy + 1.2, l0, l1), 'UNION')                                  # Halte-Lippe oben
if PRINT_VERT:   # Unterseite der Schaltertasche: 45 Grad zur Seitenwand (Rand bleibt frei von der Hauptplatine)
    vwedge(min(xi + 0.6, -12.75 - 0.4), (SPLIT_Y - 1.0 + hy + 1.2) / 2, SW_Z - hz - 1.6 + 0.3, -1.0, 0.0, (hy + 1.2) - (SPLIT_Y - 1.0))
boolean(shell, box("t", -R - 2, xi + 0.01, -SW_SLOT_W / 2, SW_SLOT_W / 2, SW_Z - SW_SLOT_L / 2, SW_Z + SW_SLOT_L / 2))  # Hebelschlitz
boolean(shell, box("t", xw - 0.01, xi, -hy, hy, SW_Z - hz, SW_Z + hz))                                            # Platz fuer den Koerper

# Passstift-Dome ueber die Trennebene
for x, z in DOWELS:
    boolean(shell, cyl_axis("t", "Y", SPLIT_Y - 3.0, SPLIT_Y + 3.0, x, z, DOWEL_DOME), 'UNION')
    if PRINT_VERT:
        sx = 1.0 if x >= 0 else -1.0; r_ = DOWEL_DOME / 2
        vwedge(x - sx*r_*0.7, SPLIT_Y, z - r_*0.7, sx, 0.0, 6.0)

# Schrauben M2 Senkkopf von hinten: Dom ueber die Trennebene (Loecher erst nach dem Teilen)
for x, z in SCREWS:
    boolean(shell, cyl_axis("t", "Y", SPLIT_Y - 3.0, SPLIT_Y + 7.0, x, z, 5.0), 'UNION')
    if PRINT_VERT:
        sx = 1.0 if x >= 0 else -1.0
        vwedge(x - sx*2.5*0.7, SPLIT_Y + 2.0, z - 2.5*0.7, sx, 0.0, 10.0)

# ---------------- Halbschalen ----------------
front = shell; front.name = "Vorderschale"
back = bpy.data.objects.new("Rueckschale", shell.data.copy()); col.objects.link(back)
boolean(front, box("t", -100, 100, -100, SPLIT_Y, -10, 400))
boolean(back, box("t", -100, 100, SPLIT_Y, 100, -10, 400))

# Schraubloecher je Schale (keine Kante liegt in der Trennebene)
for x, z in SCREWS:
    yb = -math.sqrt(R**2 - x**2)
    boolean(front, cyl_axis("t", "Y", SPLIT_Y - 1.0, SPLIT_Y + 6.0, x, z, 1.7))                # Kernloch vorne
    boolean(back, cyl_axis("t", "Y", yb - 1.0, SPLIT_Y + 1.0, x, z, 2.4))                     # Durchgang hinten
    boolean(back, cyl_axis("t", "Y", yb - 0.01, yb + 1.3, x, z, 4.4, 2.0))                    # Senkung

# Passstift-Bohrungen je Schale
for x, z in DOWELS:
    boolean(front, cyl_axis("t", "Y", SPLIT_Y - 1.0, SPLIT_Y + DOWEL_L/2 + 0.3, x, z, DOWEL_D + 0.15))
    boolean(back, cyl_axis("t", "Y", SPLIT_Y - DOWEL_L/2 - 0.3, SPLIT_Y + 1.0, x, z, DOWEL_D + 0.15))

# PAIR in der Rueckschale (MB_FLIP: Taster zeigt nach hinten; Platine gespiegelt -> x negativ)
if MB_FLIP:
    px = -PAIR_XZ[0]
    yb_p = -math.sqrt(R**2 - px**2)
    boolean(back, cyl_axis("t", "Y", -math.sqrt(R_BORE**2 - px**2) - 1.0, SPLIT_Y - 0.2, px, PAIR_XZ[1], 4.5), 'UNION')
    if PRINT_VERT:   # Rippe unter dem PAIR-Roehrchen zur Rueckwand
        _sh = shell; shell = back
        vwedge(px, SPLIT_Y - 0.5, PAIR_XZ[1] - 2.25 + 0.3, 0.0, -1.0, 1.6)
        shell = _sh
    boolean(back, cyl_axis("t", "Y", -R - 4.0, SPLIT_Y + 1.0, px, PAIR_XZ[1], PAIR_HOLE))   # auch durch die T-Track-Schiene
# Rueckschale: Druckrippen, die den Akku beim Schliessen leicht gegen die Platine druecken
for x, z in [] if MB_FLIP else ((-6.0, BAT_Z0 + 10), (6.0, BAT_Z0 + 10), (-6.0, BAT_Z0 + BAT[2] - 10), (6.0, BAT_Z0 + BAT[2] - 10)):
    yb_in = -math.sqrt(R_BORE**2 - x**2) - 1.0
    boolean(back, cyl_axis("t", "Y", yb_in, BAT_YC - BAT[1] / 2 - 0.05, x, z, 4.0), 'UNION')
# Teilungsebene am Ende nochmals plan schneiden (sonst steht z.B. eine Verstaerkung 0.18 mm ueber -> Teil liegt nicht plan auf)
boolean(front, box("t", -100, 100, -100, SPLIT_Y, -10, 400))
boolean(back, box("t", -100, 100, SPLIT_Y, 100, -10, 400))

# ---------------- Blindstopfen fuer freie Seitenloecher ----------------
def stadium_pts(w, h, seg=16):
    r, c = w / 2, (h - w) / 2
    pts = [(r*math.cos(math.pi*i/seg), c + r*math.sin(math.pi*i/seg)) for i in range(seg + 1)]
    pts += [(r*math.cos(math.pi + math.pi*i/seg), -c + r*math.sin(math.pi + math.pi*i/seg)) for i in range(seg + 1)]
    return pts                                   # (y, z)
def stadium(name, w, h, x0, x1):
    """Langloch-Prisma entlang X: Breite w (y), Hoehe h (z), mittig bei y=0/z=0"""
    bm = bmesh.new(); pts = stadium_pts(w, h)
    a = [bm.verts.new((x0, y, z)) for y, z in pts]; b = [bm.verts.new((x1, y, z)) for y, z in pts]
    bm.faces.new(a); bm.faces.new(b[::-1]); n = len(pts)
    for i in range(n):
        j = (i + 1) % n; bm.faces.new((a[i], a[j], b[j], b[i]))
    return mkobj(name, bm)
plug = stadium("Blindstopfen", BTN_HOLE - 0.05, BTN_HOLE + SIDE_SLOT - 0.05, 0.0, 3.2)      # Schaft (von innen eingesetzt)
boolean(plug, stadium("t", BTN_HOLE + 1.2, BTN_HOLE + SIDE_SLOT + 1.2, -0.8, 0.0), 'UNION')    # Kragen innen
plug.location = (60, 0, 0)

# ---------------- Platzhalter der Module (nur zur Kontrolle, nicht drucken) ----------------
ph = []
def ph_box(name, x0, x1, y0, y1, z0, z1):
    o = box(name, x0, x1, y0, y1, z0, z1); o.display_type = 'WIRE'; o.hide_render = True; ph.append(o); return o
jx0, jz0 = joy_xz(23.0, 0.0); jx1, jz1 = joy_xz(0.0, 25.0)
ph_box("PH_Joystick", jx0, jx1, BOARD_TOP - 1.6, BOARD_TOP, jz0, jz1)
dx0, dz0 = disp_xz(14.0, 0.0); dx1, dz1 = disp_xz(0.0, 20.5)
ph_box("PH_Display", dx0, dx1, BOARD_TOP - 1.6, BOARD_TOP, dz0, dz1)
ph_box("PH_Display_Glas", -6.3, 6.3, BOARD_TOP, BOARD_TOP + 5.3, DISP_Z0 + 3.0, DISP_Z0 + 16.0)
ph_box("PH_Taster_2x3", -7.0, 7.0, BTN23_TOP - 1.6, BTN23_TOP, BTN23_Z0, BTN23_Z0 + 34.0)
ph_box("PH_Seitenleiste_1x5", SIDE_TOP - 1.6, SIDE_TOP, -5.5, 5.5, SIDE_Z_BOARD, SIDE_Z_BOARD + SIDE_LEN)
ph_box("PH_Hauptplatine", -12.75, 12.75, MB_Y, MB_TOP, MB_Z0, MB_Z0 + 73.5)
ph_box("PH_Hauptplatine_JST", -10.0, 10.0, *((MB_Y - 7.0, MB_Y) if MB_FLIP else (MB_TOP, MB_TOP + 7.0)), MB_Z0 + 25.0, MB_Z0 + 52.0)
ph_box("PH_Gyro", -11.0, 11.0, GY_Y, GY_Y + 1.6, GY_Z0, GY_Z0 + 17.5)
ph_box("PH_Akku", -BAT[0]/2, BAT[0]/2, BAT_YC - BAT[1]/2, BAT_YC + BAT[1]/2, BAT_Z0, BAT_Z0 + BAT[2])
# Passstift (eigenes Teil)
dowel = cyl_axis("Passstift", "Y", 0, DOWEL_L, 0.0, 0.0, DOWEL_D); dowel.location = (60, 0, 20)

# ---------------- Kraenze ----------------
RI_TH = TH_MAJ + TH_CLEAR                  # Bohrung im Kranz
NEW_ENDS = globals().get("NEW_ENDS", PRINT_VERT or SEGMENTED)   # neues Design der Enden (wie Saber Mini Remote)
def cyl_z(name, x, y, z0, z1, d0, d1=None, seg=32):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=d0/2, radius2=(d1 if d1 is not None else d0)/2, depth=z1-z0)
    bmesh.ops.translate(bm, verts=bm.verts, vec=(x, y, (z0+z1)/2)); return mkobj(name, bm)
if NEW_ENDS:
    # Pommel-Kranz: Boden mit USB-Loch und Ringgravur, Kragen mit 8 runden Kanneluren, Rille, Zierring (stehend druckbar, Boden unten)
    RP = POMMEL_R
    pk = revolve("Pommel_Kranz", [(RP - 1.2, 0.0), (RP, 1.2), (RP, 6.0), (RP - 0.8, 6.6), (RP - 0.8, 7.8), (RP, 8.6), (RP, 14.0),
                                  (R + 1.0, 15.5), (R + 1.0, 20.5), (R + 1.8, 21.3), (R + 1.8, 23.5), (R + 1.0, 24.3), (R + 1.0, Z_TH_BOT[1])])
    boolean(pk, revolve("t", [(RI_TH, Z_TH_BOT[0] - 0.3), (RI_TH, Z_TH_BOT[1] + 1)]))
    boolean(pk, revolve("t", [((8.0 if MB_FLIP else USB_HOLE / 2), -1), ((8.0 if MB_FLIP else USB_HOLE / 2), 3)]))   # USB-Loch
    boolean(pk, thread_ridge("t", RI_TH + 0.1, TH_MIN + TH_CLEAR, Z_TH_BOT[0] + 0.4, ZM_BOT - 0.4, TH_PITCH, 1.7, 0.3), 'UNION')
    for i in range(8):   # Kanneluren, oben kegelig auslaufend (kein Ueberhang)
        a_ = math.radians(360 * i / 8 + 22.5); fx, fy = (RP + 0.3)*math.cos(a_), (RP + 0.3)*math.sin(a_)
        fl = cyl_z("t", fx, fy, 1.8, 12.0, 3.4)
        boolean(fl, cyl_z("t", fx, fy, 11.99, 13.7, 3.4, 0.01), 'UNION')
        boolean(pk, fl)
    rg = revolve("t", [(11.8, -1.0), (11.8, 0.6)]); boolean(rg, revolve("t", [(11.0, -2.0), (11.0, 2.0)])); boolean(pk, rg)   # Ringgravur Boden

    # Emitter-Kranz: Sockelband mit Rille, ausgestellter Kragen mit 6 Fenstern, Lippe mit Kerben, oben vertiefte Klingenoeffnung,
    # innen hohl mit 45-Grad-Kegeldach (stehend, Gewinde unten, stuetzfrei)
    E0, ET = Z_TH_TOP[0] + 0.3, Z_TH_TOP[1] + 22.0
    RFL = R + 4.5
    ek = revolve("Emitter_Kranz", [(R + 1.1, E0), (R + 1.5, E0 + 0.4), (R + 1.5, E0 + 4.0), (R + 0.9, E0 + 4.6), (R + 0.9, E0 + 5.8), (R + 1.5, E0 + 6.4),
                                   (R + 1.5, E0 + 12.0), (R + 2.1, E0 + 13.5), (RFL, ET - 5.0), (RFL, ET - 1.2), (RFL - 1.2, ET),
                                   (14.5, ET), (13.5, ET - 1.8), (9.5, ET - 1.8), (9.0, ET - 1.2), (8.0, ET - 1.2), (7.5, ET - 1.8), (0.01, ET - 1.8)])
    zc = Z_TH_TOP[1] + 0.3
    boolean(ek, revolve("t", [(RI_TH, E0 - 1), (RI_TH, zc), (4.0, zc + (RI_TH - 4.0)), (0.01, zc + (RI_TH - 4.0))]))   # Gewindebohrung + Kegel
    boolean(ek, thread_ridge("t", RI_TH + 0.1, TH_MIN + TH_CLEAR, ZM_TOP + 0.4, Z_TH_TOP[1] - 0.4, TH_PITCH, 1.7, 0.3), 'UNION')
    rf = R + 1.1                                   # Fensterboden (konstant -> laufen zur Lippe tiefer aus), oben 45 Grad
    for i in range(6):
        boolean(ek, radial_prism("t", 360 * i / 6 + 30, [(rf, E0 + 15.0), (RFL + 3, E0 + 15.0), (RFL + 3, ET - 6.5), (rf, ET - 6.5 - (RFL + 3 - rf))], 3.2))
    for i in range(6):   # Kerben in der Lippe
        a_ = 360 * i / 6
        boolean(ek, obox("t", (RFL + 1.0)*math.cos(math.radians(a_)), (RFL + 1.0)*math.sin(math.radians(a_)), 3.6, 2.4, ET - 3.2, ET + 1, a_))
else:
    # Pommel-Kranz (unten, von unten aufgeschraubt, Boden mit USB-Loch)
    pk = revolve("Pommel_Kranz", [(POMMEL_R - 2.0, 0.0), (POMMEL_R, 2.0), (POMMEL_R, Z_TH_BOT[1] - 2.0), (POMMEL_R - 1.5, Z_TH_BOT[1])])
    boolean(pk, revolve("t", [(RI_TH, Z_TH_BOT[0] - 0.3), (RI_TH, Z_TH_BOT[1] + 1)]))
    boolean(pk, revolve("t", [((8.0 if MB_FLIP else USB_HOLE / 2), -1), ((8.0 if MB_FLIP else USB_HOLE / 2), 3)]))   # Boden mit mittigem USB-Loch (MB_FLIP: Buchse nahe der Achse -> Ø16)
    boolean(pk, thread_ridge("t", RI_TH + 0.1, TH_MIN + TH_CLEAR, Z_TH_BOT[0] + 0.4, ZM_BOT - 0.4, TH_PITCH, 1.7, 0.3), 'UNION')
    def pommel_flat(a):
        d = POMMEL_R - 1.0 + 5
        boolean(pk, obox("t", d*math.cos(math.radians(a)), d*math.sin(math.radians(a)), 10, 12.0, 6.0, Z_TH_BOT[1] - 6.0, a))
    ring_of(POMMEL_FLATS, 90, pommel_flat)
    def pommel_notch(a):
        boolean(pk, obox("t", POMMEL_R*math.cos(math.radians(a)), POMMEL_R*math.sin(math.radians(a)), 3.0, POMMEL_NOTCH_W, -1, POMMEL_NOTCH_H, a))
    ring_of(POMMEL_NOTCH, 180 / POMMEL_NOTCH, pommel_notch)

    # Emitter-Kranz (oben, von oben aufgeschraubt, oben Flansch)
    ek = revolve("Emitter_Kranz", [(R + 1.5, Z_TH_TOP[0] + 0.3), (R + 1.5, Z_EMITTER[1] - 8), (R + 2.2, Z_EMITTER[1] - 7),
                                   (R + 2.2, Z_EMITTER[1] - 3), (R + 0.8, Z_EMITTER[1])])
    boolean(ek, revolve("t", [(RI_TH, Z_TH_TOP[0] - 1), (RI_TH, Z_TH_TOP[1] + 0.3)]))
    # oben geschlossen (Boden), damit man nicht hineinsehen kann
    boolean(ek, thread_ridge("t", RI_TH + 0.1, TH_MIN + TH_CLEAR, ZM_TOP + 0.4, Z_TH_TOP[1] - 0.4, TH_PITCH, 1.7, 0.3), 'UNION')
    def vent(a):
        d = R + 1.5 - 1.0 + 5
        boolean(ek, obox("t", d*math.cos(math.radians(a)), d*math.sin(math.radians(a)), 10, VENT_W, Z_TH_TOP[0] + 4, Z_EMITTER[1] - 10, a))
    ring_of(VENTS, 90, vent)
    def crown(a):
        rc = (R + 1) if SIZE != "SLIM" else (RI_TH - 0.4 + 6.0)       # SLIM: Kerben beginnen knapp innerhalb der Bohrung, nicht im Gewinde
        boolean(ek, obox("t", rc*math.cos(math.radians(a)), rc*math.sin(math.radians(a)), 12, CROWN_W, Z_EMITTER[1] - CROWN_H, Z_EMITTER[1] + 5, a))
    ring_of(CROWN, 180 / CROWN, crown)

# ---------------- Emitter-Rohr (nur SEGMENTED): rund, wird auf den Schalen-Stutzen geschraubt ----------------
parts = [front, back, pk, ek, plug, dowel]
if SEGMENTED:
    z0 = Z_JOINT + 0.2
    et = revolve("Emitter_Rohr", [(R - 0.5, z0), (R, z0 + 0.5)] + [p for p in P_TOP if p[1] > z0 + 0.6])   # SLIM: Hals beginnt direkt an der Teilung
    zb = Z_JOINT + JOINT_L + 0.3                                                   # Ende Innengewinde
    boolean(et, revolve("t", [(RI_J, z0 - 1), (RI_J, zb), (R_CORE_J, zb + (RI_J - R_CORE_J)), (R_CORE_J, Z_TH_TOP[1] + 5)]))   # 45 Grad
    boolean(et, revolve("t", [(RI_J + 0.6, z0 - 0.5), (RI_J - 0.4, z0 + 0.5)]))                                                  # Fase Eingang
    boolean(et, thread_ridge("t", RI_J + 0.1, TH_J_MIN + TH_CLEAR, z0 + 0.3, zb - 0.6, TH_PITCH, 1.7, 0.3), 'UNION')      # Innengewinde
    boolean(et, thread_ridge("t", TH_MIN - 0.1, TH_MAJ, ZM_TOP + 0.3, Z_TH_TOP[1] - 0.6, TH_PITCH, 1.9, 0.5), 'UNION')   # Stutzen fuer den Kranz
    def flute_t(a):
        zf0, zf1 = Z_JOINT + 4, Z_FLUTES[1] - 4
        if PRINT_VERT:
            boolean(et, radial_prism("t", a, [(R - FLUTE_DEPTH, zf0), (R + 5, zf0), (R + 5, zf1), (R, zf1), (R - FLUTE_DEPTH, zf1 - FLUTE_DEPTH)], FLUTE_W))
        else:
            d = R - FLUTE_DEPTH + 5
            boolean(et, obox("t", d*math.cos(math.radians(a)), d*math.sin(math.radians(a)), 10, FLUTE_W, zf0, zf1, a))
    if Z_FLUTES[1] - 4 > Z_JOINT + 8: ring_of(FLUTES, 180 / FLUTES, flute_t)   # SLIM: Laengsrillen liegen unterhalb der Teilung
    parts.append(et)

def keep_largest(bm):
    seen = set(); groups = []
    for v in bm.verts:
        if v.index in seen: continue
        st = [v]; seen.add(v.index); g = [v]
        while st:
            q = st.pop()
            for e in q.link_edges:
                w = e.other_vert(q)
                if w.index not in seen: seen.add(w.index); st.append(w); g.append(w)
        groups.append(g)
    groups.sort(key=len, reverse=True)
    for g in groups[1:]:
        bmesh.ops.delete(bm, geom=g, context='VERTS')

for o in parts:
    bm = bmesh.new(); bm.from_mesh(o.data)
    bm.verts.ensure_lookup_table()
    keep_largest(bm)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=0.002)
    bmesh.ops.delete(bm, geom=[e for e in bm.edges if not e.link_faces], context='EDGES')
    bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=0)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data); bm.free()
    o.name = o.name + "_" + FORM_CTRL + ("_SLIM" if SIZE == "SLIM" else "") + ("" if BAT_TYPE == "902540" else "_" + BAT_TYPE) + ("_" + GRIP_STYLE if GRIP_STYLE else "")
print("Lightsaber", FORM_CTRL, "gebaut")
