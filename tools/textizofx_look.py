#!/usr/bin/env python3
"""TextizoFX look helper (Python 3, standard library only).

Commands:
  build    <spec.json> [<out.setting>]       write a TextizoFX node from a short JSON spec, then check it
  check    <file.setting>... [--frames N]    check a look and print its timing
  to-spec  <file.setting> [<out.json>]       turn a TextizoFX node (or a Textizo preset) into a spec to edit
  looks                                      the ready looks in presets/
  controls [--page P] [--find TEXT]          TextizoFX's controls: IDs, labels, defaults, menus
  timing   --text "..." --span S --delay D   Start/End Frame and Stagger % for a row
  where                                      the folders looks can go to
  next-name [--to mylooks] [--variant 7]     the next free short name, like TextizoFX-07A
  install  <file.setting>... --to mylooks|resolve|downloads|<folder> [--overwrite]

The rules this tool applies are written out in "TextizoFX AI Guide.md". It reads reference/inputs.json, the list of
TextizoFX's controls made from the plugin itself.
"""
import argparse
import json
import math
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
INPUTS_PATH = os.path.join(KIT, "reference", "inputs.json")
PRESETS = os.path.join(KIT, "presets")
MY_LOOKS = os.path.join(KIT, "my-looks")
NODE_KIND = "ofx.com.clipizo.textizofx"
OTHER_NODES = ("ofx.com.clipizo.textizocaptions", "ofx.com.clipizo.captionizofx", "ofx.com.clipizo.popizo")

PAGES = ("In", "Out")
ROWS = ("opacity", "blur", "center", "size", "tracking", "rotation", "explosion")
ROW_ALIASES = {"position": "center", "pos": "center", "scale": "size", "spin": "rotation"}
ROW_FIELDS = ("Follower", "AnimationStart", "AnimationEnd", "Stagger", "StartValue", "EndValue",
              "CurveMode", "CurvePreset", "CurvePresetID")
EXPLOSION_FIELDS = ("Damping", "Speed", "RotationX", "RotationY", "Rotation", "Offset", "Reverse")
ELEMENT_FIELDS = ("Enable", "Appearance", "Opacity", "Thickness", "Offset", "SoftnessX", "SoftnessY",
                  "BorderLevel", "BorderExtendX", "BorderExtendY", "BorderRound", "ColorMode",
                  "GradientAngle", "MappingSize", "MappingAspect", "MappingLevel",
                  "Red", "Green", "Blue", "Alpha", "EndRed", "EndGreen", "EndBlue", "EndAlpha")
EASES = ["linear"] + ["%s_%s" % (kind, curve)
                      for curve in ("quad", "cubic", "quart", "quint", "sine", "expo", "circ", "back", "elastic", "bounce")
                      for kind in ("in", "out", "in_out")]
OVERSHOOT_EASES = {e for e in EASES if e.endswith(("back", "elastic", "bounce"))}
FOLLOWERS = ("letters", "words", "lines")
APPEARANCES = {"normal": 0, "fill": 0, "outline": 1, "stroke_only": 1, "stroke": 1,
               "border_fill": 2, "box": 2, "border_stroke": 3, "box_outline": 3}
APPEARANCE_NAMES = ["normal", "outline", "border_fill", "border_stroke"]
LEVELS = {"letters": 0, "letter": 0, "words": 1, "word": 1, "lines": 2, "line": 2}
MAPPING_LEVELS = {"letters": 0, "letter": 0, "words": 1, "word": 1, "lines": 2, "line": 2, "text": 3}
ALIGN = {"left": 0, "center": 1, "centre": 1, "right": 2}
ANCHORS = {"top": 0, "center": 1, "centre": 1, "baseline": 2, "bottom": 3}
SAFE_FONTS = ("Arial", "Arial Black", "Verdana", "Tahoma", "Trebuchet MS", "Georgia",
              "Times New Roman", "Courier New", "Impact", "Comic Sans MS")
STATE_VERSION = 12
BLUR_CAP_1080 = 30.0 / (1080 * 0.10)  # the Blur row stops growing above this at 1080p
SOFTNESS_CAP_1080 = 14.0 / (1080 * 0.10)  # shading softness stops growing above this at 1080p
EFFECTS = ("Glow", "Fire", "Frost", "Smoke", "Electric", "Rays", "Shine", "Sparkle", "Glitch", "Dust", "Float")

