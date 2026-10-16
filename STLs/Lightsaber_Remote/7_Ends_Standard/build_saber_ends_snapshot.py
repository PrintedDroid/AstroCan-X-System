# AstroCan X Lightsaber Remote - modulare Enden (2026-10-15)
# Emitter- und Pommel-Kranz geteilt "nach den Rillen":
#   Huelse (Sleeve)  = loser Ring ueber dem glatten Fuehrungsbund des Schalen-Stutzens
#   Kopf (Head)      = schraubt auf das vorhandene Gewinde und klemmt die Huelse gegen die Schulter
# Alle Koepfe/Huelsen einer Groesse sind untereinander tauschbar. Passend fuer alle Schalen (flach/stehend/segmentiert) dieser Groesse.
# Druck: Emitter-Koepfe stehend, Gewindeoeffnung unten. Pommel-Koepfe stehend, Boden unten. Huelsen stehend. Alle Ueberhaenge <= 45 Grad.
# Ausfuehren in Blender:  g = {"SIZE": "STANDARD"}; exec(open(r"...\build_saber_ends.py").read(), g)
import bpy, bmesh, math, mathutils, re, os

SIZE = globals().get("SIZE", "STANDARD")
_here = globals().get("HERE", r"C:\Users\benri\OneDrive\Astromech\Sketche & Software\Lightsaber_Remote")
_src = open(os.path.join(_here, "build_lightsaber.py"), encoding="utf-8").read()
# Masse + Grundhelfer aus build_lightsaber.py (Kopf bis vor das Schalenprofil), eigene Sammlung
_head = _src.split("# ---------------- Profil (Schalen) ----------------")[0]
_head = re.sub(r'^COL = .*$', 'COL = "Lightsaber_Ends_" + SIZE', _head, flags=re.M)
exec(_head, globals())
for _fn in ("thread_ridge", "radial_prism", "cyl_z"):
    exec(re.search(r'^def %s\(.*?(?=^\S)' % _fn, _src, flags=re.M | re.S).group(0), globals())
TH_MIN = TH_MAJ - TH_DEPTH
ZM_BOT = Z_TH_BOT[0] + (Z_TH_BOT[1] - Z_TH_BOT[0]) * TH_FRAC
ZM_TOP = Z_TH_TOP[1] - (Z_TH_TOP[1] - Z_TH_TOP[0]) * TH_FRAC
RI_TH = TH_MAJ + TH_CLEAR
USB_R = 8.0 if MB_FLIP else USB_HOLE / 2
if SIZE == "MINI":   # Saber Mini Remote (build_saber_miniremote.py): lokale Achse z, Emitter ab LockRing (z=0), Pommel auf dem Griffkoerper
    R, TH_MAJ, TH_DEPTH, TH_CLEAR, TH_PITCH = 21.0, 17.5, 1.2, 0.3, 2.5
    TH_MIN = TH_MAJ - TH_DEPTH; RI_TH = TH_MAJ + TH_CLEAR
    STUB_FREE = 27.6                       # Emitter-Stutzen frei hinter dem LockRing (STUB_L - LOCK_GAP)
    Z_TH_TOP = (-0.3, STUB_FREE); ZM_TOP = 12.6
    Z_TH_BOT = (2.3, 16.25); ZM_BOT = 16.25  # Griffkoerper-Zapfen (voll Gewinde)
    POMMEL_R = R + 2.5; USB_R = 0.0
    GRIP_TOTAL = 92.9                      # wie das bisherige GripTube (Pommel + Griff)

# ---------------- Teilungen ----------------
E0 = Z_TH_TOP[0] + 0.3              # Emitter: Unterkante (an der Schulter)
ZS = E0 + 12.0                      # Emitter: Huelse E0..ZS, Kopf ab ZS (unter dem Gewindebeginn ZM_TOP)
ET = Z_TH_TOP[1] + (36.0 if SIZE == "MINI" else 22.0)   # Emitter: Oberkante (wie bisher; MINI wie EmitterRing_Long)
ZP = ZM_BOT + 0.25                  # Pommel: Kopf 0..ZP (traegt das Gewinde), Huelse ZP..Z_TH_BOT[1]
PT = Z_TH_BOT[1]                    # Pommel: Huelse endet an der Schulter
GAP = 0.15                          # Luft zwischen Kopf und Huelse (Druck)
RP = POMMEL_R
RFL = R + 4.5
assert ZS + GAP < ZM_TOP and ZP > ZM_BOT, "Teilung liegt im Gewinde"

