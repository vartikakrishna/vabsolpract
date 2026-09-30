# DESIGN SYSTEM & UI SPECIFICATION
## "Executive Gloss" Aesthetic for INDMoney Facts-Only Assistant

**Document Version:** 1.0.0  
**Design System Name:** Executive Gloss (Dark Slate & Luminous Cyan)  
**Target Platform:** Web Desktop & Mobile (Responsive)  

---

## 1. Visual Design Theme & Philosophy

The **Executive Gloss** theme combines the institutional gravitas of top-tier financial platforms with the sleek, high-precision clarity of modern fintech applications. 

### Core Design Principles:
1. **Luminous Contrast on Deep Obsidian:** Content floats gracefully over tiered dark surfaces (`#0B0F17` base) to minimize eye strain and eliminate clutter.
2. **Subtle Glassmorphism:** Micro-diffused frosted backdrops (`backdrop-filter: blur(16px)`) with hairline specular borders (`rgba(255, 255, 255, 0.08)`).
3. **High Information Density with Breathable Typography:** Every pixel respects financial compliance—crisp numbers, bold scheme tags, and prominent official source citations.

---

## 2. Color Palette & Token System

```css
:root {
  /* Surface Layers (Obsidian to Slate) */
  --bg-primary: #07090E;         /* Deep canvas background */
  --bg-secondary: #0D121F;       /* Card & container layer */
  --bg-surface: #141B2D;         /* Chat bubbles & interactive components */
  --bg-surface-hover: #1D263E;   /* Interactive hover state */
  --bg-surface-active: #242F4D;  /* Active / pressed state */

  /* Glass & Frost Overlays */
  --glass-bg: rgba(13, 18, 31, 0.75);
  --glass-border: rgba(255, 255, 255, 0.08);
  --glass-border-hover: rgba(0, 212, 170, 0.35);

  /* Primary Brand Accent (INDMoney Vibrant Emerald / Cyan) */
  --accent-cyan: #00D4AA;
  --accent-cyan-hover: #00F5C4;
  --accent-cyan-dim: rgba(0, 212, 170, 0.12);
  --accent-blue: #2F6FED;

  /* Status & Guardrail Accents */
  --status-refusal: #FF5A5F;     /* Advice rejection & safety boundary */
  --status-refusal-dim: rgba(255, 90, 95, 0.12);
  --status-warning: #FFB300;     /* Unverified facts / caution */
  --status-warning-dim: rgba(255, 179, 0, 0.12);
  --status-verified: #00D4AA;    /* Verified official facts */

  /* Typography Colors */
  --text-primary: #F3F5F9;       /* High emphasis titles & answers */
  --text-secondary: #94A3B8;     /* Supporting metadata & labels */
  --text-muted: #64748B;         /* Footers, timestamps, and placeholders */
  --text-inverse: #07090E;

  /* Elevation & Glow Shadows */
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.4);
  --shadow-card: 0 8px 24px -4px rgba(0, 0, 0, 0.6), 0 0 0 1px var(--glass-border);
  --shadow-glow-cyan: 0 0 20px -2px rgba(0, 212, 170, 0.25);
  --shadow-glow-refusal: 0 0 20px -2px rgba(255, 90, 95, 0.25);
}
```

---

## 3. Typography Scale & Font Tokens

The typography utilizes **Inter** (fallback: system sans-serif) for tabular numerical clarity and readability.

| Token Name | Font Size | Line Height | Weight | Usage |
| :--- | :--- | :--- | :--- | :--- |
| `--font-display` | `24px` / `1.5rem` | `1.2` | `700` (Bold) | Header / Title Banner |
| `--font-heading` | `18px` / `1.125rem` | `1.3` | `600` (SemiBold) | Welcome Card Title, Modal Header |
| `--font-body-lg` | `15px` / `0.9375rem` | `1.55` | `400` (Regular) | Assistant Factual Responses |
| `--font-body-sm` | `13px` / `0.8125rem` | `1.45` | `400` / `500` | User Input, Example Pills |
| `--font-caption` | `11px` / `0.6875rem` | `1.3` | `600` (Mono/Uppercase)| "LAST UPDATED", Verification Badges |

---

## 4. Spacing & Layout Tokens

```css
:root {
  --space-2xs: 4px;
  --space-xs:  8px;
  --space-sm:  12px;
  --space-md:  16px;
  --space-lg:  24px;
  --space-xl:  32px;
  --space-2xl: 48px;

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-pill: 9999px;
}
```

---

## 5. Core Component Behaviors

### 5.1 Header Component
* Fixed at top of viewport with `backdrop-filter: blur(20px)` and bottom border `1px solid var(--glass-border)`.
* Contains INDMoney badge + "Facts-Only Mutual Fund Assistant" title.
* Dynamic status indicator pill showing active model (e.g. `Gemini 2.5 Flash • Active`).

### 5.2 Welcome Card & Quick Example Pills
* Centered informational card explaining the facts-only mandate.
* Three clickable pills with subtle borders:
  1. *"What is the minimum SIP for Mirae Asset Large Cap Fund?"*
  2. *"Does Mirae Asset ELSS Tax Saver Fund have a lock-in period?"*
  3. *"What is the exit load for Mirae Asset Midcap Fund?"*
* **Hover Interaction:** Glows with `--accent-cyan-dim` and shifts translateY(-1px).

### 5.3 Chat Area & Message Bubbles
* **User Message:** Right-aligned, dark surface with subtle blue gradient outline, concise text.
* **Assistant Factual Message:** Left-aligned card with emerald verification tag:
  * 3 concise sentences maximum.
  * Verified citation box with clickable hyperlink: `Source: [Official Document Title] ↗`.
  * Monospace metadata: `Last updated from sources: [DATE]`.
* **Assistant Refusal Message (Advice / PII):** Left-aligned card with subtle crimson border (`--status-refusal`), explaining facts-only scope with zero recommendation.

### 5.4 Input Bar & Action Triggers
* Pill-shaped container floating at the bottom with high z-index.
* Integrated character count, clear button, and Send button that illuminates with `--accent-cyan` when query is typed.
* Keyboard submission via `Enter` (disabled while generating).

### 5.5 Persistent Footer Disclaimer
* Pinned beneath the input bar:
  > **"Facts-only. No investment advice. Official sources only."**
