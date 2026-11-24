# TextizoFX AI Guide

For **TextizoFX** (Clipizo), the animated text plugin for DaVinci Resolve's Edit and Fusion pages. Give this file to any AI chat, such as ChatGPT, Claude, Gemini or Copilot, and it can write ready-to-use TextizoFX looks for you. TextizoFX is made by Clipizo (clipizo.com).

---

## Quick start (for you)

1. **Give this file to your AI.** Open the chat and attach this file (or paste all of its text). Then say what you want. For example: *"Make a TextizoFX look: the word SALE pops in letter by letter, red with a black outline, then flies away. My clip is 5 seconds at 30 fps."*
2. **Copy the code.** The AI answers with one block of code. Copy all of it; most chats have a Copy button on the block.
3. **Use it in Resolve**, one of two ways:
   - **Edit page (most people):** paste the code into a plain text file and save it with the short name the AI gave, for example `TextizoFX-01A.setting`, in `Documents/Clipizo/TextizoFX/Looks`. Select your TextizoFX clip and click **Load Look...** in the Inspector (right under the Look menu), then pick the file. Your own text stays; everything else takes the look.
   - **Fusion page:** click an empty spot in the **Nodes** area and press **Ctrl+V** (Mac: **Cmd+V**). A new TextizoFX node appears with the look. Connect it to **MediaOut1**, or put it over a clip with a **Merge** node (MediaIn1 into the yellow background input, TextizoFX into the green foreground input, the Merge into MediaOut1).

You can type your own text in the Inspector at any time.

**To keep a look in TextizoFX's Look menu,** leave the file in `Documents/Clipizo/TextizoFX/Looks`: it is listed in the Look menu (with your other looks) from the next time DaVinci Resolve starts, and in **Browse Looks...** (Windows) right away.

---

## Instructions for the AI

You are making a **look for the TextizoFX node**: plain text in Fusion's settings format holding one TextizoFX node, which the user loads with TextizoFX's **Load Look...** or pastes into Resolve's Fusion page. Everything you need is in this guide. **Only use input names that appear in this guide (section 13 lists every one), and do not guess others.** A misspelled name, or a name in the wrong capitals, is silently ignored.

**How to answer:**

1. **Ask only if something essential is missing,** and ask everything in one short message:
   - the text;
   - the style or mood;
   - colours or font (optional);
   - how long the clip is and its frame rate.

   If the user says "just do it", use these defaults: 5 seconds at 24 fps, white Montserrat Bold, and a clean blur-in reveal.
2. **Start from the closest example and change it.** Example 1 (section 11) is clean, example 2 is fun, and example 3 shows an effect (Glow). Follow every rule in the checklist below.
3. **Reply in three parts:**
   - one or two sentences describing the animation;
   - the whole look in **one** code block marked `lua`, with nothing else in it;
   - the usage steps from section 14 (save and Load Look..., or paste on the Fusion page), in 3 or 4 short lines.
4. **Give every look a short name:** `TextizoFX-` followed by a two-digit number and a capital letter, for example `TextizoFX-01A`.
   - Each new look gets the next number (`TextizoFX-01A`, `TextizoFX-02A`, …).
   - A variation of a look keeps its number and takes the next letter (`TextizoFX-01B`, `TextizoFX-01C`).
   - Use no spaces and no descriptive words in the name; describe the look in your reply instead.
   - If the user mentions looks they already have, continue after their highest number.

   Put the name in the first line of the reply. If you can create files, also offer the look as a download named after it, for example `TextizoFX-01A.setting`, in the last line of the reply.
5. **When the user asks for changes,** send the whole look again, not just the changed lines.

**Checklist (check every item before you answer):**

