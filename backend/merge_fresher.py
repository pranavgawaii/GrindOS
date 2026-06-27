import os
import re

ROOT = "/Users/8teen/Downloads/04_/Active/GrindOS"
FRONTEND = os.path.join(ROOT, "frontend")

# Read notebook
with open(os.path.join(ROOT, "interview_notes_notebook.html"), "r") as f:
    notebook_content = f.read()

# Extract notebook styles, wrap, and script
nb_style_match = re.search(r'<style>(.*?)</style>', notebook_content, flags=re.DOTALL)
nb_style = nb_style_match.group(1) if nb_style_match else ""

nb_wrap_match = re.search(r'(<div class="nb-wrap">.*?</div>\n</div>\n</div>\n</div>\n\n)', notebook_content, flags=re.DOTALL)
if not nb_wrap_match:
    # Try alternate match if the above failed
    nb_wrap_match = re.search(r'(<div class="nb-wrap">.*?</div>\s*<script>)', notebook_content, flags=re.DOTALL)
    if nb_wrap_match:
        nb_wrap = nb_wrap_match.group(1).replace('<script>', '')
    else:
        # Fallback to everything between body tags or after style
        nb_wrap = notebook_content.split('</style>')[1].split('<script>')[0]
else:
    nb_wrap = nb_wrap_match.group(1)

nb_script_match = re.search(r'<script>(.*?)</script>', notebook_content, flags=re.DOTALL)
nb_script = nb_script_match.group(1) if nb_script_match else ""

# Premium Daily Check-In HTML
checkin_html = """
    <div class="dashboard-header-row" style="margin-top: 2rem;">
      <div class="dashboard-title-area">
        <h2>Daily Check-In</h2>
        <p>Maintain your streak. Log your daily progress, learnings, and any blockers here.</p>
      </div>
      <div class="dashboard-meta-badges">
        <span class="meta-badge" style="background: var(--brand-light); color: var(--brand); border-color: var(--brand-glow);">
          <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2.5" fill="none"
            stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px;">
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
          Current Streak: <strong id="streak-counter" style="margin-left:4px;">12 Days</strong>
        </span>
      </div>
    </div>
    
    <div class="checkin-container" style="max-width: 800px; margin-top: 2rem; margin-bottom: 4rem;">
      <div class="glass-card stat-card" style="display: flex; flex-direction: column; gap: 1.5rem; padding: 2rem; border-top: 4px solid var(--brand);">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.5rem;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: var(--brand-light); display: flex; align-items: center; justify-content: center; color: var(--brand);">
                <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 20h9"></path>
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                </svg>
            </div>
            <div>
                <h3 style="margin: 0; font-size: 1.1rem; color: var(--text-1);">What did you accomplish today?</h3>
                <p style="margin: 0; font-size: 0.85rem; color: var(--text-3);">Be specific about DSA patterns, Dev features, or CS theory covered.</p>
            </div>
        </div>
        
        <textarea id="checkin-input" placeholder="Example: Today I solved 3 Sliding Window problems on LeetCode and built the authentication flow for my Next.js project..." style="width: 100%; min-height: 180px; padding: 1.25rem; border: 1px solid var(--border); border-radius: 12px; background: var(--bg); color: var(--text-1); font-family: var(--font-sans); resize: vertical; font-size: 0.95rem; line-height: 1.6; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); transition: border-color 0.2s, box-shadow 0.2s;"></textarea>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 0.85rem; color: var(--text-4);">Supports markdown formatting</div>
            <button id="submit-checkin" style="padding: 0.75rem 2rem; background: var(--brand-gradient); color: white; border: none; border-radius: 99px; cursor: pointer; font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 12px var(--brand-glow); transition: all 0.2s; display: flex; align-items: center; gap: 8px;">
                <span>Submit Entry</span>
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
            </button>
        </div>
      </div>
    </div>
"""

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <script>
    (function() {{
      const saved = localStorage.getItem('GrindOS-theme');
      if (saved) {{
        document.documentElement.classList.add(saved);
      }} else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {{
        document.documentElement.classList.add('dark');
      }}
    }})();
  </script>
  <title>Fresher Notebook — GrindOS</title>
  <link rel="stylesheet" href="frontend/assets/style.css">
  <link rel="icon" type="image/png" href="frontend/logo.png">
  <style>
    /* Notebook specific styles */
    {nb_style}
    
    /* Checkin specific styles */
    #checkin-input:focus {{
        outline: none;
        border-color: var(--brand);
        box-shadow: 0 0 0 3px var(--brand-glow), inset 0 2px 4px rgba(0,0,0,0.02) !important;
    }}
    #submit-checkin:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px var(--brand-glow) !important;
    }}
  </style>
</head>
<body>

  <header class="topbar">
    <a href="frontend/dashboard.html" class="topbar-brand">
      <img src="frontend/logo.png" alt="GrindOS Logo" class="brand-logo"
        style="width: 34px; height: 34px; object-fit: contain; border-radius: 4px; flex-shrink: 0; display: inline-block; vertical-align: middle; margin-right: 4px;">
      <span class="brand-wordmark">GrindOS</span>
    </a>
    <nav class="topbar-nav">
      <a href="frontend/dashboard.html" class="learn-nav">Learn</a>
      <a href="frontend/notes.html" class="notes-nav">Notes</a>
      <a href="frontend/tracker.html" class="tracker-nav">Tracker</a>
      <a href="frontend/practice.html" class="practice-nav">Practice</a>
      <a href="frontend/resume-builder.html" class="resume-nav">Resume</a>
      <a href="htmlfresher.html" class="checkin-nav active" style="display:inline-block;">Check In & Notes</a>
    </nav>
    <div class="topbar-right">
      <button class="icon-btn" id="theme-toggle" aria-label="Toggle theme"><span class="theme-icon">☾</span></button>
      <div id="clerk-user-widget"></div>
    </div>
  </header>

  <div class="dashboard" style="max-width: 1200px; margin: 0 auto; padding-top: 80px;">
    {checkin_html}
    
    <div class="dashboard-header-row" style="margin-top: 2rem;">
      <div class="dashboard-title-area">
        <h2>Interview Notes Notebook</h2>
        <p>Your complete guide and personalized notes.</p>
      </div>
    </div>
    
    <div class="glass-card stat-card" style="padding: 2rem; margin-top: 2rem; border-top: 4px solid var(--brand);">
      {nb_wrap}
    </div>
  </div>

  <script src="frontend/assets/script.js"></script>
  <script>
    {nb_script}
  </script>
</body>
</html>
"""

with open(os.path.join(ROOT, "htmlfresher.html"), "w") as f:
    f.write(full_html)

print("Successfully merged!")