# Rough layout estimates (Size 1 = Text+ 0.08: one em is 0.064 x Size of the frame width). Arial advance widths per
# 1000 em; other fonts scale them.
ARIAL_WIDTHS = dict(zip(
    " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~",
    [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 +
    [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722,
     778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500,
     556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500,
     500, 500, 334, 260, 334, 584]))
# Measured in TextizoFX (2026-11-24: the drawn width of three samples at Size 1, the widest of the three, against these
# Arial widths); a Bold style multiplies by 1.07. TextizoFX scales each font by its own height, so heavy fonts are less
# wide than their names suggest (Arial Black 0.87).
FONT_WIDTH_FACTOR = {"Arial": 0.89, "Arial Black": 0.87, "Verdana": 0.92, "Tahoma": 0.82, "Trebuchet MS": 0.86,
                     "Georgia": 0.9, "Times New Roman": 0.89, "Impact": 0.76, "Comic Sans MS": 0.75,
                     "Anton": 0.6, "Bebas Neue": 0.63, "Oswald": 0.58, "Bangers": 0.8, "Archivo Black": 1.13,
                     "Luckiest Guy": 1.18, "Montserrat": 0.93, "Poppins": 0.79, "Kanit": 0.68, "Fredoka": 0.8,
                     "Rubik": 0.91, "Inter": 0.87, "Open Sans": 0.79, "Roboto": 0.81, "Nunito": 0.73, "Barlow": 0.79,
                     "Permanent Marker": 0.8, "Vazirmatn": 0.62}
COURIER_EM = 0.53  # Courier New: every character, measured as above
EM_PER_SIZE = 0.064
CAP_HEIGHT_EM = 0.716
LINE_HEIGHT_EM = 1.15
DESCENT_EM = 0.21


# --------------------------------------------------------------------------- reading Fusion settings

class Table:
    """A Lua table from a settings file; `kind` is the constructor name (Input, FuID, ...)."""

    def __init__(self, kind=None):
        self.kind = kind
        self.fields = {}
        self.items = []
        self.duplicates = []

    def get(self, key, default=None):
        return self.fields.get(key, default)


class Ref:
    def __init__(self, name):
        self.name = name


TOKEN_RE = re.compile(r"""
    (?P<ws>\s+)
  | (?P<comment>--\[(?P<ceq>=*)\[.*?\](?P=ceq)\]|--[^\n]*)
  | (?P<str>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
  | (?P<longstr>\[(?P<leq>=*)\[.*?\](?P=leq)\])
  | (?P<num>-?(?:0[xX][0-9a-fA-F]+|(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?))
  | (?P<name>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<sym>[{}\[\]=,;().])
""", re.S | re.X)


def unescape_lua(body):
    simple = {"n": "\n", "t": "\t", "r": "\r", "a": "\a", "b": "\b", "f": "\f", "v": "\v",
              "\\": "\\", '"': '"', "'": "'", "\n": "\n"}
    raw = body.encode("utf-8")
    data = bytearray()
    i = 0
    while i < len(raw):
        c = raw[i:i + 1]
        if c != b"\\":
            data += c
            i += 1
            continue
        nxt = raw[i + 1:i + 2].decode("latin-1")
        if nxt in simple:
            data += simple[nxt].encode("utf-8")
            i += 2
        elif nxt.isdigit():
            m = re.match(rb"\d{1,3}", raw[i + 1:])
            data.append(int(m.group(0)) & 0xFF)
            i += 1 + len(m.group(0))
        elif nxt == "x":
            data.append(int(raw[i + 2:i + 4], 16))
            i += 4
        elif nxt == "z":
            i += 2
            while i < len(raw) and raw[i:i + 1].isspace():
                i += 1
        else:
            data += raw[i + 1:i + 2]
            i += 2
    return data.decode("utf-8", "replace")


def tokenize(text):
    pos, tokens = 0, []
    while pos < len(text):
        m = TOKEN_RE.match(text, pos)
        if not m:
            line = text.count("\n", 0, pos) + 1
            raise ValueError("cannot read the settings text at line %d: %r" % (line, text[pos:pos + 20]))
        pos = m.end()
        kind = m.lastgroup
        if kind in ("ws", "comment"):
            continue
        if kind in ("ceq", "leq"):
            kind = "longstr" if m.group("longstr") else "comment"
            if kind == "comment":
                continue
        value = m.group(kind)
        if kind == "str":
            tokens.append(("str", unescape_lua(value[1:-1])))
        elif kind == "longstr":
            eq = len(m.group("leq"))
            body = value[2 + eq:-(2 + eq)]
            tokens.append(("str", body[1:] if body.startswith("\n") else body))
        elif kind == "num":
            tokens.append(("num", float(int(value, 16)) if "x" in value.lower() else float(value)))
        else:
            tokens.append((kind, value))
    return tokens


class Parser:
    def __init__(self, text):
        self.tokens = tokenize(text)
        self.i = 0

    def peek(self, offset=0):
        j = self.i + offset
        return self.tokens[j] if j < len(self.tokens) else ("eof", None)

    def take(self, kind=None, value=None):
        tok = self.peek()
        if (kind and tok[0] != kind) or (value is not None and tok[1] != value):
            raise ValueError("expected %s but found %r" % (value or kind, tok[1]))
        self.i += 1
        return tok

    def value(self):
        kind, val = self.peek()
        if kind == "sym" and val == "{":
            return self.table(None)
        if kind == "str":
            self.i += 1
            return val
        if kind == "num":
            self.i += 1
            return int(val) if val.is_integer() and abs(val) < 1e15 else val
        if kind == "name":
            self.i += 1
            if val in ("true", "false"):
                return val == "true"
            if val == "nil":
                return None
            name = val
            while self.peek() == ("sym", "."):
                self.i += 1
                name += "." + self.take("name")[1]
            if self.peek() == ("sym", "("):
                self.take("sym", "(")
                self.take("sym", ")")
                name += "()"
            if self.peek() == ("sym", "{"):
                return self.table(name)
            return Ref(name)
        raise ValueError("unexpected %r" % (val,))

    def table(self, kind):
        t = Table(kind)
        self.take("sym", "{")
        while self.peek() != ("sym", "}"):
            kind_, val = self.peek()
            if kind_ == "name" and self.peek(1) == ("sym", "="):
                self.i += 2
                key = val
                if key in t.fields:
                    t.duplicates.append(key)
                t.fields[key] = self.value()
            elif kind_ == "sym" and val == "[":
                self.i += 1
                key = self.value()
                self.take("sym", "]")
                self.take("sym", "=")
                t.fields[key] = self.value()
            else:
                t.items.append(self.value())
            if self.peek()[0] == "sym" and self.peek()[1] in (",", ";"):
                self.i += 1
        self.take("sym", "}")
        return t


def read_setting(path):
    with open(path, "r", encoding="utf-8-sig", errors="replace") as handle:
        text = handle.read()
    root = Parser(text).value()
    if not isinstance(root, Table):
        raise ValueError("the file does not start with {")
    return root


def input_value(entry):
    """Value of `X = Input { Value = ... }`; Ref for connections."""
    if not isinstance(entry, Table) or entry.kind != "Input":
        return None
    if "SourceOp" in entry.fields:
        return Ref("connected to " + str(entry.fields.get("SourceOp")))
    return entry.fields.get("Value")


# --------------------------------------------------------------------------- the control list

_DATA = None


def load_inputs():
    """reference/inputs.json, with the node names indexed: data["by_node"][node input name] = engine input id."""
    global _DATA
    if _DATA is None:
        with open(INPUTS_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        by_node, by_param = {}, {}
        for input_id, spec in data["inputs"].items():
            node = spec.get("node")
            if node:
                by_node[node["name"]] = input_id
                by_param.setdefault(node.get("param", node["name"]), []).append(input_id)
        data["by_node"] = by_node
        data["by_param"] = by_param
        _DATA = data
    return _DATA


def fuid(value):
    if isinstance(value, Table) and value.kind == "FuID" and value.items:
        return str(value.items[0])
    return None


def make_fuid(name):
    t = Table("FuID")
    t.items = [name]
    return t


def point(value):
    if isinstance(value, Table) and value.kind is None and len(value.items) == 2 and all(
            isinstance(v, (int, float)) and not isinstance(v, bool) for v in value.items):
        return (float(value.items[0]), float(value.items[1]))
    if isinstance(value, (list, tuple)) and len(value) == 2 and all(is_number(v) for v in value):
        return (float(value[0]), float(value[1]))
    return None


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def same_value(a, b):
    if is_number(a) and is_number(b):
        return abs(float(a) - float(b)) <= 1e-6
    if fuid(a) is not None or fuid(b) is not None:
        # (a menu's default in inputs.json is its plain id: "letters" is the same as FuID { "letters" })
        fa = fuid(a) if fuid(a) is not None else (a if isinstance(a, str) else None)
        fb = fuid(b) if fuid(b) is not None else (b if isinstance(b, str) else None)
        return fa == fb
    if point(a) is not None or point(b) is not None:
        pa, pb = point(a), point(b)
        return pa is not None and pb is not None and all(abs(x - y) <= 1e-6 for x, y in zip(pa, pb))
    if isinstance(a, Table) and isinstance(b, Table):
        return gradient_stops(a) == gradient_stops(b)
    return a == b


def gradient_stops(value):
    """[(position, (r, g, b, a)), ...] of a Fusion Gradient table or of TextizoFX's gradient text."""
    if isinstance(value, str):
        stops = []
        for part in value.split(";"):
            m = re.fullmatch(r"\s*([-\d.eE]+):([-\d.eE]+),([-\d.eE]+),([-\d.eE]+),([-\d.eE]+)\s*", part)
            if not m:
                return None
            nums = [float(x) for x in m.groups()]
            stops.append((round(nums[0], 6), tuple(round(c, 6) for c in nums[1:])))
        return sorted(stops) if stops else None
    if not isinstance(value, Table) or value.kind != "Gradient":
        return None
    colors = value.get("Colors")
    if not isinstance(colors, Table):
        return None
    stops = []
    for pos, color in colors.fields.items():
        if not is_number(pos) or not isinstance(color, Table) or len(color.items) < 3:
            return None
        c = [float(x) for x in color.items] + ([1.0] if len(color.items) == 3 else [])
        stops.append((round(float(pos), 6), tuple(round(x, 6) for x in c[:4])))
    return sorted(stops)


def gradient_text(stops):
    def g(v):
        return ("%.6g" % v)
    return ";".join("%s:%s,%s,%s,%s" % (g(pos), g(c[0]), g(c[1]), g(c[2]), g(c[3] if len(c) > 3 else 1.0)) for pos, c in stops)


def plain_default(value):
    """An inputs.json default as a settings value (points become a point table)."""
    if isinstance(value, list) and len(value) == 2:
        t = Table(None)
        t.items = list(value)
        return t
    return value


def describe(value):
    if isinstance(value, Ref):
        return value.name
    if fuid(value) is not None:
        return fuid(value)
    if point(value) is not None:
        return "(%s, %s)" % tuple(fmt_num(v) for v in point(value))
    if gradient_stops(value) is not None and not isinstance(value, str):
        return "gradient %d stops" % len(gradient_stops(value))
    if is_number(value):
        return fmt_num(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=True)
    return str(value)


# --------------------------------------------------------------------------- TextizoFX nodes <-> the engine's inputs
# A TextizoFX node holds its controls as Fusion keeps an OpenFX node's: menus as their number (from 0), checkboxes 0 or
# 1, a colour by channel (<colour>Red, <colour>Green ...), points { x, y }, text and gradients as text. The checks and
# the spec builder work on the engine's inputs (the IDs the guide uses, as in Textizo's presets: menus by their ID).

def node_to_engine(node_name, value, data):
    """(engine input id, value as the engine reads it) for one input of a TextizoFX node; (None, why) if unknown."""
    input_id = data["by_node"].get(node_name)
    if input_id is None:
        return None, "unknown input %s (not a TextizoFX control; check the spelling and capitals)" % node_name
    spec = data["inputs"][input_id]
    kind = spec["node"]["kind"]
    if isinstance(value, Ref):
        return input_id, value
    if kind == "choice_id":
        ids = spec["node"].get("ids") or []
        if fuid(value) is not None:  # FuID { "id" } (a Textizo preset's way): read as TextizoFX reads it, not at all
            return input_id, Ref('FuID { "%s" } (a TextizoFX node takes the menu\'s number: %s)' % (
                fuid(value), ", ".join("%d %s" % (i, x) for i, x in enumerate(ids))))
        if is_number(value) and float(value).is_integer() and 0 <= value < len(ids):
            return input_id, make_fuid(ids[int(value)])
        return input_id, value
    if kind == "gradient":
        if isinstance(value, str):
            stops = gradient_stops(value) if value.strip() else None
            return input_id, (gradient_table(stops) if stops else value)
        return input_id, value
    return input_id, value


def gradient_table(stops):
    g = Table("Gradient")
    colors = Table(None)
    for pos, c in stops:
        t = Table(None)
        t.items = list(c)
        colors.fields[pos] = t
    g.fields["Colors"] = colors
    return g


def engine_tool(tool, data, report=None):
    """A TextizoFX node (or a Textizo preset) as a tool whose Inputs are the engine's."""
    inputs = tool.get("Inputs")
    out = Table(tool.kind)
    t = Table(None)
    out.fields["Inputs"] = t
    if not isinstance(inputs, Table):
        return out
    t.duplicates = list(inputs.duplicates)
    preset = tool.kind == "Fuse.Textizo"
    for name, entry in inputs.fields.items():
        if not isinstance(entry, Table) or entry.kind != "Input":
            if report:
                report.error("%s must be written as %s = Input { Value = ..., }," % (name, name))
            continue
        value = input_value(entry)
        if preset:
            input_id = name if name in data["inputs"] else None
            if input_id is None:
                if report and name not in ("Width", "Height", "UseFrameFormatSettings", "GlobalIn", "GlobalOut"):
                    report.note("%s is a Textizo input TextizoFX doesn't have; it is left out" % name)
                continue
        else:
            input_id, value = node_to_engine(name, value, data)
            if input_id is None:
                if report:
                    report.error(value)
                continue
        e = Table("Input")
        e.fields["Value"] = value
        t.fields[input_id] = e
    return out


def find_tools(root, data, report=None):
    """[(name, engine tool, kind)] of the TextizoFX nodes (and Textizo presets) in a settings file, other nodes."""
    tools = root.get("Tools")
    if not isinstance(tools, Table):
        raise ValueError("no Tools = ordered() { ... } block")
    found, others = [], []
    for name, tool in tools.fields.items():
        if isinstance(tool, Table) and (tool.kind == NODE_KIND or tool.kind == "Fuse.Textizo" or tool.kind in OTHER_NODES):
            found.append((name, engine_tool(tool, data, report), tool.kind))
        elif isinstance(tool, Table):
            others.append((name, tool.kind))
    return found, others


def encode(input_id, value, data):
    """The text TextizoFX's node holds for engine input `input_id` set to `value`."""
    spec = data["inputs"][input_id]
    node = spec["node"]
    kind = node["kind"]
    if kind == "choice_id":
        ids = node.get("ids") or []
        name = fuid(value) if fuid(value) is not None else (value if isinstance(value, str) else None)
        if name is not None:
            if name not in ids:
                raise ValueError("%s: %r is not one of %s" % (input_id, name, ", ".join(ids)))
            return str(ids.index(name))
        if is_number(value):
            return fmt_num(int(value))
        raise ValueError("%s needs one of: %s" % (input_id, ", ".join(ids)))
    if kind == "bool":
        if isinstance(value, bool):
            return "1" if value else "0"
        if is_number(value):
            return "1" if value >= 0.5 else "0"
        raise ValueError("%s is a checkbox: 0 or 1" % input_id)
    if kind == "double2d":
        p = point(value)
        if p is None:
            raise ValueError("%s needs a point [x, y]" % input_id)
        return "{ %s, %s }" % (fmt_num(p[0]), fmt_num(p[1]))
    if kind == "gradient":
        stops = gradient_stops(value) if not isinstance(value, Gradient) else value.stops
        if isinstance(value, Gradient):
            stops = sorted((float(p), tuple(c)) for p, c in value.stops)
        if stops is None:
            if isinstance(value, str):
                return lua_string(value)
            raise ValueError("%s needs a gradient" % input_id)
        return lua_string(gradient_text(stops))
    if kind == "string":
        if not isinstance(value, str):
            raise ValueError('%s needs text in quotes' % input_id)
        return lua_string(value)
    if isinstance(value, bool):
        return "1" if value else "0"
    if not is_number(value):
        raise ValueError("%s needs a number (it is %s)" % (input_id, describe(value)))
    return fmt_num(value)


def write_node(values, data, compact=False, keep=()):
    """A TextizoFX node from engine values {input id: value} (complete: every look control written out, the rest at
    their defaults; compact: only what differs from TextizoFX's defaults, and the inputs named in `keep`)."""
    lines = []
    for input_id, spec in data["inputs"].items():
        node = spec.get("node")
        if not node or spec.get("role") != "public":
            continue
        if input_id in values:
            value = values[input_id]
        else:
            if compact:
                continue
            value = plain_default(spec.get("default"))
            if value is None:
                continue
            if spec["node"]["kind"] == "choice_id" and isinstance(value, str):
                value = make_fuid(value)
        if compact and input_id not in keep and same_value(value, plain_default(spec.get("default"))):
            continue
        lines.append("\t\t\t\t%s = Input { Value = %s, }," % (node["name"], encode(input_id, value, data)))
    return "\n".join(["{", "\tTools = ordered() {", "\t\tTextizoFX1 = %s {" % NODE_KIND, "\t\t\tInputs = {"] + lines +
                     ["\t\t\t},", "\t\t\tViewInfo = OperatorInfo { Pos = { 0, 0 } },", "\t\t},", "\t},",
                     '\tActiveTool = "TextizoFX1"', "}", ""])


# --------------------------------------------------------------------------- timing (as the node computes it)

MARK_RANGES = ((0x0300, 0x036F), (0x0591, 0x05BD), (0x05BF, 0x05BF), (0x05C1, 0x05C2), (0x05C4, 0x05C5),
               (0x05C7, 0x05C7), (0x0610, 0x061A), (0x064B, 0x065F), (0x0670, 0x0670), (0x06D6, 0x06DC),
               (0x06DF, 0x06E4), (0x06E7, 0x06E8), (0x06EA, 0x06ED), (0x0E31, 0x0E31), (0x0E34, 0x0E3A),
               (0x0E47, 0x0E4E), (0xFE20, 0xFE2F))
CJK_RANGES = ((0x3040, 0x30FF), (0x31F0, 0x31FF), (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF),
              (0x20000, 0x2FFFF))
INVISIBLE_RANGES = ((0x200B, 0x200F), (0x202A, 0x202E), (0x2066, 0x2069), (0xFEFF, 0xFEFF), (0x061C, 0x061C))
LAM, ALEFS = 0x0644, (0x0622, 0x0623, 0x0625, 0x0627)


def in_ranges(code, ranges):
    return any(lo <= code <= hi for lo, hi in ranges)


def count_groups(text, by):
    """Letters, words or lines as TextizoFX counts them: accent and vowel marks belong to their letter, an Arabic lam +
    alef is one letter, each Chinese or Japanese character is a word."""
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    letters = words = lines = 0
    for line in text.split("\n"):
        chars = [ch for ch in line if not in_ranges(ord(ch), INVISIBLE_RANGES)]
        in_word = has_glyph = previous_cjk = False
        skip = set()
        for index, ch in enumerate(chars):
            code = ord(ch)
            if index in skip:
                continue
            if ch in " \t":
                in_word = previous_cjk = False
            elif in_ranges(code, MARK_RANGES) and has_glyph:
                continue
            else:
                if code == LAM:
                    after = index + 1
                    while after < len(chars) and in_ranges(ord(chars[after]), MARK_RANGES):
                        after += 1
                    if after < len(chars) and ord(chars[after]) in ALEFS:
                        skip.add(after)
                cjk = in_ranges(code, CJK_RANGES)
                if in_word and (cjk or (previous_cjk and ch.isalpha())):
                    in_word = False
                letters += 1
                has_glyph = True
                if not in_word:
                    words += 1
                    in_word = True
                previous_cjk = cjk
        if has_glyph:
            lines += 1
    return max(1, {"letters": letters, "words": words, "lines": lines}.get(by, letters))


def round_int(x):
    return int(math.floor(float(x) + 0.5))


def row_window(start, end, stagger, groups):
    """(frames each group moves, frames between groups) for a row."""
    window = max(1, round_int(end) - max(0, round_int(start)))
    groups = max(1, int(groups))
    fraction = max(0.0, float(stagger)) / 100.0
    delay = 0.0
    if groups > 1:
        delay = min(fraction * window / (1.0 + fraction * (groups - 1)), (window - 1) / (groups - 1))
    span = max(1.0, window - delay * (groups - 1))
    return span, delay


def plan_row(start, span, delay, groups):
    """Start Frame, End Frame and Stagger % that give each group `span` frames, `delay` apart."""
    if groups <= 1 or delay <= 0:
        return start, start + max(1, round_int(span)), 0.0
    return start, start + max(1, round_int(span + delay * (groups - 1))), round(delay / span * 100.0, 1)


# --------------------------------------------------------------------------- check

class Report:
    def __init__(self):
        self.errors, self.warnings, self.notes, self.info = [], [], [], []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def note(self, msg):
        self.notes.append(msg)


def check_type(spec, value):
    """None when `value` fits the input, else a short reason."""
    dtype = spec.get("type")
    if isinstance(value, Ref):
        if dtype == "LookUpTable" or spec.get("keyed"):
            return None
        return value.name if value.name.startswith("FuID") else "is connected to another node"
    kind = (spec.get("node") or {}).get("kind")
    if kind == "choice_id":
        fid = fuid(value)
        if fid is None:
            ids = spec["node"].get("ids") or []
            return "must be a menu number: %s" % ", ".join("%d %s" % (i, x) for i, x in enumerate(ids))
        return None
    if dtype in ("Number",) or kind in ("double", "bool", "choice", "rgba", "rgb"):
        if not is_number(value):
            return "needs a number"
        options = spec.get("options")
        if kind == "bool" and value not in (0, 1):
            return "is a checkbox: use 0 or 1"
        if options and kind == "choice":
            if not float(value).is_integer() or not 0 <= value < len(options):
                return "must be one of 0..%d (%s)" % (len(options) - 1, ", ".join(
                    "%d %s" % (i, o.get("label") or o.get("id")) for i, o in enumerate(options)))
        lo, hi = spec.get("min"), spec.get("max")
        if lo is not None and value < lo or hi is not None and value > hi:
            return "must be between %s and %s" % (fmt_num(lo) if lo is not None else "-inf", fmt_num(hi) if hi is not None else "inf")
        return None
    if dtype in ("Text", "StyledText") or kind == "string":
        return None if isinstance(value, str) else 'needs text in quotes, like "Hello"'
    if dtype == "Point" or kind == "double2d":
        return None if point(value) is not None else "needs a point { x, y }"
    if dtype == "Gradient" or kind == "gradient":
        if isinstance(value, str) and not value.strip():
            return None
        return None if gradient_stops(value) else 'needs gradient text like "0:1,1,1,1;1:0,0,0,1" (position:r,g,b,a)'
    return None


def em_widths(text, font, style):
    """Advance width of `text` in ems (rough: Arial metrics scaled per font)."""
    if font == "Courier New":
        return COURIER_EM * len(text)
    factor = FONT_WIDTH_FACTOR.get(font, 1.0)
    if "bold" in (style or "").lower() and font != "Arial Black":
        factor *= 1.07
    return sum(ARIAL_WIDTHS.get(ch, 556) for ch in text) / 1000.0 * factor


def check_layout(values, spec_inputs, report, aspect):
    """Rough resting layout: line widths, frame edges, word boxes touching."""
    def get(input_id):
        v = values.get(input_id)
        return spec_inputs.get(input_id, {}).get("default") if v is None else v

    text = (values.get("StyledText") or "").replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip():
        return None
    font, style = get("Font") or "Arial", get("Style") or "Regular"
    size = float(get("Size") or 1.0)
    tracking = float(get("Tracking") or 0.0)
    line_spacing = float(get("LineSpacing") or 1.0)
    align = int(get("Alignment") if is_number(get("Alignment")) else 1)
    anchor = int(get("VerticalAnchor") if is_number(get("VerticalAnchor")) else 1)
    fit = is_number(get("FitToFrame")) and get("FitToFrame") >= 0.5
    center = point(values.get("Center")) or point(get("Center")) or (0.5, 0.5)
    em_w = EM_PER_SIZE * size              # frame widths
    em_h = em_w * aspect                   # frame heights
    lines = text.split("\n")
    widths = [em_widths(line, font, style) * em_w + tracking * max(0, len(line) - 1) for line in lines]
    widest = max(widths)
    if widest > 0.95:
        if fit:
            report.note("the longest line is about %.2f frame widths wide: Fit to Frame shrinks the text to keep a margin "
                        "(Size about %s fits without it)" % (widest, fmt_num(round(size * 0.85 / widest, 2))))
        else:
            report.warn("the longest line is about %.2f frame widths wide, wider than the frame: use Size about %s, "
                        "split the text into more lines, or turn Fit to Frame on" % (widest, fmt_num(round(size * 0.85 / widest, 2))))
    elif widest > 0.86:
        report.note("the longest line is about %.2f frame widths wide, close to the frame edges" % widest)
    if widest <= 0.95:
        left = center[0] - {0: 0.0, 1: widest / 2.0, 2: widest}.get(align, widest / 2.0)
        right = left + widest
        block = CAP_HEIGHT_EM * em_h + (len(lines) - 1) * LINE_HEIGHT_EM * em_h * line_spacing + DESCENT_EM * em_h
        if anchor == 2:  # Baseline: the first line's baseline sits on Center
            top = center[1] + CAP_HEIGHT_EM * em_h
        elif anchor == 0:
            top = center[1]
        elif anchor == 3:
            top = center[1] + block
        else:
            top = center[1] + block / 2.0
        bottom = top - block
        outside = [name for name, bad in (("left", left < 0.02), ("right", right > 0.98),
                                          ("top", top > 0.98), ("bottom", bottom < 0.02)) if bad]
        if outside:
            report.warn("at rest the text reaches past the %s edge of the frame (text spans x %.2f to %.2f, y %.2f to %.2f "
                        "in a %s frame); move Center or lower Size" % (
                            " and ".join(outside), left, right, bottom, top, "16:9" if abs(aspect - 16 / 9.0) < 0.01 else "%.2f:1" % aspect))
    return {"em_w": em_w, "font": font, "style": style}


def check_tool(tool_name, tool, data, report, clip_frames=None, aspect=16.0 / 9.0):
    spec_inputs = data["inputs"]
    inputs_table = tool.get("Inputs")
    if not isinstance(inputs_table, Table):
        report.error("%s has no Inputs = { ... } block" % tool_name)
        return
    for dup in inputs_table.duplicates:
        report.warn("%s is written twice; the last one wins" % dup)
    values = {}
    internal = []
    for input_id, entry in inputs_table.fields.items():
        spec = spec_inputs.get(input_id)
        value = input_value(entry)
        if spec is None:
            report.error("unknown input %s (not a TextizoFX control; check the spelling and capitals)" % input_id)
            continue
        if spec.get("role") != "public":
            internal.append(input_id)
        reason = check_type(spec, value)
        if reason:
            report.error("%s %s (it is %s)" % ((spec.get("node") or {}).get("name", input_id), reason, describe(value)))
            continue
        values[input_id] = value

    def num(input_id):
        v = values.get(input_id)
        if is_number(v):
            return float(v)
        d = spec_inputs.get(input_id, {}).get("default")
        return float(d) if is_number(d) else 0.0

    def has(input_id):
        return input_id in values

    # Whole-node inputs.
    if not has("StateVersion"):
        report.warn("add StateVersion = Input { Value = %d, }, (tells TextizoFX the look uses the current row format)" % STATE_VERSION)
    elif num("StateVersion") < STATE_VERSION:
        report.note("StateVersion %s: TextizoFX converts the rows as an older look's (as Textizo's presets before state %d); "
                    "new looks write %d" % (fmt_num(num("StateVersion")), STATE_VERSION, STATE_VERSION))
    if has("InEnable") and num("InEnable") < 0.5:
        report.warn("InEnable = 0 switches the whole node off (it renders nothing)")
    text = values.get("StyledText")
    if text is None:
        report.note("no StyledText: the look keeps the text the clip has (a new node shows TextizoFX's sample text)")
        text = ""
    elif text.strip() and not (has("TextEdited") and num("TextEdited") >= 0.5):
        report.note("add TextEdited = Input { Value = 1, }, next to StyledText (marks the text as the user's)")
    font = values.get("Font")
    carried = set(data.get("fonts") or [])
    if isinstance(font, str) and font not in SAFE_FONTS and font not in carried:
        report.note('font "%s" must be installed on the computer that opens the look (TextizoFX carries: %s; safe on '
                    'Windows and Mac: %s)' % (font, ", ".join(sorted(carried)), ", ".join(SAFE_FONTS)))
    if any(is_number(values.get(c)) and float(values.get(c)) < 0.999 for c in ("Red", "Green", "Blue")):
        report.note("the Text page Color is not white: it tints Shading element 1 (colour the element instead)")
    for effect in EFFECTS:
        letters = values.get("Fx%sLetters" % effect)
        if is_number(letters) and letters >= 0.5 and num("Fx%sOn" % effect) >= 0.5:
            report.warn("Fx%sLetters is %s: Selected Letters and Other Letters need letters picked in the viewer, which "
                        "a look can't carry; use 0 (All Letters)" % (effect, fmt_num(letters)))
    if internal:
        report.note("%d inputs TextizoFX keeps for itself were left as given (%s%s)" % (
            len(internal), ", ".join(internal[:4]), ", ..." if len(internal) > 4 else ""))
    layout = check_layout(values, spec_inputs, report, aspect)

    # Animation rows.
    rows_out = []
    snappy_rows = []
    in_done = None
    out_start = None
    last_frame = None
    rows_per_page = {"In": 0, "Out": 0}
    page_window = {"In": [None, None], "Out": [None, None]}  # first Start Frame, last landing
    followers_with_opacity = {"In": set(), "Out": set()}
    followers_used = {"In": set(), "Out": set()}
    for page in PAGES:
        for row in ROWS:
            prefix = page + row
            if num(prefix + "Enable") < 0.5:
                continue
            by = fuid(values.get(prefix + "Follower")) or spec_inputs.get(prefix + "Follower", {}).get("default") or "letters"
            start = num(prefix + "AnimationStart")
            end = num(prefix + "AnimationEnd")
            stagger = num(prefix + "Stagger")
            groups = count_groups(text, by)
            if round_int(end) <= round_int(start):
                report.warn("%s: End Frame (%s) must be after Start Frame (%s)" % (prefix, fmt_num(end), fmt_num(start)))
            span, delay = row_window(start, end, stagger, groups)
            if groups > 1 and stagger > 0:
                fraction = stagger / 100.0
                wanted = fraction * max(1, round_int(end) - round_int(start)) / (1.0 + fraction * (groups - 1))
                if wanted - delay > 1e-6:
                    report.note("%s: the gap between %s was shortened to %.2f frames so every one gets at least 1 frame" % (prefix, by, delay))
            if span < 1.0 + 1e-6:
                report.warn("%s: each %s jumps in a single frame; make End Frame later or Stagger %% smaller" % (prefix, by[:-1]))
            elif span < 2.0:
                snappy_rows.append("%s (%.1f frames)" % (prefix, span))
            ease = fuid(values.get(prefix + "CurvePreset")) or spec_inputs.get(prefix + "CurvePreset", {}).get("default") or "linear"
            mirror = values.get(prefix + "CurvePresetID")
            if isinstance(mirror, str) and mirror and mirror != ease:
                report.error('%sCurvePresetID ("%s") must match %sCurvePreset ("%s")' % (prefix, mirror, prefix, ease))
            if fuid(values.get(prefix + "CurveMode")) == "custom":
                report.note("%sCurveMode is custom: the row uses its own curve (made in the plugin's curve window), not the "
                            "Ease preset" % prefix)
            sv, ev = values.get(prefix + "StartValue"), values.get(prefix + "EndValue")
            if sv is None:
                sv = plain_default(spec_inputs.get(prefix + "StartValue", {}).get("default"))
            if ev is None:
                ev = plain_default(spec_inputs.get(prefix + "EndValue", {}).get("default"))
            if row == "opacity":
                for label, v in (("StartValue", sv), ("EndValue", ev)):
                    if is_number(v) and not 0 <= v <= 1:
                        report.warn("%s%s %s: opacity is 0..1" % (prefix, label, fmt_num(v)))
            if row in ("size", "blur", "explosion"):
                for label, v in (("StartValue", sv), ("EndValue", ev)):
                    if is_number(v) and v < 0:
                        report.warn("%s%s %s: negative values count as 0" % (prefix, label, fmt_num(v)))
            if row == "blur":
                for label, v in (("StartValue", sv), ("EndValue", ev)):
                    if is_number(v) and v > BLUR_CAP_1080:
                        report.note("%s%s %s: blur stops growing at about %.2f in 1080p" % (prefix, label, fmt_num(v), BLUR_CAP_1080))
            if row == "explosion":
                spins = [num(prefix + f) for f in ("RotationX", "RotationY", "Rotation")]
                if any(abs(s) > 1e-6 for s in spins):
                    report.warn("%s: Spin X/Y/Z are not 0; explosion spin jumps when a letter lands or overshoots. "
                                "Set them to 0 and turn letters with the Rotation row" % prefix)
                if ease in OVERSHOOT_EASES and page == "In" and num(prefix + "Damping") > 0:
                    report.note("%s: Damping above 0 delays the landing; 0 keeps the ease as chosen" % prefix)
            last_end = start + delay * (groups - 1) + span
            if page == "In":
                in_done = last_end if in_done is None else max(in_done, last_end)
            else:
                out_start = start if out_start is None else min(out_start, start)
            last_frame = last_end if last_frame is None else max(last_frame, last_end)
            window = page_window[page]
            window[0] = start if window[0] is None else min(window[0], start)
            window[1] = last_end if window[1] is None else max(window[1], last_end)
            if clip_frames is not None and last_end > clip_frames - 1 + 1e-6 and not (page == "Out" and num("OutAlignEnd") >= 0.5):
                report.warn("%s ends on frame %s, after the clip's last frame (%d)" % (prefix, fmt_num(last_end), clip_frames - 1))
            rows_per_page[page] += 1
            followers_used[page].add(by)
            if row == "opacity":
                followers_with_opacity[page].add(by)
            if row == "center":
                if ease == "linear":
                    report.note("%s: a linear ease on a position move looks mechanical; use an out_ ease (In) or in_ ease (Out)" % prefix)
                offset = point(sv if page == "In" else ev)
                if offset and abs(offset[0]) > 0.12:
                    report.note("%s: a sideways move of %s frame widths; the house style avoids long sideways slides" % (
                        prefix, fmt_num(round(abs(offset[0]), 3))))
            if page == "In" and span > 30:
                report.note("%s: each %s moves for %.0f frames; the house style keeps moves under about 14-16 frames at 24 fps" % (
                    prefix, by[:-1], span))
            rows_out.append((page, row, by, groups, round_int(start), round_int(end), stagger, span, delay, ease,
                             describe(sv) if page == "In" else "", describe(ev)))
    for page in PAGES:
        if not (has(page + "StopEnable") and num(page + "StopEnable") >= 0.5):
            continue
        stop = max(0, round_int(num(page + "StopFrame")))
        first, last = page_window[page]
        if first is None:
            report.warn("%sStopEnable is on but no %s row is: Stop at Frame changes nothing" % (page, page))
        elif stop <= first:
            report.warn("%sStopFrame %d is not after the %s rows start (frame %s): the page holds before anything moves"
                        % (page, stop, page, fmt_num(first)))
        elif stop >= last:
            report.note("%sStopFrame %d is after the %s rows land (frame %s): it changes nothing"
                        % (page, stop, page, fmt_num(round(last, 1))))
        else:
            report.note("the %s page holds from frame %d on, as it looks there (Stop at Frame)" % (page, stop))
            if page == "In":
                in_done = min(in_done, stop)
    if has("InStartAt") and num("InStartAt") > 0:
        report.note("Start At: the In rows count from frame %d" % round_int(num("InStartAt")))
    if num("OutAlignEnd") >= 0.5 and page_window["Out"][0] is not None:
        report.note("Align to End: the Out rows keep their lengths and gaps, and their last piece lands %d frames "
                    "before the clip's last frame at any clip length" % max(0, round_int(num("OutBeforeEnd"))))
    if snappy_rows:
        report.note("very snappy rows, each piece pops in under 2 frames (fine for a one-after-another pop): %s"
                    % ", ".join(snappy_rows))
    if in_done is not None and out_start is not None and out_start < in_done - 1e-6 and num("OutAlignEnd") < 0.5:
        report.warn("the Out rows start on frame %s, before the In rows finish (frame %s); the exit cuts the entrance short"
                    % (fmt_num(out_start), fmt_num(in_done)))
    if in_done is None:
        report.note("no In rows are on: the text is there from the first frame")
    if out_start is None:
        report.note("no Out rows are on: the text stays until the clip ends")
    for page in PAGES:
        if rows_per_page[page] > 6:
            report.note("%d rows are on the %s page; the house style uses about 3-4 (up to 6 for fun pops)" % (rows_per_page[page], page))
    if in_done is not None and in_done > 40:
        report.note("the entrance ends on frame %s: fine for a calm look; punchy titles finish in about 15-26 frames at 24 fps" % fmt_num(round(in_done)))
    if clip_frames is not None and last_frame is not None and clip_frames - 4 < last_frame <= clip_frames - 1 + 1e-6:
        report.note("the last row ends on frame %s, right at the end of the clip (last frame %d); leave a few frames" % (
            fmt_num(round(last_frame, 1)), clip_frames - 1))

    # Shading: the selected element is drawn from the ShadingProxy... controls.
    active = fuid(values.get("ShadingActiveElement")) or "element_1"
    active_index = int(active.split("_")[-1])
    for field in list(ELEMENT_FIELDS) + ["Gradient"]:
        proxy_id = "ShadingProxy" + field
        element_id = "ShadingElement%d%s" % (active_index, field)
        if has(proxy_id) and has(element_id) and not same_value(values[proxy_id], values[element_id]):
            report.error("%s (%s) must equal %s (%s): element %d is the one the Shading page shows, and TextizoFX keeps "
                         "it in both" % (proxy_id, describe(values[proxy_id]), element_id, describe(values[element_id]), active_index))
        elif has(element_id) != has(proxy_id):
            given, other = (element_id, proxy_id) if has(element_id) else (proxy_id, element_id)
            default = plain_default(spec_inputs.get(other, {}).get("default"))
            if not same_value(values[given], default):
                report.warn("%s is %s but %s is left out: element %d is the one the Shading page shows; write both "
                            "with the same value" % (given, describe(values[given]), other, active_index))
    shading_lines = []
    for index in range(1, 9):
        def eget(field, use_proxy=(index == active_index)):
            key = ("ShadingProxy" + field) if use_proxy and has("ShadingProxy" + field) else "ShadingElement%d%s" % (index, field)
            v = values.get(key)
            return v if v is not None else spec_inputs.get("ShadingElement%d%s" % (index, field), {}).get("default")
        enabled = eget("Enable")
        if not (is_number(enabled) and enabled >= 0.5):
            continue
        appearance = eget("Appearance")
        appearance = APPEARANCE_NAMES[int(appearance)] if is_number(appearance) and 0 <= appearance < 4 else "?"
        color = tuple(fmt_num(eget(c) if is_number(eget(c)) else 1) for c in ("Red", "Green", "Blue"))
        label = "element %d" % index
        for field, low, high in (("Opacity", 0, 1), ("Thickness", 0, None), ("SoftnessX", 0, None), ("SoftnessY", 0, None),
                                 ("BorderExtendX", 0, None), ("BorderExtendY", 0, None), ("BorderRound", 0, None)):
            v = eget(field)
            if is_number(v) and (v < low or (high is not None and v > high)):
                report.warn("%s %s is %s; it must be %s" % (label, field, fmt_num(v), "0 to 1" if high else "0 or more"))
        soft = eget("SoftnessX")
        if is_number(soft) and soft > SOFTNESS_CAP_1080 + 0.005:
            report.note("%s softness %s: softness stops growing at about %.2f in 1080p; for a wide glow use the Effects "
                        "page's Glow" % (label, fmt_num(soft), SOFTNESS_CAP_1080))
        extra = []
        if appearance in ("outline", "border_stroke"):
            extra.append("thickness %s" % describe(eget("Thickness")))
        if appearance in ("border_fill", "border_stroke"):
            level = eget("BorderLevel")
            level_name = ["letters", "words", "lines"][int(level)] if is_number(level) and 0 <= level <= 2 else "letters"
            extra.append("box per %s, extend (%s, %s), round %s" % (level_name[:-1], describe(eget("BorderExtendX")),
                                                                   describe(eget("BorderExtendY")), describe(eget("BorderRound"))))
            if level_name in ("words", "lines"):
                own = {"words": ("words", "lines"), "lines": ("lines",)}[level_name]
                for page in PAGES:
                    if followers_used[page] & {"letters"} and not followers_with_opacity[page] & set(own):
                        report.warn("%s: a box per %s only follows rows animated by %s, so on the %s page it %s while "
                                    "the letters animate. Add an %s Opacity row by %s" % (
                                        label, level_name[:-1], " or ".join(own), page,
                                        "is already there" if page == "In" else "stays", page, level_name))
            if level_name == "words" and layout:
                runs = [len(m.group(0)) for line in text.replace("\r", "").split("\n")
                        for m in re.finditer(r"(?<=\S)[ \t]+(?=\S)", line)]
                space = em_widths(" ", layout["font"], layout["style"]) * layout["em_w"]
                gap = min(runs) * space if runs else None
                extend_x = eget("BorderExtendX")
                if gap is not None and is_number(extend_x) and 2 * extend_x >= gap * 0.9:
                    report.warn("%s: boxes of neighbouring words touch or overlap (2 x BorderExtendX %s >= the space between "
                                "words, about %s). Put 2-3 spaces between the words, or use BorderExtendX below about %s" % (
                                    label, fmt_num(round(2 * extend_x, 4)), fmt_num(round(gap, 4)), fmt_num(round(gap * 0.35, 4))))
            if layout:
                em = layout["em_w"]
                pad_x, pad_y, rnd = eget("BorderExtendX"), eget("BorderExtendY"), eget("BorderRound")
                if is_number(pad_x) and is_number(pad_y) and min(pad_x, pad_y) < 0.15 * em:
                    report.note("%s: the box hugs the text (padding %s / %s = %.2f / %.2f em of the text size); about 0.3-0.6 em "
                                "across and 0.2-0.3 em up and down looks better" % (
                                    label, fmt_num(pad_x), fmt_num(pad_y), pad_x / em, pad_y / em))
                if is_number(rnd) and rnd < 0.15 * em:
                    report.note("%s: the corners are almost square (round %s = %.2f em); use about 0.25 em for soft corners "
                                "or 1 em for round pill ends" % (label, fmt_num(rnd), rnd / em))
        offset = eget("Offset")
        if point(offset) and any(abs(v) > 1e-9 for v in point(offset)):
            extra.append("offset %s" % describe(offset if isinstance(offset, Table) else plain_default(list(offset))))
        if is_number(soft) and soft > 0:
            extra.append("softness %s" % fmt_num(soft))
        opacity = eget("Opacity")
        if is_number(opacity) and opacity < 0.999:
            extra.append("opacity %s" % fmt_num(opacity))
        mode = eget("ColorMode")
        colour_text = "gradient" if is_number(mode) and mode >= 0.5 else "colour (%s, %s, %s)" % color
        shading_lines.append("element %d %s, %s%s" % (index, appearance, colour_text, (", " + ", ".join(extra)) if extra else ""))
    effects_on = [e for e in EFFECTS if num("Fx%sOn" % e) >= 0.5]
    report.info.append(("rows", rows_out))
    report.info.append(("shading", shading_lines))
    report.info.append(("effects", effects_on))
    report.info.append(("text", (text, values.get("Font"), values.get("Style"), values.get("Size"), values.get("Center"))))
    report.info.append(("timeline", (in_done, out_start)))


def print_report(path, report, tool_name=None, count=None, others=None):
    print("TextizoFX look check: %s" % os.path.basename(path))
    if tool_name:
        print("  node: %s, %d inputs" % (tool_name, count))
    for name, kind in others or []:
        print("  other node in the file: %s (%s)" % (name, kind))
    info = dict(report.info)
    if "text" in info:
        text, font, style, size, center = info["text"]
        print("  text: %s  font: %s %s  size: %s  center: %s" % (
            json.dumps(text, ensure_ascii=True), font or "(node's)", style or "", describe(size) if size is not None else "(node's)",
            describe(center) if center is not None else "(node's)"))
    if info.get("rows"):
        print("  rows (frames from the clip start; each = frames one group moves, gap = frames between groups):")
        for page, row, by, groups, start, end, stagger, span, delay, ease, sv, ev in info["rows"]:
            values = ("%s -> %s" % (sv, ev)) if page == "In" else ("-> %s" % ev)
            print("    %-3s %-9s %-7s x%-3d frames %3d-%-3d stagger %5s%%  each %5.1f  gap %4.1f  %-12s %s" % (
                page, "position" if row == "center" else row, by, groups, start, end, fmt_num(stagger), span, delay,
                ease, values))
    if "timeline" in info:
        in_done, out_start = info["timeline"]
        parts = []
        if in_done is not None:
            parts.append("entrance done on frame %s" % fmt_num(round(in_done, 1)))
        if out_start is not None:
            parts.append("exit starts on frame %s" % fmt_num(out_start))
        if parts:
            print("  " + ", ".join(parts))
    for line in info.get("shading", []):
        print("  shading: " + line)
    if info.get("effects"):
        print("  effects: " + ", ".join(info["effects"]))
    for title, items in (("ERRORS", report.errors), ("WARNINGS", report.warnings), ("NOTES", report.notes)):
        if items:
            print("%s (%d):" % (title, len(items)))
            for item in items:
                print("  - " + item)
    ok = not report.errors
    print("Result: %s (%d errors, %d warnings)" % ("OK" if ok else "FAILED", len(report.errors), len(report.warnings)))
    return ok


def check_file(path, data, frames=None, aspect=16.0 / 9.0, quiet=False):
    report = Report()
    try:
        root = read_setting(path)
        tools, others = find_tools(root, data, report)
    except (OSError, ValueError) as exc:
        if not quiet:
            print("TextizoFX look check: %s\nERRORS (1):\n  - %s\nResult: FAILED" % (os.path.basename(path), exc))
        return False, report
    if not tools:
        report.error("no TextizoFX node (%s) in the file" % NODE_KIND)
        if not quiet:
            print_report(path, report, None, 0, others)
        return False, report
    ok = True
    for name, tool, kind in tools:
        if kind == "Fuse.Textizo":
            report.note("this is a Textizo preset (the Fuse's): TextizoFX's Load Look... takes it, but pasted into Fusion "
                        "it makes a Textizo node. `to-spec` and `build` turn it into a TextizoFX node")
        elif kind != NODE_KIND:
            report.note("this is a %s node; Load Look... takes it, pasted it makes that plugin's node" % kind)
        check_tool(name, tool, data, report, frames, aspect)
        if not quiet:
            ok = print_report(path, report, name, len(tool.get("Inputs").fields), others) and ok
        else:
            ok = ok and not report.errors
    return ok, report


def cmd_check(args):
    data = load_inputs()
    all_ok = True
    for path in args.files:
        ok, _ = check_file(path, data, args.frames, args.aspect)
        all_ok = ok and all_ok
        print()
    return 0 if all_ok else 1


# --------------------------------------------------------------------------- writing looks

def fmt_num(value):
    if isinstance(value, bool):
        value = int(value)
    if isinstance(value, int):
        return str(value)
    value = float(value)
    if value.is_integer() and abs(value) < 1e15:
        return str(int(value))
    text = "%.15g" % value
    if float(text) != value:
        text = "%.17g" % value
    return text


def lua_string(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    out = ['"']
    for ch in text:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append("\\%03d" % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


class Gradient:
    """Colour stops [(position 0-1, (r, g, b, a)), ...]."""

    def __init__(self, stops):
        self.stops = stops


def parse_color(value, where):
    if isinstance(value, str):
        m = re.fullmatch(r"#?([0-9a-fA-F]{6})([0-9a-fA-F]{2})?", value.strip())
        if not m:
            raise ValueError('%s: colour "%s" must be [r, g, b] (0-1) or "#RRGGBB"' % (where, value))
        rgb = [int(m.group(1)[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
        alpha = int(m.group(2), 16) / 255.0 if m.group(2) else 1.0
        return [round(c, 4) for c in rgb] + [round(alpha, 4)]
    if isinstance(value, (list, tuple)) and len(value) in (3, 4) and all(is_number(c) for c in value):
        if any(c > 1.0 for c in value[:3]):
            raise ValueError("%s: colour values are 0-1 (divide 0-255 values by 255)" % where)
        return [float(c) for c in value[:3]] + [float(value[3]) if len(value) == 4 else 1.0]
    raise ValueError('%s: colour must be [r, g, b] (0-1) or "#RRGGBB"' % where)


def pair(value, where):
    if is_number(value):
        return [float(value), float(value)]
    if isinstance(value, (list, tuple)) and len(value) == 2 and all(is_number(v) for v in value):
        return [float(value[0]), float(value[1])]
    raise ValueError("%s must be a number or [x, y]" % where)


def expect_keys(obj, allowed, where):
    if not isinstance(obj, dict):
        raise ValueError("%s must be an object { ... }" % where)
    unknown = sorted(set(obj) - set(allowed))
    if unknown:
        raise ValueError("%s: unknown key(s) %s (allowed: %s)" % (where, ", ".join(unknown), ", ".join(sorted(allowed))))


def auto_center_y(size, lines, line_spacing, aspect, anchor):
    """Center Y that puts the text block in the middle of the frame for Vertical Anchor `anchor`."""
    if anchor == 1:
        return 0.5
    em = 0.064 * size * aspect  # em height in frame heights
    cap = 0.716 * em
    line = 1.15 * em * line_spacing
    block = cap + (lines - 1) * line
    if anchor == 2:  # Baseline: the first baseline sits on Center
        return round(0.5 - cap / 2.0 + (lines - 1) * line / 2.0, 4)
    if anchor == 0:  # Top
        return round(0.5 + block / 2.0, 4)
    return round(0.5 - block / 2.0, 4)  # Bottom


ROW_KEYS = {"by", "start", "end", "stagger", "span", "delay", "from", "to", "ease", "on", "offset",
            "variance", "damping", "spin_x", "spin_y", "spin_z", "pre_roll", "reverse", "pivot"}
PIVOTS = ("left", "center", "right")
ELEMENT_KEYS = {"enabled", "appearance", "color", "opacity", "thickness", "offset", "softness",
                "border_level", "extend", "round", "gradient"}
SPEC_KEYS = {"name", "look", "text", "font", "style", "size", "center", "align", "vertical_anchor", "tracking", "line_spacing",
             "rotation", "rotation_x", "rotation_y", "fit", "alpha", "color", "motion_blur", "in", "out", "in_direction",
             "out_direction", "in_stop", "out_stop", "in_start_at", "out_from_end", "elements", "inputs", "aspect", "frames", "notes"}
DIRECTIONS = ("reading", "ltr", "rtl")
BY_ALIASES = {"letter": "letters", "word": "words", "line": "lines"}


def british(obj):
    """Accept "colour" for "color"."""
    if isinstance(obj, dict) and "colour" in obj:
        obj = dict(obj)
        if "color" in obj:
            raise ValueError('give either "color" or "colour", not both')
        obj["color"] = obj.pop("colour")
    return obj


def look_path(look):
    """The file of a ready look (presets/) or a path."""
    if os.path.isfile(look):
        return look
    for name in (look, "Textizo-" + look, "TextizoFX-" + look):
        path = os.path.join(PRESETS, name + ".setting")
        if os.path.isfile(path):
            return path
    raise ValueError('look "%s" is not in presets/ (python tools/textizofx_look.py looks lists them)' % look)


def engine_values(path, data):
    """{engine input id: value} of the first TextizoFX node (or Textizo preset) in a file."""
    tools, _ = find_tools(read_setting(path), data)
    if not tools:
        raise ValueError("no TextizoFX node in %s" % path)
    _, tool, _ = tools[0]
    return {k: input_value(v) for k, v in tool.get("Inputs").fields.items()}


def raw_value(input_id, value, data):
    """A spec's raw `inputs` value as the engine reads it: a menu by number, ID or label; a checkbox true/false."""
    spec = data["inputs"][input_id]
    kind = spec["node"]["kind"]
    if kind == "choice_id":
        ids = spec["node"].get("ids") or []
        if isinstance(value, dict) and set(value) == {"fuid"}:
            value = value["fuid"]
        if isinstance(value, str):
            labels = [(o.get("label") or "").lower() for o in spec.get("options") or []]
            if value in ids:
                return make_fuid(value)
            if value.lower() in labels:
                return make_fuid(ids[labels.index(value.lower())])
            raise ValueError("inputs.%s: %r is not one of %s" % (input_id, value, ", ".join(ids)))
        if is_number(value) and float(value).is_integer() and 0 <= value < len(ids):
            return make_fuid(ids[int(value)])
        raise ValueError("inputs.%s needs one of: %s" % (input_id, ", ".join(ids)))
    if kind == "choice" and isinstance(value, str):
        labels = [(o.get("label") or "").lower() for o in spec.get("options") or []]
        if value.lower() in labels:
            return labels.index(value.lower())
        raise ValueError("inputs.%s: %r is not one of %s" % (input_id, value, ", ".join(o.get("label") for o in spec.get("options") or [])))
    if kind == "bool" and isinstance(value, bool):
        return 1 if value else 0
    if kind == "double2d":
        return pair(value, "inputs." + input_id)
    if kind == "gradient":
        if isinstance(value, (list, dict)):
            colors = value
            if isinstance(colors, dict):
                stops = sorted((float(pos), parse_color(c, "inputs." + input_id)) for pos, c in colors.items())
            else:
                stops = [(i / (len(colors) - 1.0), parse_color(c, "inputs." + input_id)) for i, c in enumerate(colors)]
            return Gradient(stops)
        return value
    return value


def build_values(spec, data):
    """{engine input id: value} for a spec: a ready look's values (or TextizoFX's defaults) with the spec's on top."""
    spec_inputs = data["inputs"]
    spec = british(spec)
    expect_keys(spec, SPEC_KEYS, "spec")
    base_look = spec.get("look")
    vals = {}
    if base_look:
        vals.update(engine_values(look_path(base_look), data))

    def default(input_id):
        v = spec_inputs[input_id].get("default")
        return make_fuid(v) if spec_inputs[input_id]["node"]["kind"] == "choice_id" and isinstance(v, str) else v

    def put(input_id, value):
        if input_id not in spec_inputs or not spec_inputs[input_id].get("node"):
            raise ValueError("internal: %s is not a TextizoFX control" % input_id)
        vals[input_id] = value

    def current(input_id):
        v = vals.get(input_id)
        return v if v is not None else default(input_id)

    put("StateVersion", STATE_VERSION)
    if not base_look:
        put("InEnable", 1)
    text = spec.get("text", current("StyledText") if base_look else "TextizoFX")
    if "text" in spec or not base_look:
        put("StyledText", text)
        put("TextEdited", 1)
    if "font" in spec or not base_look:
        put("Font", spec.get("font", "Arial"))
    if "style" in spec or not base_look:
        put("Style", spec.get("style", "Regular"))
    size = float(spec.get("size", current("Size") if base_look else 1.0))
    if "size" in spec or not base_look:
        put("Size", size)
    anchor_name = spec.get("vertical_anchor")
    if anchor_name is not None:
        if anchor_name not in ANCHORS:
            raise ValueError("vertical_anchor must be top, center, baseline or bottom")
        put("VerticalAnchor", ANCHORS[anchor_name])
    elif not base_look:
        put("VerticalAnchor", 1)
    anchor = int(current("VerticalAnchor")) if is_number(current("VerticalAnchor")) else 1
    line_spacing = float(spec.get("line_spacing", current("LineSpacing") if base_look else 1.0))
    if "line_spacing" in spec or not base_look:
        put("LineSpacing", line_spacing)
    aspect = float(spec.get("aspect", 16.0 / 9.0))
    if "center" in spec or not base_look:
        center = spec.get("center", [0.5, 0.5])
        if center == "auto":
            center = [0.5, "auto"]
        if not (isinstance(center, (list, tuple)) and len(center) == 2):
            raise ValueError('center must be [x, y] or "auto"')
        cy = center[1]
        if cy == "auto":
            cy = auto_center_y(size, len(text.replace("\r\n", "\n").split("\n")), line_spacing, aspect, anchor)
        put("Center", [float(center[0]), float(cy)])
    if "align" in spec or not base_look:
        align = spec.get("align", "center")
        if align not in ALIGN:
            raise ValueError("align must be left, center or right")
        put("Alignment", ALIGN[align])
    for key, input_id, fallback in (("tracking", "Tracking", 0.0), ("rotation", "Rotation", 0.0),
                                    ("rotation_x", "RotationX", 0.0), ("rotation_y", "RotationY", 0.0)):
        if key in spec or not base_look:
            put(input_id, float(spec.get(key, fallback)))
    if "fit" in spec or not base_look:
        put("FitToFrame", 1 if spec.get("fit", True) else 0)
    if "alpha" in spec or not base_look:
        for c in ("Red", "Green", "Blue"):
            put(c, 1)
        put("Alpha", float(spec.get("alpha", 1.0)))

    # Animation rows.
    for page, key in (("In", "in"), ("Out", "out")):
        rows = spec.get(key, {}) or {}
        if not isinstance(rows, dict):
            raise ValueError('"%s" must be an object like {"opacity": {...}, "position": {...}}' % key)
        direction = spec.get(key + "_direction")
        if direction is not None:
            if direction not in DIRECTIONS:
                raise ValueError("%s_direction must be one of: %s" % (key, ", ".join(DIRECTIONS)))
            put(page + "Direction", make_fuid(direction))
        stop = spec.get(key + "_stop")
        if stop is not None:
            if stop is False:
                put(page + "StopEnable", 0)
            elif isinstance(stop, bool) or not is_number(stop) or stop < 0:
                raise ValueError("%s_stop must be a frame number, 0 or more, counted from the clip's first frame" % key)
            else:
                put(page + "StopEnable", 1)
                put(page + "StopFrame", round_int(stop))
        anchor_key = "in_start_at" if page == "In" else "out_from_end"
        anchor_value = spec.get(anchor_key)
        if anchor_value is not None:
            if anchor_value is False and page == "Out":
                put("OutAlignEnd", 0)
            elif isinstance(anchor_value, bool) or not is_number(anchor_value) or anchor_value < 0:
                raise ValueError("%s must be a number of frames, 0 or more" % anchor_key)
            elif page == "In":
                put("InStartAt", round_int(anchor_value))
            else:
                put("OutAlignEnd", 1)
                put("OutBeforeEnd", round_int(anchor_value))
        resolved = {}
        for name, row in rows.items():
            row_key = ROW_ALIASES.get(name, name)
            if row_key not in ROWS:
                raise ValueError('%s: unknown row "%s" (rows: opacity, blur, position, size, tracking, rotation, explosion)' % (key, name))
            resolved[row_key] = row
        for row_key in ROWS:
            prefix = page + row_key
            row = resolved.get(row_key)
            if row is None:
                if not base_look:
                    put(prefix + "Enable", 0)
                continue
            where = "%s.%s" % (key, row_key)
            expect_keys(row, ROW_KEYS, where)
            if row.get("on") is False:
                put(prefix + "Enable", 0)
                continue
            by = BY_ALIASES.get(row.get("by", "letters"), row.get("by", "letters"))
            if by not in FOLLOWERS:
                raise ValueError("%s: by must be letters, words or lines" % where)
            groups = count_groups(text, by)
            start = row.get("start", 0 if page == "In" else 100)
            if "span" in row or "delay" in row:
                if "end" in row or "stagger" in row:
                    raise ValueError("%s: give either span + delay, or end + stagger, not both" % where)
                span = float(row.get("span", 12))
                delay = float(row.get("delay", 0))
                start, end, stagger = plan_row(int(start), span, delay, groups)
            else:
                end = row.get("end", int(start) + 30)
                stagger = float(row.get("stagger", 10 if groups > 1 else 0))
            ease = row.get("ease", "linear")
            if ease not in EASES:
                raise ValueError("%s: ease %s is not one of %s" % (where, ease, ", ".join(EASES)))
            if page == "Out" and "from" in row:
                raise ValueError("%s: an Out row has no \"from\"; it starts where the In row ended" % where)
            put(prefix + "Enable", 1)
            put(prefix + "Follower", make_fuid(by))
            put(prefix + "AnimationStart", int(start))
            put(prefix + "AnimationEnd", int(end))
            put(prefix + "Stagger", stagger)
            for field, spec_key in (("StartValue", "from"), ("EndValue", "to")):
                if page == "Out" and field == "StartValue":
                    continue
                value = row.get(spec_key, current(prefix + field))
                if row_key == "center":
                    value = pair(point(value) if isinstance(value, Table) else value, "%s.%s" % (where, spec_key))
                elif not is_number(value):
                    raise ValueError("%s.%s must be a number" % (where, spec_key))
                put(prefix + field, value)
            if row_key == "explosion":
                put(prefix + "Damping", float(row.get("damping", 0.0)))
                put(prefix + "Speed", float(row.get("variance", 0.3)))
                put(prefix + "RotationX", float(row.get("spin_x", 0.0)))
                put(prefix + "RotationY", float(row.get("spin_y", 0.0)))
                put(prefix + "Rotation", float(row.get("spin_z", 0.0)))
                put(prefix + "Offset", int(row.get("pre_roll", 0)))
                put(prefix + "Reverse", 1 if row.get("reverse") else 0)
            if "pivot" in row:
                if row_key != "tracking":
                    raise ValueError("%s: pivot is only for tracking rows" % where)
                if row["pivot"] not in PIVOTS:
                    raise ValueError("%s: pivot must be left, center or right" % where)
                put(prefix + "Pivot", make_fuid(row["pivot"]))
            if "offset" in row:
                offset_id = prefix + "AnimOffset"
                if offset_id not in spec_inputs:
                    raise ValueError("%s: this TextizoFX has no Animation Offset for the row" % where)
                put(offset_id, float(row["offset"]))
            put(prefix + "CurveMode", make_fuid("preset"))
            put(prefix + "CurvePreset", make_fuid(ease))
            put(prefix + "CurvePresetID", ease)

    # Shading elements (the element the Shading page shows is written to the proxy controls too).
    elements = dict(spec.get("elements", {}) or {})
    if "color" in spec:
        elements.setdefault("1", {})
        elements["1"] = dict(elements["1"], color=spec["color"])
    for key in elements:
        if str(key) not in [str(i) for i in range(1, 9)]:
            raise ValueError('elements: keys are "1" to "8"')
    if not base_look:
        put("ShadingActiveElement", make_fuid("element_1"))
    active = fuid(current("ShadingActiveElement")) or "element_1"
    active_index = int(active.split("_")[-1])
    for index in range(1, 9):
        e = elements.get(str(index), elements.get(index))
        prefix = "ShadingElement%d" % index
        if e is None:
            if not base_look and index > 1:
                put(prefix + "Enable", 0)
                if index == active_index:
                    put("ShadingProxyEnable", 0)
            continue
        e = british(e or {})
        where = "elements.%d" % index
        expect_keys(e, ELEMENT_KEYS, where)
        if index > 1 and "appearance" not in e and e.get("enabled", True) and not base_look:
            raise ValueError("%s: give an appearance (normal, outline, border_fill or border_stroke); element %d "
                             "otherwise starts as %s" % (where, index, APPEARANCE_NAMES[int(default(prefix + "Appearance") or 0)]))
        evals = {field: (current(prefix + field) if base_look else default(prefix + field)) for field in ELEMENT_FIELDS}
        evals["Offset"] = list(point(evals["Offset"]) or (0.0, 0.0))
        evals["Enable"] = 1 if e.get("enabled", True) else 0
        if "appearance" in e:
            name = str(e["appearance"]).lower().replace(" ", "_")
            if name not in APPEARANCES:
                raise ValueError("%s.appearance must be normal, outline, border_fill or border_stroke" % where)
            evals["Appearance"] = APPEARANCES[name]
        if "color" in e:
            r, g, b, a = parse_color(e["color"], where + ".color")
            evals.update(Red=r, Green=g, Blue=b, Alpha=a)
        if "opacity" in e:
            evals["Opacity"] = float(e["opacity"])
        if "thickness" in e:
            evals["Thickness"] = float(e["thickness"])
        if "offset" in e:
            evals["Offset"] = pair(e["offset"], where + ".offset")
        if "softness" in e:
            evals["SoftnessX"], evals["SoftnessY"] = pair(e["softness"], where + ".softness")
        if "border_level" in e:
            if e["border_level"] not in LEVELS:
                raise ValueError("%s.border_level must be letters, words or lines" % where)
            evals["BorderLevel"] = LEVELS[e["border_level"]]
        if "extend" in e:
            evals["BorderExtendX"], evals["BorderExtendY"] = pair(e["extend"], where + ".extend")
        if "round" in e:
            evals["BorderRound"] = float(e["round"])
        if is_number(evals["Opacity"]) and not 0 <= evals["Opacity"] <= 1:
            raise ValueError("%s.opacity must be 0 to 1" % where)
        for field, key in (("Thickness", "thickness"), ("SoftnessX", "softness"), ("SoftnessY", "softness"),
                           ("BorderExtendX", "extend"), ("BorderExtendY", "extend"), ("BorderRound", "round")):
            if is_number(evals[field]) and evals[field] < 0:
                raise ValueError("%s.%s must be 0 or more" % (where, key))
        gradient = None
        if "gradient" in e:
            g_spec = e["gradient"]
            expect_keys(g_spec, {"colors", "angle", "span", "scale", "aspect"}, where + ".gradient")
            colors = g_spec.get("colors")
            if isinstance(colors, dict):
                stops = sorted((float(pos), parse_color(c, where + ".gradient")) for pos, c in colors.items())
            elif isinstance(colors, list) and len(colors) >= 2:
                stops = [(i / (len(colors) - 1.0), parse_color(c, where + ".gradient")) for i, c in enumerate(colors)]
            else:
                raise ValueError("%s.gradient.colors needs at least two colours" % where)
            gradient = Gradient(stops)
            evals["ColorMode"] = 1
            evals["GradientAngle"] = float(g_spec.get("angle", 0.0))
            span = g_spec.get("span", "text")
            if span not in MAPPING_LEVELS:
                raise ValueError("%s.gradient.span must be letters, words, lines or text" % where)
            evals["MappingLevel"] = MAPPING_LEVELS[span]
            evals["MappingSize"] = float(g_spec.get("scale", 1.5))
            evals["MappingAspect"] = float(g_spec.get("aspect", 1.0))
            first, last = stops[0][1], stops[-1][1]
            evals.update(Red=first[0], Green=first[1], Blue=first[2], Alpha=first[3],
                         EndRed=last[0], EndGreen=last[1], EndBlue=last[2], EndAlpha=last[3])
        prefixes = [prefix] + (["ShadingProxy"] if index == active_index else [])
        for p in prefixes:
            for field in ELEMENT_FIELDS:
                put(p + field, evals[field])
            if gradient is not None:
                put(p + "Gradient", gradient)

    # Motion blur.
    if "motion_blur" in spec or not base_look:
        mb = spec.get("motion_blur", False)
        if mb:
            mb = {} if mb is True else mb
            expect_keys(mb, {"shutter", "quality", "bias", "spread"}, "motion_blur")
            put("MotionBlurEnable", 1)
            put("MotionBlurShutterAngle", float(mb.get("shutter", 180)))
            put("MotionBlurSamples", int(mb.get("quality", 2)))
            put("MotionBlurBias", float(mb.get("bias", 0)))
            put("MotionBlurSampleSpread", float(mb.get("spread", 1)))
        else:
            put("MotionBlurEnable", 0)

    # Raw inputs: {"ID": number | "text" | [x, y] | a menu's ID or label | true/false | "#RRGGBB" for a colour}.
    raw = spec.get("inputs", {}) or {}
    for name, value in raw.items():
        input_id = name if name in spec_inputs else data["by_node"].get(name)
        params = data["by_param"].get(name)
        colour_value = isinstance(value, str) or (isinstance(value, (list, tuple)) and len(value) in (3, 4))
        if params and len(params) > 1 and colour_value and all(spec_inputs[i]["node"]["kind"] in ("rgba", "rgb") for i in params):
            # A colour by its parameter's name: "FxGlowColor": "#FF8800" (or [r, g, b]) sets all its channels.
            rgba = parse_color(value, "inputs." + name)
            for i in params:
                put(i, rgba[spec_inputs[i]["node"].get("comp", 0)])
            continue
        if input_id is None:
            raise ValueError("inputs: unknown input %s (python tools/textizofx_look.py controls --find %s)" % (name, name))
        if spec_inputs[input_id].get("role") != "public":
            raise ValueError("inputs: %s is not a look control (role %s in reference/inputs.json)" % (
                name, spec_inputs[input_id].get("role")))
        put(input_id, raw_value(input_id, value, data))
    return vals


MAKE_SHORT = re.compile(r"^(?:textizo\s*fx[-_ ]?|textizofx[-_ ]?)?(\d{1,3})([a-z])$", re.I)
SHORT_FILE_RE = re.compile(r"^TextizoFX-(\d{2,3})([A-Z])\.setting$", re.I)


def look_file_name(name):
    name = (name or "").strip()
    m = MAKE_SHORT.match(name)
    if m:
        return "TextizoFX-%02d%s.setting" % (int(m.group(1)), m.group(2).upper())
    if not name:
        return "TextizoFX-01A.setting"
    return name + ".setting"


def used_names(folders):
    """{number: set(letters)} of TextizoFX-NNL looks in the folders."""
    used = {}
    for folder in folders:
        if os.path.isdir(folder):
            for file_name in os.listdir(folder):
                m = SHORT_FILE_RE.match(file_name)
                if m:
                    used.setdefault(int(m.group(1)), set()).add(m.group(2).upper())
    return used


def cmd_next_name(args):
    folders = [MY_LOOKS] + [target_folder(t) for t in args.to or []]
    used = used_names(folders)
    if args.variant is not None:
        letters = used.get(args.variant, set())
        free = [ch for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if ch not in letters]
        if not free:
            print("all letters of %02d are used; start a new number" % args.variant)
            return 1
        print("TextizoFX-%02d%s" % (args.variant, free[0]))
        return 0
    print("TextizoFX-%02dA" % (max(used) + 1 if used else 1))
    return 0


def cmd_build(args):
    data = load_inputs()
    try:
        with open(args.spec, "r", encoding="utf-8-sig") as handle:
            spec = json.load(handle)
    except json.JSONDecodeError as exc:
        print("spec error: invalid JSON at line %d, column %d: %s (look for a missing or extra comma or quote)" % (
            exc.lineno, exc.colno, exc.msg))
        return 1
    try:
        vals = build_values(spec, data)
        keep = ("StateVersion", "StyledText", "TextEdited", "Font", "Style")
        text = write_node(vals, data, compact=args.compact, keep=keep)
    except ValueError as exc:
        print("spec error: %s" % exc)
        return 1
    out_path = args.out or os.path.join(MY_LOOKS, look_file_name(spec.get("name")))
    inside_work = os.path.normcase(os.path.abspath(out_path)).startswith(os.path.normcase(MY_LOOKS) + os.sep)
    if os.path.exists(out_path) and not (args.overwrite or inside_work):
        print("%s already exists; pass --overwrite to replace it (files in my-looks/ are replaced without asking)" % out_path)
        return 1
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print("wrote %s" % out_path)
    frames = args.frames if args.frames is not None else spec.get("frames")
    ok, report = check_file(out_path, data, frames, float(spec.get("aspect", 16.0 / 9.0)), quiet=True)
    if not SHORT_FILE_RE.match(os.path.basename(out_path)) and os.path.dirname(os.path.abspath(out_path)) == MY_LOOKS:
        report.note("looks get short names: TextizoFX-<number><letter>, for example TextizoFX-07A "
                    "(python tools/textizofx_look.py next-name)")
    tools, others = find_tools(read_setting(out_path), data)
    name, tool, _ = tools[0]
    ok = print_report(out_path, report, name, len(tool.get("Inputs").fields), others)
    return 0 if ok else 1


# --------------------------------------------------------------------------- look -> spec

def look_to_spec(path, data):
    """A spec (as build takes it, without "look") that builds the same node: the structured parts, and every other
    control that differs from TextizoFX's defaults in "inputs"."""
    spec_inputs = data["inputs"]
    values = engine_values(path, data)
    covered = set()

    def get(input_id):
        covered.add(input_id)
        v = values.get(input_id)
        if v is None:
            d = spec_inputs.get(input_id, {}).get("default")
            return make_fuid(d) if (spec_inputs.get(input_id, {}).get("node") or {}).get("kind") == "choice_id" and isinstance(d, str) else d
        return v

    def plain(v):
        if fuid(v) is not None:
            return fuid(v)
        if point(v) is not None:
            return [float(fmt_num(x)) if not float(x).is_integer() else int(x) for x in point(v)]
        if is_number(v):
            return float(fmt_num(v)) if not float(v).is_integer() else int(v)
        return v

    align_names = {0: "left", 1: "center", 2: "right"}
    anchor_names = {0: "top", 1: "center", 2: "baseline", 3: "bottom"}
    spec = {"name": os.path.splitext(os.path.basename(path))[0], "text": get("StyledText") or "",
            "font": get("Font"), "style": get("Style"), "size": plain(get("Size")), "center": plain(get("Center")),
            "align": align_names.get(int(get("Alignment") if is_number(get("Alignment")) else 1), "center"),
            "vertical_anchor": anchor_names.get(int(get("VerticalAnchor") if is_number(get("VerticalAnchor")) else 1), "center"),
            "tracking": plain(get("Tracking")), "line_spacing": plain(get("LineSpacing")),
            "rotation": plain(get("Rotation")), "rotation_x": plain(get("RotationX")), "rotation_y": plain(get("RotationY")),
            "fit": bool(is_number(get("FitToFrame")) and get("FitToFrame") >= 0.5), "alpha": plain(get("Alpha"))}
    for c in ("StateVersion", "TextEdited", "InEnable", "Red", "Green", "Blue"):
        get(c)
    for page, key in (("In", "in"), ("Out", "out")):
        rows = {}
        for row in ROWS:
            prefix = page + row
            enabled = is_number(get(prefix + "Enable")) and get(prefix + "Enable") >= 0.5
            if not enabled:
                continue
            for field in ROW_FIELDS:
                get(prefix + field)
            by = plain(get(prefix + "Follower")) or "letters"
            start = plain(get(prefix + "AnimationStart"))
            r = {"by": by, "start": start, "end": plain(get(prefix + "AnimationEnd")), "stagger": plain(get(prefix + "Stagger"))}
            if page == "In":
                r["from"] = plain(get(prefix + "StartValue"))
            r["to"] = plain(get(prefix + "EndValue"))
            r["ease"] = plain(get(prefix + "CurvePreset")) or "linear"
            if row == "explosion":
                r.update(variance=plain(get(prefix + "Speed")), damping=plain(get(prefix + "Damping")),
                         spin_x=plain(get(prefix + "RotationX")), spin_y=plain(get(prefix + "RotationY")),
                         spin_z=plain(get(prefix + "Rotation")), pre_roll=plain(get(prefix + "Offset")),
                         reverse=bool(get(prefix + "Reverse")))
            if row == "tracking" and plain(get(prefix + "Pivot")) in ("left", "right"):
                r["pivot"] = plain(get(prefix + "Pivot"))
            if (prefix + "AnimOffset") in spec_inputs and is_number(get(prefix + "AnimOffset")) and get(prefix + "AnimOffset") != 0:
                r["offset"] = plain(get(prefix + "AnimOffset"))
            rows["position" if row == "center" else row] = r
        spec[key] = rows
        if plain(get(page + "Direction")) in ("ltr", "rtl"):
            spec[key + "_direction"] = plain(get(page + "Direction"))
        if is_number(get(page + "StopEnable")) and get(page + "StopEnable") >= 0.5:
            spec[key + "_stop"] = plain(get(page + "StopFrame"))
        if page == "In" and is_number(get("InStartAt")) and get("InStartAt") > 0:
            spec["in_start_at"] = plain(get("InStartAt"))
        if page == "Out" and is_number(get("OutAlignEnd")) and get("OutAlignEnd") >= 0.5:
            spec["out_from_end"] = plain(get("OutBeforeEnd")) if is_number(get("OutBeforeEnd")) else 0
            get("OutBeforeEnd")
    active = fuid(get("ShadingActiveElement")) or "element_1"
    active_index = int(active.split("_")[-1])
    elements = {}
    for index in range(1, 9):
        def eget(field):
            get("ShadingProxy" + field)
            return get("ShadingElement%d%s" % (index, field))
        enabled = is_number(eget("Enable")) and eget("Enable") >= 0.5
        if not enabled:
            continue
        for field in ELEMENT_FIELDS:
            eget(field)
        e = {"appearance": APPEARANCE_NAMES[int(eget("Appearance") or 0)],
             "color": [plain(eget("Red")), plain(eget("Green")), plain(eget("Blue"))],
             "opacity": plain(eget("Opacity"))}
        if plain(eget("Alpha")) not in (1, 1.0):
            e["color"].append(plain(eget("Alpha")))
        e["thickness"] = plain(eget("Thickness"))
        e["offset"] = plain(eget("Offset")) or [0, 0]
        sx, sy = plain(eget("SoftnessX")), plain(eget("SoftnessY"))
        e["softness"] = sx if sx == sy else [sx, sy]
        e["border_level"] = ["letters", "words", "lines"][int(eget("BorderLevel") or 0)]
        e["extend"] = [plain(eget("BorderExtendX")), plain(eget("BorderExtendY"))]
        e["round"] = plain(eget("BorderRound"))
        if is_number(eget("ColorMode")) and eget("ColorMode") >= 0.5:
            stops = gradient_stops(eget("Gradient")) or []
            e["gradient"] = {"colors": {fmt_num(pos): list(color) for pos, color in stops} or
                             [e["color"], [plain(eget("EndRed")), plain(eget("EndGreen")), plain(eget("EndBlue"))]],
                             "angle": plain(eget("GradientAngle")),
                             "span": ["letters", "words", "lines", "text"][int(eget("MappingLevel") or 0)],
                             "scale": plain(eget("MappingSize")), "aspect": plain(eget("MappingAspect"))}
            get("ShadingElement%dGradient" % index)
            get("ShadingProxyGradient")
        elements[str(index)] = e
    spec["elements"] = elements
    if is_number(get("MotionBlurEnable")) and get("MotionBlurEnable") >= 0.5:
        spec["motion_blur"] = {"shutter": plain(get("MotionBlurShutterAngle")), "quality": plain(get("MotionBlurSamples")),
                               "bias": plain(get("MotionBlurBias")), "spread": plain(get("MotionBlurSampleSpread"))}
    else:
        spec["motion_blur"] = False
    # Everything else the look sets: by ID, menus by their ID or label.
    raw = {}
    built = build_values(dict(spec), data)
    for input_id, s in spec_inputs.items():
        if s.get("role") != "public" or not s.get("node"):
            continue
        v = values.get(input_id)
        if v is None:
            continue
        base = built.get(input_id)
        if base is None:
            base = plain_default(s.get("default"))
            if s["node"]["kind"] == "choice_id" and isinstance(base, str):
                base = make_fuid(base)
        if same_value(v, base) or (isinstance(base, Gradient) and gradient_stops(v) == sorted(
                (round(float(p), 6), tuple(round(float(x), 6) for x in c)) for p, c in base.stops)):
            continue
        if isinstance(v, Ref):
            continue
        if fuid(v) is not None:
            raw[input_id] = fuid(v)
        elif gradient_stops(v) is not None and s["node"]["kind"] == "gradient":
            raw[input_id] = {fmt_num(p): list(c) for p, c in gradient_stops(v)}
        else:
            raw[input_id] = plain(v)
    if raw:
        spec["inputs"] = raw
    return spec


def cmd_to_spec(args):
    try:
        spec = look_to_spec(args.file, load_inputs())
    except (OSError, ValueError) as exc:
        print(exc)
        return 1
    text = json.dumps(spec, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text + "\n")
        print("wrote %s" % args.out)
    else:
        print(text)
    return 0


# --------------------------------------------------------------------------- lists, timing, folders, install

def cmd_looks(_args):
    data = load_inputs()
    looks = data.get("looks") or []
    for look in looks:
        print("%-16s %-3s %s" % (look["name"], look.get("menu", ""), look.get("about", "")))
    if not looks:
        for name in sorted(os.listdir(PRESETS)):
            if name.endswith(".setting"):
                print(name[:-8])
    return 0


def cmd_controls(args):
    data = load_inputs()
    find = (args.find or "").lower()
    for input_id, s in data["inputs"].items():
        if s.get("role") != "public":
            continue
        if args.page and s.get("page", "").lower() != args.page.lower():
            continue
        node = s.get("node") or {}
        text = " ".join(str(x) for x in (input_id, node.get("name"), s.get("label"), s.get("section"))).lower()
        if find and find not in text:
            continue
        extra = ""
        if s.get("options"):
            extra = "  menu: " + ", ".join("%d %s" % (i, o.get("id") or o.get("label")) for i, o in enumerate(s["options"]))
        elif s.get("min") is not None or s.get("max") is not None:
            extra = "  %s..%s" % (fmt_num(s["min"]) if s.get("min") is not None else "", fmt_num(s["max"]) if s.get("max") is not None else "")
        print("%-32s %-10s %-28s default %s%s%s" % (node.get("name", input_id), s.get("page", ""), (s.get("label") or "")[:28],
                                                  json.dumps(s.get("default")), extra, "  (hidden)" if s.get("hidden") else ""))
    return 0


def cmd_timing(args):
    groups = args.groups or count_groups(args.text or "", args.by)
    print("groups: %d %s" % (groups, args.by))
    if args.span is not None:
        start, end, stagger = plan_row(args.start, args.span, args.delay or 0.0, groups)
        print("Start Frame %d, End Frame %d, Stagger %% %s" % (start, end, fmt_num(stagger)))
    else:
        end, stagger = args.end, args.stagger
        if end is None or stagger is None:
            print("give --span and --delay, or --end and --stagger")
            return 2
        start = args.start
    span, delay = row_window(start, end, stagger, groups)
    print("each %s moves for %.2f frames; the next starts %.2f frames later; the last one lands on frame %s"
          % (args.by[:-1], span, delay, fmt_num(round(start + delay * (groups - 1) + span, 2))))
    return 0


def documents_dir():
    home = os.path.expanduser("~")
    if sys.platform.startswith("win"):
        try:
            import ctypes
            from ctypes import wintypes

            class GUID(ctypes.Structure):
                _fields_ = [("a", wintypes.DWORD), ("b", wintypes.WORD), ("c", wintypes.WORD), ("d", ctypes.c_ubyte * 8)]
            docs = GUID(0xFDD39AD0, 0x238F, 0x46AF, (ctypes.c_ubyte * 8)(0xAD, 0xB4, 0x6C, 0x85, 0x48, 0x03, 0x69, 0xC7))
            path = ctypes.c_wchar_p()
            if ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(docs), 0, None, ctypes.byref(path)) == 0:
                result = path.value
                ctypes.windll.ole32.CoTaskMemFree(path)
                if result:
                    return result
        except Exception:
            pass
    return os.path.join(home, "Documents")


def my_looks_dir():
    """TextizoFX's looks folder: Load Look... opens there, and its looks are in the Look menu (after DaVinci Resolve
    starts again) and in Browse Looks... (Windows)."""
    return os.path.join(documents_dir(), "Clipizo", "TextizoFX", "Looks")


def resolve_settings_dir():
    home = os.path.expanduser("~")
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or os.path.join(home, "AppData", "Roaming")
        return os.path.join(base, "Blackmagic Design", "DaVinci Resolve", "Support", "Fusion", "Settings")
    if sys.platform == "darwin":
        return os.path.join(home, "Library", "Application Support", "Blackmagic Design", "DaVinci Resolve", "Fusion", "Settings")
    return os.path.join(home, ".local", "share", "DaVinciResolve", "Fusion", "Settings")


def downloads_dir():
    return os.path.join(os.path.expanduser("~"), "Downloads", "TextizoFX Looks")


def target_folder(target):
    named = {"mylooks": my_looks_dir(), "my-looks": my_looks_dir(), "resolve": resolve_settings_dir(), "downloads": downloads_dir()}
    return os.path.expanduser(named.get(target, target))


def cmd_where(_args):
    for label, path in (("mylooks", my_looks_dir()), ("resolve", resolve_settings_dir()), ("downloads", downloads_dir())):
        print("%-9s %s  (%s)" % (label, path, "exists" if os.path.isdir(path) else "will be created"))
    return 0


def cmd_install(args):
    data = load_inputs()
    target = target_folder(args.to)
    status = 0
    for path in args.files:
        ok, report = check_file(path, data, quiet=True)
        if not ok:
            print("not installed: %s has errors; run the check command" % path)
            status = 1
            continue
        os.makedirs(target, exist_ok=True)
        dest = os.path.normpath(os.path.join(target, os.path.basename(path)))
        if os.path.exists(dest) and not args.overwrite:
            print("not installed: %s already exists (pass --overwrite or use the next free name)" % dest)
            status = 1
            continue
        shutil.copyfile(path, dest)
        print("installed: %s" % dest)
    return status


def main(argv=None):
    parser = argparse.ArgumentParser(description="TextizoFX look helper: build, check, to-spec, looks, controls, timing, where, install.")
    sub = parser.add_subparsers(dest="command")
    p = sub.add_parser("build", help="write a TextizoFX node from a JSON spec")
    p.add_argument("spec")
    p.add_argument("out", nargs="?", help="default: my-looks/<name>.setting")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--frames", type=int)
    p.add_argument("--compact", action="store_true", help="only what differs from TextizoFX's defaults (for a chat answer)")
    p.set_defaults(func=cmd_build)
    p = sub.add_parser("check", help="check looks and print their timing")
    p.add_argument("files", nargs="+")
    p.add_argument("--frames", type=int, help="clip length in frames, to warn about rows that end after it")
    p.add_argument("--aspect", type=float, default=16.0 / 9.0, help="frame width / height (default 16:9; 0.5625 for 9:16)")
    p.set_defaults(func=cmd_check)
    p = sub.add_parser("to-spec", help="turn a TextizoFX node (or a Textizo preset) into a JSON spec")
    p.add_argument("file")
    p.add_argument("out", nargs="?")
    p.set_defaults(func=cmd_to_spec)
    p = sub.add_parser("looks", help="the ready looks in presets/")
    p.set_defaults(func=cmd_looks)
    p = sub.add_parser("controls", help="TextizoFX's controls")
    p.add_argument("--page", help="Text, Shading, In, Out, Motion Blur or Effects")
    p.add_argument("--find", help="a word in the ID, label or section")
    p.set_defaults(func=cmd_controls)
    p = sub.add_parser("timing", help="row timing calculator")
    p.add_argument("--text")
    p.add_argument("--groups", type=int)
    p.add_argument("--by", default="letters", choices=FOLLOWERS)
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--span", type=float, help="frames each letter/word/line moves")
    p.add_argument("--delay", type=float, help="frames between one letter/word/line and the next")
    p.add_argument("--end", type=int)
    p.add_argument("--stagger", type=float)
    p.set_defaults(func=cmd_timing)
    p = sub.add_parser("where", help="print the folders looks can go to")
    p.set_defaults(func=cmd_where)
    p = sub.add_parser("next-name", help="the next free short name, like TextizoFX-07A")
    p.add_argument("--to", action="append", help="also look in mylooks, resolve, downloads or a folder (repeat for several)")
    p.add_argument("--variant", type=int, help="number of an existing look: print its next free letter instead")
    p.set_defaults(func=cmd_next_name)
    p = sub.add_parser("install", help="copy checked looks to a folder")
    p.add_argument("files", nargs="+")
    p.add_argument("--to", required=True, help="mylooks, resolve, downloads, or a folder path")
    p.add_argument("--overwrite", action="store_true")
    p.set_defaults(func=cmd_install)
    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    if not getattr(args, "func", None):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
