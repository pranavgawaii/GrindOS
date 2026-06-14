---
name: humanize-code-oa-multilang
description: "Use during live/timed OAs in a language OTHER THAN PYTHON (Java, C++, C, JS, TS, Go, C#, etc.) — triggers: 'humanize code (Java)', 'OA mode C++', or pasting a problem with the language stated. If no language given, ASK once — don't assume; for Python use humanize-code-oa instead. Handles: (1) question only — write from scratch, (2) question + stub — fill it in, (3) partial stub with TODOs/blanks — give missing lines + location, full file only on 'full'. Auto-detects format (class-based like LeetCode 'class Solution', stdin/stdout with Scanner/cin/readline, or raw function) per that language's convention, defaulting to LeetCode-style class wrapper if ambiguous. Always web-searches for known/repeated question gotchas. Returns humanized, idiomatic-for-that-language solution, execution-verified where the sandbox supports it (Java cannot be compiled — state this and verify by manual trace instead), plus one-line complexity — no breakdown unless user asks for 'more'/'analysis'."
---

# Humanize Code (OA Mode — Multi-Language)

A speed-and-stealth skill for live/timed Online Assessments in languages other than Python (Java, C++, C, JavaScript, TypeScript, Go, C#, etc.). Same goal as `humanize-code-oa`: a correct, correctly-formatted, non-AI-looking submission, fast. For Python, use `humanize-code-oa` (or `humanize-code-python` for untimed practice) instead — this skill is specifically for everything else.

---

## How to use this skill

State the language explicitly along with the question — e.g. "Humanize code (Java): [paste question]" or "OA mode, C++: [paste question]".

If no language is stated and the problem doesn't make it obvious (e.g. a pasted Java stub), ASK once which language — don't guess and don't default to Python here (Python has its own skill). A quick "which language — Java, C++, JS, something else?" costs seconds; guessing wrong costs a full rewrite.

If starter code / function signature is visible on the platform, paste that too — it's the strongest format signal and usually also confirms the language.

**If the platform gives a partially-filled stub with blanks/TODOs/comments like `// your code here`**, paste the WHOLE stub. This triggers fill-the-blanks mode (Step 2b) — output is the missing pieces only, located precisely, unless "full" is requested.

---

## Step 0 — Format detection (ALWAYS FIRST, before writing any code)

Determine the submission format using this priority order:

1. **Starter code provided by the user** → use it exactly, including class/method names, access modifiers, imports already present. This overrides everything else.
2. **Question phrasing signals**:
   - "Implement a method/function `X` that returns..." / LeetCode-style "Example/Constraints" → **class-based wrapper** matching that language's LeetCode convention (e.g. Java: `class Solution { public int trap(int[] height) { ... } }`; C++: `class Solution { public: int trap(vector<int>& height) { ... } };`).
   - "Read input from stdin" / "Print the output" / "The first line contains..." → **stdin/stdout program** using that language's standard input pattern (Java: `Scanner` or `BufferedReader`; C++: `cin`/`cout`; JS: `readline`/`process.stdin`; Go: `bufio.Scanner`; etc.) with a `main` function as required by the language.
   - Neither signal clear → **default: LeetCode-style class wrapper** for the stated language (most common for company OAs).
3. If ambiguous, note the assumption in one line so the user can correct fast — don't block on a round trip.

---

## Step 1 — Web search (MANDATORY, runs before/alongside solving)

Same as the Python OA skill:
- Check if this is a known LeetCode/HackerRank/company-specific question (search by title or distinctive phrasing/constraints).
- Look for commonly-reported tricky edge cases or hidden-test gotchas for this exact problem.
- If known, confirm the conventional method/class name and signature for that language on that platform (helps Step 0).

Fold findings into verification (Step 3) test cases. Don't report search as a separate section unless asked for analysis. If nothing relevant turns up, proceed without blocking.

---

## Step 2 — Humanized solution, correct format

Write the solution directly in the detected format and language. General humanization principles — "how a competent person writes under 15-20 minute time pressure, not how a textbook or AI writes":

- Short, conventional variable names for that language's culture (`i`, `j`, `n`, `res`, `left`, `right`, `cnt`, `tmp` — these are normal everywhere, not just Python)
- Minimal comments — none, or one on the genuinely tricky line
- No over-engineering: no extra helper classes/interfaces, no design patterns, no unnecessary abstraction for a single function
- Use only what's needed — don't import/include libraries "just in case"
- Slightly redundant defensive checks are fine (`if (arr.length == 0) return 0;` even if the loop would handle it) — this is how people actually code under pressure
- Match the verbosity level a self-taught/CS-grad solo competitor would use, not enterprise-codebase conventions

### Per-language AI-tell tables (avoid the left column, write like the right column)

**Java**
| AI-generated tendency | Human under time pressure |
|---|---|
| Full Javadoc comments (`/** ... */`) | No comments, or one inline `//` |
| `private final` fields, getters/setters for a single-use class | Plain fields, direct access, no boilerplate |
| Verbose generic types spelled out everywhere (`HashMap<Integer, Integer>` repeated) | `var` where allowed, or short repeated use without over-explaining |
| Custom exceptions for edge cases | `if` checks returning early, no custom exception classes |
| Stream API for everything (`.stream().map().collect()`) for simple loops | Plain `for` loops — streams only where genuinely natural |

**C++**
| AI-generated tendency | Human under time pressure |
|---|---|
| `using namespace std;` debated, then `std::` everywhere consistently | `using namespace std;` at top, then bare names — very common in competitive code |
| `const&` and `constexpr` annotated everywhere | Plain `&` where needed, skip `const`/`constexpr` unless required |
| Custom structs/classes for simple pairs | `pair<int,int>` or parallel arrays, the quick way |
| Exhaustive `#include` list, alphabetized | `#include <bits/stdc++.h>` (extremely common in competitive C++, an AI rarely defaults to this) |
| Explicit `int64_t`/`size_t` everywhere | Plain `int`/`long long`, cast only where overflow is a real concern |

**JavaScript / TypeScript**
| AI-generated tendency | Human under time pressure |
|---|---|
| Full TS types on every variable, interfaces for simple objects | Minimal/no types (JS) or only function-signature types (TS), no extra interfaces |
| `const { a, b, c } = obj` destructuring even for one-off access | Direct `obj.a` access when it's used once |
| Arrow functions + `.map/.filter/.reduce` chains for everything | Plain `for` loops where a chain would be fiddly to get right fast |
| JSDoc comments | None |
| `===` explained, strict null checks everywhere | `==`/`===` used naturally without commentary, minimal null-guarding beyond what's needed |

**Go**
| AI-generated tendency | Human under time pressure |
|---|---|
| Every error explicitly checked and wrapped (`fmt.Errorf("...: %w", err)`) | `_ = err` or ignored where the OA context guarantees valid input |
| Custom types/structs for simple data | Built-in types, slices, maps directly |
| Full doc comments on every function | None |

**C# / others**: apply the same spirit — strip framework ceremony (no LINQ-chain-for-everything, no XML doc comments, no unnecessary `using` statements, plain loops over fluent APIs for simple logic).

---

## Step 2b — Fill-the-blanks mode (partial stub pasted)

Same as the Python OA skill:

1. Don't rewrite existing code — leave the platform's/user's style as-is (even if it's verbose/typed).
2. Write only the missing logic, humanized per Step 2 (reuse variable names already present in the stub).
3. Default output: missing line(s)/block(s) only, each marked with its location (e.g. "Inside the `for` loop in `trap`, replace `// TODO` with:").
4. "full" → entire file/function with blanks filled, ready to paste.
5. Verification still runs on the complete (stub + fill-in) version.

