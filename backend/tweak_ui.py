import re

# 1. Fix tracker.html (mastery glass and tickbox)
tracker_file = "/Users/8teen/Downloads/04_/Active/GrindOS/frontend/tracker.html"
with open(tracker_file, 'r') as f:
    tracker = f.read()

# Replace the full-width fixed footer with a floating pill
tracker = tracker.replace(
    '.mastery-glass { position:fixed; bottom:0; left:0; right:0; z-index:100; margin:0; background:rgba(24,24,27,0.85); padding:1rem 2rem; border-top:1px solid var(--border); backdrop-filter:blur(24px); box-shadow: 0 -4px 15px rgba(0,0,0,0.2); }',
    '.mastery-glass { position:fixed; bottom:32px; left:50%; transform:translateX(-50%); z-index:1000; width:400px; max-width:90%; background:rgba(15,15,18,0.7); padding:12px 24px; border-radius:9999px; border:1px solid rgba(255,255,255,0.08); backdrop-filter:blur(24px) saturate(200%); -webkit-backdrop-filter:blur(24px) saturate(200%); box-shadow: 0 16px 40px rgba(0,0,0,0.4), inset 0 1px 1px rgba(255,255,255,0.05); }'
)

# Remove the gradients/shadows from the checked tickbox
if '.t-cb.checked {' not in tracker:
    tracker = tracker.replace('</style>', '.t-cb.checked { background: #3B6D11 !important; border-color: #3B6D11 !important; box-shadow: none !important; }\n</style>')

with open(tracker_file, 'w') as f:
    f.write(tracker)

# 2. Fix interview_qa.html (hero component redesign)
qa_file = "/Users/8teen/Downloads/04_/Active/GrindOS/frontend/interview_qa.html"
with open(qa_file, 'r') as f:
    qa = f.read()

old_hero = '''<div class="qa-hero">
            <h1>Ultimate Interview Q&A</h1>
            <p>Don't just answer the question — dominate it. These are high-yield questions across all CS domains, formulated with premium interview strategies that signal deep expertise.</p>
        </div>'''

new_hero = '''<div class="qa-hero" style="display: flex; align-items: center; justify-content: center; gap: 16px; margin-bottom: 2rem; background: var(--surface-1); border: 1px solid var(--border); padding: 1.25rem 1.5rem; border-radius: 16px; width: fit-content; margin-left: auto; margin-right: auto; box-shadow: inset 0 1px 2px rgba(255,255,255,0.02), 0 4px 12px rgba(0,0,0,0.1);">
            <div style="width: 44px; height: 44px; border-radius: 12px; background: linear-gradient(145deg, var(--surface-2), var(--surface-0)); border: 1px solid var(--border-strong); display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                <i class="ti ti-bulb" style="font-size: 24px; color: var(--brand);"></i>
            </div>
            <div style="text-align: left;">
                <h1 style="font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin: 0; letter-spacing: -0.01em;">Interview Q&A Bank</h1>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin: 2px 0 0 0; max-width: 320px; line-height: 1.4;">Master the top CS questions with premium strategies.</p>
            </div>
        </div>'''

qa = qa.replace(old_hero, new_hero)

with open(qa_file, 'w') as f:
    f.write(qa)

print("UI Tweaks applied.")
