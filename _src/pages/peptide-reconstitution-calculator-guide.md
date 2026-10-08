title: Peptide Reconstitution Calculator: How to Calculate Doses (2026 Guide)
description: How peptide reconstitution math actually works: concentration, syringe units, and worked examples — plus a free Android calculator that does it for you.
path: blog/peptide-reconstitution-calculator-guide.html
date: 2026-10-08
type: article
---
# Peptide Reconstitution Calculator: How the Math Works (With Examples)

Reconstitution math is where most tracking mistakes happen. The formula itself is simple —
the errors come from unit conversions (mg vs mcg) and from translating a volume into marks
on an insulin syringe. This guide walks through the math step by step, with worked examples,
so you can sanity-check any calculator — including ours.

**Note:** this article explains arithmetic only. It does not recommend doses, compounds, or
protocols. Your amounts come from you and your licensed healthcare provider.

## Step 1: Concentration

When you add bacteriostatic (BAC) water to a lyophilized vial:

```
concentration (mg/mL) = vial amount (mg) ÷ BAC water added (mL)
```

**Example:** a 5 mg vial + 2 mL of BAC water → 5 ÷ 2 = **2.5 mg/mL** (which is 2,500 mcg/mL).

## Step 2: Volume per dose

```
volume (mL) = dose (mg) ÷ concentration (mg/mL)
```

**Example:** a 0.25 mg dose at 2.5 mg/mL → 0.25 ÷ 2.5 = **0.1 mL**.

## Step 3: Convert volume to insulin syringe units

Insulin syringes are marked in "units" where **100 units = 1 mL** (U-100):

```
units = volume (mL) × 100
```

So 0.1 mL = **10 units** on a U-100 syringe. On a 30-unit or 50-unit syringe the scale is
the same — the barrel is just smaller, so the marks are further apart and easier to read
for small volumes.

## The three mistakes that cause most errors

1. **mg/mcg confusion.** 1 mg = 1,000 mcg. A dose written in mcg divided by a concentration
   in mg/mL without converting gives an answer off by 1,000×. Always convert to the same
   unit first.
2. **"Units" ≠ dose.** Syringe units measure *volume*, not compound. 10 units of a
   2.5 mg/mL solution and 10 units of a 5 mg/mL solution contain different amounts.
   If you change how much water you add, your draw changes too.
3. **Losing track of reconstitution dates.** Reconstituted peptides don't last forever.
   If you don't log the date you mixed a vial, you're guessing at freshness weeks later.

## Worked example, end to end

- Vial: 10 mg. BAC water added: 3 mL.
- Concentration: 10 ÷ 3 = 3.33 mg/mL.
- Desired dose: 500 mcg = 0.5 mg.
- Volume: 0.5 ÷ 3.33 = 0.15 mL.
- Syringe: 0.15 × 100 = **15 units** on a U-100 syringe.

## Or skip the math entirely

PepMinder (free on Android) does all of the above in one screen: enter vial size, water
volume, and dose, and it shows mg/mL, mcg/mL, units to draw, and a **visual syringe diagram**
with the fill line marked for 30, 50, and 100-unit syringes. It also logs when you
reconstituted each vial and flags vials that are expiring — the two things a plain calculator
can't do.

Everything stays on your device: no account, no cloud.

[[CTA]]