def sleeve_bore(o, z0, z1):
    boolean(o, revolve("t", [(RI_TH, z0 - 1), (RI_TH, z1 + 1)]))
    for zz, s in ((z0, 1), (z1, -1)):          # Fasen an der Bohrung
        e_ = 0.07 if SIZE == "MINI" else 0.0    # MINI: sonst exakt koinzidente Kanten im Boolean
        boolean(o, revolve("t", [(RI_TH + 0.6 + e_, zz - s*0.5), (RI_TH - 0.4 + e_, zz + s*0.5)][::s]))

def emitter_bore(o):
    """Gewindebohrung + Innengewinde + 45-Grad-Kegeldach (stehend, Gewinde unten)"""
    zc = Z_TH_TOP[1] + 0.3
    boolean(o, revolve("t", [(RI_TH, ZS - 1), (RI_TH, zc), (4.0, zc + (RI_TH - 4.0)), (0.01, zc + (RI_TH - 4.0))]))
    boolean(o, revolve("t", [(RI_TH + 0.6, ZS + GAP - 0.5), (RI_TH - 0.4, ZS + GAP + 0.5)]))      # Fase Eingang
    boolean(o, thread_ridge("t", RI_TH + 0.1, TH_MIN + TH_CLEAR, ZM_TOP + 0.4, Z_TH_TOP[1] - 0.4, TH_PITCH, 1.7, 0.3), 'UNION')

def pommel_bore(o):
    boolean(o, revolve("t", [(RI_TH, Z_TH_BOT[0] - 0.3), (RI_TH, ZP + 1)]))
    if USB_R > 0: boolean(o, revolve("t", [(USB_R, -1), (USB_R, 3)]))                           # USB
    boolean(o, revolve("t", [(RI_TH - 0.4, ZP - GAP - 0.5), (RI_TH + 0.6, ZP - GAP + 0.5)]))     # Fase Eingang
    boolean(o, thread_ridge("t", RI_TH + 0.1, TH_MIN + TH_CLEAR, Z_TH_BOT[0] + 0.4, ZM_BOT - 0.4, TH_PITCH, 1.7, 0.3), 'UNION')

def blade_top(prof_top_r):
    """vertiefte Klingenoeffnung oben (wie bisher), Profil vom Aussenrand nach innen"""
    return [(prof_top_r, ET), (13.5, ET - 1.8), (9.5, ET - 1.8), (9.0, ET - 1.2), (8.0, ET - 1.2), (7.5, ET - 1.8), (0.01, ET - 1.8)]

z0e = ZS + GAP
parts = []

# =================== EMITTER-HUELSEN (E0..ZS) ===================
# Classic: Sockelband mit Rille (wie der bisherige Kranz)
s = revolve("Emitter_Sleeve_Classic", [(R + 1.1, E0), (R + 1.5, E0 + 0.4), (R + 1.5, E0 + 4.0), (R + 0.9, E0 + 4.6), (R + 0.9, E0 + 5.8),
                                       (R + 1.5, E0 + 6.4), (R + 1.5, ZS - 0.4), (R + 1.1, ZS)])
sleeve_bore(s, E0, ZS); parts.append(s)
# Ribs: drei V-Ringe (Flanken 45 Grad)
pr = [(R + 1.1, E0), (R + 1.5, E0 + 0.4)]
for k in range(3):
    zb = E0 + 1.6 + k * 3.4
    pr += [(R + 1.5, zb), (R + 2.5, zb + 1.0), (R + 2.5, zb + 1.4), (R + 1.5, zb + 2.4)]
pr += [(R + 1.5, ZS - 0.4), (R + 1.1, ZS)]
s = revolve("Emitter_Sleeve_Ribs", pr); sleeve_bore(s, E0, ZS); parts.append(s)
# Flutes: 12 Laengsnuten ueber die ganze Hoehe (offen -> keine Decke)
s = revolve("Emitter_Sleeve_Flutes", [(R + 1.1, E0), (R + 2.4, E0 + 1.3), (R + 2.4, ZS - 1.3), (R + 1.1, ZS)])
for i in range(12):
    a = 360 * i / 12
    boolean(s, obox("t", (R + 3.0)*math.cos(math.radians(a)), (R + 3.0)*math.sin(math.radians(a)), 2.4, 1.6, E0 - 1, ZS + 1, a))
