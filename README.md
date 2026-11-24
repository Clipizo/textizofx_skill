# TextizoFX AI Kit

Let your AI make **TextizoFX** looks: animated titles for DaVinci Resolve, ready to use. Describe what you want in plain words, for example *"SALE pops in letter by letter, red with a black outline"*, *"a clean blur-in title with a soft glow"* or *"a caption pill for 'Subscribe for more'"*. The AI writes the look, checks it, and saves it where you want.

This kit is made for TextizoFX (Clipizo); `reference/inputs.json` names the version it was built from. TextizoFX must be installed.

## Two ways to use it

**1. With any AI chat** (ChatGPT, Claude, Gemini, Copilot):

1. Give the chat the file **`TextizoFX AI Guide.md`**.
2. Describe the title you want.
3. Use the code it gives you:
   - **Fusion page:** copy it, click in the Nodes area and press Ctrl+V (Mac: Cmd+V). A TextizoFX node appears with the look.
   - **Edit page:** save the code as a `.setting` file, select your TextizoFX clip, and click **Load Look...** in the Inspector (right under the Look menu).

The guide's first section explains this step by step.

**2. With an AI agent that can open folders** (Claude Code, OpenAI Codex, Gemini CLI, Cursor, VS Code with Copilot):

1. Open this folder in the agent.
2. Ask for a look.

The agent reads `AGENTS.md` and `SKILL.md`, asks you a few questions (including where to save), then writes and checks the `.setting` file and can put it straight into TextizoFX's Look menu.

For Claude, you can also upload this folder, zipped, as a custom skill.

## Where looks can go

| Choice | What you get |
|---|---|
| TextizoFX's My Looks folder (recommended) | The look is in TextizoFX's **Look** menu, with your other looks, from the next time DaVinci Resolve starts, and in **Browse Looks...** (Windows) right away. **Load Look...** opens this folder too. |
| Resolve's Settings folder | For the Fusion page: a TextizoFX node's right-click **Settings > Load…** opens this folder. |
| Downloads/TextizoFX Looks | Easy to find. Use **Load Look...**, or drag the file onto the Fusion page's Nodes area. |
| Any folder you name | |

The My Looks folder is `Documents/Clipizo/TextizoFX/Looks` (Windows and Mac).

## What is inside

| File or folder | Contents |
|---|---|
| `TextizoFX AI Guide.md` | Everything an AI needs to know about TextizoFX's text, animation rows, timing, shading, effects and every control. |
| `SKILL.md`, `AGENTS.md` | Instructions for AI agents. `CLAUDE.md` and `GEMINI.md` point to them. |
| `presets/` | TextizoFX's ready looks (the Look menu's), each as a node with every value written out. |
| `specs/` | The same looks as short, editable descriptions. |
| `tools/textizofx_look.py` | Builds, checks and installs looks. Needs Python 3 and nothing else. |
| `reference/inputs.json` | The list of TextizoFX's controls (made from the plugin itself), which the checker uses. |
| `my-looks/` | Where the agent keeps your looks while it works on them. |

The ready looks:

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

New looks get short names like `TextizoFX-07A`: a number for each look and a letter for each variation.

## Using a look in Resolve

- **Edit page:** select the TextizoFX clip, click **Load Look...** and pick the file. Your text stays; everything else takes the look.
- **Look menu:** looks in the My Looks folder are listed there (after DaVinci Resolve starts again).
- **Fusion page:** paste the code into the Nodes area, or drag the `.setting` file onto it, then connect the node.
- **Your own text:** type it in the Inspector. The animation follows any length of text.

## License

Free of charge, under the Clipizo product license in `LICENSE.txt`. Use the kit and its looks in your own projects, personal or commercial, including client work and monetized videos. Please don't re-upload or redistribute the files; to recommend TextizoFX, link to its page on clipizo.com.
