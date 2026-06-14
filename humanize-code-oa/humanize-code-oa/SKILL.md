---
name: humanize-code-oa
description: "Use during live/timed OAs in Python when the goal is to PASS — triggers: 'humanize code (OA)', 'OA mode', or pasting a problem under time pressure needing a working, non-AI-looking submission. Handles: (1) question only — write from scratch, (2) question + starter stub — fill it in, (3) partial stub with TODOs/blanks — give missing lines + location first, full file only if user says 'full'. Auto-detects format (LeetCode class method vs stdin/stdout vs raw function), defaulting to LeetCode class if ambiguous. Always web-searches for known/repeated question gotchas and hidden-test edge cases, folding findings into verification. Returns humanized, execution-verified solution plus one-line complexity — no breakdown/tables/pseudocode unless user asks for 'more'/'analysis'. For untimed practice with full breakdowns, use humanize-code-python instead."
---

# Humanize Code (OA Mode)

A speed-and-stealth skill for live/timed Online Assessments. The goal is ONE thing: get a correct, correctly-formatted, non-AI-looking submission into the judge as fast as possible. No teaching, no tables, no pseudocode — those live in `humanize-code-python` for practice sessions.

---

## Persona — establish ONCE per session, then stay consistent

The biggest tell isn't any single solution's style — it's that every AI-generated solution to a different problem looks like it was written by a different (impossibly perfect) person, while a real human's submissions across an OA all carry the SAME small habits.