sleeve_bore(s, E0, ZS); parts.append(s)

# =================== EMITTER-KOEPFE (ZS..ET) ===================
# Classic: ausgestellter Kragen mit 6 Fenstern, Lippe mit Kerben (bisheriges Design, nur oberer Teil)
h = revolve("Emitter_Head_Classic", [(R + 1.1, z0e), (R + 1.5, z0e + 0.4), (R + 2.1, E0 + 13.5), (RFL, ET - 5.0), (RFL, ET - 1.2), (RFL - 1.2, ET)] + blade_top(14.5)[1:])
emitter_bore(h)
rf = R + 1.1
for i in range(6):
    boolean(h, radial_prism("t", 360 * i / 6 + 30, [(rf, E0 + 15.0), (RFL + 3, E0 + 15.0), (RFL + 3, ET - 6.5), (rf, ET - 6.5 - (RFL + 3 - rf))], 3.2))
for i in range(6):
    a = 360 * i / 6
    boolean(h, obox("t", (RFL + 1.0)*math.cos(math.radians(a)), (RFL + 1.0)*math.sin(math.radians(a)), 3.6, 2.4, ET - 3.2, ET + 1, a))
parts.append(h)

# Shroud: schlanker Hals, oben 45-Grad-Trichter auf breite Scheibe, Lochkranz in der Deckflaeche
RD = R + 7.0
h = revolve("Emitter_Head_Shroud", [(R + 1.1, z0e), (R + 1.5, z0e + 0.4), (R + 1.5, z0e + 3.0), (R + 0.9, z0e + 3.6), (R + 0.9, z0e + 5.2), (R + 1.5, z0e + 5.8),
                                    (R + 1.5, ET - 3.0 - (RD - R - 1.5)), (RD, ET - 3.0), (RD, ET - 0.6), (RD - 0.6, ET), (RD - 2.0, ET), (RD - 2.6, ET - 0.6),
                                    (16.0, ET - 0.6), (15.0, ET - 2.4), (9.0, ET - 2.4), (8.0, ET - 1.2), (0.01, ET - 1.2)])
emitter_bore(h)
for i in range(18):
    a = math.radians(360 * i / 18)
    boolean(h, cyl_z("t", (RD - 5.6)*math.cos(a), (RD - 5.6)*math.sin(a), ET - 2.0, ET + 1, 2.4, seg=16))
parts.append(h)

# Crown: achteckiger Block mit vertieften Feldern, oben Zinnenkranz
RO = R + 3.2                                     # Inkreis-Radius des Achtecks
h = revolve("Emitter_Head_Crown", [(R + 1.1, z0e), (R + 1.5, z0e + 0.4), (R + 1.5, z0e + 1.5), (RO / math.cos(math.pi / 8) + 0.2, z0e + 1.5 + (RO / math.cos(math.pi / 8) + 0.2 - R - 1.5)),
                                   (RO / math.cos(math.pi / 8) + 0.2, ET - 1.0), (RO / math.cos(math.pi / 8) - 0.8, ET)] + blade_top(14.5)[1:])
for i in range(8):   # Achteck-Flaechen
    a = 360 * i / 8 + 22.5
    boolean(h, obox("t", (RO + 5)*math.cos(math.radians(a)), (RO + 5)*math.sin(math.radians(a)), 10, 40, z0e - 1, ET + 1, a))
emitter_bore(h)
for i in range(8):   # vertiefte Felder, Oberkante 45 Grad
    a = 360 * i / 8 + 22.5
    boolean(h, radial_prism("t", a, [(RO - 0.8, z0e + 6.0), (RO + 2, z0e + 6.0), (RO + 2, ET - 7.0), (RO - 0.8, ET - 7.0 - 2.8)], 7.0))
for i in range(8):   # Zinnen oben
    a = 360 * i / 8 + 22.5
    boolean(h, obox("t", (RO + 1.5)*math.cos(math.radians(a)), (RO + 1.5)*math.sin(math.radians(a)), 6, 4.0, ET - 3.0, ET + 1, a))
parts.append(h)

