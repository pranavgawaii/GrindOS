// ── GrindOS Platform — Script ──────────────────────────────────────────────────

(function () {
  // ── Vercel Analytics Dynamic Injection ─────────────────────────────────────
  (function() {
    if (!window.va) {
      window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
      const script = document.createElement('script');
      script.src = '/_vercel/insights/script.js';
      script.defer = true;
      document.head.appendChild(script);
    }
  })();

  // ── Theme ─────────────────────────────────────────────────────────────────
  const html = document.documentElement;
  const saved = localStorage.getItem('GrindOS-theme');
  if (saved) {
    html.classList.add(saved);
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    html.classList.add('dark');
  }



  const sunIcon = `<svg class="theme-icon-svg" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="color: var(--brand); filter: drop-shadow(0 0 3px var(--brand-glow));"><circle cx="12" cy="12" r="4" fill="currentColor"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path></svg>`;
  const moonIcon = `<svg class="theme-icon-svg" viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2.2" fill="currentColor" stroke-linecap="round" stroke-linejoin="round" style="color: var(--brand); filter: drop-shadow(0 0 3px var(--brand-glow));"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;

  function setTheme(t) {
    if (t === 'dark') {
      html.classList.add('dark');
      html.classList.remove('light');
    } else {
      html.classList.add('light');
      html.classList.remove('dark');
    }
    localStorage.setItem('GrindOS-theme', t || (html.classList.contains('dark') ? 'dark' : 'light'));
    document.querySelectorAll('#theme-toggle, .theme-switch, .theme-switchatt').forEach(el => {
      if (el.classList.contains('theme-switchatt')) {
        const svg = el.querySelector('.att-svg');
        const maskCircle = el.querySelector('.att-mask-circle');
        const centerCircle = el.querySelector('.att-center-circle');
        const rays = el.querySelector('.att-rays');
        if (svg && maskCircle && centerCircle && rays) {
          if (t === 'dark') {
            svg.style.transform = 'rotate(270deg)';
            maskCircle.setAttribute('cx', '17');
            maskCircle.setAttribute('cy', '8');
            centerCircle.setAttribute('r', '9');
            rays.style.opacity = '0';
            rays.style.transform = 'scale(0) rotate(-30deg)';
          } else {
            svg.style.transform = 'rotate(0deg)';
            maskCircle.setAttribute('cx', '33');
            maskCircle.setAttribute('cy', '0');
            centerCircle.setAttribute('r', '5');
            rays.style.opacity = '1';
            rays.style.transform = 'scale(1) rotate(0deg)';
          }
        }
        return;
      }
      if (el.classList.contains('theme-switch')) {
        const sun = el.querySelector('.sun');
        const moon = el.querySelector('.moon');
        if (t === 'dark') {
          if (sun) sun.classList.remove('active');
          if (moon) moon.classList.add('active');
        } else {
          if (sun) sun.classList.add('active');
          if (moon) moon.classList.remove('active');
        }
      } else {
        el.innerHTML = t === 'dark' ? sunIcon : moonIcon;
      }
    });
  }
  setTheme(saved || (html.classList.contains('dark') ? 'dark' : 'light'));

  document.addEventListener('DOMContentLoaded', function () {

    // ── GrindOS Brand Path Resolver & Rebranding ───────────────────────────
    let rootPath = '';
    const styleLink = document.querySelector('link[rel="stylesheet"]');
    if (styleLink) {
      const href = styleLink.getAttribute('href');
      if (href.includes('assets/style.css')) {
        rootPath = href.split('assets/style.css')[0];
      }
    }
    const logoPath = '/logo.png';

    const path = window.location.pathname.toLowerCase();

    // ══════════════════════════════════════════════════════════════════════════
    // ── SPACED REPETITION ENGINE ──────────────────────────────────────────────
    // ══════════════════════════════════════════════════════════════════════════
    const SRS_KEY = 'GrindOS-srs-topics';
    const SRS_INTERVALS = [1, 3, 7, 14, 30]; // days

    function srsGetAll() {
      try { return JSON.parse(localStorage.getItem(SRS_KEY) || '{}'); } catch { return {}; }
    }
    function srsSave(data) { localStorage.setItem(SRS_KEY, JSON.stringify(data)); }

    function srsMarkComplete(courseId, topicId, topicTitle) {
      const all = srsGetAll();
      const key = `${courseId}__${topicId}`;
      const now = Date.now();
      const existing = all[key] || { firstRead: now, reviewsDone: 0 };
      const reviewsDone = existing.reviewsDone || 0;
      const nextInterval = SRS_INTERVALS[reviewsDone] || SRS_INTERVALS[SRS_INTERVALS.length - 1];
      all[key] = {
        courseId, topicId, topicTitle,
        firstRead: existing.firstRead || now,
        lastReviewed: now,
        reviewsDone: reviewsDone + 1,
        nextReview: now + nextInterval * 86400000,
        completed: true
      };
      srsSave(all);
      // Also mark in GrindOS-completed
      localStorage.setItem(`GrindOS-completed-${courseId}-${topicId}`, 'true');
    }

    function srsIsCompleted(courseId, topicId) {
      return !!localStorage.getItem(`GrindOS-completed-${courseId}-${topicId}`);
    }

    function srsDueToday() {
      const all = srsGetAll();
      const now = Date.now();
      return Object.values(all).filter(t => t.nextReview && t.nextReview <= now + 86400000 && t.reviewsDone < SRS_INTERVALS.length);
    }

    function srsRenderDashboard() {
      const dueList = document.getElementById('revision-due-list');
      const emptyState = document.getElementById('revision-empty-state');
      const noDataState = document.getElementById('revision-no-data-state');
      const countBadge = document.getElementById('revision-count-badge');
      if (!dueList) return;

      const all = srsGetAll();
      const hasAny = Object.keys(all).length > 0;
      const due = srsDueToday();

      if (!hasAny) {
        noDataState.style.display = 'block';
        emptyState.style.display = 'none';
        dueList.style.display = 'none';
        if (countBadge) countBadge.textContent = '';
        return;
      }

      noDataState.style.display = 'none';

      if (due.length === 0) {
        emptyState.style.display = 'block';
        dueList.style.display = 'none';
        if (countBadge) countBadge.textContent = '✅ All clear';
        return;
      }

      emptyState.style.display = 'none';
      dueList.style.display = 'flex';
      if (countBadge) countBadge.textContent = `${due.length} topic${due.length > 1 ? 's' : ''} due`;

      dueList.innerHTML = '';
      due.slice(0, 8).forEach(t => {
        const daysSinceRead = t.lastReviewed ? Math.floor((Date.now() - t.lastReviewed) / 86400000) : '?';
        const reviewLabel = t.reviewsDone === 0 ? 'First Review' : `Review #${t.reviewsDone + 1}`;
        const coursePathMap = { dbms: 'courses/dbms', cn: 'courses/cn', os: 'courses/os', oops: 'courses/oops', dsa: 'courses/dsa', aptitude: 'courses/aptitude', webdev: 'courses/webdev' };
        const coursePath = rootPath + (coursePathMap[t.courseId] || 'courses/' + t.courseId);
        const card = document.createElement('div');
        card.className = 'revision-card';
        card.innerHTML = `
          <div class="revision-card-left">
            <span class="revision-tag ${t.courseId}">${(t.courseId || '').toUpperCase()}</span>
            <div>
              <div class="revision-topic-title">${t.topicTitle || t.topicId}</div>
              <div class="revision-meta">${reviewLabel} &nbsp;·&nbsp; Last read ${daysSinceRead}d ago</div>
            </div>
          </div>
          <div class="revision-card-right">
            <a href="${coursePath}/topics/${t.topicId}.html" class="revision-study-btn">Study Now →</a>
            <button class="revision-done-btn" data-key="${t.courseId}__${t.topicId}">✓ Done</button>
          </div>
        `;
        card.querySelector('.revision-done-btn').addEventListener('click', function() {
          srsMarkComplete(t.courseId, t.topicId, t.topicTitle);
          srsRenderDashboard();
        });
        dueList.appendChild(card);
      });
    }

    // Inject "Mark Complete" button on topic pages
    function srsInjectMarkComplete() {
      // Detect topic page: URL contains /topics/
      const topicMatch = path.match(/\/courses\/([^/]+)\/topics\/([^/]+)\.html/);
      if (!topicMatch) return;
      const courseId = topicMatch[1];
      const topicId = topicMatch[2];
      const topicTitle = document.title.replace(/\s*[—–-]\s*GrindOS\s*/i, '').trim() || topicId;

      const alreadyDone = srsIsCompleted(courseId, topicId);
      const pill = document.createElement('div');
      pill.id = 'srs-complete-pill';
      pill.innerHTML = alreadyDone
        ? `<span class="srs-check">✓</span> Completed`
        : `<span class="srs-check"></span> Mark as Complete`;
      pill.className = alreadyDone ? 'srs-pill srs-pill--done' : 'srs-pill';
      pill.setAttribute('title', alreadyDone ? 'Already completed — click to re-schedule revision' : 'Mark topic as read and schedule revision');

      pill.addEventListener('click', function() {
        srsMarkComplete(courseId, topicId, topicTitle);
        pill.className = 'srs-pill srs-pill--done';
        pill.innerHTML = `<span class="srs-check">✓</span> Completed — Revision Scheduled`;
        setTimeout(() => { pill.innerHTML = `<span class="srs-check">✓</span> Completed`; }, 2500);
      });

      // Insert after the main heading
      const firstH1 = document.querySelector('h1, .topic-title');
      if (firstH1 && firstH1.parentNode) {
        firstH1.parentNode.insertBefore(pill, firstH1.nextSibling);
      } else {
        document.body.insertBefore(pill, document.body.firstChild);
      }
    }

    srsInjectMarkComplete();
    srsRenderDashboard();

    // ══════════════════════════════════════════════════════════════════════════
    // ── MONACO CODE EDITOR — DSA TOPIC PAGES ─────────────────────────────────
    // ══════════════════════════════════════════════════════════════════════════
    const isDSATopic = path.includes('/courses/dsa/topics/');

    if (isDSATopic) {
      // Inject Monaco CSS + loader
      const monacoCSS = document.createElement('link');
      monacoCSS.rel = 'stylesheet';
      monacoCSS.href = 'https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs/editor/editor.main.css';
      document.head.appendChild(monacoCSS);

      // Inject the editor panel HTML
      const editorPanel = document.createElement('div');
      editorPanel.id = 'grindos-code-editor';
      editorPanel.innerHTML = `
        <div class="code-editor-header">
          <div class="code-editor-header-left">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
            <span class="code-editor-title">Code Playground</span>
            <span class="code-editor-badge">Piston Engine</span>
          </div>
          <div class="code-editor-controls">
            <select id="code-lang-select" class="code-lang-select">
              <option value="python">Python 3</option>
              <option value="cpp">C++ 17</option>
              <option value="java">Java 17</option>
              <option value="javascript">JavaScript</option>
              <option value="c">C</option>
            </select>
            <button id="code-run-btn" class="code-run-btn">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              Run
            </button>
            <button id="code-reset-btn" class="code-reset-btn" title="Reset to starter code">↺</button>
          </div>
        </div>
        <div id="monaco-container" style="height:320px; border-bottom:1px solid var(--border);"></div>
        <div class="code-output-area">
          <div class="code-output-header">
            <span>Output</span>
            <span id="code-run-time" class="code-run-time"></span>
          </div>
          <pre id="code-output-pre" class="code-output-pre">// Click ▶ Run to execute your code</pre>
        </div>
      `;
      document.querySelector('.topic-content, main, .topic-body, .content-area, article, .page-content, body > div:last-child') && 
        document.querySelector('.topic-content, main, .topic-body, .content-area, article, .page-content, body > div:last-child').appendChild(editorPanel);
      if (!document.getElementById('grindos-code-editor').parentNode || document.getElementById('grindos-code-editor').parentNode === document.createElement('div')) {
        document.body.appendChild(editorPanel);
      }

      // Starter code templates per language
      const STARTER = {
        python: `# Write your solution here\ndef solve():\n    pass\n\n# Test\nprint(solve())`,
        cpp: `#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    // Write your solution here\n    cout << "Hello, World!" << endl;\n    return 0;\n}`,
        java: `public class Main {\n    public static void main(String[] args) {\n        // Write your solution here\n        System.out.println("Hello, World!");\n    }\n}`,
        javascript: `// Write your solution here\nfunction solve() {\n    \n}\n\nconsole.log(solve());`,
        c: `#include <stdio.h>\n\nint main() {\n    // Write your solution here\n    printf("Hello, World!\\n");\n    return 0;\n}`
      };

      const PISTON_LANG = { python: 'python', cpp: 'c++', java: 'java', javascript: 'javascript', c: 'c' };
      const PISTON_VERSION = { python: '3.10.0', cpp: '10.2.0', java: '15.0.2', javascript: '18.15.0', c: '10.2.0' };
      const MONACO_LANG = { python: 'python', cpp: 'cpp', java: 'java', javascript: 'javascript', c: 'c' };

      let monacoEditor = null;
      let currentLang = 'python';

      // Load Monaco
      const monacoScript = document.createElement('script');
      monacoScript.src = 'https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs/loader.js';
      monacoScript.onload = function() {
        require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs' } });
        require(['vs/editor/editor.main'], function() {
          const isDark = document.documentElement.classList.contains('dark');
          monacoEditor = monaco.editor.create(document.getElementById('monaco-container'), {
            value: STARTER.python,
            language: 'python',
            theme: isDark ? 'vs-dark' : 'vs',
            fontSize: 13.5,
            fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            lineNumbers: 'on',
            roundedSelection: true,
            padding: { top: 12, bottom: 12 },
            automaticLayout: true,
            tabSize: 4,
            wordWrap: 'on',
            cursorBlinking: 'smooth',
            smoothScrolling: true,
            contextmenu: false
          });

          // Watch theme toggle
          new MutationObserver(() => {
            if (!monacoEditor) return;
            monaco.editor.setTheme(document.documentElement.classList.contains('dark') ? 'vs-dark' : 'vs');
          }).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });

          // Lang selector
          document.getElementById('code-lang-select').addEventListener('change', function() {
            currentLang = this.value;
            monaco.editor.setModelLanguage(monacoEditor.getModel(), MONACO_LANG[currentLang]);
            monacoEditor.setValue(STARTER[currentLang]);
          });
        });
      };
      document.head.appendChild(monacoScript);

      // Run button
      document.getElementById('code-run-btn').addEventListener('click', async function() {
        const btn = this;
        const code = monacoEditor ? monacoEditor.getValue() : '';
        const outputEl = document.getElementById('code-output-pre');
        const timeEl = document.getElementById('code-run-time');
        btn.disabled = true;
        btn.innerHTML = `<svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg> Running...`;
        outputEl.textContent = '⏳ Executing...';
        outputEl.style.color = 'var(--text-3)';
        const t0 = Date.now();
        try {
          const res = await fetch('https://emkc.org/api/v2/piston/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              language: PISTON_LANG[currentLang],
              version: PISTON_VERSION[currentLang],
              files: [{ name: 'main', content: code }]
            })
          });
          const data = await res.json();
          const elapsed = ((Date.now() - t0) / 1000).toFixed(2);
          const out = (data.run?.stdout || '') + (data.run?.stderr || '');
          outputEl.textContent = out || '(no output)';
          outputEl.style.color = data.run?.stderr ? '#f87171' : 'var(--text-1)';
          timeEl.textContent = `${elapsed}s`;
        } catch (e) {
          outputEl.textContent = `Network error: ${e.message}`;
          outputEl.style.color = '#f87171';
          timeEl.textContent = '';
        }
        btn.disabled = false;
        btn.innerHTML = `<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg> Run`;
      });

      // Reset button
      document.getElementById('code-reset-btn').addEventListener('click', function() {
        if (monacoEditor) monacoEditor.setValue(STARTER[currentLang]);
        document.getElementById('code-output-pre').textContent = '// Click ▶ Run to execute your code';
        document.getElementById('code-run-time').textContent = '';
      });
    }


    
    document.querySelectorAll('.topbar-brand').forEach(brand => {
      if (path.includes('tracker.html')) {
        brand.innerHTML = `<img src="${logoPath}" alt="GrindOS Logo" class="brand-logo" style="width: 34px; height: 34px; object-fit: contain; border-radius: 50% !important; flex-shrink: 0; display: inline-block; vertical-align: middle; margin-right: 6px;"><span class="brand-wordmark">GrindOS <span style="font-size: 0.82rem; font-weight: 500; color: var(--text-3); margin-left: 8px; padding-left: 8px; border-left: 1px solid var(--border);">Code Arena</span></span>`;
      } else {
        brand.innerHTML = `<img src="${logoPath}" alt="GrindOS Logo" class="brand-logo" style="width: 34px; height: 34px; object-fit: contain; border-radius: 4px; flex-shrink: 0; display: inline-block; vertical-align: middle; margin-right: 4px;"><span class="brand-wordmark">GrindOS</span>`;
      }
    });
    if (/GrindOS|NexusLearn/i.test(document.title)) {
      document.title = document.title.replace(/GrindOS|NexusLearn|GrindOS|GrindOS/gi, 'GrindOS');
    }

    // ── Animated Morphing Theme Toggler & Synthesized Audio ─────────────
    let _ctx = null;
    let _buf = null;

    function audioCtx() {
      if (!_ctx) {
        _ctx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (_ctx.state === "suspended") _ctx.resume();
      return _ctx;
    }

    function ensureBuf(ac) {
      if (_buf && _buf.sampleRate === ac.sampleRate) return _buf;
      const rate = ac.sampleRate;
      const len = Math.floor(rate * 0.006);
      const buf = ac.createBuffer(1, len, rate);
      const ch = buf.getChannelData(0);
      for (let i = 0; i < len; i++) {
        const t = i / len;
        const sine = Math.sin(2 * Math.PI * 3400 * t);
        const noise = Math.random() * 2 - 1;
        ch[i] = (sine * 0.6 + noise * 0.4) * Math.pow(1 - t, 3);
      }
      _buf = buf;
      return buf;
    }

    let lastSnd = 0;
    function playTickSound() {
      const now = performance.now();
      if (now - lastSnd < 80) return;
      lastSnd = now;
      try {
        const ac = audioCtx();
        const buf = ensureBuf(ac);
        const src = ac.createBufferSource();
        const gain = ac.createGain();
        src.buffer = buf;
        gain.gain.value = 0.08;
        src.connect(gain);
        gain.connect(ac.destination);
        src.start();
      } catch (e) {
        /* silent */
      }
    }

    document.querySelectorAll('#theme-toggle').forEach(el => {
      el.className = 'theme-switchatt';
      el.removeAttribute('aria-label');
      
      const attId = 'att_' + Math.random().toString(36).substr(2, 9);
      el.innerHTML = `
        <svg class="att-svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" style="overflow: visible; transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);">
          <mask id="${attId}">
            <rect x="0" y="0" width="100%" height="100%" fill="white" />
            <circle class="att-mask-circle" cx="33" cy="0" r="9" fill="black" style="transition: cx 0.5s cubic-bezier(0.34, 1.56, 0.64, 1), cy 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);" />
          </mask>
          <circle class="att-center-circle" cx="12" cy="12" fill="currentColor" stroke="none" mask="url(#${attId})" r="5" style="transition: r 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);" />
          <g class="att-rays" style="transform-origin: 12px 12px; transition: opacity 0.5s ease, transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);">
            <line x1="12" y1="1" x2="12" y2="3" />
            <line x1="12" y1="21" x2="12" y2="23" />
            <line x1="1" y1="12" x2="3" y2="12" />
            <line x1="21" y1="12" x2="23" y2="12" />
            <line x1="5.64" y1="5.64" x2="4.22" y2="4.22" />
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
            <line x1="5.64" y1="18.36" x2="4.22" y2="19.78" />
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
          </g>
        </svg>
      `;

      const updateSwitchMorph = (theme) => {
        const svg = el.querySelector('.att-svg');
        const maskCircle = el.querySelector('.att-mask-circle');
        const centerCircle = el.querySelector('.att-center-circle');
        const rays = el.querySelector('.att-rays');
        
        if (!svg || !maskCircle || !centerCircle || !rays) return;
        
        if (theme === 'dark') {
          svg.style.transform = 'rotate(270deg)';
          maskCircle.setAttribute('cx', '17');
          maskCircle.setAttribute('cy', '8');
          centerCircle.setAttribute('r', '9');
          rays.style.opacity = '0';
          rays.style.transform = 'scale(0) rotate(-30deg)';
        } else {
          svg.style.transform = 'rotate(0deg)';
          maskCircle.setAttribute('cx', '33');
          maskCircle.setAttribute('cy', '0');
          centerCircle.setAttribute('r', '5');
          rays.style.opacity = '1';
          rays.style.transform = 'scale(1) rotate(0deg)';
        }
      };

      // Set initial state
      updateSwitchMorph(html.classList.contains('dark') ? 'dark' : 'light');

      // Click to toggle
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const isDark = html.classList.contains('dark');
        const newTheme = isDark ? 'light' : 'dark';
        setTheme(newTheme);
        updateSwitchMorph(newTheme);
        playTickSound();
      });
    });



    // ── Collapsible Sidebar Engine ──────────────────────────────────────────
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.getElementById('menu-toggle');
    const body = document.body;

    if (sidebar) {
      body.classList.add('has-sidebar');

      // Move menuBtn out of topbar navbar to place it floating below the navbar
      if (menuBtn) {
        menuBtn.parentNode?.removeChild(menuBtn);
        document.body.appendChild(menuBtn);
        menuBtn.className = 'floating-menu-toggle';
      }

      // Restore collapsed sidebar state on desktop
      if (localStorage.getItem('sidebar-collapsed') === 'true' && window.innerWidth > 900) {
        body.classList.add('sidebar-collapsed');
      }
    }

    if (sidebar && menuBtn) {
      // Premium stateful icons matching user-requested collapse/expand design
      const iconCollapsed = `<svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><line x1="4" y1="6" x2="20" y2="6"></line><line x1="4" y1="12" x2="20" y2="12"></line><line x1="4" y1="18" x2="20" y2="18"></line></svg>`;
      const iconOpen = `<svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><line x1="3" y1="6" x2="13" y2="6"></line><line x1="3" y1="12" x2="13" y2="12"></line><line x1="3" y1="18" x2="13" y2="18"></line><polyline points="19 7 14 12 19 17"></polyline></svg>`;

      function updateMenuIcon() {
        const isCollapsed = window.innerWidth > 900 
          ? body.classList.contains('sidebar-collapsed') 
          : !sidebar.classList.contains('open');
        menuBtn.innerHTML = isCollapsed ? iconCollapsed : iconOpen;
      }

      // Set initial icon on load
      updateMenuIcon();
      window.addEventListener('resize', updateMenuIcon, { passive: true });

      menuBtn.addEventListener('click', e => {
        e.stopPropagation();
        if (window.innerWidth > 900) {
          body.classList.toggle('sidebar-collapsed');
          localStorage.setItem('sidebar-collapsed', body.classList.contains('sidebar-collapsed'));
        } else {
          sidebar.classList.toggle('open');
        }
        updateMenuIcon();
      });

      document.addEventListener('click', e => {
        if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
          if (sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
            updateMenuIcon();
          }
        }
      });
    }

    // ── Global Premium SVGs Dynamic Injection ──────────────────────────────
    const dbmsSvg = `<svg class="course-label-svg" viewBox="0 0 24 24" width="15" height="15" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block;"><ellipse cx="9" cy="5" rx="5" ry="2.5"></ellipse><path d="M4 5v5c0 1.38 2.24 2.5 5 2.5s5-1.12 5-2.5V5"></path><path d="M4 10v5c0 1.38 2.24 2.5 5 2.5s5-1.12 5-2.5v-5"></path><ellipse cx="17" cy="14" rx="4" ry="2"></ellipse><path d="M13 14v4c0 1.1 1.79 2 4 2s4-.9 4-2v-4"></path><path d="M9 11.5c1 1 2 1 4 .5" stroke-dasharray="2 2" stroke-width="1.5"></path></svg>`;
    const cnSvg = `<svg class="course-label-svg" viewBox="0 0 24 24" width="15" height="15" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block;"><path d="M12 2L2 7l10 5 10-5-10-5z"></path><path d="M2 17l10 5 10-5M2 12l10 5 10-5"></path><circle cx="12" cy="7" r="1.5" fill="currentColor"></circle><circle cx="7" cy="9.5" r="1" fill="currentColor"></circle><circle cx="17" cy="9.5" r="1" fill="currentColor"></circle><line x1="12" y1="8.5" x2="12" y2="14.5" stroke-dasharray="1 1"></line></svg>`;
    const osSvg = `<svg class="course-label-svg" viewBox="0 0 24 24" width="15" height="15" stroke="currentColor" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block;"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line><path d="M6 8h12M6 12h8"></path></svg>`;

    // 1. Sidebar course label injection
    const sidebarLabel = document.querySelector('.sidebar-course-label');
    if (sidebarLabel) {
      const text = sidebarLabel.textContent;
      if (text.includes('Database Management Systems') || text.includes('DBMS')) {
        sidebarLabel.innerHTML = dbmsSvg + 'Database Management Systems';
      } else if (text.includes('Computer Networks') || text.includes('CN')) {
        sidebarLabel.innerHTML = cnSvg + 'Computer Networks';
      } else if (text.includes('Operating Systems') || text.includes('OS')) {
        sidebarLabel.innerHTML = osSvg + 'Operating Systems';
      }
    }

    // 2. Topbar Nav items injection - Premium unified uncluttered navbar
    const topNav = document.querySelector('.topbar-nav');
    if (topNav) {
      const hasResumeNav = topNav.querySelector('.resume-nav');
      if (!hasResumeNav) {
        topNav.innerHTML = `
          <a href="${rootPath}dashboard.html" class="learn-nav">Learn</a>
          <a href="${rootPath}tracker.html" class="tracker-nav">Tracker</a>
          <a href="${rootPath}practice.html" class="practice-nav">Practice</a>
          <a href="${rootPath}interview-prep/index.html" class="prep-nav">Prep</a>
          <a href="${rootPath}resume-builder.html" class="resume-nav">Resume</a>
        `;
      }

      // Remove existing active classes first
      topNav.querySelectorAll('a').forEach(el => el.classList.remove('active'));

      // Apply active class based on current path
      if (path.includes('/courses/') || path.includes('dashboard.html')) {
        topNav.querySelector('.learn-nav')?.classList.add('active');
      } else if (path.includes('practice.html')) {
        topNav.querySelector('.practice-nav')?.classList.add('active');
      } else if (path.includes('tracker')) {
        topNav.querySelector('.tracker-nav')?.classList.add('active');
      } else if (path.includes('interview-prep')) {
        topNav.querySelector('.prep-nav')?.classList.add('active');
      } else if (path.includes('resume-builder')) {
        topNav.querySelector('.resume-nav')?.classList.add('active');
      }
      topNav.classList.add('loaded');
    }

    // Dynamic breadcrumb for course landing pages (index.html under courses/) - Disabled

    // 3. Course Index Hero icons injection
    const heroIcon = document.querySelector('.course-hero-icon');
    if (heroIcon) {
      const text = heroIcon.textContent;
      if (text.includes('🗄️') || text.includes('Database')) {
        heroIcon.innerHTML = dbmsSvg.replace('width="15"', 'width="36"').replace('height="15"', 'height="36"').replace('vertical-align: -3px;', '');
      } else if (text.includes('🌐') || text.includes('Networks')) {
        heroIcon.innerHTML = cnSvg.replace('width="15"', 'width="36"').replace('height="15"', 'height="36"').replace('vertical-align: -3px;', '');
      } else if (text.includes('💻') || text.includes('Operating')) {
        heroIcon.innerHTML = osSvg.replace('width="15"', 'width="36"').replace('height="15"', 'height="36"').replace('vertical-align: -3px;', '');
      }
    }

    // ── Syntax Highlighting ────────────────────────────────────────────────
    if (typeof hljs !== 'undefined') {
      hljs.configure({ tabReplace: '    ', ignoreUnescapedHTML: true });
      document.querySelectorAll('pre code').forEach(b => hljs.highlightElement(b));
    }

    // ── Copy buttons on code blocks ───────────────────────────────────────
    document.querySelectorAll('pre').forEach(pre => {
      const btn = document.createElement('button');
      btn.className = 'copy-btn'; btn.textContent = 'copy';
      pre.appendChild(btn);
      btn.addEventListener('click', async () => {
        const code = pre.querySelector('code');
        const txt = code ? code.innerText : pre.innerText;
        try {
          await navigator.clipboard.writeText(txt);
          btn.textContent = 'copied!'; btn.classList.add('copied');
          setTimeout(() => { btn.textContent = 'copy'; btn.classList.remove('copied'); }, 2000);
        } catch(_) { btn.textContent = 'error'; }
      });
    });

    // ── Reading progress bar ──────────────────────────────────────────────
    const bar = document.getElementById('reading-progress');
    if (bar) {
      function updateProgress() {
        const article = document.querySelector('.main-content');
        if (!article) return;
        const rect = article.getBoundingClientRect();
        const total = article.offsetHeight - window.innerHeight;
        const scrolled = Math.max(0, -rect.top);
        bar.style.width = Math.min(100, total > 0 ? (scrolled / total) * 100 : 100) + '%';
      }
      window.addEventListener('scroll', updateProgress, { passive: true });
      updateProgress();
    }

    // ── Back to top ───────────────────────────────────────────────────────
    const btt = document.getElementById('back-to-top');
    if (btt) {
      window.addEventListener('scroll', () => {
        btt.classList.toggle('show', window.scrollY > 400);
      }, { passive: true });
      btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    // ── Dashboard search ──────────────────────────────────────────────────
    const dbSearch = document.getElementById('dashboard-search');
    if (dbSearch) {
      // Create results container dynamically
      const resultsDiv = document.createElement('div');
      resultsDiv.className = 'global-search-results';
      dbSearch.parentNode.appendChild(resultsDiv);

      dbSearch.addEventListener('input', function () {
        const q = this.value.toLowerCase().trim();
        if (q.length === 0) {
          resultsDiv.classList.remove('active');
          resultsDiv.innerHTML = '';
          // Restore all course cards
          document.querySelectorAll('.courses-grid .course-card').forEach(card => card.style.display = 'flex');
          return;
        }

        // Search the compiled SEARCH_INDEX
        const queryWords = q.split(/\s+/);
        const matches = (typeof SEARCH_INDEX !== 'undefined') ? SEARCH_INDEX.filter(item => {
          const title = item.title.toLowerCase();
          const subject = item.subject.toLowerCase();
          return queryWords.every(word => title.includes(word) || subject.includes(word));
        }) : [];

        resultsDiv.classList.add('active');
        resultsDiv.innerHTML = '';

        if (matches.length === 0) {
          resultsDiv.innerHTML = `<div class="search-result-no-results">No topics found for "${this.value}"</div>`;
        } else {
          // Limit to max 12 results
          matches.slice(0, 12).forEach(match => {
            const item = document.createElement('a');
            item.href = rootPath + match.path;
            item.className = 'search-result-item';
            item.innerHTML = `
              <span class="search-result-title">${match.title}</span>
              <span class="search-result-subject">${match.subject}</span>
            `;
            resultsDiv.appendChild(item);
          });
        }

        // Also filter course cards in real-time
        document.querySelectorAll('.courses-grid .course-card').forEach(card => {
          const title = card.querySelector('.course-card-title').textContent.toLowerCase();
          const desc = card.querySelector('.course-card-desc').textContent.toLowerCase();
          const matchesCard = title.includes(q) || desc.includes(q);
          card.style.display = matchesCard ? 'flex' : 'none';
        });
      });

      // Hide results when clicking outside
      document.addEventListener('click', function (e) {
        if (!dbSearch.contains(e.target) && !resultsDiv.contains(e.target)) {
          resultsDiv.classList.remove('active');
        }
      });

      // Show results on focus if not empty
      dbSearch.addEventListener('focus', function () {
        if (this.value.trim().length > 0) {
          resultsDiv.classList.add('active');
        }
      });

      // Hide results on Escape
      dbSearch.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
          resultsDiv.classList.remove('active');
          dbSearch.blur();
        }
      });
    }

    // ── Topic Completion Tracker & Sidebar Sync ──────────────────────────
    const topicMatch = window.location.pathname.match(/\/courses\/([^/]+)\/topics\/(\d+)-/i);
    const topicMeta = document.querySelector('.topic-meta');
    
    function syncSidebarProgress(courseId, completions) {
      const allTopicItems = document.querySelectorAll('.topic-item');
      let completedInCourse = 0;
      let totalInCourse = allTopicItems.length;
      
      allTopicItems.forEach(li => {
        const link = li.querySelector('a');
        if (link) {
          const href = link.getAttribute('href');
          const match = href.match(/\/courses\/([^/]+)\/topics\/(\d+)-/i);
          if (match) {
            const itemCourseId = match[1];
            const itemTopicNum = match[2];
            const itemKey = `${itemCourseId}/${itemTopicNum}`;
            
            if (completions[itemKey]) {
              completedInCourse++;
              if (!link.querySelector('.topic-checkmark')) {
                const check = document.createElement('span');
                check.className = 'topic-checkmark';
                check.innerHTML = '✓';
                link.appendChild(check);
              }
            } else {
              const check = link.querySelector('.topic-checkmark');
              if (check) check.remove();
            }
          }
        }
      });
      
      const progressCount = document.querySelector('.sidebar-progress .progress-count');
      const progressFill = document.querySelector('.sidebar-progress .progress-fill');
      if (progressCount && progressFill && totalInCourse > 0) {
        progressCount.textContent = `${completedInCourse} / ${totalInCourse}`;
        const pct = Math.round((completedInCourse / totalInCourse) * 100);
        progressFill.style.width = `${pct}%`;
      }
    }

    // ── Dynamic Island Table of Contents (Vanilla Engine) ──────────────────
    function initDynamicIslandTOC() {
      const article = document.querySelector('.editorial-content') || document.querySelector('.topic-article');
      if (!article) return;

      const elements = Array.from(article.querySelectorAll('h1, h2, h3, h4, [data-toc]'))
        .filter(el => !el.hasAttribute('data-toc-ignore'));

      if (elements.length === 0) return;

      const headings = elements.map((el, index) => {
        if (!el.id) {
          const generatedId = el.textContent
            .toLowerCase()
            .replace(/\s+/g, '-')
            .replace(/[^\w-]/g, '') || `toc-heading-${index}`;
          el.id = generatedId;
        }

        const depthAttr = el.getAttribute('data-toc-depth');
        let level = 2;
        if (depthAttr) {
          level = parseInt(depthAttr, 10);
        } else {
          const tagName = el.tagName.toUpperCase();
          if (tagName.startsWith('H') && tagName.length === 2) {
            level = parseInt(tagName[1], 10);
          }
        }

        const text = el.getAttribute('data-toc-title') || el.textContent.trim() || 'Section';
        return { id: el.id, text, level, element: el };
      });

      const minLevel = Math.min(...headings.map(h => h.level));

      const backdrop = document.createElement('div');
      backdrop.className = 'dynamic-island-backdrop';
      backdrop.id = 'island-backdrop';
      document.body.appendChild(backdrop);

      const container = document.createElement('div');
      container.className = 'dynamic-island-container';
      container.id = 'island-container';
      
      const closedDiv = document.createElement('div');
      closedDiv.className = 'island-closed';
      closedDiv.id = 'island-closed';
      closedDiv.innerHTML = `
        <span class="island-dot"></span>
        <span class="island-active-title" id="island-active-title">Contents</span>
        <div class="island-progress-circle">
          <svg width="24" height="24" class="progress-circle-svg">
            <circle cx="12" cy="12" r="9" fill="none" stroke="var(--border)" stroke-width="2.2" style="opacity: 0.3;" />
            <circle cx="12" cy="12" r="9" fill="none" stroke="var(--brand)" stroke-width="2.2" stroke-dasharray="56.54" stroke-dashoffset="56.54" class="progress-circle-fill" id="island-progress-fill" />
          </svg>
        </div>
      `;
      container.appendChild(closedDiv);

      const expandedDiv = document.createElement('div');
      expandedDiv.className = 'island-expanded';
      expandedDiv.id = 'island-expanded';
      expandedDiv.style.display = 'none';
      expandedDiv.innerHTML = `
        <div class="island-header">
          <span class="island-header-title">TABLE OF CONTENTS</span>
          <button class="island-close-btn" id="island-close-btn">&times;</button>
        </div>
        <div class="island-body">
          <div class="island-toc-list" id="island-toc-list"></div>
        </div>
      `;
      container.appendChild(expandedDiv);
      document.body.appendChild(container);

      const listContainer = expandedDiv.querySelector('#island-toc-list');
      headings.forEach(h => {
        const item = document.createElement('button');
        item.className = 'island-toc-item';
        item.setAttribute('data-id', h.id);
        
        const indentLevel = Math.max(0, h.level - minLevel);
        const paddingLeft = indentLevel * 14 + 12;
        item.style.paddingLeft = `${paddingLeft}px`;

        item.innerHTML = `
          <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; transition: transform 0.2s ease;">${h.text}</span>
          <span class="island-toc-dot"></span>
        `;
        
        item.addEventListener('click', (e) => {
          e.stopPropagation();
          const yOffset = -80;
          const y = h.element.getBoundingClientRect().top + window.scrollY + yOffset;
          window.scrollTo({ top: y, behavior: 'smooth' });
          closeIsland();
        });

        listContainer.appendChild(item);
      });

      let isExpanded = false;

      closedDiv.addEventListener('click', () => {
        if (isExpanded) return;
        isExpanded = true;
        container.classList.add('expanded');
        backdrop.classList.add('active');

        closedDiv.style.opacity = '0';
        closedDiv.style.pointerEvents = 'none';

        setTimeout(() => {
          closedDiv.style.display = 'none';
          expandedDiv.style.display = 'flex';
          setTimeout(() => {
            expandedDiv.style.opacity = '1';
          }, 50);
        }, 200);
      });

      function closeIsland() {
        if (!isExpanded) return;
        isExpanded = false;
        container.classList.remove('expanded');
        backdrop.classList.remove('active');

        expandedDiv.style.opacity = '0';
        setTimeout(() => {
          expandedDiv.style.display = 'none';
          closedDiv.style.display = 'flex';
          setTimeout(() => {
            closedDiv.style.opacity = '1';
            closedDiv.style.pointerEvents = 'auto';
          }, 50);
        }, 200);
      }

      document.getElementById('island-close-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        closeIsland();
      });

      backdrop.addEventListener('click', closeIsland);

      let activeId = null;

      function handleScroll() {
        let currentActiveId = null;
        for (const heading of headings) {
          const top = heading.element.getBoundingClientRect().top;
          if (top <= 130) {
            currentActiveId = heading.id;
          } else {
            break;
          }
        }

        if (!currentActiveId && headings.length > 0) {
          currentActiveId = headings[0].id;
        }

        if (currentActiveId !== activeId) {
          activeId = currentActiveId;
          const activeHeading = headings.find(h => h.id === activeId);
          if (activeHeading) {
            document.getElementById('island-active-title').textContent = activeHeading.text;
          }

          document.querySelectorAll('.island-toc-item').forEach(item => {
            const itemId = item.getAttribute('data-id');
            if (itemId === activeId) {
              item.classList.add('active');
            } else {
              item.classList.remove('active');
            }
          });
        }

        const totalScroll = document.documentElement.scrollHeight - window.innerHeight;
        const progress = totalScroll > 0 ? Math.min(100, Math.max(0, (window.scrollY / totalScroll) * 100)) : 0;

        const circ = 2 * Math.PI * 9;
        const offset = circ - (progress / 100) * circ;
        const circleFill = document.getElementById('island-progress-fill');
        if (circleFill) {
          circleFill.style.strokeDashoffset = offset;
        }
      }

      window.addEventListener('scroll', handleScroll, { passive: true });
      handleScroll();
    }

    if (topicMatch && topicMeta) {
      const courseId = topicMatch[1];
      const topicNum = topicMatch[2];
      const storageKey = `${courseId}/${topicNum}`;
      
      let completions = JSON.parse(localStorage.getItem('GrindOS-completed-topics') || '{}');
      let isCompleted = !!completions[storageKey];
      
      const completeBtn = document.createElement('button');
      completeBtn.className = 'topic-complete-btn' + (isCompleted ? ' completed' : '');
      completeBtn.id = 'toggle-complete-btn';
      completeBtn.innerHTML = isCompleted 
        ? `<span class="btn-icon">✓</span> <span class="btn-text">Completed</span>`
        : `<span class="btn-icon">○</span> <span class="btn-text">Mark Completed</span>`;
      
      topicMeta.appendChild(completeBtn);
      
      syncSidebarProgress(courseId, completions);
      
      // Initialize dynamic island TOC for documentation
      initDynamicIslandTOC();
      
      completeBtn.addEventListener('click', function() {
        completions = JSON.parse(localStorage.getItem('GrindOS-completed-topics') || '{}');
        isCompleted = !completions[storageKey];
        if (isCompleted) {
          completions[storageKey] = true;
        } else {
          delete completions[storageKey];
        }
        localStorage.setItem('GrindOS-completed-topics', JSON.stringify(completions));
        
        completeBtn.classList.toggle('completed', isCompleted);
        completeBtn.innerHTML = isCompleted
          ? `<span class="btn-icon">✓</span> <span class="btn-text">Completed</span>`
          : `<span class="btn-icon">○</span> <span class="btn-text">Mark Completed</span>`;
          
        syncSidebarProgress(courseId, completions);
      });
    } else {
      const courseLandingMatch = window.location.pathname.match(/\/courses\/([^/]+)\/index.html/i);
      if (courseLandingMatch) {
        const courseId = courseLandingMatch[1];
        const completions = JSON.parse(localStorage.getItem('GrindOS-completed-topics') || '{}');
        syncSidebarProgress(courseId, completions);
      }
    }

    // Sync Dashboard Progress Cards
    function syncDashboardProgress() {
      const completions = JSON.parse(localStorage.getItem('GrindOS-completed-topics') || '{}');
      const courseTotals = {
        dbms: 94,
        cn: 40,
        os: 17,
        oops: 15,
        dsa: 72,
        webdev: 62,
        aptitude: 35
      };
      
      document.querySelectorAll('.course-card').forEach(card => {
        const href = card.getAttribute('href');
        const match = href.match(/courses\/([^/]+)\/index.html/);
        if (match) {
          const courseId = match[1];
          const total = courseTotals[courseId] || 0;
          let completed = 0;
          Object.keys(completions).forEach(key => {
            if (key.startsWith(courseId + '/')) {
              completed++;
            }
          });
          
          const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
          const pctLabel = card.querySelector('.card-progress-percent');
          if (pctLabel) pctLabel.textContent = `${pct}%`;
          const fillBar = card.querySelector('.card-progress-fill');
          if (fillBar) fillBar.style.width = `${pct}%`;
        }
      });
    }
    syncDashboardProgress();

    // Helper to dynamically load quiz questions database script
    const loadScript = (src) => {
      if (window.QUIZ_QUESTIONS) return Promise.resolve();
      return new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = src;
        s.onload = resolve;
        s.onerror = reject;
        document.head.appendChild(s);
      });
    };

    // ── MCQ Quiz Module Injection ──────────────────────────────────────────
    const courseLandingMatch = window.location.pathname.match(/\/courses\/([^/]+)\/index.html/i);
    if (courseLandingMatch) {
      const courseId = courseLandingMatch[1];
      const startBtn = document.querySelector('.course-hero .start-btn');
      
      if (startBtn && !document.getElementById('start-quiz-btn')) {
        const quizBtn = document.createElement('a');
        quizBtn.href = '#';
        quizBtn.className = 'quiz-btn start-btn';
        quizBtn.id = 'start-quiz-btn';
        quizBtn.style.background = 'var(--bg-3)';
        quizBtn.style.border = '1px solid var(--border)';
        quizBtn.style.color = 'var(--text-1)';
        quizBtn.style.marginLeft = '12px';
        quizBtn.style.display = 'inline-flex';
        quizBtn.style.alignItems = 'center';
        quizBtn.style.justifyContent = 'center';
        quizBtn.innerHTML = 'Practice Quiz 📝';
        startBtn.parentNode.appendChild(quizBtn);
        
        quizBtn.addEventListener('click', (e) => {
          e.preventDefault();
          loadScript(rootPath + 'assets/quiz_questions.js')
            .then(() => {
              openQuizModal(courseId);
            })
            .catch(err => {
              console.error("Failed to load quiz questions:", err);
              alert("Error loading quiz questions.");
            });
        });
      }
    }

    // Modal Quiz Implementation
    function openQuizModal(courseId) {
      const completions = JSON.parse(localStorage.getItem('GrindOS-completed-topics') || '{}');
      const completedTopics = Object.keys(completions)
        .filter(key => key.startsWith(courseId + '/'))
        .map(key => key.split('/')[1]);
      
      const courseQuestions = QUIZ_QUESTIONS[courseId] || [];
      const activeQuestions = courseQuestions.filter(q => completedTopics.includes(q.topic));
      
      let modalOverlay = document.getElementById('quiz-modal-overlay');
      if (!modalOverlay) {
        modalOverlay = document.createElement('div');
        modalOverlay.id = 'quiz-modal-overlay';
        modalOverlay.className = 'quiz-modal-overlay';
        document.body.appendChild(modalOverlay);
        
        modalOverlay.addEventListener('click', (e) => {
          if (e.target === modalOverlay) closeQuiz();
        });
      }
      
      function closeQuiz() {
        modalOverlay.classList.remove('active');
        setTimeout(() => {
          modalOverlay.innerHTML = '';
        }, 300);
      }
      
      const courseTitles = {
        dbms: "Database Management Systems",
        cn: "Computer Networks",
        os: "Operating Systems",
        oops: "Object-Oriented Programming",
        dsa: "Data Structures & Algorithms",
        webdev: "Web Development",
        aptitude: "Quantitative & Logical Aptitude"
      };

      // Set HTML container matching the custom component
      modalOverlay.innerHTML = `
        <div class="quiz-modal-container">
          <div class="quiz-tool-header">
            <div class="quiz-tool-title">
              <svg class="quiz-tool-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden><path d="M3 20l1.3 -3.9a9 9 0 1 1 3.4 2.9z" /><path d="M12 16v.01" /><path d="M12 13a2 2 0 0 0 .914 -3.782a1.98 1.98 0 0 0 -2.414 .483" /></svg>
              <span>${courseTitles[courseId] || 'Course'} Quiz</span>
            </div>
            <div class="quiz-tool-nav" id="quiz-header-nav" style="display: none;">
              <button type="button" class="quiz-nav-chevron" id="quiz-prev-chevron-btn" aria-label="Previous question">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden><path d="M6 15l6 -6l6 6" /></svg>
              </button>
              <span id="quiz-header-counter">1 of 10</span>
              <button type="button" class="quiz-nav-chevron" id="quiz-next-chevron-btn" aria-label="Next question">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden><path d="M6 9l6 6l6 -6" /></svg>
              </button>
              <button class="quiz-modal-close-tool" id="quiz-close-btn" aria-label="Close quiz">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
              </button>
            </div>
            <button class="quiz-modal-close-tool" id="quiz-close-btn-direct" style="display: none;" aria-label="Close quiz">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
            </button>
          </div>
          <div class="quiz-modal-body" id="quiz-body">
            <!-- Dynamic Content -->
          </div>
          <div class="quiz-modal-footer" id="quiz-footer">
            <!-- Dynamic Buttons -->
          </div>
        </div>
      `;
      
      const closeBtn = modalOverlay.querySelector('#quiz-close-btn-direct');
      if (closeBtn) closeBtn.addEventListener('click', closeQuiz);
      
      modalOverlay.classList.add('active');
      const body = document.getElementById('quiz-body');
      const footer = document.getElementById('quiz-footer');
      
      if (activeQuestions.length === 0) {
        if (closeBtn) closeBtn.style.display = 'inline-flex';
        body.innerHTML = `
          <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 3rem; margin-bottom: 16px;">📝</div>
            <div class="quiz-result-text" style="font-size: 1.15rem; font-weight:700; margin-bottom:10px;">No Topics Completed Yet</div>
            <div class="quiz-result-subtext" style="color:var(--text-3); font-size:0.9rem; line-height:1.5; max-width: 360px; margin: 0 auto;">
              This practice quiz adapts to your progress. Mark at least one topic as <strong>Completed</strong> in this course to start testing yourself!
            </div>
          </div>
        `;
        footer.innerHTML = `
          <div style="width: 100%; text-align: right;">
            <button class="quiz-btn-primary" id="quiz-close-warning-btn" style="padding: 6px 14px;">Got it</button>
          </div>
        `;
        document.getElementById('quiz-close-warning-btn').addEventListener('click', closeQuiz);
        return;
      }
      
      // Show navigation bar
      const navBar = document.getElementById('quiz-header-nav');
      if (navBar) navBar.style.display = 'flex';
      document.getElementById('quiz-close-btn').addEventListener('click', closeQuiz);
      
      let currentIndex = 0;
      let score = 0;
      
      // Mathematically sound random shuffle for questions selection
      const quizQuestions = [...activeQuestions]
        .map(q => ({ q, sort: Math.random() }))
        .sort((a, b) => a.sort - b.sort)
        .map(({ q }) => {
          delete q.userAnswer;
          delete q.tempAnswer;
          delete q.shuffledOptions;
          return q;
        })
        .slice(0, 10);
      
      function renderQuestion() {
        const q = quizQuestions[currentIndex];
        
        // Update header counter
        document.getElementById('quiz-header-counter').textContent = `${currentIndex + 1} of ${quizQuestions.length}`;
        
        // Disable header chevrons based on bounds
        const prevChevron = document.getElementById('quiz-prev-chevron-btn');
        const nextChevron = document.getElementById('quiz-next-chevron-btn');
        if (prevChevron) prevChevron.disabled = (currentIndex === 0);
        if (nextChevron) nextChevron.disabled = (currentIndex === quizQuestions.length - 1);
        
        // Shuffle options if we haven't rendered this question yet
        if (!q.shuffledOptions) {
          const originalOptions = q.options.map((opt, idx) => ({ opt, originalIdx: idx }));
          q.shuffledOptions = originalOptions
            .map(o => ({ o, sort: Math.random() }))
            .sort((a, b) => a.sort - b.sort)
            .map(({ o }) => o);
        }
        const shuffledOptions = q.shuffledOptions;
        
        // Check if this question was already answered
        const isAnswered = q.hasOwnProperty('userAnswer');
        const isSkipped = q.userAnswer === 'skipped';
        
        body.innerHTML = `
          <div class="quiz-question-header-row">
            <span class="quiz-question-index-badge">${currentIndex + 1}</span>
            <span class="quiz-question-title-text">${q.question}</span>
          </div>
          
          <div class="quiz-options-list" id="options-list" style="margin-top: 16px;">
            ${shuffledOptions.map((optObj, idx) => {
              let classes = 'quiz-option-card';
              if (isAnswered && !isSkipped) {
                if (optObj.originalIdx === q.answer) {
                  classes += ' correct';
                } else if (optObj.originalIdx === q.userAnswer) {
                  classes += ' incorrect';
                }
              } else if (q.tempAnswer === optObj.originalIdx) {
                classes += ' selected';
              }
              
              return `
                <button class="${classes}" data-original-idx="${optObj.originalIdx}" type="button" ${isAnswered ? 'disabled' : ''}>
                  <span class="quiz-option-letter">${String.fromCharCode(65 + idx)}</span>
                  <span class="quiz-option-text">${optObj.opt}</span>
                </button>
              `;
            }).join('')}
          </div>
          <div id="explanation-container">
            ${isAnswered && !isSkipped ? `
              <div class="quiz-explanation-box">
                <strong>${q.userAnswer === q.answer ? '✓ Correct!' : '✗ Incorrect'}</strong><br/>
                ${q.explanation}
              </div>
            ` : ''}
          </div>
        `;
        
        // Render Footer matching the component buttons
        let actionBtnText = 'Submit Answer';
        let actionBtnDisabled = !isAnswered && q.tempAnswer === undefined;
        if (isAnswered) {
          actionBtnText = (currentIndex === quizQuestions.length - 1) ? 'Finish Quiz' : 'Next Question';
          actionBtnDisabled = false;
        }
        
        footer.innerHTML = `
          <div class="quiz-footer-left">
            <button type="button" class="quiz-nav-text-btn" id="quiz-prev-btn" ${currentIndex === 0 ? 'disabled' : ''}>Previous</button>
            <button type="button" class="quiz-nav-text-btn" id="quiz-next-btn" ${currentIndex === quizQuestions.length - 1 ? 'disabled' : ''}>Next</button>
          </div>
          <div class="quiz-footer-right">
            <button type="button" class="quiz-nav-text-btn skip-btn" id="quiz-skip-btn" ${isAnswered ? 'disabled' : ''}>Skip</button>
            <button type="button" class="quiz-btn-primary" id="quiz-action-btn" ${actionBtnDisabled ? 'disabled' : ''}>${actionBtnText}</button>
          </div>
        `;
        
        // Hook up option selections
        const cards = body.querySelectorAll('.quiz-option-card');
        cards.forEach(card => {
          card.addEventListener('click', () => {
            if (isAnswered) return;
            cards.forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
            q.tempAnswer = parseInt(card.getAttribute('data-original-idx'));
            document.getElementById('quiz-action-btn').removeAttribute('disabled');
          });
        });
        
        // Hook up buttons
        const actionBtn = document.getElementById('quiz-action-btn');
        actionBtn.addEventListener('click', () => {
          if (!isAnswered) {
            // Submit state
            q.userAnswer = q.tempAnswer;
            const isCorrect = (q.userAnswer === q.answer);
            if (isCorrect) score++;
            
            // Re-render to show feedback
            renderQuestion();
          } else {
            // Next/Finish state
            if (currentIndex < quizQuestions.length - 1) {
              currentIndex++;
              renderQuestion();
            } else {
              renderResults();
            }
          }
        });
        
        document.getElementById('quiz-skip-btn').addEventListener('click', () => {
          q.userAnswer = 'skipped';
          if (currentIndex < quizQuestions.length - 1) {
            currentIndex++;
            renderQuestion();
          } else {
            renderResults();
          }
        });
        
        document.getElementById('quiz-prev-btn').addEventListener('click', () => {
          if (currentIndex > 0) {
            currentIndex--;
            renderQuestion();
          }
        });
        
        document.getElementById('quiz-next-btn').addEventListener('click', () => {
          if (currentIndex < quizQuestions.length - 1) {
            currentIndex++;
            renderQuestion();
          }
        });
      }
      
      // Hook up chevron buttons in header
      const prevChevronBtn = document.getElementById('quiz-prev-chevron-btn');
      const nextChevronBtn = document.getElementById('quiz-next-chevron-btn');
      if (prevChevronBtn) {
        prevChevronBtn.addEventListener('click', () => {
          if (currentIndex > 0) {
            currentIndex--;
            renderQuestion();
          }
        });
      }
      if (nextChevronBtn) {
        nextChevronBtn.addEventListener('click', () => {
          if (currentIndex < quizQuestions.length - 1) {
            currentIndex++;
            renderQuestion();
          }
        });
      }
      
      function renderResults() {
        const total = quizQuestions.length;
        const correctCount = quizQuestions.filter(q => q.userAnswer === q.answer).length;
        const pct = Math.round((correctCount / total) * 100);
        
        let feedbackText = "Keep studying to master these concepts!";
        if (pct === 100) feedbackText = "Perfect score! You have fully mastered these topics!";
        else if (pct >= 80) feedbackText = "Excellent job! You are well prepared.";
        else if (pct >= 50) feedbackText = "Good effort! Review the explanations to improve.";
        
        const summaryText = quizQuestions.map((q, idx) => {
          let ansText = "Skipped";
          if (q.userAnswer !== 'skipped' && q.userAnswer !== undefined) {
            const origOptIdx = q.userAnswer;
            const shuffledIdx = q.shuffledOptions.findIndex(o => o.originalIdx === origOptIdx);
            ansText = String.fromCharCode(65 + shuffledIdx);
          }
          return `${idx + 1}: ${ansText}`;
        }).join(' • ');
        
        body.innerHTML = `
          <div class="quiz-result-score-circle">
            <span class="quiz-result-score-num">${correctCount}</span>
            <span class="quiz-result-score-total">out of ${total}</span>
          </div>
          <div class="quiz-result-text">Quiz Completed!</div>
          <div class="quiz-result-subtext" style="text-align: center; margin-bottom: 12px;">${feedbackText} (${pct}% Score)</div>
          
          <div class="quiz-tool-summary-answers">
            ${summaryText}
          </div>
        `;
        
        footer.innerHTML = `
          <button class="quiz-btn-secondary" id="quiz-retry-btn">Retry Quiz</button>
          <button class="quiz-btn-primary" id="quiz-finish-btn">Close</button>
        `;
        
        document.getElementById('quiz-finish-btn').addEventListener('click', closeQuiz);
        document.getElementById('quiz-retry-btn').addEventListener('click', () => {
          currentIndex = 0;
          score = 0;
          
          const reshuffled = [...activeQuestions]
            .map(q => ({ q, sort: Math.random() }))
            .sort((a, b) => a.sort - b.sort)
            .map(({ q }) => {
              delete q.userAnswer;
              delete q.tempAnswer;
              delete q.shuffledOptions;
              return q;
            })
            .slice(0, 10);
            
          quizQuestions.length = 0;
          quizQuestions.push(...reshuffled);
          
          renderQuestion();
        });
      }
      
      renderQuestion();
    }

    // ── Mermaid.js Dynamic Loader ──────────────────────────────────────────
    const isDark = document.documentElement.classList.contains('dark');
    const themeName = isDark ? 'dark' : 'default';
    
    if (!window.mermaid) {
      const s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
      s.onload = () => {
        mermaid.initialize({
          startOnLoad: true,
          theme: themeName,
          securityLevel: 'loose',
          themeVariables: {
            background: 'var(--card)',
            primaryColor: 'var(--brand)',
            primaryTextColor: 'var(--text-1)',
            lineColor: 'var(--border)'
          }
        });
      };
      document.head.appendChild(s);
    }

    // ── Sidebar search ────────────────────────────────────────────────────
    const searchInput = document.getElementById('sidebar-search');
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        const q = this.value.toLowerCase().trim();
        document.querySelectorAll('.topic-item').forEach(li => {
          const text = li.textContent.toLowerCase();
          li.classList.toggle('hidden', q.length > 0 && !text.includes(q));
        });
        // Open all chapters when searching
        if (q.length > 0) {
          document.querySelectorAll('.chapter-group').forEach(d => d.open = true);
        }
      });
    }

    // ── Scroll active item into view ───────────────────────────────────────
    const active = document.querySelector('.topic-item.active a');
    if (active) setTimeout(() => active.scrollIntoView({ block: 'nearest' }), 100);

    // ── Keyboard navigation ───────────────────────────────────────────────
    document.addEventListener('keydown', e => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.metaKey || e.ctrlKey) return;
      const prev = document.querySelector('a.nav-btn.nav-prev');
      const next = document.querySelector('a.nav-btn.nav-next');
      if (e.key === 'ArrowLeft' && prev) window.location.href = prev.href;
      if (e.key === 'ArrowRight' && next) window.location.href = next.href;
      if (e.key === '/' && searchInput) { e.preventDefault(); searchInput.focus(); }
    });

    // ── Estimated reading time ────────────────────────────────────────────
    const readingMeta = document.getElementById('reading-time');
    if (readingMeta) {
      const article = document.querySelector('.topic-article');
      if (article) {
        const wpm = 200;
        const words = article.innerText.trim().split(/\s+/).length;
        readingMeta.textContent = Math.max(1, Math.ceil(words / wpm)) + ' min read';
      }
    }

    // ── Premium Floating AI Chat Panel Injection ──────────────────────────
    // 1. Inject Dynamic Style Tag
    const styleTag = document.createElement('style');
    styleTag.textContent = `
      #ai-chat-btn {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: var(--brand);
        color: #ffffff;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow-md);
        z-index: 9999;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        animation: chat-pulse 4s infinite ease-in-out;
      }
      #ai-chat-btn:hover {
        transform: scale(1.08) translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: var(--brand-hover);
      }
      @keyframes ai-blink {
        0%, 94%, 100% { transform: scaleY(1); }
        97% { transform: scaleY(0.1); }
      }
      .ai-chat-bot-icon {
        width: 34px;
        height: 34px;
        display: block;
      }
      .ai-icon-head {
        fill: #ffffff;
      }
      .ai-icon-base {
        fill: #ffffff;
      }
      .ai-icon-eye {
        fill: var(--brand);
        transform-origin: 50px 47px;
        animation: ai-blink 4s infinite ease-in-out;
        transition: fill 0.25s ease;
      }
      #ai-chat-btn:hover .ai-icon-eye {
        fill: var(--brand-hover);
      }
      #ai-chat-panel {
        position: fixed;
        bottom: 88px;
        right: 24px;
        width: 380px;
        height: 520px;
        border-radius: 12px;
        background: var(--card);
        border: 1px solid var(--border);
        box-shadow: var(--shadow-lg), 0 10px 30px rgba(0,0,0,0.12);
        z-index: 9998;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        font-family: var(--font-sans);
        opacity: 0;
        transform: translateY(30px) scale(0.95);
        pointer-events: none;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      }
      #ai-chat-panel.active {
        opacity: 1;
        transform: translateY(0) scale(1);
        pointer-events: auto;
      }
      .ai-chat-header {
        padding: 14px 16px 10px;
        border-bottom: 1px solid var(--border);
        background: var(--bg-2);
        display: flex;
        flex-direction: column;
        gap: 8px;
      }
      .ai-chat-header-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .ai-chat-header-title {
        font-size: .95rem;
        font-weight: 700;
        color: var(--text-1);
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .ai-chat-header-close {
        background: transparent;
        border: none;
        color: var(--text-3);
        font-size: 1.3rem;
        cursor: pointer;
        line-height: 1;
        padding: 2px;
        transition: color 0.15s;
      }
      .ai-chat-header-close:hover {
        color: var(--brand);
      }
      .ai-chat-header-action {
        background: transparent;
        border: none;
        color: var(--text-3);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 4px;
        transition: color 0.15s, transform 0.15s;
      }
      .ai-chat-header-action:hover {
        color: var(--brand);
        transform: scale(1.15);
      }
      #ai-chat-panel.fullscreen {
        top: 24px;
        bottom: 24px;
        left: 24px;
        right: 24px;
        width: auto;
        height: auto;
        max-width: none;
        max-height: none;
        transform: none !important;
      }
      @media (max-width: 640px) {
        #ai-chat-panel.fullscreen {
          top: 0;
          bottom: 0;
          left: 0;
          right: 0;
          border-radius: 0;
          border: none;
        }
      }
      .ai-chat-modes {
        display: flex;
        gap: 5px;
      }
      .ai-chat-mode-btn {
        flex: 1;
        padding: 5px 2px;
        font-size: .72rem;
        font-weight: 700;
        border-radius: 6px;
        border: 1px solid var(--border);
        background: var(--card);
        color: var(--text-2);
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: .02em;
      }
      .ai-chat-mode-btn:hover {
        border-color: var(--brand);
        color: var(--brand);
      }
      .ai-chat-mode-btn.active {
        background: var(--brand) !important;
        border-color: var(--brand) !important;
        color: #ffffff !important;
        box-shadow: 0 2px 6px var(--brand-glow);
      }
      .ai-chat-thread {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      .ai-chat-bubble {
        max-width: 82%;
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 13px;
        line-height: 1.45;
        font-family: var(--font-sans);
        animation: bubbleSlideIn 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }
      @keyframes bubbleSlideIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
      }
      .ai-chat-bubble.user {
        align-self: flex-end;
        background: var(--brand);
        color: #ffffff;
        border-bottom-right-radius: 4px;
        box-shadow: 0 2px 6px var(--brand-glow);
      }
      .ai-chat-bubble.assistant {
        align-self: flex-start;
        background: var(--bg-3);
        color: var(--text-1);
        border-bottom-left-radius: 4px;
        border: 1px solid var(--border);
      }
      .ai-chat-bubble.warning {
        align-self: center;
        max-width: 90%;
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.2);
        color: #d97706;
        border-radius: 8px;
        font-size: 12px;
        display: flex;
        flex-direction: column;
        gap: 4px;
      }
      .dark .ai-chat-bubble.warning {
        background: rgba(245, 158, 11, 0.12);
        color: #fbbf24;
      }
      .ai-chat-prompts-container {
        padding: 6px 12px;
        border-top: 1px solid var(--border);
        overflow-x: auto;
        white-space: nowrap;
        background: var(--bg-2);
        display: flex;
        gap: 6px;
      }
      .ai-chat-prompts-container::-webkit-scrollbar {
        height: 0px;
      }
      .ai-chat-chip {
        display: inline-block;
        padding: 5px 12px;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        font-size: 11px;
        font-weight: 500;
        color: var(--text-2);
        cursor: pointer;
        transition: all 0.15s ease;
        flex-shrink: 0;
      }
      .ai-chat-chip:hover {
        border-color: var(--brand);
        color: var(--brand);
        background: var(--brand-light);
      }
      .ai-chat-form {
        display: flex;
        border-top: 1px solid var(--border);
        background: var(--card);
        padding: 10px;
        gap: 8px;
      }
      .ai-chat-input {
        flex: 1;
        padding: 8px 12px;
        border-radius: var(--radius);
        border: 1px solid var(--border);
        background: var(--bg-2);
        color: var(--text-1);
        font-size: 13px;
        outline: none;
        font-family: var(--font-sans);
        transition: all 0.2s;
      }
      .ai-chat-input:focus {
        border-color: var(--brand);
        background: var(--card);
      }
      .ai-chat-submit {
        background: var(--brand);
        color: #ffffff;
        border: none;
        width: 32px;
        height: 32px;
        border-radius: var(--radius);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 0.9rem;
        transition: background 0.15s;
        flex-shrink: 0;
      }
      .ai-chat-submit:hover {
        background: var(--brand-hover);
      }
      @keyframes chat-pulse {
        0%, 100% { transform: scale(1); box-shadow: var(--shadow-md); }
        50% { transform: scale(1.06); box-shadow: var(--shadow-lg); }
      }
      @media (max-width: 640px) {
        #ai-chat-panel {
          bottom: 0 !important;
          right: 0 !important;
          left: 0 !important;
          top: 0 !important;
          width: 100% !important;
          height: 100% !important;
          max-height: 100% !important;
          max-width: 100% !important;
          border-radius: 0 !important;
          border: none !important;
        }
        #ai-chat-panel.active ~ #ai-chat-btn {
          display: none !important;
        }
      }
    `;
    document.head.appendChild(styleTag);

    // 2. Inject DOM Structure
    const chatBtn = document.createElement('button');
    chatBtn.id = 'ai-chat-btn';
    chatBtn.setAttribute('aria-label', 'Ask GrindOS AI');
    chatBtn.innerHTML = `
      <svg viewBox="0 0 100 100" class="ai-chat-bot-icon">
        <!-- Claude Mascot Base Horizontal Pill -->
        <rect x="36" y="84" width="28" height="6" rx="3" class="ai-icon-base" />
        
        <!-- Claude Mascot Head Shape -->
        <path d="M 50,15 C 58,15 65,19 69,25 C 76,24 83,29 84,36 C 89,41 89,49 86,55 C 88,62 82,70 75,71 C 68,75 60,78 50,78 C 40,78 32,75 25,71 C 18,70 12,62 14,55 C 11,49 11,41 16,36 C 17,29 24,24 31,25 C 35,19 42,15 50,15 Z" class="ai-icon-head" />
        
        <!-- Claude Mascot Eyes (Contrast Colored) -->
        <rect x="37" y="38" width="6" height="18" rx="3" class="ai-icon-eye eye-left" />
        <rect x="57" y="38" width="6" height="18" rx="3" class="ai-icon-eye eye-right" />
      </svg>
    `;

    const chatPanel = document.createElement('div');
    chatPanel.id = 'ai-chat-panel';
    chatPanel.innerHTML = `
      <div class="ai-chat-header">
        <div class="ai-chat-header-top">
          <span class="ai-chat-header-title" style="display: flex; align-items: center; gap: 8px;">
            <svg viewBox="0 0 100 100" class="ai-chat-bot-icon" style="width: 28px; height: 28px; display: inline-block; vertical-align: middle;">
              <!-- Claude Mascot Base Horizontal Pill -->
              <rect x="36" y="84" width="28" height="6" rx="3" fill="var(--text-1)" />
              <!-- Claude Mascot Head Shape -->
              <path d="M 50,15 C 58,15 65,19 69,25 C 76,24 83,29 84,36 C 89,41 89,49 86,55 C 88,62 82,70 75,71 C 68,75 60,78 50,78 C 40,78 32,75 25,71 C 18,70 12,62 14,55 C 11,49 11,41 16,36 C 17,29 24,24 31,25 C 35,19 42,15 50,15 Z" fill="var(--text-1)" />
              <!-- Claude Mascot Eyes (Blinking) -->
              <rect x="37" y="38" width="6" height="18" rx="3" fill="var(--card)" style="animation: ai-blink 4s infinite ease-in-out; transform-origin: 50px 47px;" />
              <rect x="57" y="38" width="6" height="18" rx="3" fill="var(--card)" style="animation: ai-blink 4s infinite ease-in-out; transform-origin: 50px 47px;" />
            </svg>
            GrindOS AI
          </span>
          <div style="display: flex; align-items: center; gap: 8px;">
            <button class="ai-chat-header-action" id="ai-chat-fullscreen" aria-label="Toggle Fullscreen">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 3 21 3 21 9" />
                <polyline points="9 21 3 21 3 15" />
                <line x1="21" y1="3" x2="14" y2="10" />
                <line x1="3" y1="21" x2="10" y2="14" />
              </svg>
            </button>
            <button class="ai-chat-header-close" id="ai-chat-close">&times;</button>
          </div>
        </div>
        <div class="ai-chat-status-bar">
          <span class="ai-chat-status-dot"></span>
          Placement AI &nbsp;·&nbsp; Ready to help
        </div>
      </div>
      <div class="ai-chat-thread" id="ai-chat-thread"></div>
      <div class="ai-chat-prompts-container" id="ai-chat-prompts"></div>
      <form class="ai-chat-form" id="ai-chat-form">
        <input type="text" class="ai-chat-input" id="ai-chat-input" placeholder="Ask Pranav anything..." autocomplete="off">
        <button type="submit" class="ai-chat-submit">➔</button>
      </form>
    `;

    document.body.appendChild(chatPanel);
    document.body.appendChild(chatBtn);

    // 3. Chat Panel Navigation & State Logics
    let currentMode = 'general';
    let chatHistory = JSON.parse(localStorage.getItem('GrindOS-chat-history') || '[]');

    const threadEl = document.getElementById('ai-chat-thread');
    const inputEl = document.getElementById('ai-chat-input');
    const formEl = document.getElementById('ai-chat-form');
    const promptsEl = document.getElementById('ai-chat-prompts');
    const chatCloseBtn = document.getElementById('ai-chat-close');

    // Quick prompt dictionary configurations
    const modePrompts = {
      general: ["Tell me about yourself", "Explain DBMS ACID properties", "Explain process vs thread", "Describe PlacePro architecture", "GATE study tips"]
    };

    function saveHistory() {
      if (chatHistory.length > 20) {
        chatHistory = chatHistory.slice(-20); // Keep last 20 messages only
      }
      localStorage.setItem('GrindOS-chat-history', JSON.stringify(chatHistory));
    }

    function parseMarkdown(text) {
      if (!text) return '';
      
      let html = text;
      const codeBlocks = [];
      
      // Match fenced code blocks (```mermaid or ```javascript etc)
      html = html.replace(/```(mermaid|[\w-]+)?\n([\s\S]*?)```/g, (match, lang, code) => {
        const index = codeBlocks.length;
        if (lang === 'mermaid') {
          codeBlocks.push(`<div class="mermaid-container"><div class="mermaid">${code.trim()}</div></div>`);
        } else {
          const escapedCode = code
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
          codeBlocks.push(`<pre style="background: var(--bg-3); padding: 12px; border-radius: 8px; font-family: var(--font-mono); font-size: 0.82rem; overflow-x: auto; border: 1px solid var(--border); margin: 12px 0;"><code class="language-${lang || 'txt'}">${escapedCode.trim()}</code></pre>`);
        }
        return `\n\n__BLOCK_PLACEHOLDER_${index}__\n\n`;
      });

      // Escape HTML for normal text parts to prevent XSS
      const parts = html.split(/(__BLOCK_PLACEHOLDER_\d+__)/);
      for (let i = 0; i < parts.length; i++) {
        if (parts[i].startsWith('__BLOCK_PLACEHOLDER_')) continue;
        parts[i] = parts[i]
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          // Inline code: `code`
          .replace(/`(.*?)`/g, '<code style="background: var(--bg-3); padding: 2px 4px; border-radius: 3px; font-family: var(--font-mono); font-size: 0.85rem; color: var(--brand);">$1</code>')
          // Bold: **text**
          .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
          // Italics: *text*
          .replace(/\*(.*?)\*/g, '<em>$1</em>');
      }
      
      html = parts.join('');

      // Split into structural blocks (paragraphs, lists)
      const blocks = html.split(/\n\s*\n/);
      let result = [];
      
      for (let block of blocks) {
        block = block.trim();
        if (!block) continue;
        
        if (block.startsWith('__BLOCK_PLACEHOLDER_')) {
          const index = parseInt(block.match(/\d+/)[0]);
          result.push(codeBlocks[index]);
          continue;
        }
        
        // Bullet list
        if (block.startsWith('* ') || block.startsWith('- ')) {
          const items = block.split(/\n[\*\-]\s+/);
          let listHtml = '<ul style="margin: 8px 0; padding-left: 20px; list-style-type: disc;">';
          for (let item of items) {
            item = item.replace(/^[\*\-]\s+/, '').trim();
            if (item) {
              listHtml += `<li style="margin-bottom: 6px; line-height: 1.5;">${item.replace(/\n/g, '<br>')}</li>`;
            }
          }
          listHtml += '</ul>';
          result.push(listHtml);
        }
        // Numbered list
        else if (/^\d+\.\s+/.test(block)) {
          const items = block.split(/\n\d+\.\s+/);
          let listHtml = '<ol style="margin: 8px 0; padding-left: 20px; list-style-type: decimal;">';
          for (let item of items) {
            item = item.replace(/^\d+\.\s+/, '').trim();
            if (item) {
              listHtml += `<li style="margin-bottom: 6px; line-height: 1.5;">${item.replace(/\n/g, '<br>')}</li>`;
            }
          }
          listHtml += '</ol>';
          result.push(listHtml);
        }
        // Regular paragraph
        else {
          result.push(`<p style="margin: 0 0 12px 0; line-height: 1.5; text-align: justify;">${block.replace(/\n/g, '<br>')}</p>`);
        }
      }
      
      return result.join('');
    }

    function appendMessage(role, text, isWarning = false) {
      const bubble = document.createElement('div');
      if (isWarning) {
        bubble.className = 'ai-chat-bubble warning';
        bubble.innerHTML = `
          <strong style="font-weight: 700; display: block; margin-bottom: 2px;">⚠️ Offline State</strong>
          <span>${text}</span>
        `;
      } else {
        bubble.className = `ai-chat-bubble ${role}`;
        if (role === 'assistant') {
          bubble.innerHTML = parseMarkdown(text);
        } else {
          bubble.textContent = text;
        }
      }
      threadEl.appendChild(bubble);
      threadEl.scrollTop = threadEl.scrollHeight;

      // Render Mermaid diagram blocks if present
      if (role === 'assistant' && text.includes('```mermaid')) {
        setTimeout(() => {
          if (window.mermaid) {
            try {
              window.mermaid.run({
                nodes: bubble.querySelectorAll('.mermaid')
              });
            } catch (e) {
              console.error("Mermaid parsing error:", e);
            }
          }
        }, 80);
      }
    }

    function loadHistory() {
      threadEl.innerHTML = '';
      if (chatHistory.length === 0) {
        appendMessage('assistant', "Hello! I am Pranav's AI helper. Select a category below or ask me any question to begin!");
      } else {
        chatHistory.forEach(msg => appendMessage(msg.role, msg.text));
      }
    }

    function renderQuickPrompts() {
      promptsEl.innerHTML = '';
      const chips = modePrompts[currentMode] || [];
      chips.forEach(chipText => {
        const chip = document.createElement('span');
        chip.className = 'ai-chat-chip';
        chip.textContent = chipText;
        chip.addEventListener('click', () => {
          inputEl.value = chipText;
          formEl.dispatchEvent(new Event('submit'));
        });
        promptsEl.appendChild(chip);
      });
    }

    const maximizeIcon = `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 3 21 3 21 9" /><polyline points="9 21 3 21 3 15" /><line x1="21" y1="3" x2="14" y2="10" /><line x1="3" y1="21" x2="10" y2="14" /></svg>`;
    const minimizeIcon = `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 14 10 14 10 20" /><polyline points="20 10 14 10 14 4" /><line x1="14" y1="10" x2="21" y2="3" /><line x1="10" y1="14" x2="3" y2="21" /></svg>`;

    const chatFullscreenBtn = document.getElementById('ai-chat-fullscreen');

    // Toggle Chat Panel visibility
    chatBtn.addEventListener('click', () => {
      chatPanel.classList.toggle('active');
      if (chatPanel.classList.contains('active')) {
        threadEl.scrollTop = threadEl.scrollHeight;
        inputEl.focus();
      }
    });

    chatCloseBtn.addEventListener('click', () => {
      chatPanel.classList.remove('active');
      chatPanel.classList.remove('fullscreen');
      if (chatFullscreenBtn) chatFullscreenBtn.innerHTML = maximizeIcon;
    });

    // Toggle Chat Panel Fullscreen
    if (chatFullscreenBtn) {
      chatFullscreenBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        chatPanel.classList.toggle('fullscreen');
        if (chatPanel.classList.contains('fullscreen')) {
          chatFullscreenBtn.innerHTML = minimizeIcon;
        } else {
          chatFullscreenBtn.innerHTML = maximizeIcon;
        }
        threadEl.scrollTop = threadEl.scrollHeight;
        inputEl.focus();
      });
    }

    // Close panel on clicking outside
    document.addEventListener('click', e => {
      if (!chatPanel.contains(e.target) && !chatBtn.contains(e.target)) {
        chatPanel.classList.remove('active');
        chatPanel.classList.remove('fullscreen');
        if (chatFullscreenBtn) chatFullscreenBtn.innerHTML = maximizeIcon;
      }
    });

    // Mode Pill Selector clicks
    document.querySelectorAll('.ai-chat-mode-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        document.querySelectorAll('.ai-chat-mode-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        currentMode = this.getAttribute('data-mode');
        renderQuickPrompts();
        inputEl.placeholder = `Ask in ${currentMode.toUpperCase()} mode...`;
        inputEl.focus();
      });
    });

    // Handle Form submissions & API interactions
    formEl.addEventListener('submit', async e => {
      e.preventDefault();
      const text = inputEl.value.trim();
      if (!text) return;

      inputEl.value = '';
      appendMessage('user', text);
      chatHistory.push({ role: 'user', text: text });
      saveHistory();

      // Show temporary loader bubble
      const loadingBubble = document.createElement('div');
      loadingBubble.className = 'ai-chat-bubble assistant';
      loadingBubble.textContent = 'Thinking...';
      threadEl.appendChild(loadingBubble);
      threadEl.scrollTop = threadEl.scrollHeight;

      try {
        const apiBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
          ? 'http://localhost:8000'
          : '';
        const res = await fetch(`${apiBase}/ask`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: text, mode: currentMode })
        });
        
        loadingBubble.remove();

        if (res.ok) {
          const data = await res.json();
          appendMessage('assistant', data.answer);
          chatHistory.push({ role: 'assistant', text: data.answer });
          saveHistory();
        } else {
          appendMessage('assistant', 'The server returned an error: ' + res.statusText);
        }
      } catch (err) {
        loadingBubble.remove();
        appendMessage('assistant', 'AI features require the local backend. Run:\ncd backend && uvicorn main:app --reload', true);
      }
    });

    // ── Unified Calendar Event & Focus Timer Engine ───────────────────────────
    let timerCheckInterval = null;

    // 1. Today's Date String Helper (YYYY-MM-DD)
    function getTodayLocalDateStr() {
      const today = new Date();
      const y = today.getFullYear();
      const m = String(today.getMonth() + 1).padStart(2, '0');
      const d = String(today.getDate()).padStart(2, '0');
      return `${y}-${m}-${d}`;
    }

    // 2. Synthesize Alarm Audio Chime
    function playAlarmSound() {
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        // Chime 1 (A5)
        let osc1 = audioCtx.createOscillator();
        let gain1 = audioCtx.createGain();
        osc1.connect(gain1);
        gain1.connect(audioCtx.destination);
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(880, audioCtx.currentTime);
        gain1.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain1.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
        osc1.start();
        osc1.stop(audioCtx.currentTime + 0.4);
        
        // Chime 2 (C6)
        setTimeout(() => {
          let osc2 = audioCtx.createOscillator();
          let gain2 = audioCtx.createGain();
          osc2.connect(gain2);
          gain2.connect(audioCtx.destination);
          osc2.type = 'sine';
          osc2.frequency.setValueAtTime(1046.5, audioCtx.currentTime);
          gain2.gain.setValueAtTime(0.3, audioCtx.currentTime);
          gain2.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
          osc2.start();
          osc2.stop(audioCtx.currentTime + 0.5);
        }, 150);
      } catch (_) {}
    }

    // 3. Calendar Event Persistence & List Rendering
    window.renderEvents = function() {
      const events = JSON.parse(localStorage.getItem('GrindOS-calendar-events') || '[]');
      events.sort((a, b) => new Date(a.date) - new Date(b.date));

      // Update today's calendar badge count
      const todayStr = getTodayLocalDateStr();
      const todayEvents = events.filter(e => e.date === todayStr);
      const calendarBadge = document.getElementById('global-calendar-badge');
      if (calendarBadge) {
        if (todayEvents.length > 0) {
          calendarBadge.textContent = todayEvents.length;
          calendarBadge.style.display = 'block';
        } else {
          calendarBadge.style.display = 'none';
        }
      }

      // Render on Dashboard List
      const dbEventsList = document.getElementById('upcoming-events-list');
      if (dbEventsList) {
        dbEventsList.innerHTML = '';
        if (events.length === 0) {
          dbEventsList.innerHTML = `<span style="font-size: 0.8rem; color: var(--text-4); font-style: italic;">No coming events scheduled</span>`;
        } else {
          events.forEach(event => {
            const item = document.createElement('div');
            item.className = 'upcoming-event-item';
            const dateObj = new Date(event.date);
            const formattedDate = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', weekday: 'short' });
            item.innerHTML = `
              <div style="display: flex; flex-direction: column; gap: 2px;">
                <strong style="color: var(--text-1); font-size: 0.82rem;">${event.title}</strong>
                <span style="font-size: 0.72rem; color: var(--text-3); font-family: var(--font-mono);">${formattedDate}</span>
              </div>
              <button class="upcoming-event-delete" data-id="${event.id}" title="Delete event">&times;</button>
            `;
            dbEventsList.appendChild(item);
          });
        }
      }

      // Render on Popover List
      const popoverEventsList = document.getElementById('popover-events-list');
      if (popoverEventsList) {
        popoverEventsList.innerHTML = '';
        if (events.length === 0) {
          popoverEventsList.innerHTML = `<span style="font-size: 0.75rem; color: var(--text-4); font-style: italic; text-align: center; display: block; padding: 10px 0;">No coming events scheduled</span>`;
        } else {
          events.forEach(event => {
            const item = document.createElement('div');
            item.className = 'upcoming-event-item';
            item.style.padding = '6px 10px';
            const dateObj = new Date(event.date);
            const formattedDate = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            item.innerHTML = `
              <div style="display: flex; flex-direction: column;">
                <strong style="color: var(--text-1); font-size: 0.78rem;">${event.title}</strong>
                <span style="font-size: 0.68rem; color: var(--text-3);">${formattedDate}</span>
              </div>
              <button class="upcoming-event-delete" data-id="${event.id}" style="font-size: 0.85rem;">&times;</button>
            `;
            popoverEventsList.appendChild(item);
          });
        }
      }
    };

    // Calendar deletion handler (uses delegation)
    document.addEventListener('click', function(e) {
      if (e.target.classList.contains('upcoming-event-delete') || e.target.closest('.upcoming-event-delete')) {
        const target = e.target.classList.contains('upcoming-event-delete') ? e.target : e.target.closest('.upcoming-event-delete');
        const id = parseInt(target.getAttribute('data-id'));
        let events = JSON.parse(localStorage.getItem('GrindOS-calendar-events') || '[]');
        events = events.filter(ev => ev.id !== id);
        localStorage.setItem('GrindOS-calendar-events', JSON.stringify(events));
        window.renderEvents();
        
        // Dynamically refresh Apple Calendar modal details if open
        if (typeof updateAppleCalendarGrid === 'function' && document.getElementById('apple-calendar-modal')?.style.display === 'flex') {
          updateAppleCalendarGrid();
          renderAppleCalendarAgenda();
        }
      }
    });

    // Calendar adding helper
    window.addCalendarEvent = function(dateVal, titleVal) {
      if (!dateVal || !titleVal.trim()) return;
      const events = JSON.parse(localStorage.getItem('GrindOS-calendar-events') || '[]');
      events.push({
        id: Date.now(),
        date: dateVal,
        title: titleVal.trim()
      });
      localStorage.setItem('GrindOS-calendar-events', JSON.stringify(events));
      window.renderEvents();
    };

    // 4. Timer Logic
    function getActiveTimer() {
      return JSON.parse(localStorage.getItem('GrindOS-active-timer') || 'null');
    }

    function saveActiveTimer(timerState) {
      if (timerState) {
        localStorage.setItem('GrindOS-active-timer', JSON.stringify(timerState));
      } else {
        localStorage.removeItem('GrindOS-active-timer');
      }
    }

    function getDurationAndLabelFromInputs() {
      const dbDurationInput = document.getElementById('dashboard-timer-duration');
      const dbLabelInput = document.getElementById('dashboard-timer-label');
      const popoverDurationInput = document.getElementById('popover-timer-duration');
      const popoverLabelInput = document.getElementById('popover-timer-label');
      
      let mins = 25;
      let label = 'Focus Session';
      
      if (dbDurationInput) {
        mins = parseInt(dbDurationInput.value) || 25;
      } else if (popoverDurationInput) {
        mins = parseInt(popoverDurationInput.value) || 25;
      }
      
      if (dbLabelInput && dbLabelInput.value.trim()) {
        label = dbLabelInput.value.trim();
      } else if (popoverLabelInput && popoverLabelInput.value.trim()) {
        label = popoverLabelInput.value.trim();
      }
      
      return { mins, label };
    }

    window.startTimer = function(durationMinutes, labelText) {
      const duration = parseInt(durationMinutes) || 25;
      const label = labelText.trim() || 'Focus Session';
      const endTime = Date.now() + duration * 60 * 1000;
      
      saveActiveTimer({
        endTime: endTime,
        duration: duration,
        label: label,
        isPaused: false
      });

      if (window.Notification && Notification.permission === 'default') {
        Notification.requestPermission();
      }
    };

    window.pauseTimer = function() {
      const timer = getActiveTimer();
      if (!timer || timer.isPaused) return;

      const remaining = Math.max(0, Math.round((timer.endTime - Date.now()) / 1000));
      timer.isPaused = true;
      timer.remainingTimeSecs = remaining;
      timer.endTime = 0;
      saveActiveTimer(timer);
    };

    window.resumeTimer = function() {
      const timer = getActiveTimer();
      if (!timer || !timer.isPaused) return;

      const endTime = Date.now() + (timer.remainingTimeSecs || 0) * 1000;
      timer.isPaused = false;
      timer.endTime = endTime;
      delete timer.remainingTimeSecs;
      saveActiveTimer(timer);
    };

    window.resetTimer = function() {
      saveActiveTimer(null);
    };

    // Synchronize UI display loop
    // Helper to update timer displays with individual digit animations
    window.updateTimerDisplay = function(displayEl, mins, secs) {
      if (!displayEl) return;
      
      const minStr = String(mins).padStart(2, '0');
      const secStr = String(secs).padStart(2, '0');
      
      // If the container doesn't have the timer-digits-container yet, build it
      if (!displayEl.querySelector('.timer-digits-container')) {
        displayEl.innerHTML = `
          <div class="timer-digits-container">
            <div class="timer-digit-wrap"><span class="timer-digit">${minStr[0]}</span></div>
            <div class="timer-digit-wrap"><span class="timer-digit">${minStr[1]}</span></div>
            <span class="timer-colon">:</span>
            <div class="timer-digit-wrap"><span class="timer-digit">${secStr[0]}</span></div>
            <div class="timer-digit-wrap"><span class="timer-digit">${secStr[1]}</span></div>
          </div>
        `;
        return;
      }
      
      const digitWraps = displayEl.querySelectorAll('.timer-digit-wrap');
      if (digitWraps.length !== 4) {
        displayEl.innerHTML = `
          <div class="timer-digits-container">
            <div class="timer-digit-wrap"><span class="timer-digit">${minStr[0]}</span></div>
            <div class="timer-digit-wrap"><span class="timer-digit">${minStr[1]}</span></div>
            <span class="timer-colon">:</span>
            <div class="timer-digit-wrap"><span class="timer-digit">${secStr[0]}</span></div>
            <div class="timer-digit-wrap"><span class="timer-digit">${secStr[1]}</span></div>
          </div>
        `;
        return;
      }
      
      const targetChars = [minStr[0], minStr[1], secStr[0], secStr[1]];
      for (let i = 0; i < 4; i++) {
        const wrapEl = digitWraps[i];
        const targetChar = targetChars[i];
        let currentDigitEl = wrapEl.querySelector('.timer-digit:not(.digit-leaving)');
        
        if (!currentDigitEl) {
          wrapEl.innerHTML = `<span class="timer-digit">${targetChar}</span>`;
        } else if (currentDigitEl.textContent !== targetChar) {
          const nextDigitEl = document.createElement('span');
          nextDigitEl.className = 'timer-digit digit-entering';
          nextDigitEl.textContent = targetChar;
          
          currentDigitEl.classList.add('digit-leaving');
          wrapEl.appendChild(nextDigitEl);
          
          // Force reflow
          void nextDigitEl.offsetWidth;
          
           const oldEl = currentDigitEl;
          setTimeout(() => {
            if (oldEl.parentNode === wrapEl) {
              wrapEl.removeChild(oldEl);
            }
            nextDigitEl.classList.remove('digit-entering');
          }, 450);
        }
      }
    };

    // Synchronize UI display loop
    window.syncTimerUI = function() {
      const timer = getActiveTimer();
      
      const dbDisplay = document.getElementById('dashboard-timer-display');
      const dbLabel = document.getElementById('dashboard-timer-current-label');
      const dbStartBtn = document.getElementById('dashboard-timer-start-btn');
      const dbDurationInput = document.getElementById('dashboard-timer-duration');
      const dbLabelInput = document.getElementById('dashboard-timer-label');
      
      const popoverDisplay = document.getElementById('popover-timer-display');
      const popoverLabel = document.getElementById('popover-timer-current-label');
      const popoverStartBtn = document.getElementById('popover-timer-start-btn');
      const popoverDurationInput = document.getElementById('popover-timer-duration');
      const popoverLabelInput = document.getElementById('popover-timer-label');

      const fsDisplay = document.getElementById('fullscreen-timer-display');
      const fsLabel = document.getElementById('fullscreen-timer-label');
      const fsProgressFill = document.getElementById('fullscreen-timer-progress-fill');
      const fsStartBtn = document.getElementById('fullscreen-timer-start-btn');
      
      const navBadge = document.getElementById('global-timer-badge');

      if (!timer) {
        // No timer active
        const { mins: defaultMins, label: defaultLabel } = getDurationAndLabelFromInputs();
        
        if (dbDisplay) window.updateTimerDisplay(dbDisplay, defaultMins, 0);
        if (dbLabel) dbLabel.textContent = defaultLabel;
        if (dbStartBtn) {
          dbStartBtn.textContent = '▶ Start';
          dbStartBtn.style.background = '#22c55e';
        }

        if (popoverDisplay) window.updateTimerDisplay(popoverDisplay, defaultMins, 0);
        if (popoverLabel) popoverLabel.textContent = defaultLabel;
        if (popoverStartBtn) {
          popoverStartBtn.textContent = '▶ Start';
          popoverStartBtn.style.background = '#22c55e';
        }

        if (fsDisplay) window.updateTimerDisplay(fsDisplay, defaultMins, 0);
        if (fsLabel) fsLabel.textContent = defaultLabel;
        if (fsProgressFill) fsProgressFill.style.width = '0%';
        if (fsStartBtn) {
          fsStartBtn.textContent = '▶ Start';
          fsStartBtn.style.background = '#22c55e';
        }

        if (navBadge) {
          navBadge.style.display = 'none';
        }
        return;
      }

      // Timer active
      let remainingSecs = 0;
      if (timer.isPaused) {
        remainingSecs = timer.remainingTimeSecs || 0;
      } else {
        remainingSecs = Math.max(0, Math.round((timer.endTime - Date.now()) / 1000));
      }

      const mins = Math.floor(remainingSecs / 60);
      const secs = remainingSecs % 60;
      
      if (dbDisplay) window.updateTimerDisplay(dbDisplay, mins, secs);
      if (dbLabel) dbLabel.textContent = timer.label || 'Focus Session';
      if (popoverDisplay) window.updateTimerDisplay(popoverDisplay, mins, secs);
      if (popoverLabel) popoverLabel.textContent = timer.label || 'Focus Session';
      if (fsDisplay) window.updateTimerDisplay(fsDisplay, mins, secs);
      if (fsLabel) fsLabel.textContent = timer.label || 'Focus Session';

      // Sync progress bar
      if (fsProgressFill) {
        const totalSecs = timer.duration * 60;
        const elapsedSecs = totalSecs - remainingSecs;
        const percent = Math.max(0, Math.min(100, Math.round((elapsedSecs / totalSecs) * 100)));
        fsProgressFill.style.width = `${percent}%`;
      }

      if (dbDurationInput && document.activeElement !== dbDurationInput) dbDurationInput.value = timer.duration;
      if (dbLabelInput && document.activeElement !== dbLabelInput) dbLabelInput.value = timer.label;
      if (popoverDurationInput && document.activeElement !== popoverDurationInput) popoverDurationInput.value = timer.duration;
      if (popoverLabelInput && document.activeElement !== popoverLabelInput) popoverLabelInput.value = timer.label;

      if (timer.isPaused) {
        if (dbStartBtn) {
          dbStartBtn.textContent = '▶ Resume';
          dbStartBtn.style.background = '#22c55e';
        }
        if (popoverStartBtn) {
          popoverStartBtn.textContent = '▶ Resume';
          popoverStartBtn.style.background = '#22c55e';
        }
        if (fsStartBtn) {
          fsStartBtn.textContent = '▶ Resume';
          fsStartBtn.style.background = '#22c55e';
        }
        if (navBadge) {
          navBadge.textContent = 'PAUSED';
          navBadge.style.display = 'block';
          navBadge.style.background = '#f59e0b';
        }
      } else {
        if (dbStartBtn) {
          dbStartBtn.textContent = '⏸ Pause';
          dbStartBtn.style.background = '#f59e0b';
        }
        if (popoverStartBtn) {
          popoverStartBtn.textContent = '⏸ Pause';
          popoverStartBtn.style.background = '#f59e0b';
        }
        if (fsStartBtn) {
          fsStartBtn.textContent = '⏸ Pause';
          fsStartBtn.style.background = '#f59e0b';
        }
        if (navBadge) {
          const remainingForBadge = timer.isPaused ? (timer.remainingTimeSecs || 0) : Math.max(0, Math.round((timer.endTime - Date.now()) / 1000));
          const bMins = Math.floor(remainingForBadge / 60);
          const bSecs = remainingForBadge % 60;
          navBadge.textContent = `${String(bMins).padStart(2,'0')}:${String(bSecs).padStart(2,'0')}`;
          navBadge.style.display = 'block';
          navBadge.style.background = 'var(--brand)';
        }
      }

      if (!timer.isPaused && remainingSecs <= 0) {
        saveActiveTimer(null);
        playAlarmSound();

        // Log the session
        const gateSessions = JSON.parse(localStorage.getItem('GrindOS-gate-sessions') || '[]');
        const dateObj = new Date();
        const dateStr = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        gateSessions.push({
          date: dateStr,
          subject: timer.label || 'Focus Session',
          duration: `${timer.duration} mins`
        });
        localStorage.setItem('GrindOS-gate-sessions', JSON.stringify(gateSessions));

        if (window.Notification && Notification.permission === 'granted') {
          new Notification('GrindOS Focus Completed! 🎉', {
            body: `Focus Session "${timer.label || 'Focus Session'}" of ${timer.duration} mins completed.`,
            icon: logoPath
          });
        } else {
          alert(`🎉 Focus Session "${timer.label || 'Focus Session'}" completed!`);
        }

        if (window.updateSmartDailySchedule) {
          window.updateSmartDailySchedule();
        }
      }
    };

    // 5. Initialize Topbar Buttons and popover event listeners
    const topbarRight = document.querySelector('.topbar-right');
    if (topbarRight && !document.getElementById('global-timer-toggle')) {
      const timerBtn = document.createElement('button');
      timerBtn.className = 'icon-btn';
      timerBtn.id = 'global-timer-toggle';
      timerBtn.setAttribute('aria-label', 'Focus Timer');
      // Premium SVG timer icon
      timerBtn.innerHTML = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="pointer-events:none;"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15.5 12"/><path d="M6.3 3.7A10 10 0 0 1 22 12"/></svg><span id="global-timer-badge" style="display: none; position: absolute; top: -4px; right: -4px; background: var(--brand); color: #fff; font-size: 0.58rem; padding: 1px 5px; border-radius: 8px; font-weight: 700; line-height: 1; font-family: var(--font-mono); white-space: nowrap;"></span>`;
      timerBtn.style.position = 'relative';
      timerBtn.style.marginRight = '8px';

      const calendarBtn = document.createElement('button');
      calendarBtn.className = 'icon-btn';
      calendarBtn.id = 'global-calendar-toggle';
      calendarBtn.setAttribute('aria-label', 'Calendar Planner');
      // Premium SVG calendar icon
      calendarBtn.innerHTML = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="pointer-events:none;"><rect x="3" y="4" width="18" height="18" rx="3"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><circle cx="8" cy="15" r="1" fill="currentColor" stroke="none"/><circle cx="12" cy="15" r="1" fill="currentColor" stroke="none"/><circle cx="16" cy="15" r="1" fill="currentColor" stroke="none"/></svg><span id="global-calendar-badge" style="display: none; position: absolute; top: -4px; right: -4px; background: #22c55e; color: #fff; font-size: 0.58rem; padding: 1px 5px; border-radius: 8px; font-weight: 700; line-height: 1;"></span>`;
      calendarBtn.style.position = 'relative';
      calendarBtn.style.marginRight = '8px';

      const themeToggle = document.getElementById('theme-toggle');
      if (themeToggle) {
        topbarRight.insertBefore(calendarBtn, themeToggle);
        topbarRight.insertBefore(timerBtn, calendarBtn);
      } else {
        topbarRight.appendChild(timerBtn);
        topbarRight.appendChild(calendarBtn);
      }

      // Event Listeners for Toggles
      timerBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        togglePopover('timer');
      });

      calendarBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        togglePopover('calendar');
      });
    }

    // Toggle popover function
    function togglePopover(type) {
      const existing = document.getElementById(`global-${type}-popover`);
      
      // Close all popovers first
      document.querySelectorAll('.global-popover').forEach(p => p.remove());

      if (existing) return; // Closed it

      const popover = document.createElement('div');
      popover.className = 'global-popover';
      popover.id = `global-${type}-popover`;

      const toggleBtn = document.getElementById(`global-${type}-toggle`);
      const rect = toggleBtn.getBoundingClientRect();
      popover.style.top = `${rect.bottom + 8}px`;
      popover.style.right = `${window.innerWidth - rect.right}px`;

      if (type === 'timer') {
        popover.innerHTML = `
          <div class="popover-title-row" style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <span class="popover-title">⏱ Focus Timer</span>
            <div style="display: flex; align-items: center; gap: 8px;">
              <button id="popover-timer-fullscreen-btn" style="background: transparent; border: none; color: var(--text-3); font-size: 0.95rem; cursor: pointer; display: flex; align-items: center; padding: 2px; border-radius: 4px; transition: all 0.15s;" title="Fullscreen Mode">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <polyline points="9 21 3 21 3 15"></polyline>
                  <line x1="21" y1="3" x2="14" y2="10"></line>
                  <line x1="3" y1="21" x2="10" y2="14"></line>
                </svg>
              </button>
              <button class="popover-close-btn">&times;</button>
            </div>
          </div>
          <div style="text-align: center; margin: 8px 0;">
            <div id="popover-timer-display" style="font-family: var(--font-mono); font-size: 2.2rem; font-weight: 800; color: var(--text-1); line-height: 1.1;">25:00</div>
            <div id="popover-timer-current-label" style="font-size: 0.75rem; color: var(--text-3); margin-top: 4px; font-weight: 600;">Focus Session</div>
          </div>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            <div style="display: flex; gap: 6px;">
              <input type="number" id="popover-timer-duration" min="1" max="180" value="25" style="width: 60px; padding: 4px 6px; border-radius: 4px; border: 1px solid var(--border); background: var(--bg-2); color: var(--text-1); font-size: 0.8rem; font-weight: bold;" title="Minutes">
              <input type="text" id="popover-timer-label" placeholder="Session Label" style="flex: 1; padding: 4px 6px; border-radius: 4px; border: 1px solid var(--border); background: var(--bg-2); color: var(--text-1); font-size: 0.8rem;">
            </div>
            <div style="display: flex; gap: 6px;">
              <button class="primary-btn" id="popover-timer-start-btn" style="flex: 1; padding: 6px; background: #22c55e; color: #fff; font-size: 0.8rem; font-weight: bold; border-radius: 4px; border: none; cursor: pointer;">▶ Start</button>
              <button class="primary-btn" id="popover-timer-reset-btn" style="flex: 1; padding: 6px; background: var(--bg-3); color: var(--text-2); border: 1px solid var(--border); font-size: 0.8rem; font-weight: bold; border-radius: 4px; cursor: pointer;">↺ Reset</button>
            </div>
          </div>
        `;
        document.body.appendChild(popover);

        // Bind controls
        const startBtn = document.getElementById('popover-timer-start-btn');
        const resetBtn = document.getElementById('popover-timer-reset-btn');
        const popoverFsBtn = document.getElementById('popover-timer-fullscreen-btn');
        
        if (popoverFsBtn) {
          popoverFsBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            window.openFullscreenTimer();
            popover.remove();
          });
        }
        
        startBtn.addEventListener('click', function() {
          const timer = getActiveTimer();
          if (!timer) {
            const mins = document.getElementById('popover-timer-duration').value;
            const lbl = document.getElementById('popover-timer-label').value;
            window.startTimer(mins, lbl || 'Focus Session');
          } else if (timer.isPaused) {
            window.resumeTimer();
          } else {
            window.pauseTimer();
          }
          window.syncTimerUI();
        });

        resetBtn.addEventListener('click', function() {
          window.resetTimer();
          window.syncTimerUI();
        });

      } else {
        popover.innerHTML = `
          <div class="popover-title-row">
            <span class="popover-title">📅 Calendar Events</span>
            <button class="popover-close-btn">&times;</button>
          </div>
          <div style="display: flex; flex-direction: column; gap: 6px; max-height: 150px; overflow-y: auto; margin-bottom: 4px; padding-right: 4px;" id="popover-events-list">
            <!-- List of upcoming events -->
          </div>
          <div style="border-top: 1px solid var(--border); padding-top: 8px; margin-top: 4px; display: flex; flex-direction: column; gap: 6px;">
            <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-3); text-transform: uppercase;">Quick Add Event</span>
            <input type="date" id="popover-event-date" style="padding: 4px 6px; border-radius: 4px; border: 1px solid var(--border); background: var(--bg-2); color: var(--text-1); font-size: 0.8rem;">
            <div style="display: flex; gap: 6px;">
              <input type="text" id="popover-event-title" placeholder="Event Title" style="flex: 1; padding: 4px 6px; border-radius: 4px; border: 1px solid var(--border); background: var(--bg-2); color: var(--text-1); font-size: 0.8rem;">
              <button class="primary-btn" id="popover-event-add-btn" style="padding: 4px 10px; background: var(--brand); color: #fff; font-size: 0.8rem; font-weight: bold; border-radius: 4px; border: none; cursor: pointer;">Add</button>
            </div>
          </div>
        `;
        document.body.appendChild(popover);

        // Set default date to today
        document.getElementById('popover-event-date').value = getTodayLocalDateStr();

        // Bind controls
        const popoverAddBtn = document.getElementById('popover-event-add-btn');
        popoverAddBtn.addEventListener('click', function() {
          const dateVal = document.getElementById('popover-event-date').value;
          const titleInput = document.getElementById('popover-event-title');
          const titleVal = titleInput.value;
          if (!dateVal || !titleVal.trim()) return;
          window.addCalendarEvent(dateVal, titleVal);
          titleInput.value = '';
        });

        const popoverTitleInput = document.getElementById('popover-event-title');
        if (popoverTitleInput) {
          popoverTitleInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
              e.preventDefault();
              popoverAddBtn.click();
            }
          });
        }
      }

      // Bind close button
      popover.querySelector('.popover-close-btn').addEventListener('click', function(e) {
        e.stopPropagation();
        popover.remove();
      });

      // Stop propagation inside popover to prevent clicking outside from closing it
      popover.addEventListener('click', function(e) {
        e.stopPropagation();
      });

      // Render items
      if (type === 'calendar') {
        window.renderEvents();
      } else {
        window.syncTimerUI();
      }
    }

    // Close popovers clicking outside
    document.addEventListener('click', function() {
      document.querySelectorAll('.global-popover').forEach(p => p.remove());
    });

    // 6. Bind Dashboard inputs/buttons if present
    const dbTimerStart = document.getElementById('dashboard-timer-start-btn');
    if (dbTimerStart) {
      dbTimerStart.addEventListener('click', function() {
        const timer = getActiveTimer();
        if (!timer) {
          const mins = document.getElementById('dashboard-timer-duration').value;
          const lbl = document.getElementById('dashboard-timer-label').value;
          window.startTimer(mins, lbl || 'Focus Session');
        } else if (timer.isPaused) {
          window.resumeTimer();
        } else {
          window.pauseTimer();
        }
        window.syncTimerUI();
      });
    }

    const dbTimerReset = document.getElementById('dashboard-timer-reset-btn');
    if (dbTimerReset) {
      dbTimerReset.addEventListener('click', function() {
        window.resetTimer();
        window.syncTimerUI();
      });
    }

    const dbAddBtn = document.getElementById('scheduler-add-btn');
    if (dbAddBtn) {
      const dateInput = document.getElementById('scheduler-date');
      if (dateInput) dateInput.value = getTodayLocalDateStr();

      dbAddBtn.addEventListener('click', function() {
        const dateVal = dateInput.value;
        const titleInput = document.getElementById('scheduler-title');
        const titleVal = titleInput.value;
        if (!dateVal || !titleVal.trim()) return;
        window.addCalendarEvent(dateVal, titleVal);
        titleInput.value = '';
      });

      const titleInput = document.getElementById('scheduler-title');
      if (titleInput) {
        titleInput.addEventListener('keydown', function(e) {
          if (e.key === 'Enter') {
            e.preventDefault();
            dbAddBtn.click();
          }
        });
      }
    }

    // 7. Define window.updateSmartDailySchedule
    window.updateSmartDailySchedule = function() {
      const monthEl = document.getElementById('calendar-header-month');
      const dateEl = document.getElementById('calendar-header-date');
      const dayNameEl = document.getElementById('calendar-header-dayname');
      
      if (!monthEl || !dateEl || !dayNameEl) return;

      const todayDate = new Date();
      const monthName = todayDate.toLocaleDateString('en-US', { month: 'short' }).toUpperCase();
      const dateNum = todayDate.getDate();
      const dayName = todayDate.toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase();
      
      monthEl.textContent = monthName;
      dateEl.textContent = dateNum;
      dayNameEl.textContent = dayName;

      function formatLocalDate(date) {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
      }
      
      const todayStr = formatLocalDate(todayDate);

      const activityLog = JSON.parse(localStorage.getItem('GrindOS-activity-log') || '{}');
      const todayActivity = activityLog[todayStr] || { habits: 0, lc: 0, topics: 0 };
      const habits = JSON.parse(localStorage.getItem('GrindOS-habits') || '[]');
      const dsaSolved = JSON.parse(localStorage.getItem('GrindOS-dsa-solved') || '{}');
      const gateSessions = JSON.parse(localStorage.getItem('GrindOS-gate-sessions') || '[]');
      
      const tasksList = document.getElementById('calendar-tasks-list');
      if (!tasksList) return;
      
      tasksList.innerHTML = '';
      let pendingCount = 0;

      // Task 1: LeetCode Solve
      const dsaTask = document.createElement('div');
      dsaTask.className = 'calendar-task-item';
      
      const todayStart = new Date();
      todayStart.setHours(0,0,0,0);
      const todayEnd = new Date();
      todayEnd.setHours(23,59,59,999);
      
      let solvedToday = false;
      Object.values(dsaSolved).forEach(val => {
        if (typeof val === 'number' && val >= todayStart.getTime() && val <= todayEnd.getTime()) {
          solvedToday = true;
        }
      });
      
      if (solvedToday || (todayActivity.lc && todayActivity.lc > 0)) {
        dsaTask.innerHTML = `
          <div class="calendar-task-left">
            <span class="calendar-task-status done">✓</span>
            <span style="font-weight: 600;">LeetCode Solve</span>
            <span style="color: var(--text-3); font-size: 0.8rem;">— Problem marked solved today!</span>
          </div>
          <span style="font-size: 0.72rem; font-weight: 700; color: #22c55e; background: rgba(34,197,94,0.1); padding: 2px 8px; border-radius: 12px; text-transform: uppercase;">Completed</span>
        `;
      } else {
        pendingCount++;
        dsaTask.innerHTML = `
          <div class="calendar-task-left">
            <span class="calendar-task-status pending"></span>
            <span style="font-weight: 600;">LeetCode Solve</span>
            <span style="color: var(--text-3); font-size: 0.8rem;">— Solve 1 DSA problem cold beat.</span>
          </div>
          <a href="tracker.html#dsa" class="calendar-task-action">Go Solve →</a>
        `;
      }
      tasksList.appendChild(dsaTask);

      // Task 2: Habits Completion
      const habitsTask = document.createElement('div');
      habitsTask.className = 'calendar-task-item';
      const totalHabits = habits.length || 5;
      const completedHabits = habits.filter(h => h.completedToday).length;
      const allHabitsDone = completedHabits === totalHabits && totalHabits > 0;
      
      if (allHabitsDone) {
        habitsTask.innerHTML = `
          <div class="calendar-task-left">
            <span class="calendar-task-status done">✓</span>
            <span style="font-weight: 600;">Daily Habits</span>
            <span style="color: var(--text-3); font-size: 0.8rem;">— All ${completedHabits}/${totalHabits} daily habits checked!</span>
          </div>
          <span style="font-size: 0.72rem; font-weight: 700; color: #22c55e; background: rgba(34,197,94,0.1); padding: 2px 8px; border-radius: 12px; text-transform: uppercase;">Completed</span>
        `;
      } else {
        pendingCount++;
        habitsTask.innerHTML = `
          <div class="calendar-task-left">
            <span class="calendar-task-status pending"></span>
            <span style="font-weight: 600;">Daily Habits</span>
            <span style="color: var(--text-3); font-size: 0.8rem;">— Checked off ${completedHabits}/${totalHabits} habits today.</span>
          </div>
          <a href="tracker.html#habits" class="calendar-task-action">Complete →</a>
        `;
      }
      tasksList.appendChild(habitsTask);

      // Task 3: Focus Study Session
      const focusTask = document.createElement('div');
      focusTask.className = 'calendar-task-item';
      
      let loggedToday = false;
      const localDateStr = todayDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
      gateSessions.forEach(s => {
        if (s.date === localDateStr) {
          loggedToday = true;
        }
      });
      
      if (loggedToday) {
        focusTask.innerHTML = `
          <div class="calendar-task-left">
            <span class="calendar-task-status done">✓</span>
            <span style="font-weight: 600;">GATE Focus Session</span>
            <span style="color: var(--text-3); font-size: 0.8rem;">— Logged study session for today!</span>
          </div>
          <span style="font-size: 0.72rem; font-weight: 700; color: #22c55e; background: rgba(34,197,94,0.1); padding: 2px 8px; border-radius: 12px; text-transform: uppercase;">Completed</span>
        `;
      } else {
        pendingCount++;
        focusTask.innerHTML = `
          <div class="calendar-task-left">
            <span class="calendar-task-status pending"></span>
            <span style="font-weight: 600;">GATE Focus Session</span>
            <span style="color: var(--text-3); font-size: 0.8rem;">— Complete at least one focus block.</span>
          </div>
          <a href="tracker.html#gate" class="calendar-task-action">Start Timer →</a>
        `;
      }
      tasksList.appendChild(focusTask);

      const summaryText = document.getElementById('calendar-recommendation-summary');
      if (summaryText) {
        if (pendingCount === 0) {
          summaryText.innerHTML = `🔥 <strong>All non-negotiables checked!</strong> You are 100% prepared today. Keep the momentum going!`;
        } else {
          summaryText.innerHTML = `You have <strong>${pendingCount} pending task(s)</strong> to finish today to maintain your streak and compound your progress.`;
        }
      }
    };

    // ── Fullscreen Focus Timer Overlay ───────────────────────────────────────
    if (!document.getElementById('fullscreen-timer-overlay')) {
      const fsOverlay = document.createElement('div');
      fsOverlay.id = 'fullscreen-timer-overlay';
      fsOverlay.style.cssText = 'display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #09090b; z-index: 10000; flex-direction: column; align-items: center; justify-content: center; color: #fff; font-family: var(--font-sans); animation: overlayFadeIn 0.3s ease;';
      fsOverlay.innerHTML = `
        <!-- Exit Button -->
        <button id="fullscreen-timer-exit" style="position: absolute; top: 24px; right: 24px; background: transparent; border: none; color: #a1a1aa; font-size: 2.2rem; cursor: pointer; transition: color 0.2s; line-height: 1;">&times;</button>
        
        <div style="z-index: 10001; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 24px; width: 100%; max-width: 600px; padding: 0 24px;">
          <!-- Subject Label -->
          <h2 id="fullscreen-timer-label" style="font-size: 2.2rem; font-weight: 700; color: #fafafa; margin: 0; letter-spacing: -0.02em;">Focus Session</h2>
          
          <!-- Large Timer Display -->
          <div id="fullscreen-timer-display" style="font-family: var(--font-mono); font-size: 8rem; font-weight: 800; color: var(--brand); line-height: 1; letter-spacing: -0.03em;">25:00</div>
          
          <!-- Interactive Progress bar -->
          <div style="width: 320px; max-width: 100%; height: 6px; background: #27272a; border-radius: 3px; overflow: hidden; margin-top: 10px; position: relative;">
            <div id="fullscreen-timer-progress-fill" style="width: 0%; height: 100%; background: var(--brand); transition: width 0.2s linear;"></div>
          </div>

          <!-- Controls -->
          <div style="display: flex; gap: 16px; margin-top: 20px;">
            <button id="fullscreen-timer-start-btn" style="padding: 12px 32px; background: #22c55e; color: #fff; font-size: 1.1rem; font-weight: 700; border: none; border-radius: 8px; cursor: pointer; transition: all 0.2s;">▶ Start</button>
            <button id="fullscreen-timer-reset-btn" style="padding: 12px 32px; background: #27272a; color: #e4e4e7; font-size: 1.1rem; font-weight: 700; border: 1px solid #3f3f46; border-radius: 8px; cursor: pointer; transition: all 0.2s;">↺ Reset</button>
          </div>
        </div>
      `;
      document.body.appendChild(fsOverlay);

      // Event listeners for Fullscreen controls
      document.getElementById('fullscreen-timer-exit').addEventListener('click', function() {
        exitFullscreenTimer();
      });
      document.getElementById('fullscreen-timer-start-btn').addEventListener('click', function() {
        const timer = getActiveTimer();
        if (!timer) {
          const { mins, label } = getDurationAndLabelFromInputs();
          window.startTimer(mins, label);
        } else if (timer.isPaused) {
          window.resumeTimer();
        } else {
          window.pauseTimer();
        }
        window.syncTimerUI();
      });
      document.getElementById('fullscreen-timer-reset-btn').addEventListener('click', function() {
        window.resetTimer();
        window.syncTimerUI();
      });
    }

    window.openFullscreenTimer = function() {
      const overlay = document.getElementById('fullscreen-timer-overlay');
      if (overlay) {
        overlay.style.display = 'flex';
        window.syncTimerUI();
        
        // Enter native fullscreen (like YouTube)
        if (overlay.requestFullscreen) {
          overlay.requestFullscreen().catch(err => console.log(err));
        } else if (overlay.webkitRequestFullscreen) {
          overlay.webkitRequestFullscreen();
        } else if (overlay.msRequestFullscreen) {
          overlay.msRequestFullscreen();
        }
      }
    };

    window.exitFullscreenTimer = function() {
      const overlay = document.getElementById('fullscreen-timer-overlay');
      if (overlay) {
        overlay.style.display = 'none';
      }
      
      // Exit native fullscreen if active
      if (document.fullscreenElement || document.webkitFullscreenElement) {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen();
        }
      }
    };

    // Listen for native exit fullscreen (e.g. Escape key) to hide overlay
    document.addEventListener('fullscreenchange', () => {
      if (!document.fullscreenElement) {
        const overlay = document.getElementById('fullscreen-timer-overlay');
        if (overlay) overlay.style.display = 'none';
      }
    });
    document.addEventListener('webkitfullscreenchange', () => {
      if (!document.webkitFullscreenElement) {
        const overlay = document.getElementById('fullscreen-timer-overlay');
        if (overlay) overlay.style.display = 'none';
      }
    });

    // Bind triggers for fullscreen on dashboard timer card
    const dbFsBtn = document.getElementById('dashboard-timer-fullscreen-btn');
    if (dbFsBtn) {
      dbFsBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        window.openFullscreenTimer();
      });
    }


    // ── Apple Calendar Planner Modal ─────────────────────────────────────────
    let calCurrentDate = new Date();
    let calSelectedDay = new Date().getDate();

    if (!document.getElementById('apple-calendar-modal')) {
      const calModal = document.createElement('div');
      calModal.id = 'apple-calendar-modal';
      calModal.style.cssText = 'display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0, 0, 0, 0.6); z-index: 10005; align-items: center; justify-content: center; font-family: var(--font-sans); padding: 16px; backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); animation: modalFadeIn 0.25s ease;';
      calModal.innerHTML = `
        <!-- Modal Card -->
        <div class="apple-calendar-card" style="background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg), 0 20px 40px rgba(0,0,0,0.2); width: 850px; max-width: 100%; height: 580px; display: flex; overflow: hidden; position: relative; animation: modalSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);">
          <!-- Close Button -->
          <button id="apple-calendar-close" style="position: absolute; top: 12px; right: 12px; background: transparent; border: none; color: var(--text-3); font-size: 1.5rem; cursor: pointer; z-index: 10; line-height: 1;">&times;</button>
          
          <!-- Left Column: Calendar Sheet -->
          <div style="flex: 1.2; padding: 24px; border-right: 1px solid var(--border); display: flex; flex-direction: column; justify-content: space-between; overflow-y: auto;">
            <div>
              <!-- Calendar Header (Month + Nav) -->
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
                <h3 id="cal-modal-month-year" style="font-size: 1.2rem; font-weight: 700; color: var(--text-1); margin: 0;">May 2026</h3>
                <div style="display: flex; gap: 8px;">
                  <button id="cal-modal-prev-month" style="background: var(--bg-3); border: 1px solid var(--border); border-radius: 6px; padding: 4px 10px; cursor: pointer; color: var(--text-2); font-weight: bold; transition: all 0.15s;">&larr;</button>
                  <button id="cal-modal-next-month" style="background: var(--bg-3); border: 1px solid var(--border); border-radius: 6px; padding: 4px 10px; cursor: pointer; color: var(--text-2); font-weight: bold; transition: all 0.15s;">&rarr;</button>
                </div>
              </div>

              <!-- Weekday Headers -->
              <div style="display: grid; grid-template-columns: repeat(7, 1fr); text-align: center; margin-bottom: 8px; border-bottom: 1px solid var(--border); padding-bottom: 6px;">
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-4);">SUN</span>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-4);">MON</span>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-4);">TUE</span>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-4);">WED</span>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-4);">THU</span>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-4);">FRI</span>
                <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-4);">SAT</span>
              </div>

              <!-- Days Grid -->
              <div id="cal-modal-days-grid" style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; text-align: center;">
                <!-- Days populated dynamically -->
              </div>
            </div>

            <div style="font-size: 0.75rem; color: var(--text-3); display: flex; align-items: center; gap: 12px; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border); flex-wrap: wrap;">
              <span style="display: inline-flex; align-items: center; gap: 4px;"><span style="width: 8px; height: 8px; border-radius: 50%; background: var(--brand); display: inline-block;"></span> Today</span>
              <span style="display: inline-flex; align-items: center; gap: 4px;"><span style="width: 8px; height: 8px; border-radius: 50%; border: 1px dashed var(--brand); background: var(--brand-light); display: inline-block;"></span> Selected</span>
              <span style="display: inline-flex; align-items: center; gap: 4px;"><span style="width: 4px; height: 4px; border-radius: 50%; background: var(--text-3); display: inline-block;"></span> Has Event</span>
            </div>
          </div>

          <!-- Right Column: Agenda Detail Panel -->
          <div style="flex: 0.8; padding: 24px; background: var(--bg-2); display: flex; flex-direction: column; justify-content: space-between; overflow-y: auto;">
            <div style="display: flex; flex-direction: column; gap: 16px;">
              <!-- Selected Date Header -->
              <div>
                <h4 id="cal-modal-selected-date-title" style="font-size: 1.05rem; font-weight: 700; color: var(--text-1); margin: 0 0 2px 0;">Sunday, May 24</h4>
                <span style="font-size: 0.78rem; color: var(--text-3); font-weight: 600;">Daily Agenda Details</span>
              </div>

              <!-- Events List for Date -->
              <div>
                <h5 style="font-size: 0.78rem; font-weight: 700; color: var(--text-3); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Events / Tasks</h5>
                <div id="cal-modal-events-list" style="display: flex; flex-direction: column; gap: 6px; max-height: 120px; overflow-y: auto; padding-right: 4px;">
                  <!-- Events -->
                </div>
              </div>

              <!-- Logs (Focus sessions, LeetCode solved, habits) for Date -->
              <div>
                <h5 style="font-size: 0.78rem; font-weight: 700; color: var(--text-3); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Grind Logs</h5>
                <div id="cal-modal-logs-list" style="display: flex; flex-direction: column; gap: 6px; max-height: 120px; overflow-y: auto; padding-right: 4px;">
                  <!-- Logs -->
                </div>
              </div>
            </div>

            <!-- Quick Add Task Form -->
            <div style="border-top: 1px solid var(--border); padding-top: 14px; margin-top: 16px;">
              <h5 style="font-size: 0.78rem; font-weight: 700; color: var(--text-3); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Add Event to Date</h5>
              <div style="display: flex; gap: 6px;">
                <input type="text" id="cal-modal-add-title" placeholder="Event title..." style="flex: 1; padding: 6px 10px; border-radius: 6px; border: 1px solid var(--border); background: var(--card); color: var(--text-1); font-size: 0.8rem;">
                <button id="cal-modal-add-btn" style="padding: 6px 14px; background: var(--brand); color: #fff; font-size: 0.8rem; font-weight: bold; border-radius: 6px; border: none; cursor: pointer; transition: background 0.15s;">Add</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      `;
      document.body.appendChild(calModal);

      // Event listeners for Apple Calendar Modal controls
      document.getElementById('apple-calendar-close').addEventListener('click', function() {
        closeAppleCalendar();
      });
      document.getElementById('apple-calendar-modal').addEventListener('click', function(e) {
        if (e.target === document.getElementById('apple-calendar-modal')) {
          closeAppleCalendar();
        }
      });

      document.getElementById('cal-modal-prev-month').addEventListener('click', function() {
        calCurrentDate.setMonth(calCurrentDate.getMonth() - 1);
        updateAppleCalendarGrid();
      });

      document.getElementById('cal-modal-next-month').addEventListener('click', function() {
        calCurrentDate.setMonth(calCurrentDate.getMonth() + 1);
        updateAppleCalendarGrid();
      });

      document.getElementById('cal-modal-add-btn').addEventListener('click', function() {
        const titleInput = document.getElementById('cal-modal-add-title');
        const title = titleInput.value.trim();
        if (!title) return;
        const year = calCurrentDate.getFullYear();
        const month = String(calCurrentDate.getMonth() + 1).padStart(2, '0');
        const day = String(calSelectedDay).padStart(2, '0');
        const dateStr = `${year}-${month}-${day}`;
        window.addCalendarEvent(dateStr, title);
        titleInput.value = '';
        updateAppleCalendarGrid();
        renderAppleCalendarAgenda();
      });

      document.getElementById('cal-modal-add-title').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          document.getElementById('cal-modal-add-btn').click();
        }
      });
    }

    window.openAppleCalendar = function() {
      const modal = document.getElementById('apple-calendar-modal');
      if (modal) {
        modal.style.display = 'flex';
        calCurrentDate = new Date();
        calSelectedDay = new Date().getDate();
        updateAppleCalendarGrid();
        renderAppleCalendarAgenda();
      }
    };

    window.closeAppleCalendar = function() {
      const modal = document.getElementById('apple-calendar-modal');
      if (modal) {
        modal.style.display = 'none';
      }
    };

    function updateAppleCalendarGrid() {
      const daysGrid = document.getElementById('cal-modal-days-grid');
      const monthYearTitle = document.getElementById('cal-modal-month-year');
      if (!daysGrid || !monthYearTitle) return;

      const year = calCurrentDate.getFullYear();
      const month = calCurrentDate.getMonth();

      const monthName = calCurrentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
      monthYearTitle.textContent = monthName;

      daysGrid.innerHTML = '';

      const firstDayIndex = new Date(year, month, 1).getDay();
      const daysInMonth = new Date(year, month + 1, 0).getDate();

      for (let i = 0; i < firstDayIndex; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'cal-day-cell empty-cell';
        daysGrid.appendChild(emptyCell);
      }

      const today = new Date();
      const events = JSON.parse(localStorage.getItem('GrindOS-calendar-events') || '[]');

      for (let day = 1; day <= daysInMonth; day++) {
        const cell = document.createElement('div');
        cell.className = 'cal-day-cell';
        cell.textContent = day;

        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

        if (today.getFullYear() === year && today.getMonth() === month && today.getDate() === day) {
          cell.classList.add('today-cell');
        }

        if (calSelectedDay === day) {
          cell.classList.add('selected-day');
        }

        const dayHasEvents = events.some(e => e.date === dateStr);
        if (dayHasEvents) {
          const dot = document.createElement('span');
          dot.className = 'cal-day-dot';
          cell.appendChild(dot);
        }

        cell.addEventListener('click', function() {
          calSelectedDay = day;
          document.querySelectorAll('.cal-day-cell').forEach(c => c.classList.remove('selected-day'));
          cell.classList.add('selected-day');
          renderAppleCalendarAgenda();
        });

        daysGrid.appendChild(cell);
      }
    }

    function renderAppleCalendarAgenda() {
      const year = calCurrentDate.getFullYear();
      const month = calCurrentDate.getMonth();
      const day = calSelectedDay;

      const dateObj = new Date(year, month, day);
      const selectedDateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

      const agendaTitle = document.getElementById('cal-modal-selected-date-title');
      if (agendaTitle) {
        agendaTitle.textContent = dateObj.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' });
      }

      const eventsList = document.getElementById('cal-modal-events-list');
      if (eventsList) {
        eventsList.innerHTML = '';
        const events = JSON.parse(localStorage.getItem('GrindOS-calendar-events') || '[]');
        const dayEvents = events.filter(e => e.date === selectedDateStr);

        if (dayEvents.length === 0) {
          eventsList.innerHTML = `<span style="font-size: 0.78rem; color: var(--text-4); font-style: italic;">No events for this date</span>`;
        } else {
          dayEvents.forEach(event => {
            const item = document.createElement('div');
            item.className = 'upcoming-event-item';
            item.style.padding = '6px 10px';
            item.innerHTML = `
              <span style="color: var(--text-1); font-size: 0.78rem; font-weight: 600;">${event.title}</span>
              <button class="upcoming-event-delete" data-id="${event.id}" style="font-size: 0.85rem;">&times;</button>
            `;
            eventsList.appendChild(item);
          });
        }
      }

      const logsList = document.getElementById('cal-modal-logs-list');
      if (logsList) {
        logsList.innerHTML = '';

        const gateSessions = JSON.parse(localStorage.getItem('GrindOS-gate-sessions') || '[]');
        const formattedDateForGate = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        const daySessions = gateSessions.filter(s => s.date === formattedDateForGate);

        const dsaSolved = JSON.parse(localStorage.getItem('GrindOS-dsa-solved') || '{}');
        const dayStart = new Date(year, month, day, 0, 0, 0, 0).getTime();
        const dayEnd = new Date(year, month, day, 23, 59, 59, 999).getTime();
        let dsaCount = 0;
        Object.values(dsaSolved).forEach(ts => {
          if (typeof ts === 'number' && ts >= dayStart && ts <= dayEnd) {
            dsaCount++;
          }
        });

        const activityLog = JSON.parse(localStorage.getItem('GrindOS-activity-log') || '{}');
        const activity = activityLog[selectedDateStr];

        let logsHTML = '';

        if (daySessions.length > 0) {
          daySessions.forEach(s => {
            logsHTML += `
              <div style="display: flex; align-items: center; gap: 6px; font-size: 0.78rem; color: var(--text-2); background: var(--bg-3); padding: 5px 8px; border-radius: 4px;">
                <span style="color: var(--brand);">⏱</span> 
                <span>Focus: <strong>${s.subject}</strong> (${s.duration})</span>
              </div>
            `;
          });
        }

        if (dsaCount > 0) {
          logsHTML += `
            <div style="display: flex; align-items: center; gap: 6px; font-size: 0.78rem; color: var(--text-2); background: var(--bg-3); padding: 5px 8px; border-radius: 4px;">
              <span style="color: #3b82f6;">💻</span>
              <span>Solved <strong>${dsaCount} LeetCode</strong> problems</span>
            </div>
          `;
        }

        if (activity) {
          if (activity.habits > 0) {
            logsHTML += `
              <div style="display: flex; align-items: center; gap: 6px; font-size: 0.78rem; color: var(--text-2); background: var(--bg-3); padding: 5px 8px; border-radius: 4px;">
                <span style="color: #10b981;">✓</span>
                <span>Completed <strong>${activity.habits} habits</strong></span>
              </div>
            `;
          }
          if (activity.topics > 0) {
            logsHTML += `
              <div style="display: flex; align-items: center; gap: 6px; font-size: 0.78rem; color: var(--text-2); background: var(--bg-3); padding: 5px 8px; border-radius: 4px;">
                <span style="color: var(--brand);">📖</span>
                <span>Read <strong>${activity.topics} theory topics</strong></span>
              </div>
            `;
          }
        }

        if (!logsHTML) {
          logsList.innerHTML = `<span style="font-size: 0.78rem; color: var(--text-4); font-style: italic;">No grind activity recorded</span>`;
        } else {
          logsList.innerHTML = logsHTML;
        }
      }
    }

    // Connect topbar calendar trigger to Apple Calendar instead of Popover
    // Using delegation to avoid the outerHTML listener-removal hack
    document.addEventListener('click', function(e) {
      const calToggle = e.target.closest('#global-calendar-toggle');
      if (calToggle) {
        e.stopPropagation();
        // Close any timer popovers first
        document.querySelectorAll('.global-popover').forEach(p => p.remove());
        window.openAppleCalendar();
      }
    }, true); // capture phase so it fires before the close-popover handler

    // Connect Dashboard calendar card sheet click
    const dbCalSheet = document.querySelector('#dashboard-calendar-card .calendar-icon-sheet');
    if (dbCalSheet) {
      dbCalSheet.style.cursor = 'pointer';
      dbCalSheet.title = 'Open Apple Calendar Planner';
      dbCalSheet.addEventListener('click', function() {
        window.openAppleCalendar();
      });
    }

    const dbOpenCalBtn = document.getElementById('dashboard-open-calendar-btn');
    if (dbOpenCalBtn) {
      dbOpenCalBtn.addEventListener('click', function() {
        window.openAppleCalendar();
      });
    }


    // 8. Start Background Intervals
    window.renderEvents();
    window.syncTimerUI();
    if (!timerCheckInterval) {
      timerCheckInterval = setInterval(function() {
        window.syncTimerUI();
      }, 1000);
    }

    // Initialize panel components
    loadHistory();
    renderQuickPrompts();
  });
})();
