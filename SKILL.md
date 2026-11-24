---
name: textizofx-looks
description: Makes ready-to-use TextizoFX animated-text looks (.setting files holding one TextizoFX node) for DaVinci Resolve from a plain description (for example "a bouncy pink title", "an Apple-style blur reveal", "a caption pill that pops in word by word", "gold text with a glow"). It checks each look and saves it where the user wants, including TextizoFX's own My Looks folder (its Look menu). Use it whenever the user asks for a TextizoFX look, title, text animation or caption style, or for changes to one.
---

# TextizoFX looks

You make looks for **TextizoFX**, an animated text plugin (OpenFX) for DaVinci Resolve's Edit and Fusion pages. A look is a small `.setting` text file holding one TextizoFX node: its text, font, animation rows, shading and effects. On the Edit page the user loads it with **Load Look...** (or picks it in the Look menu); on the Fusion page they paste it as a node.

## Before you start

- **Read `TextizoFX AI Guide.md` completely, once per session.** It is the reference for:
  - the node file and its values (section 2; menus are numbers in a TextizoFX node);
  - the text, fonts and size (section 3), the animation rows and their timing (sections 4 to 6);
  - the shading layers (section 7), motion blur (section 8), the effects and TextizoFX's own controls (section 9);
  - the house style (section 10), the ready looks (section 12) and every control (section 13);
  - how users use a look (section 14).

  This file only adds the workflow for agents that can use files.
- **The helper** is `python tools/textizofx_look.py` (use `python3` on Mac and Linux, or `py` on some Windows installs). It needs Python 3 and nothing else. It reads `reference/inputs.json`, the list of TextizoFX's controls.
- **If Python is not available,** write the node by hand from the guide's examples and go through the guide's checklist yourself.

## Workflow

1. **Understand the request.** Ask, in one message and only for what is missing:
   - the text;
   - the look or mood, colours or font (optional);
   - how long the clip is and its frame rate (default: 5 s at 24 fps);
   - whether it goes over footage, and whether the video is vertical (9:16).

   Use the house style from guide section 10 unless the user wants something else.
2. **Ask where to save** (once per session; remember the answer), unless the user already named a folder. Show the real paths from `python tools/textizofx_look.py where`. The options:
   1. **TextizoFX's My Looks folder** (recommended): the look is in TextizoFX's Look menu from the next time DaVinci Resolve starts, in Browse Looks... (Windows) right away, and Load Look... opens there.
   2. **Resolve's Settings folder**, for the Fusion page (Settings > Load… on a TextizoFX node opens it).
   3. **Downloads/TextizoFX Looks.** Easy to find.
   4. **A folder the user names.**