# Stepped: glatter Schaft mit 3 V-Rillen, oben 45-Grad-Stufe auf breite Lippe
h = revolve("Emitter_Head_Stepped", [(R + 1.1, z0e), (R + 1.5, z0e + 0.4)]
            + sum([[(R + 1.5, z0e + 4 + 4*k), (R + 0.9, z0e + 4.6 + 4*k), (R + 1.5, z0e + 5.6 + 4*k)] for k in range(3)], [])
            + [(R + 1.5, ET - 9.0), (R + 4.0, ET - 6.5), (R + 4.0, ET - 4.5), (R + 3.2, ET - 3.7), (R + 3.2, ET - 3.0), (R + 4.0, ET - 2.2), (R + 4.0, ET - 0.6),
               (R + 3.4, ET), (17.0, ET), (16.0, ET - 3.0), (10.0, ET - 3.0), (9.0, ET - 2.0), (0.01, ET - 2.0)])
emitter_bore(h)
parts.append(h)

# =================== POMMEL-HUELSEN (ZP..PT) ===================
if SIZE != "MINI":
  exec(compile(r'''
# Classic: Zierring (wie bisher)
s = revolve("Pommel_Sleeve_Classic", [(R + 0.6, ZP + GAP), (R + 1.0, ZP + GAP + 0.4), (R + 1.0, ZP + 4.0), (R + 1.8, ZP + 4.8), (R + 1.8, ZP + 7.0),
                                      (R + 1.0, ZP + 7.8), (R + 1.0, PT - 0.4), (R + 0.6, PT)])
sleeve_bore(s, ZP + GAP, PT); parts.append(s)
s = revolve("Pommel_Sleeve_Ribs", [(R + 0.6, ZP + GAP), (R + 1.0, ZP + GAP + 0.4)]
            + sum([[(R + 1.0, ZP + 1.5 + 3.8*k), (R + 2.0, ZP + 2.5 + 3.8*k), (R + 2.0, ZP + 2.9 + 3.8*k), (R + 1.0, ZP + 3.9 + 3.8*k)] for k in range(3)], [])
            + [(R + 1.0, PT - 0.4), (R + 0.6, PT)])
sleeve_bore(s, ZP + GAP, PT); parts.append(s)
s = revolve("Pommel_Sleeve_Flutes", [(R + 0.6, ZP + GAP), (R + 2.2, ZP + GAP + 1.6), (R + 2.2, PT - 1.6), (R + 0.6, PT)])
for i in range(12):
    a = 360 * i / 12
    boolean(s, obox("t", (R + 2.8)*math.cos(math.radians(a)), (R + 2.8)*math.sin(math.radians(a)), 2.4, 1.6, ZP - 1, PT + 1, a))
sleeve_bore(s, ZP + GAP, PT); parts.append(s)
''', "pommel_sleeves", "exec"), globals())

# =================== POMMEL-KOEPFE (0..ZP) - Boden unten, flach ===================
z1p = ZP - GAP
# Classic: Fase, Rille, 8 Kanneluren (oben kegelig), Uebergang auf R+1
h = revolve("Pommel_Head_Classic", [(0.01, 0.0), (RP - 1.2, 0.0), (RP, 1.2), (RP, 6.0), (RP - 0.8, 6.6), (RP - 0.8, 7.8), (RP, 8.6), (RP, z1p - 2.4),
                                    (R + 1.0, z1p - 2.4 + (RP - R - 1.0)), (R + 1.0, z1p - 0.4), (R + 0.6, z1p), (0.01, z1p)])
pommel_bore(h)
for i in range(8):
    a_ = math.radians(360 * i / 8 + 22.5); fx, fy = (RP + 0.3)*math.cos(a_), (RP + 0.3)*math.sin(a_)
    fl = cyl_z("t", fx, fy, 1.8, z1p - 5.0, 3.4); boolean(fl, cyl_z("t", fx, fy, z1p - 5.01, z1p - 3.3, 3.4, 0.01), 'UNION'); boolean(h, fl)
rg = revolve("t", [(11.8, -1.0), (11.8, 0.6)]); boolean(rg, revolve("t", [(11.0, -2.0), (11.0, 2.0)])); boolean(h, rg)
parts.append(h)