---

## Step 3 — Verification (execute where possible)

**Known sandbox capability**: C++ (g++) and JavaScript/Node are fully compilable/runnable here. **Java is NOT compilable in this sandbox** (JRE present but no `javac`/JDK) — for Java, verification must be done by careful manual trace against all the cases below, and this limitation must be stated explicitly to the user (don't silently skip or imply it was run). Other languages: check availability via the bash tool before claiming execution.

For languages that ARE runnable in-sandbox, actually compile and run the solution against:
- The example(s) from the problem
- Edge cases surfaced by Step 1's search
- Standard boundary cases (empty input, single element, all-same, etc., as relevant)
- One stress case if n's bound suggests performance matters

If the detected format is class-based, verify by instantiating/calling as the judge would (e.g. `new Solution().trap(...)` via a `main`/driver).

**If a language can't be executed in-sandbox** (e.g. Java), say so explicitly in the response, do a careful manual trace through the same case list instead, and flag this clearly — don't silently skip verification or claim it ran.

If anything fails, fix and re-run all cases before presenting.

---

## Step 4 — Output (default: minimal)

**From-scratch mode**: ONLY the solution code in a fenced block with the correct language tag, in correct submission format, ready to paste — followed by ONE line: complexity, plus a one-line note if Step 0 had to guess format/language.

**Fill-the-blanks mode**: missing piece(s) only, located per gap, plus the same one-line complexity note. Full file only on "full".

No pseudocode, approach explanation, AI-vs-human table, or constraints breakdown by default in either mode.

---

## "More" / "analysis" follow-up

On "more"/"analysis"/"explain": 2-3 sentence approach explanation, then key edge cases handled (especially from Step 1's search), then pseudocode if asked, then anything further on request — same staged structure as the Python OA skill.

---

## Notes

- This is the non-Python counterpart to `humanize-code-oa`. If the user says "Python" or doesn't specify and Python is clearly implied by context, redirect to that skill instead of using this one.
- Per-language AI-tell tables above are starting points, not exhaustive — if the user's pasted stub already shows a particular house style (e.g. their company's Java style guide leaks through), match THAT over the generic table; consistency with what's already there beats generic "human-ness."
- Verification standards are the same as the Python skill: non-negotiable, must be real execution wherever the sandbox supports the language, every time.
- If the user frequently OAs in one specific non-Python language, consider noting that as a preference so format-detection defaults can lean that way without asking each time.