3. **Pick a short name.** Looks are named `TextizoFX-` plus a two-digit number and a capital letter, for example `TextizoFX-07A`.
   - The number is the look. Get the next free one with `python tools/textizofx_look.py next-name --to mylooks` (use the user's folder choice).
   - The letter is a variation of that look: `next-name --to mylooks --variant 7` gives `TextizoFX-07B`.
   - Use no spaces and no descriptive words in the name. Describe the look in your message instead.
4. **Write a spec.** Start from the closest ready look (`"look": "Bounce Drop"`; `python tools/textizofx_look.py looks` lists them, `specs/` has each as a spec) and change what the user wants, or start from TextizoFX's defaults (no `"look"`). Save it as `my-looks/<short name>.json`. The format is below.
5. **Build and check:**
   ```
   python tools/textizofx_look.py build "my-looks/TextizoFX-07A.json" --frames <clip length in frames>
   ```
   This writes `my-looks/TextizoFX-07A.setting`: a complete node (every control written out, so loading it gives exactly this look). Rebuilding replaces files in `my-looks/` without asking: it is the kit's work folder. Files in the folder the user chose are never replaced without asking (step 6).

   The report shows the text, every row's frames (how long each piece moves and how far apart they start), the shading, the effects and an estimate of how much of the frame's width the text takes. You cannot see the render, so take its warnings seriously.
   - Fix every **ERROR**.
   - Fix every **WARNING** unless the user asked for that.
   - **NOTES** are house-style hints (guide section 10); follow them unless the request says otherwise.
6. **Install:**
   ```
   python tools/textizofx_look.py install "my-looks/TextizoFX-07A.setting" --to mylooks
   ```
   Use `--to resolve`, `--to downloads` or `--to "<folder>"` for the other choices. The command refuses to overwrite an existing file; ask the user whether to replace it (`--overwrite`) or use the next free name.
7. **Tell the user:**
   - the look's short name, what it looks like and how it moves;
   - where the file is;
   - how to use it (guide section 14): on the Edit page, select the TextizoFX clip and click **Load Look...** (or, in the My Looks folder, pick it in the **Look** menu after restarting DaVinci Resolve); on the Fusion page, drag the file onto the Nodes area;
   - that their own text stays (Load Look... keeps it), and how to move the exit for a longer clip.

   They have the file, so do not paste the node's text unless they ask for it. You cannot see the result, so describe it, and never claim you have tested it in Resolve.
8. **Change it on feedback.** A fix to the same look keeps its name: edit the spec, rebuild, and reinstall with `--overwrite`. When the user wants to keep both versions, give the new one the next letter.

You can also start from a look the user saved (TextizoFX's **Save as My Look**), a TextizoFX node copied from Fusion, or a Textizo preset (the Fuse's): `python tools/textizofx_look.py to-spec "<file.setting>" my-looks/TextizoFX-07A.json`.

For a chat answer (no files), `build --compact` writes only what differs from TextizoFX's defaults, like the guide's examples. Compact nodes give exactly the look when pasted as a new node or loaded with Load Look... (both start from the defaults).

## Spec format

```json
{
  "name": "TextizoFX-07A",
  "look": "Apple Reveal",
  "text": "NEON\nPOP",
  "font": "Bebas Neue", "style": "Regular", "size": 2.2,
  "center": [0.5, 0.5], "align": "center", "vertical_anchor": "center",
  "tracking": 0, "line_spacing": 1, "rotation": 0, "rotation_x": 0, "rotation_y": 12, "fit": true,
  "in": {
    "opacity":  {"by": "letters", "start": 0, "span": 4,  "delay": 2, "from": 0, "to": 1, "ease": "out_quad"},
    "size":     {"by": "letters", "start": 0, "span": 14, "delay": 2, "from": 0, "to": 1, "ease": "out_elastic"},
    "position": {"by": "letters", "start": 0, "span": 12, "delay": 2, "from": [0, -0.1], "to": [0, 0], "ease": "out_back"}
  },
  "out": {
    "opacity":  {"start": 100, "span": 8, "delay": 1.5, "to": 0, "ease": "in_cubic"}
  },
  "elements": {
    "1": {"color": "#29E0FF"},
    "2": {"appearance": "outline", "color": "#000000", "thickness": 0.0083}
  },
  "motion_blur": true,
  "inputs": {"FxGlowOn": true, "FxGlowColor": "#29E0FF", "FxGlowAmount": 1.2}
}
```

**Top level:**

- `name`: the short name, for example `TextizoFX-07A` (`07A` works too); the file becomes `TextizoFX-07A.setting`.
- `look`: optional, a ready look in `presets/` to start from (its values first, then yours). With a look, rows and elements you don't list keep the look's; without one, the spec starts from TextizoFX's defaults and rows you leave out are off.
- `text`, `font`, `style`, `size`: as in guide section 3. `\n` makes a new line. Any language works.
- `center`: `[x, y]`, or `"auto"` to centre the block. With `vertical_anchor` `center` (TextizoFX's default) Center is the middle of the text block, so `[0.5, 0.5]` is the middle of the frame.
- `align`: `left`, `center` or `right`. `vertical_anchor`: `top`, `center`, `baseline` or `bottom`.
- `tracking`, `line_spacing`, `rotation` (degrees), `rotation_x`, `rotation_y` (the 3D turn, degrees), `fit` (Fit to Frame, on by default), `alpha`.
- `color`: a shortcut for element 1's colour.
- `motion_blur`: `false`, `true`, or `{"shutter", "quality", "bias", "spread"}`.
- `in`, `out`: the animation rows (below). `in_direction`, `out_direction`: `reading`, `ltr` or `rtl`. `in_stop`, `out_stop`: Stop at Frame. `in_start_at`: Start At. `out_from_end`: Align to End with Before End frames (guide section 5).
- `elements`: the shading layers, `"1"` to `"8"` (guide section 7).
- `inputs`: any other control by its ID (guide section 13; `python tools/textizofx_look.py controls --find glow`): numbers, `true`/`false` for checkboxes, a menu's ID or label (`"Wave Left to Right"`) or number, text in quotes, `[x, y]` for points. A colour is its control's name with `"#RRGGBB"` or `[r, g, b]` (`"FxGlowColor": "#FF8800"`). This is how you set the effects (Glow, Fire, Frost, Smoke, Electric, Light Rays, Shine, Sparkle, Glitch, Dust), Float and the Overlap rows.
- `frames`: the clip length, used by the check (the same as `--frames`). `aspect`: the frame's width / height for the fit estimate (0.5625 for 9:16). `notes`: ignored.

**Rows** (the keys of `in` and `out`): `opacity`, `blur`, `position`, `size`, `tracking`, `rotation`, `explosion`. Each row you list is turned on (write `"on": false` to turn off a row a look has). Fields:

- `by`: `letters` (default), `words` or `lines`.
- `start`: the Start Frame.
- **Either** `span` + `delay` (frames each piece moves, and frames between pieces; the tool works out End Frame and Stagger % from the text) **or** `end` + `stagger`, not both. Prefer `span` + `delay`.
- `from` (In rows only) and `to`: numbers, or `[x, y]` for `position`.
- `ease`: one of the ease names in guide section 6.
- `offset`: the row's Animation Offset in frames (plays it that much later).
- Explosion extras: `variance`, `damping`, `spin_x`, `spin_y`, `spin_z` (keep these 0), `pre_roll`, `reverse`. Tracking extra: `pivot` (`left`, `center`, `right`).

**Elements** (`"1"` to `"8"`): `enabled`, `appearance` (`normal`, `outline`, `border_fill`, `border_stroke`; **required for elements 2 to 8** without a look), `color`, `opacity`, `thickness`, `offset` `[x, y]`, `softness` (a number or `[x, y]`), `border_level` (`letters`, `words`, `lines`), `extend` `[x, y]`, `round`, `gradient` (`{"colors": [c1, c2, ...], "angle", "span": letters|words|lines|text, "scale", "aspect"}`).

## Other commands

```
python tools/textizofx_look.py check "<file.setting>" [--frames N] [--aspect 0.5625]
python tools/textizofx_look.py to-spec "<file.setting>" [out.json]
python tools/textizofx_look.py looks
python tools/textizofx_look.py controls [--page Effects] [--find glow]
python tools/textizofx_look.py timing --text "HELLO WORLD" --by letters --span 8 --delay 2
python tools/textizofx_look.py where
python tools/textizofx_look.py next-name --to mylooks [--variant 7]
```

`build` with an output path outside `my-looks/` refuses to replace an existing file unless you pass `--overwrite`.

## Rules

- **Only write to `my-looks/` and the folder the user chose.** Never delete files. Outside `my-looks/`, never overwrite a file without asking.
- **Leave the kit unchanged** (`presets/`, `specs/`, `reference/`, `tools/`, the guide, this file) unless the user asks.
- **Use short names:** `TextizoFX-07A.setting`, with a new number for each look and a new letter for each variation. Never use spaces or descriptive words in the name.
- **Never guess input IDs.** Use the guide, `controls`, or `reference/inputs.json` with `role: public`.
- **Keep the effects on all letters:** an effect's Letters menu (`Fx<Effect>Letters`) stays 0 (All Letters). Selected Letters needs letters picked in the viewer, which a look can't carry.
- **Keep the text the user's:** their words, spelling and capitals.
- **A new look shows in the Look menu after DaVinci Resolve starts again**; until then, use Load Look... (or Browse Looks... on Windows).