# Grenade: Stapel aus V-Ringen (Flanken 45 Grad)
pr = [(0.01, 0.0), (RP - 1.0, 0.0), (RP, 1.0)]
z = 1.0
while z + 3.2 <= z1p - 3.0:
    pr += [(RP, z + 0.6), (RP - 1.2, z + 1.8), (RP, z + 3.0)]; z += 3.0
pr += [(RP, z + 0.4), (R + 1.0, z + 0.4 + (RP - R - 1.0)), (R + 1.0, z1p - 0.4), (R + 0.6, z1p), (0.01, z1p)]
h = revolve("Pommel_Head_Grenade", pr); pommel_bore(h); parts.append(h)

# Facet: achteckiger Klotz mit Laengsschlitzen
RO = RP - 0.3
h = revolve("Pommel_Head_Facet", [(0.01, 0.0), (RO / math.cos(math.pi / 8) - 1.0, 0.0), (RO / math.cos(math.pi / 8), 1.0), (RO / math.cos(math.pi / 8), z1p - 3.5),
                                  (R + 1.0, z1p - 3.5 + (RO / math.cos(math.pi / 8) - R - 1.0)), (R + 1.0, z1p - 0.4), (R + 0.6, z1p), (0.01, z1p)])
for i in range(8):
    a = 360 * i / 8
    boolean(h, obox("t", (RO + 5)*math.cos(math.radians(a)), (RO + 5)*math.sin(math.radians(a)), 10, 40, -1, z1p + 1, a))
pommel_bore(h)
for i in range(8):   # Schlitz in jeder Flaeche, oben 45 Grad
    a = 360 * i / 8
    boolean(h, radial_prism("t", a, [(RO - 1.0, 2.5), (RO + 2, 2.5), (RO + 2, z1p - 5.0), (RO - 1.0, z1p - 5.0 - 3.0)], 2.2))
rg = revolve("t", [(11.8, -1.0), (11.8, 0.6)]); boolean(rg, revolve("t", [(11.0, -2.0), (11.0, 2.0)])); boolean(h, rg)
parts.append(h)

# Spool: breiter Fussteller, Taille, 45-Grad-Uebergang
RW = RP + 2.0
h = revolve("Pommel_Head_Spool", [(0.01, 0.0), (RW - 0.8, 0.0), (RW, 0.8), (RW, 3.2), (R + 1.2, 3.2 + (RW - R - 1.2)), (R + 1.2, z1p - 4.5),
                                  (R + 1.8, z1p - 3.9), (R + 1.8, z1p - 1.2), (R + 1.0, z1p - 0.6), (R + 1.0, z1p - 0.4), (R + 0.6, z1p), (0.01, z1p)])
pommel_bore(h)
for i in range(24):   # Riffel am Teller
    a = 360 * i / 24
    boolean(h, obox("t", (RW + 0.2)*math.cos(math.radians(a)), (RW + 0.2)*math.sin(math.radians(a)), 1.6, 1.2, -1, 4.0, a))
parts.append(h)