- [ ] **One node, written exactly like the examples.** The file contains exactly one node, `TextizoFX1 = ofx.com.clipizo.textizofx { Inputs = { ... } }`, inside `{ Tools = ordered() { ... } }`, with the same structure as the examples. No comments, no other nodes.
- [ ] **Menus are numbers.** Every menu (Animate by, Ease, Direction, Appearance, Alignment, the Overlap rows' Property ...) is written as its number from 0, from the tables in this guide. Never `FuID { "..." }`: TextizoFX ignores it.
- [ ] **Required inputs:** `StateVersion` is 12; `StyledText` holds the text, with `TextEdited` set to 1; `Font` and `Style` are set.
- [ ] **Every animation row that is on:** `...Enable` 1, and each of these that differs from its default (section 4): `...Follower`, `...AnimationStart`, `...AnimationEnd`, `...Stagger`, `...StartValue` (In rows only), `...EndValue`, `...CurvePreset` (the ease's number). Rows you don't use need nothing (they are off by default).
- [ ] **Timing:** computed with the formula in section 5; the entrance finishes before the exit starts; the exit ends before the clip's last frame.
- [ ] **Shading:** element 1 is the one the Shading page shows. If you change element 1, write each changed field **twice**, as `ShadingProxy...` and as `ShadingElement1...`, with **identical** values (section 7). Elements 2 to 8 are written once, as `ShadingElement<N>...`.
- [ ] **Explosion:** in every Explosion row that is on, write Spin X/Y/Z (`...RotationX`, `...RotationY`, `...Rotation`) as 0: they default to 180, 180 and 240. Make letters turn with the Rotation row instead.
- [ ] **Effects:** an effect's Letters menu (`Fx<Effect>Letters`) stays 0 (All Letters).
- [ ] **Fonts:** use one TextizoFX carries or a safe one (section 3), unless the user named another font.
- [ ] **Name:** the look has a short name like `TextizoFX-01A` (step 4 above).

---

## 1. How TextizoFX works

TextizoFX is a text generator: on the Edit page it is a clip of its own (or an effect over a clip), on the Fusion page a node. Its Inspector has six pages:

- **Text:** the Look menu, Load Look..., the text, the font, size, position, rotation (with a 3D turn) and colour, Fit to Frame, the letters picked in the viewer.
- **Shading:** the look of the letters, in up to 8 layers (elements), for example fill, outline, shadow and box.
- **In:** the entrance animation (and four Overlap rows: extra animations at their own frames).
- **Out:** the exit animation.
- **Motion Blur.**
- **Effects:** ten effects drawn over the text (Glow, Fire, Frost, Smoke, Electric, Light Rays, Shine, Sparkles, Glitch, Dust) and Float (a gentle drift).

The In and Out pages each have **seven animation rows**: Opacity, Blur, Position, Size, Tracking, Rotation and Explosion. A row animates one property of each **letter**, each **word** or each **line**, from a Start Value to an End Value:

- It runs between a **Start Frame** and an **End Frame**.
- Its **Stagger %** spreads the pieces out in time.
- Its **Ease** shapes the motion.

Rows that are on all play at once and add up. For example, Opacity, Blur and Position together give a "fade up into focus".

A look is everything but the text: Load Look... (and the Look menu) keep the user's text and set every other control to the look's value, or to its default when the look doesn't name it.

## 2. The node file

A look is Fusion settings text. Every input is written like this:

```
				<Name> = Input { Value = <value>, },
```

Value formats:

| Kind | Write it as | Example |
|---|---|---|
| number | plain decimal number (use a dot, not a comma) | `2.4`, `-0.06`, `0` |
| checkbox | `1` on, `0` off | `1` |
| menu | its **number**, counting from 0, from this guide's tables | `InopacityFollower = Input { Value = 1, },` (words) |
| text | in double quotes. Write a new line as `\n`, a quote as `\"`, and a backslash as `\\` | `"Hello\nWorld"` |
| point | `{ x, y }` | `{ 0.5, 0.5 }` |
| colour | one input per channel: the colour's name + `Red`, `Green`, `Blue` (and `Alpha`), each 0 to 1 | `RedRed`, `RedGreen`, `RedBlue`, `RedAlpha` (the text's Color) |
| gradient | text: `position:r,g,b,a` stops joined by `;` | `"0:1,0.24,0.55,1;1:0.2,0.4,1,1"` |

The order of the inputs does not matter. Do not write the same input twice.

**Write only what differs from TextizoFX's defaults** (plus `StateVersion`, `StyledText`, `TextEdited`, `Font` and `Style`), as the examples do. Load Look... sets everything a look doesn't name to its default, and a node pasted on the Fusion page starts from the defaults, so a short look gives exactly the same result as a complete one. (Only Fusion's own Settings > Load… onto an *existing* node keeps that node's values for what a look leaves out; use Load Look... or paste a new node.)

## 3. Text controls

| Name | What it does | Values |
|---|---|---|
| `StateVersion` | the look format | always `12` |
| `StyledText` | the text | `"Hello"`, `"Two\nlines"` |
| `TextEdited` | marks the text as set | always `1` |
| `Font` | font family | `"Montserrat"` |
| `Style` | font style | `"Regular"`, `"Bold"`, `"Italic"`, `"Bold Italic"`, `"Black"` ... (what the font has) |
| `Size` | text size. 1 is the same as a Text+ node at 0.08 | usually 0.6 to 2.8 (see "Size and width" below) |
| `Center` | where the text sits, 0 to 1 across the frame; y goes up (0 is the bottom). With the default Vertical Anchor (Center), `{ 0.5, 0.5 }` puts the middle of the text block in the middle of the frame | `{ 0.5, 0.5 }` |
| `VerticalAnchor` | which part of the text block sits on Center's y | `0` Top, `1` Center (default), `2` Baseline (the first line's baseline: Textizo's older looks), `3` Bottom |
| `Alignment` | how lines sit around Center X | `0` left (text starts at Center X), `1` center, `2` right |
| `Tracking` | extra space after every letter, in frame widths (0.01 is about 19 px at 1920 wide) | `0`. Tight Apple look: `-0.003` |
| `LineSpacing` | distance between lines (multiplier) | `1` |
| `Rotation` | turns the whole text (Rotation Z), in degrees | `0` |
| `RotationX`, `RotationY` | turns the whole text in 3D (perspective), in degrees: X tips it back or forward, Y swings it sideways | `0`; a slight 3D feel: `RotationY` 12 to 20 |
| `FitToFrame` | shrinks the text (never grows it) when it would run out of the frame, keeping a small margin | `1` (default) |
| `RedRed`, `RedGreen`, `RedBlue` | the text's Color: tints Shading element 1. **Keep them at 1** and set colours on the Shading elements | `1` |
| `RedAlpha` | opacity of the whole text, all layers | `1` |

**Size and width.** Capital letters are about 0.07 x Size of the frame height (in 16:9): Size 1 gives capitals 70 to 80 px tall at 1080p, depending on the font (Arial 80, Montserrat 71). To estimate a line's width as a fraction of the frame width:

1. Add up its characters in ems (spaces count): narrow (i, j, l, t, f, r, I, space, and . , ! ' : ;) 0.28; most lower-case 0.55; most capitals and digits 0.67; wide (m, w, M, W, @) 0.9.
2. Multiply by the font factor (measured in TextizoFX, which scales every font by its own height, so heavy fonts are less wide than their names suggest):
   - Arial 0.89, Arial Bold 0.95, Arial Black 0.87, Verdana 0.92, Georgia 0.9, Times New Roman 0.89, Impact 0.76, Comic Sans MS 0.75
   - Montserrat Bold 0.99, Inter Bold 0.93, Rubik Bold 0.97, Poppins Bold 0.85, Archivo Black 1.13, Luckiest Guy 1.18, Bangers 0.8, Permanent Marker 0.8, Anton 0.6, Bebas Neue 0.63, Oswald Bold 0.62
   - Courier New: every character is 0.53, with no factor
3. Multiply by 0.064 x Size.

Keep every line under about 0.85 of the frame width. For example, "PARTY TIME!" in Archivo Black is about 6.4 ems x 1.13 x 0.064 x 1.8 = 0.84, so Size 1.8 fits. Fit to Frame (on by default) shrinks a line that would still run out of the frame, but a look that fits by itself keeps its intended size. For long sentences, use Size 0.8 or less, or split the text into lines with `\n`.

**Fonts TextizoFX carries** (they work on every computer that has TextizoFX, Windows and Mac): <!-- fonts -->
Anton, Archivo Black, Bangers, Barlow, Bebas Neue, Fredoka, Inter, Kanit, Luckiest Guy, Montserrat, Nunito, Open Sans, Oswald, Permanent Marker, Poppins, Roboto, Rubik, Vazirmatn
<!-- /fonts -->

**Fonts that work on both Windows and Mac** besides those: Arial, Arial Black, Verdana, Tahoma, Trebuchet MS, Georgia, Times New Roman, Courier New, Impact and Comic Sans MS.

- If the user names another font, use it, and tell them it must be installed on every computer that opens the project.
- Bold looks: `"Montserrat"` + `"Bold"`, `"Archivo Black"` + `"Regular"`, `"Anton"`, `"Bebas Neue"` (all capitals), `"Bangers"` (comic), `"Luckiest Guy"` (playful).

**Other languages.** Write Arabic, Persian, Urdu, Hebrew, Chinese, Japanese or Korean text straight into `StyledText`, as the characters themselves. TextizoFX joins Arabic letters, runs Arabic and Hebrew right to left (Latin words and numbers inside them stay left to right), keeps vowel and accent marks on their letter, and treats each Chinese or Japanese character as a word. If the font has no letters for the language, TextizoFX draws them with an installed font that has them. `"Vazirmatn"` (carried) suits Arabic and Persian.

## 4. Animation rows

Each row's name is the page, then the row, then the field. For example, `In` + `opacity` + `Enable` gives `InopacityEnable`.

- Pages: `In` and `Out`.
- Rows, as written in names: `opacity`, `blur`, `center` (shown as "Position" in the Inspector), `size`, `tracking`, `rotation`, `explosion`.

**Fields of a row:**

| Field | Meaning | Write it as |
|---|---|---|
| `Enable` | row on or off | `1` or `0` |
| `Follower` | what moves separately | `0` letters, `1` words, `2` lines |
| `AnimationStart` | Start Frame, counted from the first frame of the clip (0) | whole number |
| `AnimationEnd` | End Frame. The **last** piece finishes exactly here | whole number, after the Start Frame |
| `Stagger` | Stagger % (section 5) | number, 0 or more |
| `StartValue` | value at the start. **In rows only** | see the table below |
| `EndValue` | value at the end | see the table below |
| `CurvePreset` | the ease (section 6) | its number: `5` out_cubic |
| `AnimOffset` | the row's Animation Offset: plays it that many frames later (earlier below 0) | `0` |

**Row defaults:** Animate `0` (letters), Start Frame 0 (Out rows: 100), End Frame 30 (Out rows: 130), Stagger % 10, Ease `0` (linear); the values' defaults are in the next table. A field at its default can be left out.

The examples also write `...CurvePresetID`, the ease's name in quotes (`"out_cubic"`). If you write it, it must name the same ease as `...CurvePreset`.

**What the values mean:**

| Row | Value | In default (Start to End) | Notes |
|---|---|---|---|
| `opacity` | 0 (invisible) to 1 | 0 to 1 | |
| `blur` | extra softness: 0.1 is about 11 px of blur at 1080p | 0.1 to 0 | Typical 0.08 to 0.15. Values above about 0.27 add nothing at 1080p. It also blurs outlines and shadows |
| `center` | **offset** from where the text sits, `{ x, y }`. x is in frame widths and y in frame heights; +y is up | `{ 0, 0 }` to `{ 0, 0 }` | `{ 0, -0.06 }` starts 6% of the frame height lower |
| `size` | scale around each piece's own centre: 1 is normal and 0 is gone | 0 to 1 | 1.1 to 1 gives a gentle settle; 0 to 1 is a pop |
| `tracking` | spreads letters (or words) apart: the step between neighbours, in frame widths | 0 to 0 | 0.05 to 0 gives letters that gather in |
| `rotation` | degrees around each piece's centre | 0 to 0 | -120 to 0 gives a spin in |
| `explosion` | distance each piece flies, in frame widths, along its own random direction. Each piece goes 0.45 to 1.25 times the value | 0 to 1 | For an entrance use 0.3 to 0.6 down to 0. To fly away on Out, use 1 to 1.5 and fade out with an Opacity row too |

**Out rows (the exit).** An Out row's `EndValue` is where that property ends up, in the same units as on the In page: `OutopacityEndValue` 0 fades out, `OutcenterEndValue` `{ 0, 0.1 }` rises 10% of the frame height, `OutsizeEndValue` 0 shrinks away. The exit always starts from wherever the In row ended, so the Out page has no Start Value: do **not** write `...StartValue` on Out rows.

**Out defaults:** Start Frame 100 and End Frame 130. The End Values are opacity 0, blur 0.1, size 0 and explosion 1; all others are 0.

**The Rotation rows turn in 3D too:** besides `InrotationStartValue` / `EndValue` (Z), the In row has `InrotationStartX`, `InrotationEndX`, `InrotationStartY`, `InrotationEndY` (degrees), and the Out row `OutrotationEndX` and `OutrotationEndY` (section 13 has them all).

**Tracking extra.** A Tracking row can have `Pivot`, what stays put while the pieces spread or close up: `0` left, `1` center (default), `2` right. For example `IntrackingPivot = Input { Value = 0, },`.

**Page extras.**

- **Direction** (`InDirection`, `OutDirection`): the order the pieces go in: `0` reading order (default; right to left for Arabic and Hebrew), `1` left to right, `2` right to left.
- **Animation Offset** (`InAnimOffset`, `OutAnimOffset`): moves a whole page later (earlier below 0), in frames.

**Explosion extras.** An Explosion row that is on also uses:

| Field | Inspector | Use |
|---|---|---|
| `Damping` | Damping (0 to 8, default 2) | `0` follows the ease exactly. With 1 to 3 the pieces wait, then rush |
| `Speed` | Variance (0 to 1, default 0.35) | random speed per piece. `0.3` is lively |
| `RotationX`, `RotationY`, `Rotation` | Spin X/Y/Z (default 180, 180, 240) | **always write `0`**: explosion spin jumps when a piece lands or overshoots. Turn letters with the Rotation row instead |
| `Offset` | Pre-Roll (frames) | `0`. Above 0, the pieces are already in flight at the Start Frame |
| `Reverse` | Reverse | `0`. With 1, the last piece goes first |

## 5. Timing

Frames count from the clip's first frame (frame 0). A row fits completely between its Start Frame and End Frame: the first piece starts at the Start Frame, and the last piece lands exactly on the End Frame.

**Stagger %** says how far one piece is into its own move when the next one starts: 0 all pieces move together, 50 the next starts halfway, 100 one after another, above 100 gaps between pieces.

**Design with per-piece numbers.** Choose S, how many frames each piece moves, and D, how many frames apart the pieces start. N is the number of pieces in that row. Then:

```
End Frame = Start Frame + S + D x (N - 1)      (round to a whole frame)
Stagger % = 100 x D / S                        (use 0 when N is 1)
```

**Counting N:** letters are every character except spaces, tabs and line breaks (punctuation counts; accent and vowel marks don't, an Arabic lam + alef is one letter); words are pieces separated by spaces (each Chinese or Japanese character is a word); lines are lines that are not empty.

**Example.** For "HELLO" (N = 5) with each letter moving 8 frames, 2 frames apart: End Frame = 0 + 8 + 2 x 4 = 16, and Stagger % = 25.

**Frame rate.** Numbers in this guide assume 24 fps. At other rates, multiply every frame count, S and D included, by fps / 24: 1.25 at 30 fps, 2.5 at 60 fps.

**Clip length.** End the exit a few frames before the clip ends:

```
last frame      = seconds x fps - 1
Out End Frame   = last frame - about 5
Out Start Frame = Out End Frame - (S + D x (N - 1))
```

For example, a 5-second clip at 24 fps has frames 0 to 119, so the exit starts around 100 and ends around 112 to 116.

**Align to End** keeps the exit at the clip's end whatever its length: `OutAlignEnd = Input { Value = 1, },` moves the Out rows so their last piece lands `OutBeforeEnd` frames before the clip's last frame (0: on the last frame), keeping their lengths and gaps. Some of the ready looks use it. **Start At** (`InStartAt`, frames) makes every In row count from that frame.

**Stop at Frame** ends a page part way: `InStopEnable = Input { Value = 1, },` and `InStopFrame` (a frame from the clip's start). From there every piece keeps the look it has. The Out page has `OutStopEnable` and `OutStopFrame`.

## 6. Eases

`CurvePreset` takes the ease's number:

| Number | Ease | Number | Ease | Number | Ease |
|---|---|---|---|---|---|
| 0 | linear | 11 | out_quint | 22 | in_back |
| 1 | in_quad | 12 | in_out_quint | 23 | out_back |
| 2 | out_quad | 13 | in_sine | 24 | in_out_back |
| 3 | in_out_quad | 14 | out_sine | 25 | in_elastic |
| 4 | in_cubic | 15 | in_out_sine | 26 | out_elastic |
| 5 | out_cubic | 16 | in_expo | 27 | in_out_elastic |
| 6 | in_out_cubic | 17 | out_expo | 28 | in_bounce |
| 7 | in_quart | 18 | in_out_expo | 29 | out_bounce |
| 8 | out_quart | 19 | in_circ | 30 | in_out_bounce |
| 9 | in_out_quart | 20 | out_circ | | |
| 10 | in_quint | 21 | in_out_circ | | |

| Use | Good eases |
|---|---|
| entrances: fast start, soft landing | `5` out_cubic, `8` out_quart, `17` out_expo |
| a little overshoot | `23` out_back |
| wobble | `26` out_elastic (pops, Size or Rotation) |
| drop and bounce | `29` out_bounce (a Position drop) |
| exits: slow start, fast end | `1` in_quad, `4` in_cubic, `22` in_back (winds up first) |
| fades | `15` in_out_sine, `2` out_quad |

## 7. Look: shading elements

Shading has **8 layers (elements)**. Element 1 is drawn on top and is the text fill; higher numbers are drawn behind it. Each element has an **Appearance**: `0` Normal (filled letters), `1` Outline, `2` Border Fill (a box behind each letter, word or line) or `3` Border Stroke (the outline of that box).

**The shown-element rule (important).** The Shading page shows one element at a time, element 1 at first, through its visible `ShadingProxy...` controls, and TextizoFX keeps that element in both places. So when you change element 1, write each changed field twice, as `ShadingProxy<Field>` and as `ShadingElement1<Field>`, with identical values. Elements 2 to 8 are written once, as `ShadingElement<N><Field>`.

The proxy's colours are colour inputs (one per channel); the elements' own are plain numbers:

| Field | `ShadingElement<N>...` | `ShadingProxy...` |
|---|---|---|
| colour | `Red`, `Green`, `Blue`, `Alpha` | `RedRed`, `RedGreen`, `RedBlue`, `RedAlpha` |
| gradient's last colour ("Color 2") | `EndRed`, `EndGreen`, `EndBlue`, `EndAlpha` | `EndRedRed`, `EndRedGreen`, `EndRedBlue`, `EndRedAlpha` |

For example, a yellow fill: `ShadingElement1Red` 1, `ShadingElement1Green` 0.86, `ShadingElement1Blue` 0, and `ShadingProxyRedRed` 1, `ShadingProxyRedGreen` 0.86, `ShadingProxyRedBlue` 0.

**Element fields:**

| Field | Meaning |
|---|---|
| `Enable` | 1 on, 0 off (elements 2 to 8 are off by default) |
| `Appearance` | 0 Normal, 1 Outline, 2 Border Fill, 3 Border Stroke |
| `Opacity` | 0 to 1 |
| `Thickness` | outline width in frame widths (0.004 is about 8 px at 1920 wide), centred on the letter edge. It does **not** follow Size: use about 0.00375 x Size for a bold sticker outline |
| `Offset` | `{ x, y }` shift: x in frame widths, y in frame heights, +y up. Hard shadow: about `{ 0.0025 x Size, -0.005 x Size }` |
| `SoftnessX`, `SoftnessY` | blur of this layer: 0.05 is about 5 px at 1080p. It stops growing at about 0.13; for a real glow use the Effects page's Glow |
| `BorderLevel` | the box is around each 0 letter, 1 word or 2 line |
| `BorderExtendX`, `BorderExtendY` | box padding on each side, in frame widths |
| `BorderRound` | box corner radius, in frame widths |
| `ColorMode` | 0 solid colour, 1 gradient |
| `GradientAngle` | gradient direction in degrees: 0 bottom to top, -90 left to right |
| `MappingLevel` | the gradient spans each 0 letter, 1 word, 2 line or 3 whole text |
| `MappingSize` | gradient length relative to that span (default 1.5; 1 reaches the edges) |
| `MappingAspect` | vertical stretch of the gradient (default 1) |
| `Gradient` | the gradient itself, as text (section 2) |

**Each element's own defaults:** opacity 1, thickness 0.02, offset `{ 0, 0 }`, softness 0, solid colour, Color 2 white; except element 1 (on, white), element 2 (an Outline, red, thickness 0.004), element 3 (black, softness 0.01) and element 4 (a Border Fill, blue, extend 0.02). Always give elements 2 to 8 their Appearance and colour.

**Recipes:**

- **Sticker:** element 1 a bright fill; element 2 Outline, black, thickness 0.00375 x Size; element 3 Normal, black, offset `{ 0.0025 x Size, -0.005 x Size }`, softness 0, opacity 0.85.
- **Soft shadow:** element 3 Normal, black, offset `{ 0.002 x Size, -0.004 x Size }`, softness 0.05, opacity 0.6.
- **Boxes need room.** Measure box sizes in **em = 0.064 x Size** (frame widths). Padding under about 0.2 em looks cramped, a round under about 0.15 em looks square.
- **Caption pill behind the line:** element 2 Border Fill, `BorderLevel` 2, extend about 0.6 em / 0.28 em, round 1 em or more; animate it with an In Size row by lines (0 to 1, out_back, S 12) and the words with Opacity and Position rows by words starting about 4 frames later.
- **Word chips** (one box per word): put 2 or 3 spaces between the words in the text, then extend about 0.3 em / 0.22 em and round 1 em. Animate by words.
- **Gradient fill (element 1):** `ColorMode` 1, `GradientAngle` -90, `MappingLevel` 3, `MappingSize` 1, the first and last colours as Color and Color 2, and the gradient on both `ShadingProxyGradient` and `ShadingElement1Gradient`:

```
				ShadingElement1Gradient = Input { Value = "0:1,0.24,0.55,1;1:0.2,0.4,1,1", },
```

**Boxes follow** only the rows animated at their own level or above: a word box follows `words` and `lines` rows, a line box `lines` rows. If letters animate inside word boxes, add an Opacity row by words.

## 8. Motion blur

| Name | Use |
|---|---|
| `MotionBlurEnable` | `1` for fast, big moves (pops, drops, spins). `0` for calm fades |
| `MotionBlurShutterAngle` | `180` |
| `MotionBlurSamples` | Quality, 1 to 10. Use `2` |
| `MotionBlurBias` | `0` |
| `MotionBlurSampleSpread` | `1` |

## 9. TextizoFX's own controls

**Effects** (the Effects page). Each effect has a switch, `Fx<Effect>On`, and its own controls (section 13 lists them all, by section):

| Effect | Switch | What it does |
|---|---|---|
| Glow | `FxGlowOn` | a soft glow round the text, in its own colours (`FxGlowTextColors` 1) or one colour (`FxGlowTextColors` 0 and `FxGlowColorRed`, `FxGlowColorGreen`, `FxGlowColorBlue`); `FxGlowAmount` (1), `FxGlowSize` (1) |
| Fire | `FxFireOn` | flames rising from the letters |
| Frost | `FxFrostOn` | an icy crust and cold mist |
| Smoke | `FxSmokeOn` | smoke drifting off the letters |
| Electric | `FxElectricOn` | crackling arcs along the letters |
| Light Rays | `FxRaysOn` | rays of light streaming from the text |
| Shine | `FxShineOn` | a light sweep across the letters |
| Sparkles | `FxSparkleOn` | sparkles round the text |
| Glitch | `FxGlitchOn` | digital glitch slices and colour splits |
| Dust | `FxDustOn` | dust drifting round the text |

An effect's `Fx<Effect>Letters` stays `0` (All Letters). Effects cost render time: one or two per look.

**Float** (`FxFloatOn`): a gentle drift of the letters, words, lines or whole text (`FxFloatPieces` 0 to 3) in a style (`FxFloatStyle`: 0 Random, 1 Wave Left to Right, 2 Wave Right to Left, 3 Wave from the Middle, 4 Together), `FxFloatAmount` (1) and `FxFloatSpeed` (1: a swing about every 3 seconds). Use it for calm, living holds.

**The 3D turn:** `RotationX` and `RotationY` on the Text page (section 3) and the Rotation rows' X and Y (section 4), seen in perspective.

**Overlap rows** (`Ov1` to `Ov4`, on the In page): extra animations at their own frames, over the In and Out rows (Size and Opacity multiply them, Position, Rotation, Blur and Tracking add to them). Each has `Ov<n>On`, `Ov<n>Prop` (0 Size, 1 Position, 2 Rotation, 3 Opacity, 4 Blur, 5 Tracking), `Ov<n>Animate` (0 letters, 1 words, 2 lines), `Ov<n>Start`, `Ov<n>End` (frames), `Ov<n>Stagger`, `Ov<n>Ease` (the ease's number, section 6) and the property's From and To (`Ov<n>SizeFrom`, `Ov<n>SizeTo`, `Ov<n>PositionFrom` ...). For example a pulse in the middle of a hold: `Ov1Prop` 0, `Ov1Start` 48, `Ov1End` 60, `Ov1SizeFrom` 1, `Ov1SizeTo` 1.12, `Ov1Ease` 26.

**Fit to Frame** (`FitToFrame`, on by default) shrinks text that would run out of the frame. Leave it on.

## 10. What looks good

These are the house style the ready looks follow.

**Fast and crisp.** Entrances about 15 to 26 frames in total at 24 fps; 1.5 to 2 frames between letters; each letter moves for 6 to 14 frames; exits 12 to 16 frames.

**Move only during In and Out.** The hold in between stays still (or floats gently with Float), with no slow slides or constant zooms.

**Short moves:** position offsets of 0.04 to 0.12 of the frame height; size 1.1 to 1 for a settle, or 0 to 1 for a pop; rotation 15 to 30 degrees for a tilt, 120 to 360 for a spin.

**Premium reveals.** Opacity 0 to 1, blur 0.1 to 0.12 down to 0, and a small rise or settle. White Montserrat or Inter Bold with `Tracking` -0.003 gives an Apple-like look.

**Fun.** The sticker look (a bright fill, a black outline and a hard shadow) with out_elastic or out_back pops, the Rotation row and motion blur on. Fun pops can use up to 6 rows per page; clean looks need 3 or 4.

**Calm and elegant** (weddings, documentaries, luxury): roughly double the timings, soft eases (in_out_sine, out_cubic), no overshoot, small moves (0.03 to 0.04), motion blur off, a warm colour.

**Avoid:** long sideways slides; linear moves on positions; more than about 6 rows per page; text bigger than the frame; more than two effects.

**Ideas** (S and D per letter or per word):

| Look | In rows | Out rows |
|---|---|---|
| Blur reveal | opacity 0 to 1 (S 10, in_out_sine); blur 0.12 to 0 (S 14, out_cubic); size 1.1 to 1 (S 13, out_quart). D 2 | opacity to 0 (in_out_sine), blur to 0.12 and size to 0.95 (in_quad); S 5, D 1.2 |
| Rise | as Blur reveal, plus position `{ 0, -0.05 }` to `{ 0, 0 }` (S 14, out_quart) | position to `{ 0, 0.04 }`, opacity to 0 (S 6, D 1.2, in_quad) |
| Drop and bounce | opacity 0 to 1 (S 4); position `{ 0, 0.45 }` to `{ 0, 0 }` (S 12, out_bounce); rotation -25 to 0 (S 14, out_elastic) | position to `{ 0, 0.7 }`, rotation to 120, opacity to 0 (S 7, in_back) |
| Zoom slam | opacity (S 4); blur 0.2 to 0 (S 9); size 4 to 1 (S 10, out_back); rotation 25 to 0 (S 10, out_back) | size to 3.5, blur to 0.2, opacity to 0 (S 8, in_cubic) |
| Word lift | by words: opacity, blur 0.1 to 0, position `{ 0, -0.06 }` to `{ 0, 0 }` (S 14, D 4) | by words: opacity to 0, position to `{ 0, 0.05 }` (S 8, D 2) |
| Neon | letters: opacity (S 2, out_quad), blur 0.2 to 0 (S 7, out_cubic), size 1.35 to 1 (S 9, out_cubic), D 2; a near-white fill and Glow in a neon colour | opacity to 0 and blur to 0.2 (S 5, D 1, in_quad) |
| Caption pill | size by lines 0 to 1 (S 12, out_back); opacity by words (start 4, S 5, D 4); position by words `{ 0, -0.02 }` to `{ 0, 0 }` (start 4, S 10, D 4, out_cubic); a pill on element 2 (section 7) | size and opacity by lines to 0 (S 9, in_back / in_quad) |

## 11. Examples

These are complete looks, written short (only what differs from TextizoFX's defaults).

**Example 1: a clean reveal (`TextizoFX-01A`).** White Montserrat Bold. Each letter fades in, comes into focus and settles from 110% size, 2 frames after the one before; the text holds, then blurs away from frame 100.

<!-- example1 -->
```lua
{
	Tools = ordered() {
		TextizoFX1 = ofx.com.clipizo.textizofx {
			Inputs = {
				StateVersion = Input { Value = 12, },
				TextEdited = Input { Value = 1, },
				StyledText = Input { Value = "Welcome", },
				Font = Input { Value = "Montserrat", },
				Style = Input { Value = "Bold", },
				Size = Input { Value = 2.6, },
				Tracking = Input { Value = -0.003, },
				InopacityEnable = Input { Value = 1, },
				InopacityAnimationEnd = Input { Value = 22, },
				InopacityStagger = Input { Value = 20, },
				InopacityCurvePreset = Input { Value = 15, },
				InopacityCurvePresetID = Input { Value = "in_out_sine", },
				InblurEnable = Input { Value = 1, },
				InblurAnimationEnd = Input { Value = 26, },
				InblurStagger = Input { Value = 14.3, },
				InblurStartValue = Input { Value = 0.12, },
				InblurCurvePreset = Input { Value = 5, },
				InblurCurvePresetID = Input { Value = "out_cubic", },
				InsizeEnable = Input { Value = 1, },
				InsizeAnimationEnd = Input { Value = 25, },
				InsizeStagger = Input { Value = 15.4, },
				InsizeStartValue = Input { Value = 1.1, },
				InsizeCurvePreset = Input { Value = 8, },
				InsizeCurvePresetID = Input { Value = "out_quart", },
				OutopacityEnable = Input { Value = 1, },
				OutopacityAnimationEnd = Input { Value = 112, },
				OutopacityStagger = Input { Value = 24, },
				OutopacityCurvePreset = Input { Value = 15, },
				OutopacityCurvePresetID = Input { Value = "in_out_sine", },
				OutblurEnable = Input { Value = 1, },
				OutblurAnimationEnd = Input { Value = 112, },
				OutblurStagger = Input { Value = 24, },
				OutblurEndValue = Input { Value = 0.12, },
				OutblurCurvePreset = Input { Value = 1, },
				OutblurCurvePresetID = Input { Value = "in_quad", },
				OutsizeEnable = Input { Value = 1, },
				OutsizeAnimationEnd = Input { Value = 112, },
				OutsizeStagger = Input { Value = 24, },
				OutsizeEndValue = Input { Value = 0.95, },
				OutsizeCurvePreset = Input { Value = 1, },
				OutsizeCurvePresetID = Input { Value = "in_quad", },
			},
			ViewInfo = OperatorInfo { Pos = { 0, 0 } },
		},
	},
	ActiveTool = "TextizoFX1"
}
```
<!-- /example1 -->

**Example 2: a sticker pop (`TextizoFX-02A`).** Yellow Archivo Black with a black outline (element 2) and a hard shadow (element 3). The letters pop in from size 0 with an elastic bounce, rise into place and spin in from -120 degrees, with motion blur on. From frame 100 they spin up and away.

<!-- example2 -->
```lua
{
	Tools = ordered() {
		TextizoFX1 = ofx.com.clipizo.textizofx {
			Inputs = {
				StateVersion = Input { Value = 12, },
				TextEdited = Input { Value = 1, },
				StyledText = Input { Value = "PARTY TIME!", },
				Font = Input { Value = "Archivo Black", },
				Style = Input { Value = "Regular", },
				Size = Input { Value = 1.8, },
				ShadingProxyRedGreen = Input { Value = 0.8392, },
				ShadingProxyRedBlue = Input { Value = 0.0392, },
				ShadingElement1Green = Input { Value = 0.8392, },
				ShadingElement1Blue = Input { Value = 0.0392, },
				ShadingElement2Enable = Input { Value = 1, },
				ShadingElement2Thickness = Input { Value = 0.00675, },
				ShadingElement2Red = Input { Value = 0, },
				ShadingElement3Enable = Input { Value = 1, },
				ShadingElement3Opacity = Input { Value = 0.85, },
				ShadingElement3Offset = Input { Value = { 0.0045, -0.009 }, },
				ShadingElement3SoftnessX = Input { Value = 0, },
				ShadingElement3SoftnessY = Input { Value = 0, },
				InopacityEnable = Input { Value = 1, },
				InopacityAnimationEnd = Input { Value = 18, },
				InopacityStagger = Input { Value = 37.5, },
				InopacityCurvePreset = Input { Value = 2, },
				InopacityCurvePresetID = Input { Value = "out_quad", },
				IncenterEnable = Input { Value = 1, },
				IncenterAnimationEnd = Input { Value = 26, },
				IncenterStagger = Input { Value = 12.5, },
				IncenterStartValue = Input { Value = { 0, -0.12 }, },
				IncenterCurvePreset = Input { Value = 23, },
				IncenterCurvePresetID = Input { Value = "out_back", },
				InsizeEnable = Input { Value = 1, },
				InsizeAnimationEnd = Input { Value = 28, },
				InsizeStagger = Input { Value = 10.7, },
				InsizeCurvePreset = Input { Value = 26, },
				InsizeCurvePresetID = Input { Value = "out_elastic", },
				InrotationEnable = Input { Value = 1, },
				InrotationAnimationEnd = Input { Value = 26, },
				InrotationStagger = Input { Value = 12.5, },
				InrotationStartValue = Input { Value = -120, },
				InrotationCurvePreset = Input { Value = 23, },
				InrotationCurvePresetID = Input { Value = "out_back", },
				OutcenterEnable = Input { Value = 1, },
				OutcenterAnimationEnd = Input { Value = 115, },
				OutcenterStagger = Input { Value = 16.7, },
				OutcenterEndValue = Input { Value = { 0, 0.1 }, },
				OutcenterCurvePreset = Input { Value = 22, },
				OutcenterCurvePresetID = Input { Value = "in_back", },
				OutsizeEnable = Input { Value = 1, },
				OutsizeAnimationEnd = Input { Value = 115, },
				OutsizeStagger = Input { Value = 16.7, },
				OutsizeCurvePreset = Input { Value = 22, },
				OutsizeCurvePresetID = Input { Value = "in_back", },
				OutrotationEnable = Input { Value = 1, },
				OutrotationAnimationEnd = Input { Value = 115, },
				OutrotationStagger = Input { Value = 16.7, },
				OutrotationEndValue = Input { Value = 180, },
				OutrotationCurvePreset = Input { Value = 22, },
				OutrotationCurvePresetID = Input { Value = "in_back", },
				MotionBlurEnable = Input { Value = 1, },
			},
			ViewInfo = OperatorInfo { Pos = { 0, 0 } },
		},
	},
	ActiveTool = "TextizoFX1"
}
```
<!-- /example2 -->

**Example 3: neon with Glow (`TextizoFX-03A`).** Near-white letters flick on out of a blur, each settling from 135% size, with a cyan Glow (the Effects page) around the text. From frame 100 they blur away.

<!-- example3 -->
```lua
{
	Tools = ordered() {
		TextizoFX1 = ofx.com.clipizo.textizofx {
			Inputs = {
				StateVersion = Input { Value = 12, },
				TextEdited = Input { Value = 1, },
				StyledText = Input { Value = "NEON NIGHTS", },
				Font = Input { Value = "Archivo Black", },
				Style = Input { Value = "Regular", },
				Size = Input { Value = 1.6, },
				ShadingProxyRedRed = Input { Value = 0.9137, },
				ShadingElement1Red = Input { Value = 0.9137, },
				InopacityEnable = Input { Value = 1, },
				InopacityAnimationEnd = Input { Value = 20, },
				InopacityStagger = Input { Value = 100, },
				InopacityCurvePreset = Input { Value = 2, },
				InopacityCurvePresetID = Input { Value = "out_quad", },
				InblurEnable = Input { Value = 1, },
				InblurAnimationEnd = Input { Value = 25, },
				InblurStagger = Input { Value = 28.6, },
				InblurStartValue = Input { Value = 0.2, },
				InblurCurvePreset = Input { Value = 5, },
				InblurCurvePresetID = Input { Value = "out_cubic", },
				InsizeEnable = Input { Value = 1, },
				InsizeAnimationEnd = Input { Value = 27, },
				InsizeStagger = Input { Value = 22.2, },
				InsizeStartValue = Input { Value = 1.35, },
				InsizeCurvePreset = Input { Value = 5, },
				InsizeCurvePresetID = Input { Value = "out_cubic", },
				OutopacityEnable = Input { Value = 1, },
				OutopacityAnimationEnd = Input { Value = 114, },
				OutopacityStagger = Input { Value = 20, },
				OutopacityCurvePreset = Input { Value = 1, },
				OutopacityCurvePresetID = Input { Value = "in_quad", },
				OutblurEnable = Input { Value = 1, },
				OutblurAnimationEnd = Input { Value = 114, },
				OutblurStagger = Input { Value = 20, },
				OutblurEndValue = Input { Value = 0.2, },
				OutblurCurvePreset = Input { Value = 1, },
				OutblurCurvePresetID = Input { Value = "in_quad", },
				FxGlowOn = Input { Value = 1, },
				FxGlowAmount = Input { Value = 1.2, },
				FxGlowTextColors = Input { Value = 0, },
				FxGlowColorRed = Input { Value = 0, },
				FxGlowColorGreen = Input { Value = 0.898, },
				FxGlowColorBlue = Input { Value = 1, },
			},
			ViewInfo = OperatorInfo { Pos = { 0, 0 } },
		},
	},
	ActiveTool = "TextizoFX1"
}
```
<!-- /example3 -->

## 12. The ready looks

TextizoFX's Look menu has these looks (the kit's `presets/` folder holds each as a complete node):

<!-- looks -->
| Look | Look menu | Sample text | What it is |
|---|---|---|---|
| Textizo-01A | 1 | "I LOVE NICARAGUA" | Arial Black Regular; in: opacity by letters (out_quad), blur by letters (out_cubic), position by letters (out_back), size by letters (out_elastic), tracking by letters (out_back), rotation by letters (out_back); out: opacity by letters (in_cubic), blur by letters (in_quad), position by letters (in_back), size by letters (in_back), rotation by letters (in_back); shading: outline, normal; motion blur |
| Textizo-01B | 2 | "FIESTA TIME!" | Arial Black Regular; in: opacity by letters (out_quad), blur by letters (out_cubic), position by letters (out_back), size by letters (out_elastic), tracking by letters (out_back), rotation by letters (out_back); out: opacity by letters (in_cubic), blur by letters (in_quad), position by letters (in_back), size by letters (in_back), rotation by letters (in_back); shading: outline, normal; motion blur |
| Textizo-01C | 3 | "LET'S GO!" | Arial Black Regular; in: opacity by letters (out_quad), blur by letters (out_cubic), position by letters (out_back), size by letters (out_elastic), tracking by letters (out_back), rotation by letters (out_back); out: opacity by letters (in_cubic), blur by letters (in_quad), position by letters (in_back), size by letters (in_back), rotation by letters (in_back); shading: outline, normal; motion blur |
| Textizo-02A | 4 | "NEON NIGHTS" | Arial Black Regular; in: opacity by letters (out_quad), blur by letters (out_cubic), size by letters (out_cubic); out: opacity by letters (in_quad), blur by letters (in_quad); shading: normal, outline |
| Textizo-03A | 5 | "BIG NEWS TODAY" | Impact Regular; in: opacity by words (out_quad), blur by words (out_cubic), size by words (out_back); out: opacity by words (in_quad), blur by words (in_quad), size by words (in_cubic); shading: outline, normal; motion blur |
| Textizo-04A | 6 | "SYSTEM ERROR" | Arial Black Regular; in: opacity by letters (out_quad), blur by letters (out_cubic), explosion by letters (out_expo); out: opacity by letters (in_quad), blur by letters (in_quad), explosion by letters (in_expo); shading: normal, normal |
| Textizo-05A | 7 | "SPIN IT!" | Arial Black Regular; in: opacity by letters (out_quad), size by letters (out_back), rotation by letters (out_back); out: size by letters (in_back), rotation by letters (in_back); shading: outline, normal; motion blur |
| Textizo-06A | 8 | "SALE" | Arial Black Regular; in: opacity by lines (out_quad), blur by lines (out_cubic), size by lines (out_back); out: opacity by lines (in_quad), size by lines (in_back); shading: border_fill, border_fill; motion blur |
| Textizo-07A | 9 | "Happy Anniversary" | Georgia Regular; in: opacity by letters (in_out_sine), blur by letters (out_cubic), position by letters (out_cubic); out: opacity by letters (in_out_sine), blur by letters (in_quad), position by letters (in_quad); shading: normal |
| Textizo-08A | 10 | "PARTY TIME" | Arial Black Regular; in: opacity by letters (out_quad), position by letters (out_elastic), size by letters (out_back); out: opacity by letters (in_cubic), position by letters (in_back); shading: outline, normal; gradient fill; motion blur |
| Textizo-09A | 11 | "Loading story..." | Courier New Bold; in: opacity by letters (linear), blur by letters (out_quad); out: opacity by letters (in_quad); shading: normal |
| Textizo-10A | 12 | "YOU GOT THIS" | Arial Black Regular; in: opacity by words (out_quad), position by words (out_bounce), rotation by words (out_elastic); out: opacity by words (in_cubic), position by words (in_back); shading: outline, normal; motion blur |
| Apple Drop | 13 | "Textizo" | Arial Bold; in: opacity by letters (in_out_sine), blur by letters (out_cubic), position by letters (out_quart); out: opacity by letters (in_out_sine), blur by letters (in_quad), position by letters (in_quart) |
| Apple Line Rise | 14 | "Simply / beautiful." | Arial Bold; in: opacity by lines (in_out_sine), blur by lines (out_cubic), position by lines (out_quart); out: opacity by lines (in_out_sine), blur by lines (in_quad), position by lines (in_quart) |
| Apple Reveal | 15 | "Textizo" | Arial Bold; in: opacity by letters (in_out_sine), blur by letters (out_cubic), size by letters (out_quart); out: opacity by letters (in_out_sine), blur by letters (in_quad), size by letters (in_quad) |
| Apple Rise | 16 | "Textizo" | Arial Bold; in: opacity by letters (in_out_sine), blur by letters (out_cubic), position by letters (out_quart); out: opacity by letters (in_out_sine), blur by letters (in_quad), position by letters (in_quart) |
| Apple Word Lift | 17 | "Designed to move" | Arial Bold; in: opacity by words (in_out_sine), blur by words (out_cubic), position by words (out_quart), size by words (out_quart); out: opacity by words (in_out_sine), blur by words (in_quad), position by words (in_quart) |
| Bounce Drop | 18 | "BOUNCE!" | Arial Black Regular; in: opacity by letters (out_quad), blur by letters (out_cubic), position by letters (out_bounce), rotation by letters (out_elastic); out: opacity by letters (in_cubic), blur by letters (in_quad), position by letters (in_back), rotation by letters (in_back); shading: outline, normal; motion blur |
| Jelly Wave | 19 | "JELLY!" | Arial Black Regular; in: opacity by letters (out_quad), position by letters (out_elastic), size by letters (out_elastic), rotation by letters (out_elastic); out: opacity by letters (in_cubic), position by letters (in_quad), rotation by letters (in_quad); shading: outline, normal; motion blur |
| Party Pop | 20 | "TEXTIZO!" | Arial Black Regular; in: opacity by letters (out_quad), blur by letters (out_cubic), position by letters (out_back), size by letters (out_elastic), tracking by letters (out_back), rotation by letters (out_back); out: opacity by letters (in_cubic), blur by letters (in_quad), position by letters (in_back), size by letters (in_back), rotation by letters (in_back); shading: outline, normal; motion blur |
| Scatter Spin | 21 | "WHOOSH!" | Arial Black Regular; in: opacity by letters (out_quad), blur by letters (out_cubic), size by letters (out_back), rotation by letters (out_cubic), explosion by letters (out_back); out: opacity by letters (in_quad), blur by letters (in_quad), rotation by letters (in_cubic), explosion by letters (in_cubic); shading: outline, normal; motion blur |
| Zoom Slam | 22 | "BOOM!" | Arial Black Regular; in: opacity by letters (out_quad), blur by letters (out_cubic), size by letters (out_back), rotation by letters (out_back); out: opacity by letters (in_quad), blur by letters (in_quad), size by letters (in_cubic); shading: outline, normal; motion blur |
| Textizo-11A | 23 | "NEW VIDEO" | Poppins Bold; in: opacity by words (out_quad), blur by words (out_cubic), position by words (out_back), size by lines (out_back); out: opacity by lines (in_quad), size by lines (in_back); shading: border_fill, border_fill; motion blur |
| Textizo-12A | 24 | "BREAKING NEWS" | Anton Regular; in: opacity by letters (out_quad), blur by letters (out_cubic), position by letters (out_back), size by lines (out_back); out: opacity by letters (in_quad), blur by letters (in_quad), position by letters (in_back), size by lines (in_back); shading: border_fill, border_fill; motion blur |
| Textizo-13A | 25 | "BOOM!" | Bangers Regular; in: opacity by letters (out_quad), size by letters (out_elastic), rotation by letters (out_back); out: size by letters (in_back), rotation by letters (in_back); shading: outline, normal; motion blur |
| Textizo-14A | 26 | "LEGENDARY" | Montserrat ExtraBold; in: opacity by letters (out_quad), blur by letters (out_cubic), size by letters (out_cubic); out: opacity by letters (in_quad), blur by letters (in_quad), size by letters (in_cubic); shading: outline, normal; gradient fill |
| Textizo-15A | 27 | "Summer Vibes" | Fredoka Bold; in: opacity by letters (out_quad), position by letters (out_back), size by letters (out_back); out: opacity by letters (in_cubic), position by letters (in_back); shading: normal; gradient fill; motion blur |
| Textizo-16A | 28 | "RETRO" | Archivo Black Regular; in: opacity by letters (out_quad), position by letters (out_back); out: opacity by letters (in_cubic), position by letters (in_back); shading: normal, normal, normal; motion blur |
| Textizo-17A | 29 | "hello there!" | Permanent Marker Regular; in: opacity by letters (linear), size by letters (out_back); out: opacity by letters (in_quad), size by letters (in_quad); shading: normal |
| Textizo-18A | 30 | "Jane Cooper  \|  Director" | Inter SemiBold; in: opacity by lines (out_quad), blur by words (out_cubic), size by lines (out_cubic); out: opacity by lines (in_quad), blur by lines (in_quad); shading: border_fill |
| Textizo-19A | 31 | "$1,000,000" | Kanit Black; in: opacity by letters (out_quad), blur by letters (out_cubic), size by letters (out_cubic); out: opacity by letters (in_quad), size by letters (in_back); shading: outline, normal; gradient fill; motion blur |
| Textizo-20A | 32 | "COMING SOON" | Bebas Neue Regular; in: opacity by lines (out_quad), blur by lines (out_cubic), tracking by letters (out_cubic); out: opacity by lines (in_quad), blur by lines (in_quad); shading: normal |
<!-- /looks -->

## 13. Every control

Every input a look can set, by page, as it is written in a TextizoFX node. "(element storage)" marks the Shading elements' own inputs (written by looks; the Shading page shows one element at a time through its `ShadingProxy...` controls, section 7). Menus list their numbers.

<!-- controls -->
### Text page

| Node input | Label | Section | Default | Range or menu (number: ID) |
|---|---|---|---|---|
| `StateVersion` | State Version |  | 12 |  |
| `TextEdited` | Text Edited |  | 0 |  |
| `InEnable` | Enable |  | 1 |  |
| `StyledText` | Text | Text | "" |  |
| `Font` | Font |  | "Arial" |  |
| `Style` | Style |  | "Regular" |  |
| `Center` | Center | Font and Layout | { 0.5, 0.5 } |  |
| `Size` | Size | Font and Layout | 1 | 0.0001 to 50.0 |
| `Tracking` | Tracking | Font and Layout | 0 |  |
| `LineSpacing` | Line Spacing | Font and Layout | 1 |  |
| `Alignment` | Alignment | Font and Layout | 1 | 0 Left, 1 Center, 2 Right |
| `VerticalAnchor` | Vertical Anchor |  | 1 | 0 Top, 1 Center, 2 Baseline, 3 Bottom |
| `RotationX` | Rotation X | Font and Layout | 0 |  |
| `RotationY` | Rotation Y | Font and Layout | 0 |  |
| `Rotation` | Rotation Z | Font and Layout | 0 |  |
| `RedRed` | Color (Red) | Font and Layout | 1 |  |
| `RedGreen` | Color (Green) | Font and Layout | 1 |  |
| `RedBlue` | Color (Blue) | Font and Layout | 1 |  |
| `RedAlpha` | Color (Alpha) | Font and Layout | 1 |  |
| `FitToFrame` | Fit to Frame | Font and Layout | 1 |  |

### Shading page

| Node input | Label | Section | Default | Range or menu (number: ID) |
|---|---|---|---|---|
| `ShadingActiveElement` | Element |  | 0 (element_1) | 0 element_1, 1 element_2, 2 element_3, 3 element_4, 4 element_5, 5 element_6, 6 element_7, 7 element_8 |
| `ShadingProxyEnable` | Enabled |  | 1 |  |
| `ShadingProxyLetters` | Letters |  | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `ShadingProxyAppearance` | Appearance |  | 0 | 0 Normal, 1 Outline, 2 Border Fill, 3 Border Stroke |
| `ShadingProxyOpacity` | Opacity |  | 1 |  |
| `ShadingProxyThickness` | Thickness |  | 0.02 |  |
| `ShadingProxyJoinStyle` | Join Style |  | 1 | 0 Sharp, 1 Round, 2 Bevel |
| `ShadingProxyLineStyle` | Line Style |  | 0 | 0 Solid, 1 Dash, 2 Dot, 3 Dash Dot, 4 Dash Dot Dot |
| `ShadingProxyOffset` | Offset |  | { 0.0, 0.0 } |  |
| `ShadingProxySoftnessX` | Softness X |  | 0 |  |
| `ShadingProxySoftnessY` | Softness Y |  | 0 |  |
| `ShadingProxyBorderLevel` | Border |  | 0 | 0 Letter, 1 Word, 2 Line |
| `ShadingProxyBorderExtendX` | Extend X |  | 0 |  |
| `ShadingProxyBorderExtendY` | Extend Y |  | 0 |  |
| `ShadingProxyBorderRound` | Round |  | 0 |  |
| `ShadingProxyColorMode` | Fill |  | 0 | 0 Solid, 1 Gradient |
| `ShadingProxyGradient` | Gradient |  | None |  |
| `ShadingProxyGradientAngle` | Angle |  | 0 |  |
| `ShadingProxyMappingSize` | Scale |  | 1.5 |  |
| `ShadingProxyMappingAspect` | Aspect |  | 1 |  |
| `ShadingProxyMappingLevel` | Span |  | 0 | 0 Letter, 1 Word, 2 Line, 3 Text |
| `ShadingProxyGradientStart` | Gradient Start |  | { 0.25, 0.5 } |  |
| `ShadingProxyGradientEnd` | Gradient End |  | { 0.75, 0.5 } |  |
| `ShadingProxyRedRed` | Color (Red) |  | 1 |  |
| `ShadingProxyRedGreen` | Color (Green) |  | 1 |  |
| `ShadingProxyRedBlue` | Color (Blue) |  | 1 |  |
| `ShadingProxyRedAlpha` | Color (Alpha) |  | 1 |  |
| `ShadingProxyEndRedRed` | Color 2 (Red) |  | 1 |  |
| `ShadingProxyEndRedGreen` | Color 2 (Green) |  | 1 |  |
| `ShadingProxyEndRedBlue` | Color 2 (Blue) |  | 1 |  |
| `ShadingProxyEndRedAlpha` | Color 2 (Alpha) |  | 1 |  |
| `ShadingElement1Enable` | Enabled (element storage) |  | 1 |  |
| `ShadingElement1Appearance` | Appearance (element storage) |  | 0 | 0 Normal, 1 Outline, 2 Border Fill, 3 Border Stroke |
| `ShadingElement1Opacity` | Opacity (element storage) |  | 1 |  |
| `ShadingElement1Thickness` | Thickness (element storage) |  | 0.02 |  |
| `ShadingElement1JoinStyle` | Join Style (element storage) |  | 1 | 0 Sharp, 1 Round, 2 Bevel |
| `ShadingElement1LineStyle` | Line Style (element storage) |  | 0 | 0 Solid, 1 Dash, 2 Dot, 3 Dash Dot, 4 Dash Dot Dot |
| `ShadingElement1Offset` | Offset (element storage) |  | { 0.0, 0.0 } |  |
| `ShadingElement1SoftnessX` | Softness X (element storage) |  | 0 |  |
| `ShadingElement1SoftnessY` | Softness Y (element storage) |  | 0 |  |
| `ShadingElement1BorderLevel` | Border Level (element storage) |  | 0 | 0 Letter, 1 Word, 2 Line |
| `ShadingElement1BorderExtendX` | Extend Horizontal (element storage) |  | 0 |  |
| `ShadingElement1BorderExtendY` | Extend Vertical (element storage) |  | 0 |  |
| `ShadingElement1BorderRound` | Round (element storage) |  | 0 |  |
| `ShadingElement1ColorMode` | Color Mode (element storage) |  | 0 | 0 Solid, 1 Gradient |
| `ShadingElement1Gradient` | Shading Gradient (element storage) |  | None |  |
| `ShadingElement1GradientSeedPending` | Gradient Seed Pending (element storage) |  | 1 |  |
| `ShadingElement1GradientAngle` | Mapping Angle (element storage) |  | 0 |  |
| `ShadingElement1MappingSize` | Mapping Size (element storage) |  | 1.5 |  |
| `ShadingElement1MappingAspect` | Mapping Aspect (element storage) |  | 1 |  |
| `ShadingElement1MappingLevel` | Mapping Level (element storage) |  | 0 | 0 Character, 1 Word, 2 Line, 3 Text |
| `ShadingElement1GradientStart` | Gradient Start (element storage) |  | { 0.25, 0.5 } |  |
| `ShadingElement1GradientEnd` | Gradient End (element storage) |  | { 0.75, 0.5 } |  |
| `ShadingElement1Red` | Color (element storage) |  | 1 |  |
| `ShadingElement1Green` | Green (element storage) |  | 1 |  |
| `ShadingElement1Blue` | Blue (element storage) |  | 1 |  |
| `ShadingElement1Alpha` | Alpha (element storage) |  | 1 |  |
| `ShadingElement1EndRed` | Color 2 (element storage) |  | 1 |  |
| `ShadingElement1EndGreen` | Green 2 (element storage) |  | 1 |  |
| `ShadingElement1EndBlue` | Blue 2 (element storage) |  | 1 |  |
| `ShadingElement1EndAlpha` | Alpha 2 (element storage) |  | 1 |  |
| `ShadingElement2Enable` | Enabled (element storage) |  | 0 |  |
| `ShadingElement2Appearance` | Appearance (element storage) |  | 1 | 0 Normal, 1 Outline, 2 Border Fill, 3 Border Stroke |
| `ShadingElement2Opacity` | Opacity (element storage) |  | 1 |  |
| `ShadingElement2Thickness` | Thickness (element storage) |  | 0.004 |  |
| `ShadingElement2JoinStyle` | Join Style (element storage) |  | 1 | 0 Sharp, 1 Round, 2 Bevel |
| `ShadingElement2LineStyle` | Line Style (element storage) |  | 0 | 0 Solid, 1 Dash, 2 Dot, 3 Dash Dot, 4 Dash Dot Dot |
| `ShadingElement2Offset` | Offset (element storage) |  | { 0.0, 0.0 } |  |
| `ShadingElement2SoftnessX` | Softness X (element storage) |  | 0 |  |
| `ShadingElement2SoftnessY` | Softness Y (element storage) |  | 0 |  |
| `ShadingElement2BorderLevel` | Border Level (element storage) |  | 0 | 0 Letter, 1 Word, 2 Line |
| `ShadingElement2BorderExtendX` | Extend Horizontal (element storage) |  | 0 |  |
| `ShadingElement2BorderExtendY` | Extend Vertical (element storage) |  | 0 |  |
| `ShadingElement2BorderRound` | Round (element storage) |  | 0 |  |
| `ShadingElement2ColorMode` | Color Mode (element storage) |  | 0 | 0 Solid, 1 Gradient |
| `ShadingElement2Gradient` | Shading Gradient (element storage) |  | None |  |
| `ShadingElement2GradientSeedPending` | Gradient Seed Pending (element storage) |  | 1 |  |
| `ShadingElement2GradientAngle` | Mapping Angle (element storage) |  | 0 |  |
| `ShadingElement2MappingSize` | Mapping Size (element storage) |  | 1.5 |  |
| `ShadingElement2MappingAspect` | Mapping Aspect (element storage) |  | 1 |  |
| `ShadingElement2MappingLevel` | Mapping Level (element storage) |  | 0 | 0 Character, 1 Word, 2 Line, 3 Text |
| `ShadingElement2GradientStart` | Gradient Start (element storage) |  | { 0.25, 0.5 } |  |
| `ShadingElement2GradientEnd` | Gradient End (element storage) |  | { 0.75, 0.5 } |  |
| `ShadingElement2Red` | Color (element storage) |  | 1 |  |
| `ShadingElement2Green` | Green (element storage) |  | 0 |  |
| `ShadingElement2Blue` | Blue (element storage) |  | 0 |  |
| `ShadingElement2Alpha` | Alpha (element storage) |  | 1 |  |
| `ShadingElement2EndRed` | Color 2 (element storage) |  | 1 |  |
| `ShadingElement2EndGreen` | Green 2 (element storage) |  | 1 |  |
| `ShadingElement2EndBlue` | Blue 2 (element storage) |  | 1 |  |
| `ShadingElement2EndAlpha` | Alpha 2 (element storage) |  | 1 |  |
| `ShadingElement3Enable` | Enabled (element storage) |  | 0 |  |
| `ShadingElement3Appearance` | Appearance (element storage) |  | 0 | 0 Normal, 1 Outline, 2 Border Fill, 3 Border Stroke |
| `ShadingElement3Opacity` | Opacity (element storage) |  | 1 |  |
| `ShadingElement3Thickness` | Thickness (element storage) |  | 0.02 |  |
| `ShadingElement3JoinStyle` | Join Style (element storage) |  | 1 | 0 Sharp, 1 Round, 2 Bevel |
| `ShadingElement3LineStyle` | Line Style (element storage) |  | 0 | 0 Solid, 1 Dash, 2 Dot, 3 Dash Dot, 4 Dash Dot Dot |
| `ShadingElement3Offset` | Offset (element storage) |  | { 0.0, 0.0 } |  |
| `ShadingElement3SoftnessX` | Softness X (element storage) |  | 0.01 |  |
| `ShadingElement3SoftnessY` | Softness Y (element storage) |  | 0.01 |  |
| `ShadingElement3BorderLevel` | Border Level (element storage) |  | 0 | 0 Letter, 1 Word, 2 Line |
| `ShadingElement3BorderExtendX` | Extend Horizontal (element storage) |  | 0 |  |
| `ShadingElement3BorderExtendY` | Extend Vertical (element storage) |  | 0 |  |
| `ShadingElement3BorderRound` | Round (element storage) |  | 0 |  |
| `ShadingElement3ColorMode` | Color Mode (element storage) |  | 0 | 0 Solid, 1 Gradient |
| `ShadingElement3Gradient` | Shading Gradient (element storage) |  | None |  |
| `ShadingElement3GradientSeedPending` | Gradient Seed Pending (element storage) |  | 1 |  |
| `ShadingElement3GradientAngle` | Mapping Angle (element storage) |  | 0 |  |
| `ShadingElement3MappingSize` | Mapping Size (element storage) |  | 1.5 |  |
| `ShadingElement3MappingAspect` | Mapping Aspect (element storage) |  | 1 |  |
| `ShadingElement3MappingLevel` | Mapping Level (element storage) |  | 0 | 0 Character, 1 Word, 2 Line, 3 Text |
| `ShadingElement3GradientStart` | Gradient Start (element storage) |  | { 0.25, 0.5 } |  |
| `ShadingElement3GradientEnd` | Gradient End (element storage) |  | { 0.75, 0.5 } |  |
| `ShadingElement3Red` | Color (element storage) |  | 0 |  |
| `ShadingElement3Green` | Green (element storage) |  | 0 |  |
| `ShadingElement3Blue` | Blue (element storage) |  | 0 |  |
| `ShadingElement3Alpha` | Alpha (element storage) |  | 1 |  |
| `ShadingElement3EndRed` | Color 2 (element storage) |  | 1 |  |
| `ShadingElement3EndGreen` | Green 2 (element storage) |  | 1 |  |
| `ShadingElement3EndBlue` | Blue 2 (element storage) |  | 1 |  |
| `ShadingElement3EndAlpha` | Alpha 2 (element storage) |  | 1 |  |
| `ShadingElement4Enable` | Enabled (element storage) |  | 0 |  |
| `ShadingElement4Appearance` | Appearance (element storage) |  | 2 | 0 Normal, 1 Outline, 2 Border Fill, 3 Border Stroke |
| `ShadingElement4Opacity` | Opacity (element storage) |  | 1 |  |
| `ShadingElement4Thickness` | Thickness (element storage) |  | 0.02 |  |
| `ShadingElement4JoinStyle` | Join Style (element storage) |  | 1 | 0 Sharp, 1 Round, 2 Bevel |
| `ShadingElement4LineStyle` | Line Style (element storage) |  | 0 | 0 Solid, 1 Dash, 2 Dot, 3 Dash Dot, 4 Dash Dot Dot |
| `ShadingElement4Offset` | Offset (element storage) |  | { 0.0, 0.0 } |  |
| `ShadingElement4SoftnessX` | Softness X (element storage) |  | 0 |  |
| `ShadingElement4SoftnessY` | Softness Y (element storage) |  | 0 |  |
| `ShadingElement4BorderLevel` | Border Level (element storage) |  | 0 | 0 Letter, 1 Word, 2 Line |
| `ShadingElement4BorderExtendX` | Extend Horizontal (element storage) |  | 0.02 |  |
| `ShadingElement4BorderExtendY` | Extend Vertical (element storage) |  | 0.02 |  |
| `ShadingElement4BorderRound` | Round (element storage) |  | 0 |  |
| `ShadingElement4ColorMode` | Color Mode (element storage) |  | 0 | 0 Solid, 1 Gradient |
| `ShadingElement4Gradient` | Shading Gradient (element storage) |  | None |  |
| `ShadingElement4GradientSeedPending` | Gradient Seed Pending (element storage) |  | 1 |  |
| `ShadingElement4GradientAngle` | Mapping Angle (element storage) |  | 0 |  |
| `ShadingElement4MappingSize` | Mapping Size (element storage) |  | 1.5 |  |
| `ShadingElement4MappingAspect` | Mapping Aspect (element storage) |  | 1 |  |
| `ShadingElement4MappingLevel` | Mapping Level (element storage) |  | 0 | 0 Character, 1 Word, 2 Line, 3 Text |
| `ShadingElement4GradientStart` | Gradient Start (element storage) |  | { 0.25, 0.5 } |  |
| `ShadingElement4GradientEnd` | Gradient End (element storage) |  | { 0.75, 0.5 } |  |
| `ShadingElement4Red` | Color (element storage) |  | 0 |  |
| `ShadingElement4Green` | Green (element storage) |  | 0 |  |
| `ShadingElement4Blue` | Blue (element storage) |  | 1 |  |
| `ShadingElement4Alpha` | Alpha (element storage) |  | 1 |  |
| `ShadingElement4EndRed` | Color 2 (element storage) |  | 1 |  |
| `ShadingElement4EndGreen` | Green 2 (element storage) |  | 1 |  |
| `ShadingElement4EndBlue` | Blue 2 (element storage) |  | 1 |  |
| `ShadingElement4EndAlpha` | Alpha 2 (element storage) |  | 1 |  |
| `ShadingElement5Enable` | Enabled (element storage) |  | 0 |  |
| `ShadingElement5Appearance` | Appearance (element storage) |  | 0 | 0 Normal, 1 Outline, 2 Border Fill, 3 Border Stroke |
| `ShadingElement5Opacity` | Opacity (element storage) |  | 1 |  |
| `ShadingElement5Thickness` | Thickness (element storage) |  | 0.02 |  |
| `ShadingElement5JoinStyle` | Join Style (element storage) |  | 1 | 0 Sharp, 1 Round, 2 Bevel |
| `ShadingElement5LineStyle` | Line Style (element storage) |  | 0 | 0 Solid, 1 Dash, 2 Dot, 3 Dash Dot, 4 Dash Dot Dot |
| `ShadingElement5Offset` | Offset (element storage) |  | { 0.0, 0.0 } |  |
| `ShadingElement5SoftnessX` | Softness X (element storage) |  | 0 |  |
| `ShadingElement5SoftnessY` | Softness Y (element storage) |  | 0 |  |
| `ShadingElement5BorderLevel` | Border Level (element storage) |  | 0 | 0 Letter, 1 Word, 2 Line |
| `ShadingElement5BorderExtendX` | Extend Horizontal (element storage) |  | 0 |  |
| `ShadingElement5BorderExtendY` | Extend Vertical (element storage) |  | 0 |  |
| `ShadingElement5BorderRound` | Round (element storage) |  | 0 |  |
| `ShadingElement5ColorMode` | Color Mode (element storage) |  | 0 | 0 Solid, 1 Gradient |
| `ShadingElement5Gradient` | Shading Gradient (element storage) |  | None |  |
| `ShadingElement5GradientSeedPending` | Gradient Seed Pending (element storage) |  | 1 |  |
| `ShadingElement5GradientAngle` | Mapping Angle (element storage) |  | 0 |  |
| `ShadingElement5MappingSize` | Mapping Size (element storage) |  | 1.5 |  |
| `ShadingElement5MappingAspect` | Mapping Aspect (element storage) |  | 1 |  |
| `ShadingElement5MappingLevel` | Mapping Level (element storage) |  | 0 | 0 Character, 1 Word, 2 Line, 3 Text |
| `ShadingElement5GradientStart` | Gradient Start (element storage) |  | { 0.25, 0.5 } |  |
| `ShadingElement5GradientEnd` | Gradient End (element storage) |  | { 0.75, 0.5 } |  |
| `ShadingElement5Red` | Color (element storage) |  | 1 |  |
| `ShadingElement5Green` | Green (element storage) |  | 1 |  |
| `ShadingElement5Blue` | Blue (element storage) |  | 1 |  |
| `ShadingElement5Alpha` | Alpha (element storage) |  | 1 |  |
| `ShadingElement5EndRed` | Color 2 (element storage) |  | 1 |  |
| `ShadingElement5EndGreen` | Green 2 (element storage) |  | 1 |  |
| `ShadingElement5EndBlue` | Blue 2 (element storage) |  | 1 |  |
| `ShadingElement5EndAlpha` | Alpha 2 (element storage) |  | 1 |  |
| `ShadingElement6Enable` | Enabled (element storage) |  | 0 |  |
| `ShadingElement6Appearance` | Appearance (element storage) |  | 0 | 0 Normal, 1 Outline, 2 Border Fill, 3 Border Stroke |
| `ShadingElement6Opacity` | Opacity (element storage) |  | 1 |  |
| `ShadingElement6Thickness` | Thickness (element storage) |  | 0.02 |  |
| `ShadingElement6JoinStyle` | Join Style (element storage) |  | 1 | 0 Sharp, 1 Round, 2 Bevel |
| `ShadingElement6LineStyle` | Line Style (element storage) |  | 0 | 0 Solid, 1 Dash, 2 Dot, 3 Dash Dot, 4 Dash Dot Dot |
| `ShadingElement6Offset` | Offset (element storage) |  | { 0.0, 0.0 } |  |
| `ShadingElement6SoftnessX` | Softness X (element storage) |  | 0 |  |
| `ShadingElement6SoftnessY` | Softness Y (element storage) |  | 0 |  |
| `ShadingElement6BorderLevel` | Border Level (element storage) |  | 0 | 0 Letter, 1 Word, 2 Line |
| `ShadingElement6BorderExtendX` | Extend Horizontal (element storage) |  | 0 |  |
| `ShadingElement6BorderExtendY` | Extend Vertical (element storage) |  | 0 |  |
| `ShadingElement6BorderRound` | Round (element storage) |  | 0 |  |
| `ShadingElement6ColorMode` | Color Mode (element storage) |  | 0 | 0 Solid, 1 Gradient |
| `ShadingElement6Gradient` | Shading Gradient (element storage) |  | None |  |
| `ShadingElement6GradientSeedPending` | Gradient Seed Pending (element storage) |  | 1 |  |
| `ShadingElement6GradientAngle` | Mapping Angle (element storage) |  | 0 |  |
| `ShadingElement6MappingSize` | Mapping Size (element storage) |  | 1.5 |  |
| `ShadingElement6MappingAspect` | Mapping Aspect (element storage) |  | 1 |  |
| `ShadingElement6MappingLevel` | Mapping Level (element storage) |  | 0 | 0 Character, 1 Word, 2 Line, 3 Text |
| `ShadingElement6GradientStart` | Gradient Start (element storage) |  | { 0.25, 0.5 } |  |
| `ShadingElement6GradientEnd` | Gradient End (element storage) |  | { 0.75, 0.5 } |  |
| `ShadingElement6Red` | Color (element storage) |  | 1 |  |
| `ShadingElement6Green` | Green (element storage) |  | 1 |  |
| `ShadingElement6Blue` | Blue (element storage) |  | 1 |  |
| `ShadingElement6Alpha` | Alpha (element storage) |  | 1 |  |
| `ShadingElement6EndRed` | Color 2 (element storage) |  | 1 |  |
| `ShadingElement6EndGreen` | Green 2 (element storage) |  | 1 |  |
| `ShadingElement6EndBlue` | Blue 2 (element storage) |  | 1 |  |
| `ShadingElement6EndAlpha` | Alpha 2 (element storage) |  | 1 |  |
| `ShadingElement7Enable` | Enabled (element storage) |  | 0 |  |
| `ShadingElement7Appearance` | Appearance (element storage) |  | 0 | 0 Normal, 1 Outline, 2 Border Fill, 3 Border Stroke |
| `ShadingElement7Opacity` | Opacity (element storage) |  | 1 |  |
| `ShadingElement7Thickness` | Thickness (element storage) |  | 0.02 |  |
| `ShadingElement7JoinStyle` | Join Style (element storage) |  | 1 | 0 Sharp, 1 Round, 2 Bevel |
| `ShadingElement7LineStyle` | Line Style (element storage) |  | 0 | 0 Solid, 1 Dash, 2 Dot, 3 Dash Dot, 4 Dash Dot Dot |
| `ShadingElement7Offset` | Offset (element storage) |  | { 0.0, 0.0 } |  |
| `ShadingElement7SoftnessX` | Softness X (element storage) |  | 0 |  |
| `ShadingElement7SoftnessY` | Softness Y (element storage) |  | 0 |  |
| `ShadingElement7BorderLevel` | Border Level (element storage) |  | 0 | 0 Letter, 1 Word, 2 Line |
| `ShadingElement7BorderExtendX` | Extend Horizontal (element storage) |  | 0 |  |
| `ShadingElement7BorderExtendY` | Extend Vertical (element storage) |  | 0 |  |
| `ShadingElement7BorderRound` | Round (element storage) |  | 0 |  |
| `ShadingElement7ColorMode` | Color Mode (element storage) |  | 0 | 0 Solid, 1 Gradient |
| `ShadingElement7Gradient` | Shading Gradient (element storage) |  | None |  |
| `ShadingElement7GradientSeedPending` | Gradient Seed Pending (element storage) |  | 1 |  |
| `ShadingElement7GradientAngle` | Mapping Angle (element storage) |  | 0 |  |
| `ShadingElement7MappingSize` | Mapping Size (element storage) |  | 1.5 |  |
| `ShadingElement7MappingAspect` | Mapping Aspect (element storage) |  | 1 |  |
| `ShadingElement7MappingLevel` | Mapping Level (element storage) |  | 0 | 0 Character, 1 Word, 2 Line, 3 Text |
| `ShadingElement7GradientStart` | Gradient Start (element storage) |  | { 0.25, 0.5 } |  |
| `ShadingElement7GradientEnd` | Gradient End (element storage) |  | { 0.75, 0.5 } |  |
| `ShadingElement7Red` | Color (element storage) |  | 1 |  |
| `ShadingElement7Green` | Green (element storage) |  | 1 |  |
| `ShadingElement7Blue` | Blue (element storage) |  | 1 |  |
| `ShadingElement7Alpha` | Alpha (element storage) |  | 1 |  |
| `ShadingElement7EndRed` | Color 2 (element storage) |  | 1 |  |
| `ShadingElement7EndGreen` | Green 2 (element storage) |  | 1 |  |
| `ShadingElement7EndBlue` | Blue 2 (element storage) |  | 1 |  |
| `ShadingElement7EndAlpha` | Alpha 2 (element storage) |  | 1 |  |
| `ShadingElement8Enable` | Enabled (element storage) |  | 0 |  |
| `ShadingElement8Appearance` | Appearance (element storage) |  | 0 | 0 Normal, 1 Outline, 2 Border Fill, 3 Border Stroke |
| `ShadingElement8Opacity` | Opacity (element storage) |  | 1 |  |
| `ShadingElement8Thickness` | Thickness (element storage) |  | 0.02 |  |
| `ShadingElement8JoinStyle` | Join Style (element storage) |  | 1 | 0 Sharp, 1 Round, 2 Bevel |
| `ShadingElement8LineStyle` | Line Style (element storage) |  | 0 | 0 Solid, 1 Dash, 2 Dot, 3 Dash Dot, 4 Dash Dot Dot |
| `ShadingElement8Offset` | Offset (element storage) |  | { 0.0, 0.0 } |  |
| `ShadingElement8SoftnessX` | Softness X (element storage) |  | 0 |  |
| `ShadingElement8SoftnessY` | Softness Y (element storage) |  | 0 |  |
| `ShadingElement8BorderLevel` | Border Level (element storage) |  | 0 | 0 Letter, 1 Word, 2 Line |
| `ShadingElement8BorderExtendX` | Extend Horizontal (element storage) |  | 0 |  |
| `ShadingElement8BorderExtendY` | Extend Vertical (element storage) |  | 0 |  |
| `ShadingElement8BorderRound` | Round (element storage) |  | 0 |  |
| `ShadingElement8ColorMode` | Color Mode (element storage) |  | 0 | 0 Solid, 1 Gradient |
| `ShadingElement8Gradient` | Shading Gradient (element storage) |  | None |  |
| `ShadingElement8GradientSeedPending` | Gradient Seed Pending (element storage) |  | 1 |  |
| `ShadingElement8GradientAngle` | Mapping Angle (element storage) |  | 0 |  |
| `ShadingElement8MappingSize` | Mapping Size (element storage) |  | 1.5 |  |
| `ShadingElement8MappingAspect` | Mapping Aspect (element storage) |  | 1 |  |
| `ShadingElement8MappingLevel` | Mapping Level (element storage) |  | 0 | 0 Character, 1 Word, 2 Line, 3 Text |
| `ShadingElement8GradientStart` | Gradient Start (element storage) |  | { 0.25, 0.5 } |  |
| `ShadingElement8GradientEnd` | Gradient End (element storage) |  | { 0.75, 0.5 } |  |
| `ShadingElement8Red` | Color (element storage) |  | 1 |  |
| `ShadingElement8Green` | Green (element storage) |  | 1 |  |
| `ShadingElement8Blue` | Blue (element storage) |  | 1 |  |
| `ShadingElement8Alpha` | Alpha (element storage) |  | 1 |  |
| `ShadingElement8EndRed` | Color 2 (element storage) |  | 1 |  |
| `ShadingElement8EndGreen` | Green 2 (element storage) |  | 1 |  |
| `ShadingElement8EndBlue` | Blue 2 (element storage) |  | 1 |  |
| `ShadingElement8EndAlpha` | Alpha 2 (element storage) |  | 1 |  |
| `ShadingElement1Letters` | Letters 1 (element storage) |  | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `ShadingElement2Letters` | Letters 2 (element storage) |  | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `ShadingElement3Letters` | Letters 3 (element storage) |  | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `ShadingElement4Letters` | Letters 4 (element storage) |  | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `ShadingElement5Letters` | Letters 5 (element storage) |  | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `ShadingElement6Letters` | Letters 6 (element storage) |  | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `ShadingElement7Letters` | Letters 7 (element storage) |  | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `ShadingElement8Letters` | Letters 8 (element storage) |  | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |

### In page

| Node input | Label | Section | Default | Range or menu (number: ID) |
|---|---|---|---|---|
| `InFollower` | Follower (Legacy Hidden) |  | 0 (letters) | 0 letters, 1 words, 2 lines |
| `InDelay` | Follower Delay (Legacy Hidden) |  | 0 |  |
| `InAnimationStart` | Animation Start |  | 0 |  to 100000.0 |
| `InDirection` | Direction |  | 0 (reading) | 0 reading, 1 ltr, 2 rtl |
| `InSyncEnable` | Sync to Speech |  | 0 |  |
| `InSyncWords` | Words Shown |  | 0 | 0.0 to  |
| `InStopEnable` | Stop at Frame |  | 0 |  |
| `InStopFrame` | Stop Frame |  | 10 |  to 100000.0 |
| `InStartAt` | Start At |  | 0 |  to 100000.0 |
| `InopacityEnable` | Opacity | Opacity | 0 |  |
| `InopacityFollower` | Animate | Opacity | 0 (letters) | 0 letters, 1 words, 2 lines |
| `InopacityAnimationStart` | Start Frame | Opacity | 0 |  to 100000.0 |
| `InopacityAnimationEnd` | End Frame | Opacity | 30 |  to 100000.0 |
| `InopacityLength` | Duration (Legacy) | Opacity | 20 | 1.0 to  |
| `InopacityAnimationSpeed` | Speed (Legacy) | Opacity | 1 | 0.01 to 100.0 |
| `InopacityDuration` | Stagger Frames (Legacy) | Opacity | 1 | 0.0 to  |
| `InopacityStagger` | Stagger % | Opacity | 10 | 0.0 to  |
| `InopacityStartValue` | Start Value | Opacity | 0 |  |
| `InopacityEndValue` | End Value | Opacity | 1 |  |
| `InopacityCurveMode` | Curve | Opacity | 0 (preset) | 0 preset, 1 custom |
| `InopacityCurvePreset` | Ease | Opacity | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `InopacityCurvePresetCurve` | Custom Curve | Opacity | "0.65 0 0.35 1" |  |
| `InopacityCurvePresetID` | InopacityCurvePresetID | Opacity | "" |  |
| `InopacityCurveResetLatch` | InopacityCurveResetLatch | Opacity | 0 |  |
| `InblurEnable` | Blur | Blur | 0 |  |
| `InblurFollower` | Animate | Blur | 0 (letters) | 0 letters, 1 words, 2 lines |
| `InblurAnimationStart` | Start Frame | Blur | 0 |  to 100000.0 |
| `InblurAnimationEnd` | End Frame | Blur | 30 |  to 100000.0 |
| `InblurLength` | Duration (Legacy) | Blur | 20 | 1.0 to  |
| `InblurAnimationSpeed` | Speed (Legacy) | Blur | 1 | 0.01 to 100.0 |
| `InblurDuration` | Stagger Frames (Legacy) | Blur | 1 | 0.0 to  |
| `InblurStagger` | Stagger % | Blur | 10 | 0.0 to  |
| `InblurStartValue` | Start Value | Blur | 0.1 |  |
| `InblurEndValue` | End Value | Blur | 0 |  |
| `InblurCurveMode` | Curve | Blur | 0 (preset) | 0 preset, 1 custom |
| `InblurCurvePreset` | Ease | Blur | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `InblurCurvePresetCurve` | Custom Curve | Blur | "0.65 0 0.35 1" |  |
| `InblurCurvePresetID` | InblurCurvePresetID | Blur | "" |  |
| `InblurCurveResetLatch` | InblurCurveResetLatch | Blur | 0 |  |
| `IncenterEnable` | Position | Position | 0 |  |
| `IncenterFollower` | Animate | Position | 0 (letters) | 0 letters, 1 words, 2 lines |
| `IncenterAnimationStart` | Start Frame | Position | 0 |  to 100000.0 |
| `IncenterAnimationEnd` | End Frame | Position | 30 |  to 100000.0 |
| `IncenterLength` | Duration (Legacy) | Position | 20 | 1.0 to  |
| `IncenterAnimationSpeed` | Speed (Legacy) | Position | 1 | 0.01 to 100.0 |
| `IncenterDuration` | Stagger Frames (Legacy) | Position | 1 | 0.0 to  |
| `IncenterStagger` | Stagger % | Position | 10 | 0.0 to  |
| `IncenterStartValue` | Start Value | Position | { 0.0, 0.0 } |  |
| `IncenterEndValue` | End Value | Position | { 0.0, 0.0 } |  |
| `IncenterCurveMode` | Curve | Position | 0 (preset) | 0 preset, 1 custom |
| `IncenterCurvePreset` | Ease | Position | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `IncenterCurvePresetCurve` | Custom Curve | Position | "0.65 0 0.35 1" |  |
| `IncenterCurvePresetID` | IncenterCurvePresetID | Position | "" |  |
| `IncenterCurveResetLatch` | IncenterCurveResetLatch | Position | 0 |  |
| `InsizeEnable` | Size | Size | 0 |  |
| `InsizeFollower` | Animate | Size | 0 (letters) | 0 letters, 1 words, 2 lines |
| `InsizeAnimationStart` | Start Frame | Size | 0 |  to 100000.0 |
| `InsizeAnimationEnd` | End Frame | Size | 30 |  to 100000.0 |
| `InsizeLength` | Duration (Legacy) | Size | 20 | 1.0 to  |
| `InsizeAnimationSpeed` | Speed (Legacy) | Size | 1 | 0.01 to 100.0 |
| `InsizeDuration` | Stagger Frames (Legacy) | Size | 1 | 0.0 to  |
| `InsizeStagger` | Stagger % | Size | 10 | 0.0 to  |
| `InsizeStartValue` | Start Value | Size | 0 |  |
| `InsizeEndValue` | End Value | Size | 1 |  |
| `InsizeCurveMode` | Curve | Size | 0 (preset) | 0 preset, 1 custom |
| `InsizeCurvePreset` | Ease | Size | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `InsizeCurvePresetCurve` | Custom Curve | Size | "0.65 0 0.35 1" |  |
| `InsizeCurvePresetID` | InsizeCurvePresetID | Size | "" |  |
| `InsizeCurveResetLatch` | InsizeCurveResetLatch | Size | 0 |  |
| `IntrackingEnable` | Tracking | Tracking | 0 |  |
| `IntrackingFollower` | Animate | Tracking | 0 (letters) | 0 letters, 1 words, 2 lines |
| `IntrackingAnimationStart` | Start Frame | Tracking | 0 |  to 100000.0 |
| `IntrackingAnimationEnd` | End Frame | Tracking | 30 |  to 100000.0 |
| `IntrackingLength` | Duration (Legacy) | Tracking | 20 | 1.0 to  |
| `IntrackingAnimationSpeed` | Speed (Legacy) | Tracking | 1 | 0.01 to 100.0 |
| `IntrackingDuration` | Stagger Frames (Legacy) | Tracking | 1 | 0.0 to  |
| `IntrackingStagger` | Stagger % | Tracking | 10 | 0.0 to  |
| `IntrackingStartValue` | Start Value | Tracking | 0 |  |
| `IntrackingEndValue` | End Value | Tracking | 0 |  |
| `IntrackingPivot` | Pivot | Tracking | 1 (center) | 0 left, 1 center, 2 right |
| `IntrackingCurveMode` | Curve | Tracking | 0 (preset) | 0 preset, 1 custom |
| `IntrackingCurvePreset` | Ease | Tracking | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `IntrackingCurvePresetCurve` | Custom Curve | Tracking | "0.65 0 0.35 1" |  |
| `IntrackingCurvePresetID` | IntrackingCurvePresetID | Tracking | "" |  |
| `IntrackingCurveResetLatch` | IntrackingCurveResetLatch | Tracking | 0 |  |
| `InrotationEnable` | Rotation | Rotation | 0 |  |
| `InrotationFollower` | Animate | Rotation | 0 (letters) | 0 letters, 1 words, 2 lines |
| `InrotationAnimationStart` | Start Frame | Rotation | 0 |  to 100000.0 |
| `InrotationAnimationEnd` | End Frame | Rotation | 30 |  to 100000.0 |
| `InrotationLength` | Duration (Legacy) | Rotation | 20 | 1.0 to  |
| `InrotationAnimationSpeed` | Speed (Legacy) | Rotation | 1 | 0.01 to 100.0 |
| `InrotationDuration` | Stagger Frames (Legacy) | Rotation | 1 | 0.0 to  |
| `InrotationStagger` | Stagger % | Rotation | 10 | 0.0 to  |
| `InrotationStartX` | Start X | Rotation | 0 |  |
| `InrotationStartY` | Start Y | Rotation | 0 |  |
| `InrotationStartValue` | Start Z | Rotation | 0 |  |
| `InrotationEndX` | End X | Rotation | 0 |  |
| `InrotationEndY` | End Y | Rotation | 0 |  |
| `InrotationEndValue` | End Z | Rotation | 0 |  |
| `InrotationCurveMode` | Curve | Rotation | 0 (preset) | 0 preset, 1 custom |
| `InrotationCurvePreset` | Ease | Rotation | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `InrotationCurvePresetCurve` | Custom Curve | Rotation | "0.65 0 0.35 1" |  |
| `InrotationCurvePresetID` | InrotationCurvePresetID | Rotation | "" |  |
| `InrotationCurveResetLatch` | InrotationCurveResetLatch | Rotation | 0 |  |
| `InexplosionEnable` | Explosion | Explosion | 0 |  |
| `InexplosionFollower` | Animate | Explosion | 0 (letters) | 0 letters, 1 words, 2 lines |
| `InexplosionAnimationStart` | Start Frame | Explosion | 0 |  to 100000.0 |
| `InexplosionAnimationEnd` | End Frame | Explosion | 30 |  to 100000.0 |
| `InexplosionLength` | Duration (Legacy) | Explosion | 20 | 1.0 to  |
| `InexplosionAnimationSpeed` | Speed (Legacy) | Explosion | 1 | 0.01 to 100.0 |
| `InexplosionDuration` | Stagger Frames (Legacy) | Explosion | 1 | 0.0 to  |
| `InexplosionStagger` | Stagger % | Explosion | 10 | 0.0 to  |
| `InexplosionStartValue` | Start Value | Explosion | 0 |  |
| `InexplosionEndValue` | End Value | Explosion | 1 |  |
| `InexplosionDamping` | Damping | Explosion | 2 |  |
| `InexplosionSpeed` | Variance | Explosion | 0.35 |  |
| `InexplosionRotationX` | Spin X | Explosion | 180 |  |
| `InexplosionRotationY` | Spin Y | Explosion | 180 |  |
| `InexplosionRotation` | Spin Z | Explosion | 240 |  |
| `InexplosionOffset` | Pre-Roll | Explosion | 0 |  |
| `InexplosionReverse` | Reverse | Explosion | 0 |  |
| `InexplosionCurveMode` | Curve | Explosion | 0 (preset) | 0 preset, 1 custom |
| `InexplosionCurvePreset` | Ease | Explosion | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `InexplosionCurvePresetCurve` | Custom Curve | Explosion | "0.65 0 0.35 1" |  |
| `InexplosionCurvePresetID` | InexplosionCurvePresetID | Explosion | "" |  |
| `InexplosionCurveResetLatch` | InexplosionCurveResetLatch | Explosion | 0 |  |
| `InAnimOffset` | Animation Offset |  | 0 |  |
| `InopacityAnimOffset` | Animation Offset | Opacity | 0 |  |
| `InblurAnimOffset` | Animation Offset | Blur | 0 |  |
| `IncenterAnimOffset` | Animation Offset | Position | 0 |  |
| `InsizeAnimOffset` | Animation Offset | Size | 0 |  |
| `IntrackingAnimOffset` | Animation Offset | Tracking | 0 |  |
| `InrotationAnimOffset` | Animation Offset | Rotation | 0 |  |
| `InexplosionAnimOffset` | Animation Offset | Explosion | 0 |  |
| `Ov1On` | On | Overlap 1 | 0 |  |
| `Ov1Prop` | Property | Overlap 1 | 0 | 0 Size, 1 Position, 2 Rotation, 3 Opacity, 4 Blur, 5 Tracking |
| `Ov1Animate` | Animate | Overlap 1 | 0 | 0 Letters, 1 Words, 2 Lines |
| `Ov1Start` | Start Frame | Overlap 1 | 0 |  |
| `Ov1End` | End Frame | Overlap 1 | 15 |  |
| `Ov1Stagger` | Stagger | Overlap 1 | 0 |  |
| `Ov1Ease` | Ease | Overlap 1 | 6 (in_out_cubic) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `Ov1EaseCurve` | Custom Curve | Overlap 1 | "0.65 0 0.35 1" |  |
| `Ov1SizeFrom` | Size From | Overlap 1 | 1 |  |
| `Ov1SizeTo` | Size To | Overlap 1 | 1 |  |
| `Ov1PositionFrom` | Position From | Overlap 1 | { 0.0, 0.0 } |  |
| `Ov1PositionTo` | Position To | Overlap 1 | { 0.0, 0.0 } |  |
| `Ov1RotationXFrom` | Rotation X From | Overlap 1 | 0 |  |
| `Ov1RotationXTo` | Rotation X To | Overlap 1 | 0 |  |
| `Ov1RotationYFrom` | Rotation Y From | Overlap 1 | 0 |  |
| `Ov1RotationYTo` | Rotation Y To | Overlap 1 | 0 |  |
| `Ov1RotationFrom` | Rotation Z From | Overlap 1 | 0 |  |
| `Ov1RotationTo` | Rotation Z To | Overlap 1 | 0 |  |
| `Ov1OpacityFrom` | Opacity From | Overlap 1 | 1 |  |
| `Ov1OpacityTo` | Opacity To | Overlap 1 | 1 |  |
| `Ov1BlurFrom` | Blur From | Overlap 1 | 0 |  |
| `Ov1BlurTo` | Blur To | Overlap 1 | 0 |  |
| `Ov1TrackingFrom` | Tracking From | Overlap 1 | 0 |  |
| `Ov1TrackingTo` | Tracking To | Overlap 1 | 0 |  |
| `Ov1Offset` | Animation Offset | Overlap 1 | 0 |  |
| `Ov2On` | On | Overlap 2 | 0 |  |
| `Ov2Prop` | Property | Overlap 2 | 0 | 0 Size, 1 Position, 2 Rotation, 3 Opacity, 4 Blur, 5 Tracking |
| `Ov2Animate` | Animate | Overlap 2 | 0 | 0 Letters, 1 Words, 2 Lines |
| `Ov2Start` | Start Frame | Overlap 2 | 0 |  |
| `Ov2End` | End Frame | Overlap 2 | 15 |  |
| `Ov2Stagger` | Stagger | Overlap 2 | 0 |  |
| `Ov2Ease` | Ease | Overlap 2 | 6 (in_out_cubic) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `Ov2EaseCurve` | Custom Curve | Overlap 2 | "0.65 0 0.35 1" |  |
| `Ov2SizeFrom` | Size From | Overlap 2 | 1 |  |
| `Ov2SizeTo` | Size To | Overlap 2 | 1 |  |
| `Ov2PositionFrom` | Position From | Overlap 2 | { 0.0, 0.0 } |  |
| `Ov2PositionTo` | Position To | Overlap 2 | { 0.0, 0.0 } |  |
| `Ov2RotationXFrom` | Rotation X From | Overlap 2 | 0 |  |
| `Ov2RotationXTo` | Rotation X To | Overlap 2 | 0 |  |
| `Ov2RotationYFrom` | Rotation Y From | Overlap 2 | 0 |  |
| `Ov2RotationYTo` | Rotation Y To | Overlap 2 | 0 |  |
| `Ov2RotationFrom` | Rotation Z From | Overlap 2 | 0 |  |
| `Ov2RotationTo` | Rotation Z To | Overlap 2 | 0 |  |
| `Ov2OpacityFrom` | Opacity From | Overlap 2 | 1 |  |
| `Ov2OpacityTo` | Opacity To | Overlap 2 | 1 |  |
| `Ov2BlurFrom` | Blur From | Overlap 2 | 0 |  |
| `Ov2BlurTo` | Blur To | Overlap 2 | 0 |  |
| `Ov2TrackingFrom` | Tracking From | Overlap 2 | 0 |  |
| `Ov2TrackingTo` | Tracking To | Overlap 2 | 0 |  |
| `Ov2Offset` | Animation Offset | Overlap 2 | 0 |  |
| `Ov3On` | On | Overlap 3 | 0 |  |
| `Ov3Prop` | Property | Overlap 3 | 0 | 0 Size, 1 Position, 2 Rotation, 3 Opacity, 4 Blur, 5 Tracking |
| `Ov3Animate` | Animate | Overlap 3 | 0 | 0 Letters, 1 Words, 2 Lines |
| `Ov3Start` | Start Frame | Overlap 3 | 0 |  |
| `Ov3End` | End Frame | Overlap 3 | 15 |  |
| `Ov3Stagger` | Stagger | Overlap 3 | 0 |  |
| `Ov3Ease` | Ease | Overlap 3 | 6 (in_out_cubic) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `Ov3EaseCurve` | Custom Curve | Overlap 3 | "0.65 0 0.35 1" |  |
| `Ov3SizeFrom` | Size From | Overlap 3 | 1 |  |
| `Ov3SizeTo` | Size To | Overlap 3 | 1 |  |
| `Ov3PositionFrom` | Position From | Overlap 3 | { 0.0, 0.0 } |  |
| `Ov3PositionTo` | Position To | Overlap 3 | { 0.0, 0.0 } |  |
| `Ov3RotationXFrom` | Rotation X From | Overlap 3 | 0 |  |
| `Ov3RotationXTo` | Rotation X To | Overlap 3 | 0 |  |
| `Ov3RotationYFrom` | Rotation Y From | Overlap 3 | 0 |  |
| `Ov3RotationYTo` | Rotation Y To | Overlap 3 | 0 |  |
| `Ov3RotationFrom` | Rotation Z From | Overlap 3 | 0 |  |
| `Ov3RotationTo` | Rotation Z To | Overlap 3 | 0 |  |
| `Ov3OpacityFrom` | Opacity From | Overlap 3 | 1 |  |
| `Ov3OpacityTo` | Opacity To | Overlap 3 | 1 |  |
| `Ov3BlurFrom` | Blur From | Overlap 3 | 0 |  |
| `Ov3BlurTo` | Blur To | Overlap 3 | 0 |  |
| `Ov3TrackingFrom` | Tracking From | Overlap 3 | 0 |  |
| `Ov3TrackingTo` | Tracking To | Overlap 3 | 0 |  |
| `Ov3Offset` | Animation Offset | Overlap 3 | 0 |  |
| `Ov4On` | On | Overlap 4 | 0 |  |
| `Ov4Prop` | Property | Overlap 4 | 0 | 0 Size, 1 Position, 2 Rotation, 3 Opacity, 4 Blur, 5 Tracking |
| `Ov4Animate` | Animate | Overlap 4 | 0 | 0 Letters, 1 Words, 2 Lines |
| `Ov4Start` | Start Frame | Overlap 4 | 0 |  |
| `Ov4End` | End Frame | Overlap 4 | 15 |  |
| `Ov4Stagger` | Stagger | Overlap 4 | 0 |  |
| `Ov4Ease` | Ease | Overlap 4 | 6 (in_out_cubic) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `Ov4EaseCurve` | Custom Curve | Overlap 4 | "0.65 0 0.35 1" |  |
| `Ov4SizeFrom` | Size From | Overlap 4 | 1 |  |
| `Ov4SizeTo` | Size To | Overlap 4 | 1 |  |
| `Ov4PositionFrom` | Position From | Overlap 4 | { 0.0, 0.0 } |  |
| `Ov4PositionTo` | Position To | Overlap 4 | { 0.0, 0.0 } |  |
| `Ov4RotationXFrom` | Rotation X From | Overlap 4 | 0 |  |
| `Ov4RotationXTo` | Rotation X To | Overlap 4 | 0 |  |
| `Ov4RotationYFrom` | Rotation Y From | Overlap 4 | 0 |  |
| `Ov4RotationYTo` | Rotation Y To | Overlap 4 | 0 |  |
| `Ov4RotationFrom` | Rotation Z From | Overlap 4 | 0 |  |
| `Ov4RotationTo` | Rotation Z To | Overlap 4 | 0 |  |
| `Ov4OpacityFrom` | Opacity From | Overlap 4 | 1 |  |
| `Ov4OpacityTo` | Opacity To | Overlap 4 | 1 |  |
| `Ov4BlurFrom` | Blur From | Overlap 4 | 0 |  |
| `Ov4BlurTo` | Blur To | Overlap 4 | 0 |  |
| `Ov4TrackingFrom` | Tracking From | Overlap 4 | 0 |  |
| `Ov4TrackingTo` | Tracking To | Overlap 4 | 0 |  |
| `Ov4Offset` | Animation Offset | Overlap 4 | 0 |  |

### Out page

| Node input | Label | Section | Default | Range or menu (number: ID) |
|---|---|---|---|---|
| `OutFollower` | Follower (Legacy Hidden) |  | 0 (letters) | 0 letters, 1 words, 2 lines |
| `OutDelay` | Follower Delay (Legacy Hidden) |  | 0 |  |
| `OutStartMode` | Align (Legacy) |  | 0 (before_end) | 0 before_end, 1 frame_number |
| `OutAnimationStart` | Animation Start |  | 0 |  to 100000.0 |
| `OutDirection` | Direction |  | 0 (reading) | 0 reading, 1 ltr, 2 rtl |
| `OutStopEnable` | Stop at Frame |  | 0 |  |
| `OutStopFrame` | Stop Frame |  | 10 |  to 100000.0 |
| `OutAlignEnd` | Align to End |  | 0 |  |
| `OutEndAt` | End At |  | 0 |  to 100000.0 |
| `OutBeforeEnd` | Before End |  | 0 |  to 100000.0 |
| `OutopacityEnable` | Opacity | Opacity | 0 |  |
| `OutopacityFollower` | Animate | Opacity | 0 (letters) | 0 letters, 1 words, 2 lines |
| `OutopacityAnimationStart` | Start Frame | Opacity | 100 |  to 100000.0 |
| `OutopacityAnimationEnd` | End Frame | Opacity | 130 |  to 100000.0 |
| `OutopacityBeforeEnd` | Before End (Legacy) | Opacity | 0 | 0.0 to  |
| `OutopacityLength` | Duration (Legacy) | Opacity | 20 | 1.0 to  |
| `OutopacityAnimationSpeed` | Speed (Legacy) | Opacity | 1 | 0.01 to 100.0 |
| `OutopacityDuration` | Stagger Frames (Legacy) | Opacity | 1 | 0.0 to  |
| `OutopacityStagger` | Stagger % | Opacity | 10 | 0.0 to  |
| `OutopacityEndValue` | End Value | Opacity | 0 |  |
| `OutopacityCurveMode` | Curve | Opacity | 0 (preset) | 0 preset, 1 custom |
| `OutopacityCurvePreset` | Ease | Opacity | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `OutopacityCurvePresetCurve` | Custom Curve | Opacity | "0.65 0 0.35 1" |  |
| `OutopacityCurvePresetID` | OutopacityCurvePresetID | Opacity | "" |  |
| `OutopacityCurveResetLatch` | OutopacityCurveResetLatch | Opacity | 0 |  |
| `OutblurEnable` | Blur | Blur | 0 |  |
| `OutblurFollower` | Animate | Blur | 0 (letters) | 0 letters, 1 words, 2 lines |
| `OutblurAnimationStart` | Start Frame | Blur | 100 |  to 100000.0 |
| `OutblurAnimationEnd` | End Frame | Blur | 130 |  to 100000.0 |
| `OutblurBeforeEnd` | Before End (Legacy) | Blur | 0 | 0.0 to  |
| `OutblurLength` | Duration (Legacy) | Blur | 20 | 1.0 to  |
| `OutblurAnimationSpeed` | Speed (Legacy) | Blur | 1 | 0.01 to 100.0 |
| `OutblurDuration` | Stagger Frames (Legacy) | Blur | 1 | 0.0 to  |
| `OutblurStagger` | Stagger % | Blur | 10 | 0.0 to  |
| `OutblurEndValue` | End Value | Blur | 0.1 |  |
| `OutblurCurveMode` | Curve | Blur | 0 (preset) | 0 preset, 1 custom |
| `OutblurCurvePreset` | Ease | Blur | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `OutblurCurvePresetCurve` | Custom Curve | Blur | "0.65 0 0.35 1" |  |
| `OutblurCurvePresetID` | OutblurCurvePresetID | Blur | "" |  |
| `OutblurCurveResetLatch` | OutblurCurveResetLatch | Blur | 0 |  |
| `OutcenterEnable` | Position | Position | 0 |  |
| `OutcenterFollower` | Animate | Position | 0 (letters) | 0 letters, 1 words, 2 lines |
| `OutcenterAnimationStart` | Start Frame | Position | 100 |  to 100000.0 |
| `OutcenterAnimationEnd` | End Frame | Position | 130 |  to 100000.0 |
| `OutcenterBeforeEnd` | Before End (Legacy) | Position | 0 | 0.0 to  |
| `OutcenterLength` | Duration (Legacy) | Position | 20 | 1.0 to  |
| `OutcenterAnimationSpeed` | Speed (Legacy) | Position | 1 | 0.01 to 100.0 |
| `OutcenterDuration` | Stagger Frames (Legacy) | Position | 1 | 0.0 to  |
| `OutcenterStagger` | Stagger % | Position | 10 | 0.0 to  |
| `OutcenterEndValue` | End Value | Position | { 0.0, 0.0 } |  |
| `OutcenterCurveMode` | Curve | Position | 0 (preset) | 0 preset, 1 custom |
| `OutcenterCurvePreset` | Ease | Position | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `OutcenterCurvePresetCurve` | Custom Curve | Position | "0.65 0 0.35 1" |  |
| `OutcenterCurvePresetID` | OutcenterCurvePresetID | Position | "" |  |
| `OutcenterCurveResetLatch` | OutcenterCurveResetLatch | Position | 0 |  |
| `OutsizeEnable` | Size | Size | 0 |  |
| `OutsizeFollower` | Animate | Size | 0 (letters) | 0 letters, 1 words, 2 lines |
| `OutsizeAnimationStart` | Start Frame | Size | 100 |  to 100000.0 |
| `OutsizeAnimationEnd` | End Frame | Size | 130 |  to 100000.0 |
| `OutsizeBeforeEnd` | Before End (Legacy) | Size | 0 | 0.0 to  |
| `OutsizeLength` | Duration (Legacy) | Size | 20 | 1.0 to  |
| `OutsizeAnimationSpeed` | Speed (Legacy) | Size | 1 | 0.01 to 100.0 |
| `OutsizeDuration` | Stagger Frames (Legacy) | Size | 1 | 0.0 to  |
| `OutsizeStagger` | Stagger % | Size | 10 | 0.0 to  |
| `OutsizeEndValue` | End Value | Size | 0 |  |
| `OutsizeCurveMode` | Curve | Size | 0 (preset) | 0 preset, 1 custom |
| `OutsizeCurvePreset` | Ease | Size | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `OutsizeCurvePresetCurve` | Custom Curve | Size | "0.65 0 0.35 1" |  |
| `OutsizeCurvePresetID` | OutsizeCurvePresetID | Size | "" |  |
| `OutsizeCurveResetLatch` | OutsizeCurveResetLatch | Size | 0 |  |
| `OuttrackingEnable` | Tracking | Tracking | 0 |  |
| `OuttrackingFollower` | Animate | Tracking | 0 (letters) | 0 letters, 1 words, 2 lines |
| `OuttrackingAnimationStart` | Start Frame | Tracking | 100 |  to 100000.0 |
| `OuttrackingAnimationEnd` | End Frame | Tracking | 130 |  to 100000.0 |
| `OuttrackingBeforeEnd` | Before End (Legacy) | Tracking | 0 | 0.0 to  |
| `OuttrackingLength` | Duration (Legacy) | Tracking | 20 | 1.0 to  |
| `OuttrackingAnimationSpeed` | Speed (Legacy) | Tracking | 1 | 0.01 to 100.0 |
| `OuttrackingDuration` | Stagger Frames (Legacy) | Tracking | 1 | 0.0 to  |
| `OuttrackingStagger` | Stagger % | Tracking | 10 | 0.0 to  |
| `OuttrackingEndValue` | End Value | Tracking | 0 |  |
| `OuttrackingPivot` | Pivot | Tracking | 1 (center) | 0 left, 1 center, 2 right |
| `OuttrackingCurveMode` | Curve | Tracking | 0 (preset) | 0 preset, 1 custom |
| `OuttrackingCurvePreset` | Ease | Tracking | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `OuttrackingCurvePresetCurve` | Custom Curve | Tracking | "0.65 0 0.35 1" |  |
| `OuttrackingCurvePresetID` | OuttrackingCurvePresetID | Tracking | "" |  |
| `OuttrackingCurveResetLatch` | OuttrackingCurveResetLatch | Tracking | 0 |  |
| `OutrotationEnable` | Rotation | Rotation | 0 |  |
| `OutrotationFollower` | Animate | Rotation | 0 (letters) | 0 letters, 1 words, 2 lines |
| `OutrotationAnimationStart` | Start Frame | Rotation | 100 |  to 100000.0 |
| `OutrotationAnimationEnd` | End Frame | Rotation | 130 |  to 100000.0 |
| `OutrotationBeforeEnd` | Before End (Legacy) | Rotation | 0 | 0.0 to  |
| `OutrotationLength` | Duration (Legacy) | Rotation | 20 | 1.0 to  |
| `OutrotationAnimationSpeed` | Speed (Legacy) | Rotation | 1 | 0.01 to 100.0 |
| `OutrotationDuration` | Stagger Frames (Legacy) | Rotation | 1 | 0.0 to  |
| `OutrotationStagger` | Stagger % | Rotation | 10 | 0.0 to  |
| `OutrotationEndX` | End X | Rotation | 0 |  |
| `OutrotationEndY` | End Y | Rotation | 0 |  |
| `OutrotationEndValue` | End Z | Rotation | 0 |  |
| `OutrotationCurveMode` | Curve | Rotation | 0 (preset) | 0 preset, 1 custom |
| `OutrotationCurvePreset` | Ease | Rotation | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `OutrotationCurvePresetCurve` | Custom Curve | Rotation | "0.65 0 0.35 1" |  |
| `OutrotationCurvePresetID` | OutrotationCurvePresetID | Rotation | "" |  |
| `OutrotationCurveResetLatch` | OutrotationCurveResetLatch | Rotation | 0 |  |
| `OutexplosionEnable` | Explosion | Explosion | 0 |  |
| `OutexplosionFollower` | Animate | Explosion | 0 (letters) | 0 letters, 1 words, 2 lines |
| `OutexplosionAnimationStart` | Start Frame | Explosion | 100 |  to 100000.0 |
| `OutexplosionAnimationEnd` | End Frame | Explosion | 130 |  to 100000.0 |
| `OutexplosionBeforeEnd` | Before End (Legacy) | Explosion | 0 | 0.0 to  |
| `OutexplosionLength` | Duration (Legacy) | Explosion | 20 | 1.0 to  |
| `OutexplosionAnimationSpeed` | Speed (Legacy) | Explosion | 1 | 0.01 to 100.0 |
| `OutexplosionDuration` | Stagger Frames (Legacy) | Explosion | 1 | 0.0 to  |
| `OutexplosionStagger` | Stagger % | Explosion | 10 | 0.0 to  |
| `OutexplosionEndValue` | End Value | Explosion | 1 |  |
| `OutexplosionDamping` | Damping | Explosion | 2 |  |
| `OutexplosionSpeed` | Variance | Explosion | 0.35 |  |
| `OutexplosionRotationX` | Spin X | Explosion | 180 |  |
| `OutexplosionRotationY` | Spin Y | Explosion | 180 |  |
| `OutexplosionRotation` | Spin Z | Explosion | 240 |  |
| `OutexplosionOffset` | Pre-Roll | Explosion | 0 |  |
| `OutexplosionReverse` | Reverse | Explosion | 0 |  |
| `OutexplosionCurveMode` | Curve | Explosion | 0 (preset) | 0 preset, 1 custom |
| `OutexplosionCurvePreset` | Ease | Explosion | 0 (linear) | 0 linear, 1 in_quad, 2 out_quad, 3 in_out_quad, 4 in_cubic, 5 out_cubic, 6 in_out_cubic, 7 in_quart, 8 out_quart, 9 in_out_quart, 10 in_quint, 11 out_quint, ... |
| `OutexplosionCurvePresetCurve` | Custom Curve | Explosion | "0.65 0 0.35 1" |  |
| `OutexplosionCurvePresetID` | OutexplosionCurvePresetID | Explosion | "" |  |
| `OutexplosionCurveResetLatch` | OutexplosionCurveResetLatch | Explosion | 0 |  |
| `OutAnimOffset` | Animation Offset |  | 0 |  |
| `OutopacityAnimOffset` | Animation Offset | Opacity | 0 |  |
| `OutblurAnimOffset` | Animation Offset | Blur | 0 |  |
| `OutcenterAnimOffset` | Animation Offset | Position | 0 |  |
| `OutsizeAnimOffset` | Animation Offset | Size | 0 |  |
| `OuttrackingAnimOffset` | Animation Offset | Tracking | 0 |  |
| `OutrotationAnimOffset` | Animation Offset | Rotation | 0 |  |
| `OutexplosionAnimOffset` | Animation Offset | Explosion | 0 |  |

### Motion Blur page

| Node input | Label | Section | Default | Range or menu (number: ID) |
|---|---|---|---|---|
| `MotionBlurEnable` | Motion Blur |  | 0 |  |
| `MotionBlurShutterAngle` | Shutter |  | 180 |  |
| `MotionBlurSamples` | Quality |  | 2 | 1.0 to 10.0 |
| `MotionBlurBias` | Bias |  | 0 |  |
| `MotionBlurSampleSpread` | Spread |  | 1 | 0.0 to 1.0 |

### Effects page

| Node input | Label | Section | Default | Range or menu (number: ID) |
|---|---|---|---|---|
| `FxFloatOn` | Float | Float | 0 |  |
| `FxFloatLetters` | Letters | Float | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxFloatPieces` | Float By | Float | 0 | 0 Letters, 1 Words, 2 Lines, 3 Whole Text |
| `FxFloatStyle` | Float Style | Float | 0 | 0 Random, 1 Wave Left to Right, 2 Wave Right to Left, 3 Wave from the Middle, 4 Together |
| `FxFloatAmount` | Float Amount | Float | 1 | 0.0 to  |
| `FxFloatRotation` | Float Rotation | Float | 1 | 0.0 to  |
| `FxFloatSpeed` | Float Speed | Float | 1 | 0.0 to  |
| `FxFloatX` | Float X | Float | 4 | 0.0 to  |
| `FxFloatY` | Float Y | Float | 9 | 0.0 to  |
| `FxFloatSize` | Float Size | Float | 2 | 0.0 to  |
| `FxFloatAngle` | Float Angle | Float | 3 | 0.0 to  |
| `FxFloatWave` | Wave Length | Float | 6 | 0.0 to  |
| `FxFloatPace` | Pace Variation | Float | 1 | 0.0 to  |
| `FxFloatRipple` | Ripple | Float | 0.35 | 0.0 to  |
| `FxFloatEaseIn` | Ease In (seconds) | Float | 0 | 0.0 to  |
| `FxFloatSeed` | Float Seed | Float | 0 | 0.0 to  |
| `FxGlowOn` | Glow | Glow | 0 |  |
| `FxGlowLetters` | Letters | Glow | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxGlowAmount` | Glow Amount | Glow | 1 | 0.0 to  |
| `FxGlowSize` | Glow Size | Glow | 1 | 0.0 to  |
| `FxGlowTextColors` | Text's Colors | Glow | 1 |  |
| `FxGlowColorRed` | Glow Color (Red) | Glow | 1 |  |
| `FxGlowColorGreen` | Glow Color (Green) | Glow | 0.82 |  |
| `FxGlowColorBlue` | Glow Color (Blue) | Glow | 0.35 |  |
| `FxFireOn` | Fire | Fire | 0 |  |
| `FxFireLetters` | Letters | Fire | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxFireInside` | Inside the Letters | Fire | 0 |  |
| `FxFireFlames` | Flames | Fire | 1 | 0.0 to  |
| `FxFireHeight` | Flame Height | Fire | 1 | 0.0 to  |
| `FxFireEmbers` | Embers | Fire | 1 | 0.0 to  |
| `FxFireSpeed` | Fire Speed | Fire | 1 | 0.0 to  |
| `FxFireDirection` | Fire Direction | Fire | 90 |  |
| `FxFireCenter` | Center Effect | Fire | 0 |  |
| `FxFireCenterX` | Center X | Fire | 0 |  |
| `FxFireCenterY` | Center Y | Fire | 0 |  |
| `FxFireCenterWidth` | Center Width | Fire | 30 | 0.0 to  |
| `FxFireColorRed` | Fire Color (Red) | Fire | 1 |  |
| `FxFireColorGreen` | Fire Color (Green) | Fire | 0.42 |  |
| `FxFireColorBlue` | Fire Color (Blue) | Fire | 0.06 |  |
| `FxFrostOn` | Frost | Frost | 0 |  |
| `FxFrostLetters` | Letters | Frost | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxFrostInside` | Inside the Letters | Frost | 0 |  |
| `FxFrostMist` | Mist | Frost | 1 | 0.0 to  |
| `FxFrostHeight` | Mist Reach | Frost | 1 | 0.0 to  |
| `FxFrostSnow` | Snow | Frost | 1 | 0.0 to  |
| `FxFrostSpeed` | Frost Speed | Frost | 1 | 0.0 to  |
| `FxFrostDirection` | Frost Direction | Frost | -90 |  |
| `FxFrostCenter` | Center Effect | Frost | 0 |  |
| `FxFrostCenterX` | Center X | Frost | 0 |  |
| `FxFrostCenterY` | Center Y | Frost | 0 |  |
| `FxFrostCenterWidth` | Center Width | Frost | 30 | 0.0 to  |
| `FxFrostColorRed` | Frost Color (Red) | Frost | 0.75 |  |
| `FxFrostColorGreen` | Frost Color (Green) | Frost | 0.92 |  |
| `FxFrostColorBlue` | Frost Color (Blue) | Frost | 1 |  |
| `FxSmokeOn` | Smoke | Smoke | 0 |  |
| `FxSmokeLetters` | Letters | Smoke | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxSmokeInside` | Inside the Letters | Smoke | 0 |  |
| `FxSmokeAmount` | Smoke Amount | Smoke | 1 | 0.0 to  |
| `FxSmokeHeight` | Smoke Height | Smoke | 1 | 0.0 to  |
| `FxSmokeSpeed` | Smoke Speed | Smoke | 1 | 0.0 to  |
| `FxSmokeDirection` | Smoke Direction | Smoke | 90 |  |
| `FxSmokeCenter` | Center Effect | Smoke | 0 |  |
| `FxSmokeCenterX` | Center X | Smoke | 0 |  |
| `FxSmokeCenterY` | Center Y | Smoke | 0 |  |
| `FxSmokeCenterWidth` | Center Width | Smoke | 30 | 0.0 to  |
| `FxSmokeColorRed` | Smoke Color (Red) | Smoke | 0.32 |  |
| `FxSmokeColorGreen` | Smoke Color (Green) | Smoke | 0.32 |  |
| `FxSmokeColorBlue` | Smoke Color (Blue) | Smoke | 0.35 |  |
| `FxElectricOn` | Electric | Electric | 0 |  |
| `FxElectricLetters` | Letters | Electric | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxElectricInside` | Inside the Letters | Electric | 0 |  |
| `FxElectricAmount` | Electric Amount | Electric | 1 | 0.0 to  |
| `FxElectricReach` | Arc Reach | Electric | 1 | 0.0 to  |
| `FxElectricSpeed` | Flicker Speed | Electric | 1 | 0.0 to  |
| `FxElectricColorRed` | Electric Color (Red) | Electric | 0.45 |  |
| `FxElectricColorGreen` | Electric Color (Green) | Electric | 0.75 |  |
| `FxElectricColorBlue` | Electric Color (Blue) | Electric | 1 |  |
| `FxRaysOn` | Light Rays | Light Rays | 0 |  |
| `FxRaysLetters` | Letters | Light Rays | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxRaysAmount` | Ray Amount | Light Rays | 1 | 0.0 to  |
| `FxRaysLength` | Ray Length | Light Rays | 1 | 0.0 to  |
| `FxRaysDirection` | Ray Direction | Light Rays | 90 |  |
| `FxRaysCenter` | Center Effect | Light Rays | 0 |  |
| `FxRaysCenterX` | Center X | Light Rays | 0 |  |
| `FxRaysCenterY` | Center Y | Light Rays | 0 |  |
| `FxRaysCenterWidth` | Center Width | Light Rays | 0 | 0.0 to  |
| `FxRaysColorRed` | Ray Color (Red) | Light Rays | 1 |  |
| `FxRaysColorGreen` | Ray Color (Green) | Light Rays | 0.92 |  |
| `FxRaysColorBlue` | Ray Color (Blue) | Light Rays | 0.75 |  |
| `FxShineOn` | Shine | Shine | 0 |  |
| `FxShineLetters` | Letters | Shine | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxShineAmount` | Shine Amount | Shine | 1 | 0.0 to  |
| `FxShineWidth` | Shine Width | Shine | 1 | 0.0 to  |
| `FxShineEvery` | Shine Every (seconds) | Shine | 2.5 | 0.0 to  |
| `FxShineDirection` | Shine Direction | Shine | -20 |  |
| `FxShineCenter` | Center Effect | Shine | 0 |  |
| `FxShineCenterX` | Center X | Shine | 0 |  |
| `FxShineCenterY` | Center Y | Shine | 0 |  |
| `FxShineCenterWidth` | Center Width | Shine | 40 | 0.0 to  |
| `FxShineColorRed` | Shine Color (Red) | Shine | 1 |  |
| `FxShineColorGreen` | Shine Color (Green) | Shine | 1 |  |
| `FxShineColorBlue` | Shine Color (Blue) | Shine | 1 |  |
| `FxSparkleOn` | Sparkles | Sparkles | 0 |  |
| `FxSparkleLetters` | Letters | Sparkles | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxSparkleAmount` | Sparkle Amount | Sparkles | 1 | 0.0 to  |
| `FxSparkleSize` | Sparkle Size | Sparkles | 1 | 0.0 to  |
| `FxSparkleSpeed` | Twinkle Speed | Sparkles | 1 | 0.0 to  |
| `FxSparkleColorRed` | Sparkle Color (Red) | Sparkles | 1 |  |
| `FxSparkleColorGreen` | Sparkle Color (Green) | Sparkles | 1 |  |
| `FxSparkleColorBlue` | Sparkle Color (Blue) | Sparkles | 1 |  |
| `FxGlitchOn` | Glitch | Glitch | 0 |  |
| `FxGlitchLetters` | Letters | Glitch | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxGlitchAmount` | Glitch Amount | Glitch | 1 | 0.0 to  |
| `FxGlitchFrequency` | Glitch Frequency | Glitch | 1 | 0.0 to  |
| `FxGlitchDirection` | Glitch Direction | Glitch | 0 |  |
| `FxDustOn` | Dust | Dust | 0 |  |
| `FxDustLetters` | Letters | Dust | 0 | 0 All Letters, 1 Selected Letters, 2 Other Letters |
| `FxDustAmount` | Dust Amount | Dust | 1 | 0.0 to  |
| `FxDustSize` | Dust Size | Dust | 1 | 0.0 to  |
| `FxDustSpeed` | Dust Speed | Dust | 1 | 0.0 to  |
| `FxDustDirection` | Dust Direction | Dust | 60 |  |
| `FxDustCenter` | Center Effect | Dust | 0 |  |
| `FxDustCenterX` | Center X | Dust | 0 |  |
| `FxDustCenterY` | Center Y | Dust | 0 |  |
| `FxDustCenterWidth` | Center Width | Dust | 30 | 0.0 to  |
| `FxDustColorRed` | Dust Color (Red) | Dust | 1 |  |
| `FxDustColorGreen` | Dust Color (Green) | Dust | 0.93 |  |
| `FxDustColorBlue` | Dust Color (Blue) | Dust | 0.82 |  |
<!-- /controls -->

## 14. Using a look in Resolve

- **Edit page:** save the look as a `.setting` file (TextizoFX's own folder is `Documents/Clipizo/TextizoFX/Looks`), select the TextizoFX clip, click **Load Look...** (right under the Look menu) and pick the file. Your text stays; everything else takes the look, as one undo step.
- **Look menu:** looks in `Documents/Clipizo/TextizoFX/Looks` are listed in the Look menu from the next time DaVinci Resolve starts, and in **Browse Looks...** (Windows) right away.
- **Fusion page:** paste the code into the Nodes area (or drag the `.setting` file onto it); a TextizoFX node appears. Connect it to MediaOut1, or Merge it over a clip.
- **Your own text:** type it in the Inspector. The animation follows any length of text.
- **A longer or shorter clip:** looks with Align to End keep the exit at the clip's end; otherwise move the Out rows' Start and End Frames.

## 15. Troubleshooting

- **Nothing changed after Load Look...:** the file must hold a `TextizoFX1 = ofx.com.clipizo.textizofx { ... }` node (or a Textizo preset). A message says why a file couldn't be loaded.
- **A menu didn't take:** menus are numbers in a TextizoFX node, never `FuID { "..." }`.
- **The wrong colour:** element 1's colour is written twice (`ShadingProxyRed...` channels and `ShadingElement1Red`...), and the Text page's Color (`RedRed` ...) tints it: keep that at 1.
- **The text is cut off or shrunk:** lower Size until every line is under about 0.85 of the frame width ("Size and width", section 3), and keep Fit to Frame on.
- **Pasting on the Fusion page made nothing:** click an empty spot of the Nodes area first, then paste.