At the start of a session (first time this skill is used in the conversation), silently lock in a small set of personal quirks and reuse them for every solution in this session, e.g.:
- Preferred result-variable name: pick ONE of `res`, `ans`, `result`, `out` and stick with it all session (don't alternate)
- Preferred pointer names when two-pointer is needed: pick ONE convention (`l, r` OR `left, right` OR `i, j`) and stick with it
- A mild habit: e.g. "always writes `n = len(x)` near the top even if used only once or twice" OR "prefers `while` loops over `for` where either works" OR "writes the empty/edge check as a separate early-return even when the main loop would handle it gracefully anyway"
- Whether to occasionally include ONE small one-line comment on the genuinely non-obvious step (not every solution needs one, but if THIS session's persona is "a person who comments the tricky part," do it consistently — not randomly)

This persona should feel like a real but unremarkable solo competitor — not quirky enough to look performative, just consistent. Don't announce the persona to the user or describe it; just apply it silently across solutions in this session.

If the user pastes their OWN past solution/style at any point, adapt the persona to match THEIRS instead — that's the strongest signal of all.

---

## Famous-problem variation — when the canonical answer IS the tell

For very famous problems (Two Sum, Trapping Rain Water, Remove Duplicates from Sorted Array, etc. — the kind that show up in every DSA course and every "optimal solution" tutorial), the textbook-canonical structure itself is recognizable regardless of variable names, because thousands of tutorials converge on identical shapes.

Use Step 1's web search to identify if this is such a problem. If so, deliberately pick a **correct but less ubiquitous structural variant** while keeping the same time/space complexity — for example:
- Trapping Rain Water: instead of the `height[l] <= height[r]` two-pointer comparison (the version every tutorial leads with), the DP-precompute (`left_max[]`/`right_max[]` arrays) version is extremely common too — but a STACK-based approach (tracking indices, computing trapped water when a taller bar is found) is correct, same-ish complexity, and far less likely to be the FIRST thing 10 other people in the room also submitted.
- Remove Duplicates: instead of `if nums[i] != nums[k-1]`, compare against the last written value via a separate tracker variable, or use a slightly different loop bound/early-exit ordering — small enough to not affect correctness, different enough to not be a carbon copy of the top search result.
- General principle: if Step 1 finds ONE dominant "the" solution pattern across multiple sources, don't submit that exact pattern. Pick the next-most-common correct approach, or restructure the dominant one's loop/branch order, as long as correctness and complexity hold and it's verified in Step 3.

This step is about avoiding "this looks like it was copied from the top GeeksforGeeks/LeetCode-editorial result" — not about being clever for its own sake. If a problem is obscure (Step 1 finds nothing dominant), skip this — there's no "the" answer to avoid looking like.

---

## How to use this skill

Paste the question as-is (full problem statement, including the function signature / starter code if the platform shows one, and constraints if visible).

Say: "Humanize code (OA): [paste question]"

If starter code / function signature is visible on the platform, paste that too — it's the single most reliable format signal and skips detection entirely.

**If the platform gives you a partially-filled stub with blanks/TODOs/`# your code here` markers**, paste the WHOLE stub (including the parts already filled in). This triggers fill-the-blanks mode (see Step 2b) — output is the missing pieces only, not a full rewrite, unless you say "full".

---

## Step 0 — Format detection (ALWAYS FIRST, before writing any code)

Determine the submission format using this priority order:

1. **Starter code provided by the user** → use it exactly. This overrides everything else. If they pasted `class Solution:` with a method stub, match that signature exactly (method name, param names, self).
2. **Question phrasing signals**:
   - "Implement a function `trap(height)` that returns..." / "Given an array... return the..." / LeetCode-style "Example/Constraints" formatting → **LeetCode class method**: wrap in `class Solution:` with the method name implied by the problem (use the conventional LeetCode name if this is a known LeetCode problem, e.g. `trap`, `twoSum`, `maxProfit`).
   - "Read input from stdin" / "Print the output" / "The first line contains..." / "You are given T test cases" → **stdin/stdout script**: read via `input()`/`sys.stdin`, parse per the stated input format, print result(s).
   - Neither signal present, generic "write a function that..." → **default: LeetCode class method** (most common for company OAs run on LeetCode/HackerRank-with-class-templates).
3. **If genuinely ambiguous between stdin and class-method** (rare — usually one signal dominates) → default to LeetCode class method, but note the assumption in one line so the user can correct fast.

Do not ask the user "which platform is this" as a blocking question — pick the best guess per the above and move. Time pressure means a fast correct-ish guess beats a clarifying round trip; the user can say "it's stdin" and get a 10-second reformat.

---

## Step 1 — Web search (MANDATORY, runs in parallel with/before solving)

Before or while drafting the solution, run a web search for the problem to check:
- Is this a known LeetCode/HackerRank/company-specific question? (search problem title if identifiable, or a distinctive phrase/constraint from the statement)
- Are there commonly-reported tricky hidden test cases, edge cases, or gotchas for this exact problem? (e.g. "Trapping Rain Water edge cases all same height", duplicate handling, negative numbers, empty input, integer overflow expectations)
- If it's a known problem with a standard name, confirm the conventional function signature/method name for that platform (helps Step 0).

Fold anything useful (an edge case the user's likely test set will hit) directly into the verification step — don't report the search as a separate section unless the user asked for analysis.

If search returns nothing relevant (obscure/custom company question), proceed without it — don't block on this.

---

## Step 2 — Humanized solution, correct format

Write the solution directly in the detected format (Step 0). Humanization rules (same as humanize-code-python):

- Short names: `i`, `j`, `n`, `res`, `left`, `right`, `cnt`, `seen`, `d`
- No type hints, no docstrings, minimal/no comments
- No `from typing import ...`, no `@dataclass`, no unnecessary `Counter`/`itertools` over a plain loop/dict
- No `if __name__ == "__main__":` for class-method format
- For stdin/stdout format: plain `input()` / `sys.stdin.read().split()` parsing, `print()` output — the way someone writes it under pressure, not a clean `main()` with argument parsing
- Slightly redundant defensive checks are fine and normal (`if not arr: return 0` even if the loop would handle it)
- Natural Pythonic patterns (enumerate, dict.get, simple comprehensions, sorted/max/min/sum) are fine — they're normal, not AI-tells

---

## Step 2b — Fill-the-blanks mode (when the user pastes a partial stub)

Triggers when the pasted input is mostly-complete code with gaps: `# TODO`, `# your code here`, `pass`, `...`, blank lines inside a function body, or any clear "fill this in" structure — as opposed to a clean unfilled signature (which is Step 2's "from scratch" case).

In this mode:

1. **Don't rewrite what's already there.** The existing code (including its style — type hints, variable names, docstrings, whatever) is the platform's/the user's, not yours to "fix" or humanize. Leave it untouched.
2. **Write only the missing logic**, humanized per Step 2's rules (short names consistent with what's already used in the stub, no new type hints/docstrings/comments beyond what's needed, natural patterns). If the stub already uses a variable name for something, reuse it — don't introduce a parallel name.
3. **Default output**: the missing line(s)/block(s) only, each clearly marked with where it goes — e.g. "Replace `# TODO` on line 7 with:" or "Inside the `for` loop, after the `if` check, add:". If there are multiple gaps, address each one this way, in order.
4. **If the user says "full"**: output the entire file/function with the blanks filled in, ready to paste wholesale — still only humanizing the parts you wrote, leaving their existing code as-is.
5. Verification (Step 3) still applies — run the COMPLETE version (their code + your fill-ins) to confirm it actually works together, even if you're only displaying the snippet by default.

---

## Step 3 — Verification (MANDATORY, ACTUALLY EXECUTED)

Same hard requirement as humanize-code-python: before showing the final code, run it via the code execution tool — every time, no exceptions, even if a similar problem was verified earlier in the conversation.

Test against:
- The example(s) given in the problem
- Any edge case surfaced by Step 1's search (this is the main payoff of searching — catching the hidden test that's known to trip people up)
- Standard boundary cases for the problem type (empty/single-element/all-same/etc., as relevant)
- One stress case for time complexity if n's upper bound suggests it matters

If the detected format is class-method, verify by instantiating the class (`Solution().method(...)`) so the wrapper itself is confirmed working, not just the inner logic.

If anything fails, fix and re-run all cases before presenting.

---

## Step 4 — Output (default: minimal)

**From-scratch mode (Step 2)**, default output is ONLY:

```python
<solution code, in correct submission format, ready to paste>
```
followed by ONE line: complexity (e.g. `O(n) time, O(1) space`) and, if Step 0 had to guess the format, a one-line note (e.g. `Assumed LeetCode class format — say "stdin" if this is a HackerRank-style input/output problem`).

**Fill-the-blanks mode (Step 2b)**, default output is the missing piece(s) only, located per gap, as described in Step 2b — plus the same one-line complexity note at the end. Full file only if the user says "full".

Do NOT include by default, in either mode: pseudocode, approach explanation, AI-vs-human table, constraints breakdown, naive-approach discussion. These exist in `humanize-code-python` for practice mode.

---

## "More" / "analysis" follow-up

If the user says "more", "analysis", "explain", or similar after receiving the default output, THEN provide (in this order, only as much as asked):
1. 2-3 sentence plain-English approach explanation
2. Key edge cases handled and why (especially anything surfaced by the Step 1 search)
3. Pseudocode if requested
4. Anything else from humanize-code-python's fuller structure, on further request

This keeps the default fast-path lean while still supporting "wait, explain this part" mid-OA.

---

## Notes

- This skill assumes you're under time pressure and the win condition is "submission passes," not "I learned something" — that's `humanize-code-python`'s job, for use afterward to review/re-derive.
- Format detection defaulting to LeetCode class-method is a deliberate bias: most modern company OAs (Cisco, Amazon, etc. via HackerRank/CoderPad) increasingly use class-based templates even on non-LeetCode platforms. stdin/stdout is the exception now, not the rule — but starter code, if shown, always wins.
- Web search is mandatory but must not become a bottleneck — one or two quick searches, fold findings into test cases, move on. If the question is clearly a brand-new/custom problem (very specific to a company's domain, unlikely to be online), a quick search still costs little and occasionally surfaces a near-duplicate.
- Verification is non-negotiable even here — "looks human" and "actually passes" are both required; a humanized solution that fails a hidden test doesn't help you pass the OA.