# =================== MINI: GRIFFKOERPER (Druckkoordinaten: p=0 Remote-Seite auf dem Bett, Zapfen oben) ===================
# Innengewinde unten (auf den Griffstutzen der Schalen), oben Aussengewinde-Zapfen fuer die Pommel-Koepfe.
# Gleiches Gewinde wie die Schalen-Stutzen -> Griffkoerper sind auch untereinander stapelbar (Verlaengerung).
if SIZE == "MINI":
    PSH = GRIP_TOTAL - (ZP + GAP)               # Schulter (Pommel-Kopf liegt hier an)
    PZT = PSH + (ZP + GAP - Z_TH_BOT[0] - 0.3)  # Zapfenende
    RC = 14.5                                   # Hohlraum (USB-Stecker)
    def grip_body(name, style):
        pr = [(RI_TH + 0.4, 0.0), (R - 0.6, 0.0), (R, 0.6)]
        if style == "CLASSIC":                  # umlaufende V-Rillen wie das bisherige GripTube
            z = 6.0
            while z + 2.0 <= PSH - 8.0:
                pr += [(R, z), (R - 1.0, z + 1.0), (R, z + 2.0)]; z += 5.0
        pr += [(R, PSH - 2.4), (R + 0.9, PSH - 1.5), (R + 0.9, PSH - 0.5), (R + 0.4, PSH), (TH_MIN + 0.1, PSH), (TH_MIN, PSH + 0.1), (TH_MIN, PZT - 0.4), (TH_MIN - 0.4, PZT), (RC + 0.01, PZT)]
        g = revolve(name, pr)
        boolean(g, revolve("t", [(RI_TH, -1.0), (RI_TH, STUB_FREE + 0.3), (RC, STUB_FREE + 0.3 + (RI_TH - RC)), (RC, PZT + 1)]))   # Bohrung, 45 Grad, Hohlraum
        boolean(g, revolve("t", [(RI_TH + 0.6, -0.5), (RI_TH - 0.4, 0.5)]))                                                        # Fase Eingang
        boolean(g, thread_ridge("t", RI_TH + 0.1, TH_MIN + TH_CLEAR, 0.4, STUB_FREE - 0.4, TH_PITCH, 1.7, 0.3), 'UNION')           # Innengewinde
        boolean(g, thread_ridge("t", TH_MIN - 0.1, TH_MAJ, PSH + 0.6, PZT - 0.6, TH_PITCH, 1.9, 0.5), 'UNION')                      # Zapfen
        if style in ("GRENADE", "RIBS", "PANELS"):
            gs = {"GRENADE": dict(n=12, w=6.0, h=1.2, seg=6.0, gap=2.5), "RIBS": dict(n=16, w=4.0, h=1.0, seg=999.0, gap=0.0),
                  "PANELS": dict(n=8, w=10.0, h=1.0, seg=20.0, gap=3.0)}[style]
            bm = bmesh.new(); z0, z1 = 4.0, PSH - 6.0
            def blk(phi, za, zb, w, h):
                ca, sa = math.cos(math.radians(phi)), math.sin(math.radians(phi)); t = (-sa, ca)
                bw = w / 2; r0 = math.sqrt(R**2 - bw**2) - 0.4; d = R + h - r0; tw = max(bw - d, 0.3); tz0, tz1 = za + d, zb - d
                if tz1 - tz0 < 0.6: tz0, tz1 = (za + zb) / 2 - 0.3, (za + zb) / 2 + 0.3
                P = lambda r, s_, z: bm.verts.new((r*ca + s_*t[0], r*sa + s_*t[1], z))
                B = [P(r0, -bw, za), P(r0, bw, za), P(r0, bw, zb), P(r0, -bw, zb)]
                T = [P(R + h, -tw, tz0), P(R + h, tw, tz0), P(R + h, tw, tz1), P(R + h, -tw, tz1)]
                bm.faces.new(B[::-1]); bm.faces.new(T)
                for i in range(4):
                    j = (i + 1) % 4; bm.faces.new((B[i], B[j], T[j], T[i]))
            for k in range(gs["n"]):
                phi = 360.0 * k / gs["n"] + (180.0 / gs["n"] if style == "GRENADE" else 0.0)
                if gs["seg"] > 900: blk(phi, z0, z1, gs["w"], gs["h"]); continue
                n_ = int((z1 - z0 + gs["gap"]) // (gs["seg"] + gs["gap"])); L = (z1 - z0 - (n_ - 1) * gs["gap"]) / n_
                if style == "GRENADE": L = gs["seg"]; n_ = int((z1 - z0 + gs["gap"]) // (L + gs["gap"]))
                off = (z1 - z0 - (n_ * L + (n_ - 1) * gs["gap"])) / 2
                for i in range(n_):
                    za = z0 + off + i * (L + gs["gap"])
                    if style == "GRENADE" and k % 2: za += (L + gs["gap"]) / 2       # versetzte Reihen
                    if za + L <= z1 + 0.01: blk(phi, za, za + L, gs["w"], gs["h"])
            boolean(g, mkobj("t", bm), 'UNION')
        return g
    for st in ("CLASSIC", "GRENADE", "RIBS", "PANELS"):
        parts.append(grip_body("Grip_Body_" + st.capitalize(), st))

# =================== Aufraeumen ===================
for o in parts:
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0005)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=0.002)
    bmesh.ops.delete(bm, geom=[e for e in bm.edges if not e.link_faces], context='EDGES')
    bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=0)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(o.data); bm.free()
    o.name = o.name.split(".")[0] + {"SLIM": "_SLIM", "MINI": "_MINI"}.get(SIZE, "")
print("Saber ends", SIZE, "gebaut:", [o.name for o in parts])
