# Applied Chain: AI supply chain website

Homepage prototype for Applied Chain (*Practical AI for Supply Chain*): what we offer, how we work, and four interactive demos of AI agents doing supply chain work.

**Current version: V3** ([`ux-prototype/index-v3.html`](ux-prototype/index-v3.html)). It is content only: no logo, top menu or footer, because it is meant to sit inside a tab of a host website.

## Run it

Open the file in a browser. There is nothing to install or build.

```bash
open ux-prototype/index-v3.html
```

Each version is a single self-contained HTML file (HTML, CSS and JavaScript inline). The only external resource is Google Fonts (Manrope, Inter, IBM Plex Mono), with system-font fallbacks.

## Versions

| File | Version | What it is |
| --- | --- | --- |
| `ux-prototype/index-v3.html` | **V3 (current)** | Content only, for a host site's tab. Order: intro, approach, demos, offers, contact. Four demos, AI workforce first. |
| `ux-prototype/index-v2.html` | V2 | Full site with Applied Chain header and footer, About (team + technology partner), and a founding-client pilot program. No results section. |
| `ux-prototype/index.html` | V1 | First full site, including sample case-study results. Kept for reference only; the sample results are not real. |

## Where things are in `index-v3.html`

Search for these comment markers:

| Part | Marker |
| --- | --- |
| Design tokens (colours, fonts) | `:root {` at the top of `<style>` |
| Page sections | `<!-- HERO -->`, `<!-- APPROACH -->`, `<!-- DEMO -->`, `<!-- OFFER -->`, `<!-- CONTACT -->` |
| Demo picker (the four demo cards) | `/* Demo picker` (CSS), `class="demo-tabs"` (HTML), `function setDemo` (JS) |
| Demo 1: AI workforce | `/* ---------- Demo: AI workforce` |
| Demo 2: Restock agent | `/* ---------- Demo 2: Restock agent` |
| Demo 3: AI planner in team chat | `/* ---------- Demo 3: Wilson` |
| Demo 4: Freight matching | `/* ---------- Demo: Freight Scout story mode` |
| Contact form, design-notes toggle | `/* ---------- Contact, notes` |

Each demo has a story mode (it autoplays when scrolled into view, with play, pause, step and progress controls) and a "try it" mode (sliders, typed questions, approve buttons).

### Demo logic

- **AI workforce:** scripted story. Three agents (Supply Planner, Logistics Planner, Supply Chain Analyst for freight cost and billing), each with one or two use cases. A person approves every action. Edit `WF`, `WF_STEPS` and `WF_APPROVALS`.
- **Restock agent:** uses the restock formula from the AI Merchant Assistant project: `restock = daily sales × (lead time + safety days + restock cadence) − current inventory`. Health status: Out of Stock (0 units), Critical (under 15 days of stock), Low (under 30), Healthy. Sample SKUs are in `RS_SKUS`. Chat replies are rule-based (`rsAsk`); in production these would go to an LLM with tool calls.
- **AI planner in team chat:** a Slack/Teams-style thread using the same restock logic. It is a generic chat look, deliberately not Slack's branding. Replies are rule-based (`skAsk`).
- **Freight matching:** a port of the Freight Scout matching approach. Seeded random load board (`buildRun`), hard constraints (equipment, weight, pickup window, deadhead), and a weighted score (rate per mile, deadhead, fill, broker trust, timing).

All companies, people, suppliers, carriers and numbers in the demos are fictional sample data.

## Not connected yet

- The contact form and the "Pick a time on our calendar" button show a notice only. They need a form backend (e.g. Netlify Forms or Formspree) and a booking link (Cal.com or Calendly).
- The yellow **Show design notes** button (bottom left) reveals review notes and open decisions in each section. Remove it, and the `.note` blocks, before going live.

## Publishing copies (optional)

`ux-prototype/build-share.py` makes copies for claude.ai review links by stripping the `<!doctype>`, `<html>`, `<head>` and `<body>` tags, which that host adds itself. You don't need it for a normal website.

```bash
python3 ux-prototype/build-share.py      # all versions
python3 ux-prototype/build-share.py v3   # just V3
```

Output goes to `ux-prototype/share/`, which is not committed.

## Embedding V3 in a host site

V3 currently ships with its own global styles (`html`, `body`, `section`, `h1`–`h3`, `p`, `input`, `textarea`, `label`). Inside another site these can clash with the host's CSS. Before embedding, either:

- load it in an `<iframe>` (simplest, fully isolated), or
- scope the styles under one wrapper class and move the markup into the host page.

## Documents

`documents/` holds the original product requirements document (Markdown, Word, PDF) and its timeline image. It predates later decisions: it describes a solo "AI consulting" site. Where they differ, follow V3: the Applied Chain name, "AI solutions" wording, "we" voice, no results section, four demos, and live demos customised to each client.
