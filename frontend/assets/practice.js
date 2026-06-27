document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyzeBtn');
  const resultsContainer = document.getElementById('results');
  const loading = document.getElementById('loading');
  const loadingMsg = document.getElementById('loadingMsg');
  const problemTextarea = document.getElementById('problem');
  const starterCodeTextarea = document.getElementById('starterCode');
  const completionFormatSelect = document.getElementById('completionFormat');
  const ocrTrigger = document.getElementById('ocrTrigger');
  const ocrInput = document.getElementById('ocrInput');
  const modelProviderEl = document.getElementById('modelProvider');
  const claudeModelGroupEl = document.getElementById('claudeModelGroup');
  const oaModeToggle = document.getElementById('oaModeToggle');
  const envSelect = document.getElementById('environment');
  const amazonMlModeToggle = document.getElementById('amazonMlModeToggle');
  // MLSS Panel elements
  const mlssInputPanel = document.getElementById('mlssInputPanel');
  const mlssSectionSelector = document.getElementById('mlssSectionSelector'); // legacy, hidden
  const mlssChatPanel = document.getElementById('mlssChatPanel');
  const mlssChatMessages = document.getElementById('mlssChatMessages');
  const mlssChatInput = document.getElementById('mlssChatInput');
  const mlssChatSendBtn = document.getElementById('mlssChatSendBtn');
  const mlssSectionLabel = document.getElementById('mlssSectionLabel');
  const mlssSendBtn = document.getElementById('mlssSendBtn');
  const mlssQuestionInput = document.getElementById('mlssQuestionInput');
  const mlssCodeStub = document.getElementById('mlssCodeStub');
  const mlssCodeGutter = document.getElementById('mlssCodeGutter');
  const mlssCodeStubArea = document.getElementById('mlssCodeStubArea');
  const mlssStubToggle = document.getElementById('mlssStubToggle');
  const mainWorkspaceLayout = document.getElementById('mainWorkspaceLayout');
  
  const apiBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
      ? 'http://localhost:8000' 
      : '';

  // 1. Model Selection Toggle
  if (modelProviderEl && claudeModelGroupEl) {
    const toggleClaude = () => {
      if (modelProviderEl.value === 'claude') {
        claudeModelGroupEl.classList.remove('hidden');
      } else {
        claudeModelGroupEl.classList.add('hidden');
      }
    };
    modelProviderEl.addEventListener('change', toggleClaude);
    toggleClaude(); // Initial check on load
  }

  // 1a. OA Mode Toggle logic
  if (oaModeToggle && envSelect) {
    const langSelect = document.getElementById('language');
    let lastSelectedLanguage = langSelect ? langSelect.value : 'python3';

    // Force environment context to 'leetcode' (OFF) on initial load
    envSelect.value = 'leetcode';

    if (langSelect) {
      langSelect.addEventListener('change', () => {
        if (envSelect.value !== 'oa') {
          lastSelectedLanguage = langSelect.value;
        }
      });
    }

    const syncOaMode = () => {
      const active = envSelect.value === 'oa';
      if (active) {
        oaModeToggle.classList.add('active');
      } else {
        oaModeToggle.classList.remove('active');
      }
      const label = oaModeToggle.querySelector('span');
      if (label) {
        label.textContent = active ? 'OA Mode: ON' : 'OA Mode: OFF';
      }
      // Force Python 3 selection & lock when OA mode is active
      if (langSelect) {
        if (active) {
          lastSelectedLanguage = langSelect.value;
          langSelect.value = 'python3';
          langSelect.disabled = true;
        } else {
          langSelect.disabled = false;
          langSelect.value = lastSelectedLanguage;
        }
      }

      // Hide extra options on the left under OA Mode
      const advOpt = document.getElementById('advancedOptionsAccordion');
      const codeVerify = document.getElementById('codeVerificationWrapper');
      
      if (active) {
        if (advOpt) advOpt.classList.add('hidden');
        if (codeVerify) codeVerify.classList.add('hidden');
      } else {
        if (advOpt) advOpt.classList.remove('hidden');
        if (codeVerify) codeVerify.classList.remove('hidden');
      }
    };

    oaModeToggle.addEventListener('click', (e) => {
      e.preventDefault();
      // Disable AMAZONML when switching OA on
      if (amazonMlModeActive && envSelect.value !== 'oa') {
        // do nothing extra, OA takes over
      }
      if (amazonMlModeActive) {
        setAmazonMlMode(false);
      }
      const isActive = envSelect.value === 'oa';
      envSelect.value = isActive ? 'leetcode' : 'oa';
      syncOaMode();
    });

    syncOaMode(); // Initial check on load
  }

  // 2. Starter Code Tab Key Interception
  if (starterCodeTextarea) {
    starterCodeTextarea.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        e.preventDefault();
        const start = starterCodeTextarea.selectionStart;
        const end = starterCodeTextarea.selectionEnd;
        const value = starterCodeTextarea.value;
        starterCodeTextarea.value = value.substring(0, start) + "    " + value.substring(end);
        starterCodeTextarea.selectionStart = starterCodeTextarea.selectionEnd = start + 4;
      }
    });
  }

  // 3. Solve Actions Keyboard Shortcuts (Cmd+Enter / Ctrl+Enter)
  [problemTextarea, starterCodeTextarea].forEach(el => {
    if (el) {
      el.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
          e.preventDefault();
          if (analyzeBtn && !analyzeBtn.disabled) {
            analyzeBtn.click();
          }
        }
      });
    }
  });

  // 4. OCR Trigger & Clipboard Image Paste Logic
  if (ocrTrigger && ocrInput) {
    ocrTrigger.addEventListener('click', (e) => {
      e.preventDefault();
      ocrInput.click();
    });

    ocrInput.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if (file) {
        await processOcrFile(file);
      }
    });
  }

  // Listen to clipboard pastes on problem statement
  if (problemTextarea) {
    problemTextarea.addEventListener('paste', async (e) => {
      const items = (e.clipboardData || e.originalEvent.clipboardData).items;
      for (let item of items) {
        if (item.kind === 'file' && item.type.startsWith('image/')) {
          e.preventDefault();
          const file = item.getAsFile();
          await processOcrFile(file);
          break;
        }
      }
    });
  }

  // Helper to extract text from image using backend API
  async function processOcrFile(file) {
    if (!ocrTrigger || !problemTextarea) return;
    
    ocrTrigger.disabled = true;
    const originalText = ocrTrigger.innerHTML;
    ocrTrigger.innerHTML = '<div class="spinner" style="width: 14px; height: 14px; border-width: 2px; border-top-color: var(--text-2); margin-right: 4px; display: inline-block; vertical-align: middle; animation: spin 1s linear infinite;"></div> Extracting...';

    const reader = new FileReader();
    reader.onload = async (event) => {
      const base64Data = event.target.result;
      
      try {
        const res = await fetch(`${apiBase}/api/practice/extract-text`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image_base64: base64Data })
        });
        
        if (!res.ok) {
          throw new Error(`Extraction failed: ${await res.text()}`);
        }
        
        const data = await res.json();
        const divider = problemTextarea.value.trim() ? "\n\n" : "";
        problemTextarea.value = problemTextarea.value + divider + data.extracted_text;
        problemTextarea.focus();
        
      } catch (err) {
        console.error(err);
        alert("OCR Failed: " + err.message);
      } finally {
        ocrTrigger.disabled = false;
        ocrTrigger.innerHTML = originalText;
      }
    };
    reader.readAsDataURL(file);
  }

  // Version History state
  let sessionHistory = {
    activeVersionIdx: 0,
    versions: [] // array of { code, error, responseData }
  };
  let currentFontSize = 0.95; // rem units for editor text size

  // ─── AMAZONML Mode State & Logic ─────────────────────────────────────────
  let amazonMlModeActive = false;
  let activeMlSection = 'mcq'; // MCQ is default (first tab)
  let mlChatHistory = [];

  const MLSS_SECTION_LABELS = {
    dsa: 'DSA Prep',
    sql: 'SQL Prep',
    mcq: 'Math & ML MCQs'
  };

  const MLSS_WELCOME = {
    mcq: '**MLSS AI Copilot — MCQ / Math Mode**\n\nPaste any MCQ or concept question. I give 100% accurate answers for:\n- Probability & Statistics\n- Linear Algebra & Calculus\n- ML theory, distributions, hypothesis testing\n\nPaste options A/B/C/D and I will identify the correct one with a clear explanation.',
    dsa: '**MLSS AI Copilot — DSA Mode**\n\nPaste any DSA problem and I will solve it with:\n- Optimal algorithm + explanation\n- Clean Python 3 code\n- Time & space complexity analysis\n- Edge case handling\n\nYou can also paste **half-written code** — use *+ Add Code* and I will complete it line by line.',
    sql: '**MLSS AI Copilot — SQL Mode**\n\nPaste any SQL problem or describe a query. I will give you:\n- A correct, optimized query\n- Clause-by-clause explanation\n- Alternative approaches (JOINs, CTEs, Window functions)'
  };

  function safeRenderMarkdown(text) {
    if (!text) return '';
    try {
      if (typeof marked === 'object' && typeof marked.parse === 'function') {
        return marked.parse(text);
      } else if (typeof marked === 'function') {
        return marked(text);
      }
    } catch (e) {
      console.warn("Markdown rendering failed, falling back to plain text:", e);
    }
    // Fallback: escape HTML and replace newlines with breaks
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\n/g, '<br>');
  }

  function formatChatCodeBlocks(div) {
    div.querySelectorAll('pre').forEach(preBlock => {
      if (preBlock.querySelector('.chat-code-copy-btn')) return;

      preBlock.style.position = 'relative';
      
      const copyBtn = document.createElement('button');
      copyBtn.className = 'chat-code-copy-btn';
      copyBtn.title = 'Copy code';
      copyBtn.innerHTML = `
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
          <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
      `;
      copyBtn.style.position = 'absolute';
      copyBtn.style.top = '8px';
      copyBtn.style.right = '8px';
      copyBtn.style.background = 'rgba(255, 255, 255, 0.08)';
      copyBtn.style.border = '1px solid rgba(255, 255, 255, 0.15)';
      copyBtn.style.color = 'var(--text-3)';
      copyBtn.style.borderRadius = '4px';
      copyBtn.style.padding = '4px';
      copyBtn.style.cursor = 'pointer';
      copyBtn.style.display = 'flex';
      copyBtn.style.alignItems = 'center';
      copyBtn.style.justifyContent = 'center';
      copyBtn.style.transition = 'all 0.15s';
      copyBtn.style.zIndex = '10';

      copyBtn.addEventListener('mouseenter', () => {
        copyBtn.style.background = 'rgba(255, 255, 255, 0.15)';
        copyBtn.style.color = 'var(--text-1)';
      });
      copyBtn.addEventListener('mouseleave', () => {
        copyBtn.style.background = 'rgba(255, 255, 255, 0.08)';
        copyBtn.style.color = 'var(--text-3)';
      });

      copyBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const codeEl = preBlock.querySelector('code');
        let textToCopy = codeEl ? codeEl.innerText : preBlock.innerText;
        
        // Strip line numbers if they are prepended (e.g. "1: def solve..." -> "def solve...")
        const lines = textToCopy.split('\n');
        const firstLine = lines.find(l => l.trim() !== '');
        if (firstLine && /^\d+:/.test(firstLine.trim())) {
          textToCopy = lines.map(line => {
            return line.replace(/^\s*\d+:\s?/, '');
          }).join('\n');
        }

        navigator.clipboard.writeText(textToCopy).then(() => {
          copyBtn.innerHTML = `
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          `;
          setTimeout(() => {
            copyBtn.innerHTML = `
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            `;
          }, 2000);
        });
      });

      preBlock.appendChild(copyBtn);
    });
  }

  function appendChatActionButtons() {
    if (!mlssChatMessages) return;
    
    // Remove any existing action button containers to prevent duplicate clicks on older messages
    mlssChatMessages.querySelectorAll('.mlss-chat-actions-container').forEach(c => c.remove());

    const container = document.createElement('div');
    container.className = 'mlss-chat-actions-container';
    container.style.display = 'flex';
    container.style.gap = '10px';
    container.style.padding = '8px 16px';
    container.style.marginTop = '8px';
    container.style.animation = 'slideUp 0.2s ease';

    // Follow-up Button
    const followupBtn = document.createElement('button');
    followupBtn.className = 'mlss-chat-action-btn';
    followupBtn.innerHTML = `<i class="ti ti-message-square" style="font-size:14px; margin-right:4px;"></i> Follow-up`;
    followupBtn.style.background = 'var(--bg-3)';
    followupBtn.style.border = '0.5px solid var(--border)';
    followupBtn.style.color = 'var(--text-2)';
    followupBtn.style.padding = '6px 14px';
    followupBtn.style.borderRadius = '20px';
    followupBtn.style.fontSize = '12px';
    followupBtn.style.fontWeight = '600';
    followupBtn.style.cursor = 'pointer';
    followupBtn.style.display = 'inline-flex';
    followupBtn.style.alignItems = 'center';
    followupBtn.style.fontFamily = 'var(--font-sans)';
    followupBtn.style.transition = 'all 0.15s';

    followupBtn.addEventListener('mouseenter', () => {
      followupBtn.style.borderColor = 'var(--text-2)';
      followupBtn.style.color = 'var(--text-1)';
      followupBtn.style.transform = 'translateY(-1px)';
    });
    followupBtn.addEventListener('mouseleave', () => {
      followupBtn.style.borderColor = 'var(--border)';
      followupBtn.style.color = 'var(--text-2)';
      followupBtn.style.transform = 'none';
    });

    followupBtn.addEventListener('click', () => {
      if (mlssChatInput) {
        mlssChatInput.placeholder = 'Type your follow-up or paste the execution error here...';
        mlssChatInput.focus();
        mlssChatInput.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });

    // Next Question Button
    const nextBtn = document.createElement('button');
    nextBtn.className = 'mlss-chat-action-btn primary';
    nextBtn.innerHTML = `<i class="ti ti-sparkles" style="font-size:14px; margin-right:4px;"></i> Next Question`;
    nextBtn.style.background = 'var(--brand)';
    nextBtn.style.border = 'none';
    nextBtn.style.color = '#fff';
    nextBtn.style.padding = '6px 14px';
    nextBtn.style.borderRadius = '20px';
    nextBtn.style.fontSize = '12px';
    nextBtn.style.fontWeight = '600';
    nextBtn.style.cursor = 'pointer';
    nextBtn.style.display = 'inline-flex';
    nextBtn.style.alignItems = 'center';
    nextBtn.style.fontFamily = 'var(--font-sans)';
    nextBtn.style.transition = 'all 0.15s';

    nextBtn.addEventListener('mouseenter', () => {
      nextBtn.style.background = 'var(--brand-hover)';
      nextBtn.style.transform = 'translateY(-1px)';
      nextBtn.style.boxShadow = '0 4px 12px rgba(234, 118, 63, 0.25)';
    });
    nextBtn.addEventListener('mouseleave', () => {
      nextBtn.style.background = 'var(--brand)';
      nextBtn.style.transform = 'none';
      nextBtn.style.boxShadow = 'none';
    });

    nextBtn.addEventListener('click', () => {
      mlChatHistory = [];
      if (mlssChatMessages) {
        mlssChatMessages.innerHTML = '';
        appendChatMsg('ai', MLSS_WELCOME[activeMlSection]);
      }
      if (mlssChatInput) {
        mlssChatInput.value = '';
        mlssChatInput.placeholder = 'Paste your MCQ, DSA problem, SQL query, or ask anything...';
      }
    });

    container.appendChild(followupBtn);
    container.appendChild(nextBtn);
    mlssChatMessages.appendChild(container);
    mlssChatMessages.scrollTop = mlssChatMessages.scrollHeight;
  }

  function appendChatMsg(role, contentMd, isTyping = false) {
    if (!mlssChatMessages) return;
    const div = document.createElement('div');
    div.className = `chat-msg ${role}${isTyping ? ' typing' : ''}`;
    if (isTyping) {
      div.innerHTML = `<div class="typing-dots"><span></span><span></span><span></span></div>`;
    } else {
      div.innerHTML = safeRenderMarkdown(contentMd);
      // Apply highlight.js to code blocks inside chat
      div.querySelectorAll('pre code').forEach(block => {
        if (window.hljs) hljs.highlightElement(block);
      });
      formatChatCodeBlocks(div);
    }
    mlssChatMessages.appendChild(div);
    mlssChatMessages.scrollTop = mlssChatMessages.scrollHeight;
    return div;
  }

  function setAmazonMlMode(active) {
    amazonMlModeActive = active;
    if (!amazonMlModeToggle) return;
    const label = amazonMlModeToggle.querySelector('span:not(.mlss-dot)');

    const tabsInner = document.getElementById('mlssSectionTabsInner');

    if (active) {
      amazonMlModeToggle.classList.add('active');
      if (label) label.textContent = 'MLSS: ON';
      // Turn off OA mode if it was on
      if (envSelect && envSelect.value === 'oa') {
        envSelect.value = 'leetcode';
        if (typeof syncOaMode === 'function') syncOaMode();
      }
      // Lock page scroll so they can only scroll inside the chat box!
      document.body.style.overflow = 'hidden';
      // Show MLSS tabs
      if (tabsInner) tabsInner.style.display = 'flex';
      // Hide standard workspace layout
      if (mainWorkspaceLayout) mainWorkspaceLayout.classList.add('hidden');
      // Show centered chat panel
      if (mlssChatPanel) mlssChatPanel.classList.add('visible');
      if (resultsContainer) resultsContainer.style.display = 'none';

      // Reset and show welcome message
      mlChatHistory = [];
      if (mlssChatMessages) mlssChatMessages.innerHTML = '';
      appendChatMsg('ai', MLSS_WELCOME[activeMlSection]);
      // Update section label pill
      updateSectionLabel(activeMlSection);
      // Show/hide code stub based on section
      syncCodeStubVisibility();
    } else {
      amazonMlModeToggle.classList.remove('active');
      if (label) label.textContent = 'MLSS: OFF';
      // Restore normal page scrolling
      document.body.style.overflow = '';
      // Hide MLSS tabs
      if (tabsInner) tabsInner.style.display = 'none';
      // Show standard workspace layout
      if (mainWorkspaceLayout) mainWorkspaceLayout.classList.remove('hidden');
      if (mlssChatPanel) mlssChatPanel.classList.remove('visible');
      if (resultsContainer) resultsContainer.style.display = 'block';
      // Restore language selector
      const langSelect = document.getElementById('language');
      if (langSelect) langSelect.disabled = false;
      // Restore analyze btn
      if (analyzeBtn) {
        analyzeBtn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg> Analyze & Solve`;
      }
      mlChatHistory = [];
    }
  }

  function syncCodeStubVisibility() {
    // Show stub toggle only for DSA
    const stubWrapper = document.getElementById('mlssCodeStubWrapper');
    if (stubWrapper) {
      stubWrapper.style.display = activeMlSection === 'dsa' ? 'block' : 'none';
    }
  }

  function lockLanguageForSection(section) {
    const langSelect = document.getElementById('language');
    if (!langSelect) return;
    if (section === 'sql') {
      langSelect.value = 'sql';
    } else {
      langSelect.value = 'python3';
    }
    langSelect.disabled = true;
  }

  function updateSectionLabel(section) {
    if (mlssSectionLabel) {
      const labelMap = { dsa: 'DSA', sql: 'SQL', mcq: 'MCQ' };
      mlssSectionLabel.textContent = labelMap[section] || section.toUpperCase();
    }
  }

  // AMAZONML Toggle button click
  if (amazonMlModeToggle) {
    amazonMlModeToggle.addEventListener('click', (e) => {
      e.preventDefault();
      setAmazonMlMode(!amazonMlModeActive);
    });
  }

  // Section chip/tab clicks — wire up BOTH old chips (if any) and new panel tabs
  const sectionClickHandler = (section) => {
    if (!section || section === activeMlSection) return;
    activeMlSection = section;
    // Update both old chips and new tabs
    document.querySelectorAll('.mlss-chip, .mlss-section-tab').forEach(c => {
      c.classList.toggle('active', c.getAttribute('data-section') === section);
    });
    // Lock language
    lockLanguageForSection(section);
    // Update label
    updateSectionLabel(section);
    // Show/hide code stub
    syncCodeStubVisibility();
    // Update question placeholder
    const placeholders = {
      dsa: 'Paste your DSA problem or half-written code...\n\nExamples:\n- "Find the longest palindrome substring"\n- "BFS/DFS on graph" ',
      sql: 'Paste your SQL problem or query...\n\nExamples:\n- "Get 2nd highest salary"\n- "Find employees with no orders"',
      mcq: 'Paste your MCQ or concept question...\n\nExamples:\n- "What is the bias-variance tradeoff?"\n- "P(A|B) if A and B are independent?"'
    };
    if (mlssQuestionInput) mlssQuestionInput.placeholder = placeholders[section] || '';
    // Reset chat with new welcome message
    mlChatHistory = [];
    if (mlssChatMessages) mlssChatMessages.innerHTML = '';
    appendChatMsg('ai', MLSS_WELCOME[section]);
  };

  if (mlssSectionSelector) {
    mlssSectionSelector.querySelectorAll('.mlss-chip').forEach(chip => {
      chip.addEventListener('click', () => sectionClickHandler(chip.getAttribute('data-section')));
    });
  }
  // New panel tabs
  const mlssSectionTabsInner = document.getElementById('mlssSectionTabsInner');
  if (mlssSectionTabsInner) {
    mlssSectionTabsInner.querySelectorAll('.mlss-section-tab').forEach(tab => {
      tab.addEventListener('click', () => sectionClickHandler(tab.getAttribute('data-section')));
    });
  }

  // Code Stub Toggle
  if (mlssStubToggle && mlssCodeStubArea) {
    mlssStubToggle.addEventListener('click', () => {
      const open = mlssCodeStubArea.classList.toggle('open');
      mlssStubToggle.classList.toggle('active', open);
      mlssStubToggle.textContent = open ? '− Hide Code' : '+ Add Code';
    });
  }

  // Code Stub Gutter Sync
  if (mlssCodeStub && mlssCodeGutter) {
    const updateMlssGutter = () => {
      const lines = mlssCodeStub.value.split('\n');
      const count = Math.max(1, lines.length);
      let g = '';
      for (let i = 1; i <= count; i++) g += `<div style="line-height:1.5;">${i}</div>`;
      mlssCodeGutter.innerHTML = g;
    };
    mlssCodeStub.addEventListener('input', updateMlssGutter);
    mlssCodeStub.addEventListener('paste', () => setTimeout(updateMlssGutter, 0));
    mlssCodeStub.addEventListener('change', updateMlssGutter);
    mlssCodeStub.addEventListener('scroll', () => { mlssCodeGutter.scrollTop = mlssCodeStub.scrollTop; });
    mlssCodeStub.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        e.preventDefault();
        const s = mlssCodeStub.selectionStart;
        mlssCodeStub.value = mlssCodeStub.value.substring(0, s) + '    ' + mlssCodeStub.value.substring(mlssCodeStub.selectionEnd);
        mlssCodeStub.selectionStart = mlssCodeStub.selectionEnd = s + 4;
        updateMlssGutter();
      }
    });
    updateMlssGutter();
  }

  // MLSS Chat follow-up send
  async function sendMlssMessage(userText) {
    if (!userText || !userText.trim()) return;
    let text = userText.trim();

    // Check for DSA code stub
    const codeStub = (activeMlSection === 'dsa' && mlssCodeStubArea && mlssCodeStubArea.classList.contains('open') && mlssCodeStub)
      ? mlssCodeStub.value.trim() : '';
    if (codeStub) {
      const numberedCode = codeStub.split('\n').map((line, idx) => `${idx + 1}: ${line}`).join('\n');
      text += `\n\n**My partial code (with line numbers):**\n\`\`\`\n${numberedCode}\n\`\`\``;
    }

    // Append user bubble
    appendChatMsg('user', text);
    mlChatHistory.push({ role: 'user', content: text });

    // Show typing indicator
    const typingBubble = appendChatMsg('ai', '', true);

    // Save button HTML values
    const origChatSendBtnHtml = mlssChatSendBtn ? mlssChatSendBtn.innerHTML : '';

    if (mlssChatInput) {
      mlssChatInput.value = '';
      mlssChatInput.style.height = 'auto'; // Reset auto-grow height
    }

    // Clear code stub if sent
    if (codeStub) {
      if (mlssCodeStub) mlssCodeStub.value = '';
      if (mlssCodeStubArea) mlssCodeStubArea.classList.remove('open');
      if (mlssStubToggle) {
        mlssStubToggle.classList.remove('active');
        mlssStubToggle.textContent = '+ Add Code';
      }
      if (mlssCodeGutter) {
        mlssCodeGutter.innerHTML = '<div style="line-height:1.5;">1</div>';
      }
    }

    if (mlssChatSendBtn) {
      mlssChatSendBtn.disabled = true;
      mlssChatSendBtn.innerHTML = `<span class="mlss-spinner" style="width:12px; height:12px; border-width:1.5px;"></span>`;
    }

    // Scroll chat panel into view smoothly
    if (mlssChatPanel) {
      setTimeout(() => {
        mlssChatPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 50);
    }

    try {
      const res = await fetch(`${apiBase}/api/practice/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          problem: text,
          language: activeMlSection === 'sql' ? 'sql' : 'python3',
          amazonMlMode: true,
          mlSection: activeMlSection,
          history: mlChatHistory.slice(0, -1), // all prior turns
          constraints: '',
          userAttempt: '',
          environment: 'leetcode',
          verbosity: 'concise',
          verify_code: false,
          model: 'gemini'
        })
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      const aiText = data.explanation || 'Sorry, I could not generate a response.';

      // Replace typing bubble with actual response
      if (typingBubble && typingBubble.parentNode) {
        typingBubble.classList.remove('typing');
        typingBubble.innerHTML = safeRenderMarkdown(aiText);
        typingBubble.querySelectorAll('pre code').forEach(block => {
          if (window.hljs) hljs.highlightElement(block);
        });
        formatChatCodeBlocks(typingBubble);
        appendChatActionButtons();
        
        // Smooth scroll message feed to bottom
        mlssChatMessages.scrollTop = mlssChatMessages.scrollHeight;
        setTimeout(() => {
          if (mlssChatMessages) {
            mlssChatMessages.scrollTo({
              top: mlssChatMessages.scrollHeight,
              behavior: 'smooth'
            });
          }
        }, 50);
      }
      mlChatHistory.push({ role: 'assistant', content: aiText });
    } catch (err) {
      if (typingBubble && typingBubble.parentNode) typingBubble.remove();
      appendChatMsg('ai', `❌ Error: ${err.message}`);
    } finally {
      if (mlssChatSendBtn) {
        mlssChatSendBtn.disabled = false;
        mlssChatSendBtn.innerHTML = origChatSendBtnHtml;
      }
    }
  }

  if (mlssChatSendBtn) {
    mlssChatSendBtn.addEventListener('click', () => {
      if (mlssChatInput) sendMlssMessage(mlssChatInput.value);
    });
  }
  if (mlssChatInput) {
    mlssChatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMlssMessage(mlssChatInput.value);
      }
    });
    mlssChatInput.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = (this.scrollHeight) + 'px';
    });
  }
  // ─── End AMAZONML Mode ─────────────────────────────────────────────────────


  // Reset Session Trigger
  const resetBtn = document.getElementById('resetSessionBtn');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      if (problemTextarea) problemTextarea.value = '';
      if (starterCodeTextarea) starterCodeTextarea.value = '';
      if (envSelect) envSelect.value = 'leetcode';
      if (oaModeToggle) {
        oaModeToggle.classList.remove('active');
        const label = oaModeToggle.querySelector('span');
        if (label) label.textContent = 'OA Mode: OFF';
      }
      // Reset AMAZONML mode
      if (amazonMlModeActive) setAmazonMlMode(false);
      const langSelect = document.getElementById('language');
      if (langSelect) langSelect.disabled = false;
      sessionHistory = {
        activeVersionIdx: 0,
        versions: []
      };
      resetBtn.classList.add('hidden');
      resultsContainer.style.display = 'block';
      resultsContainer.innerHTML = `
        <div style="background: #09090b; border: 1px solid var(--border); border-radius: 12px; padding: 24px; min-height: 480px; font-family: var(--font-mono); font-size: 0.85rem; color: var(--text-3); box-shadow: var(--shadow-sm); display: flex; flex-direction: column; gap: 12px; line-height: 1.6; text-align: left; box-sizing: border-box;">
          <div style="display: flex; align-items: center; gap: 6px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 8px; margin-bottom: 12px; user-select: none;">
            <span style="width: 10px; height: 10px; border-radius: 50%; background: #ef4444; display: inline-block;"></span>
            <span style="width: 10px; height: 10px; border-radius: 50%; background: #fbbf24; display: inline-block;"></span>
            <span style="width: 10px; height: 10px; border-radius: 50%; background: #22c55e; display: inline-block;"></span>
            <span style="color: var(--text-4); font-size: 0.75rem; margin-left: 8px;">oa-copilot-terminal</span>
          </div>
          <div><span style="color: var(--brand);">$</span> grindos --status</div>
          <div style="color: var(--text-2);">Awaiting problem input on the left pane...</div>
          <div><span style="color: var(--brand);">$</span> cat instructions.txt</div>
          <div style="color: var(--text-4); white-space: pre-line;">
1. Paste the problem description or stuck code attempt.
2. Provide any optional starter code or constraints.
3. Click "Analyze & Solve" (or press Cmd+Enter) to generate verification script.
          </div>
          <div><span style="color: var(--brand);">$</span> <span class="cursor-blink"></span></div>
        </div>
      `;
    });
  }

  // 5. Solve & Explain submission API call
  if (analyzeBtn) {
    analyzeBtn.addEventListener('click', async () => {
      const problem = problemTextarea ? problemTextarea.value.trim() : '';
      const language = document.getElementById('language').value;
      const environment = document.getElementById('environment').value;
      const verbosity = document.getElementById('verbosity').value;
      const namingStyleEl = document.getElementById('namingStyle');
      const namingStyle = namingStyleEl ? namingStyleEl.value : 'short';
      const constraints = document.getElementById('constraints') ? document.getElementById('constraints').value.trim() : '';
      const verifyCode = document.getElementById('verifyCode') ? document.getElementById('verifyCode').checked : true;
      
      const modelProvider = modelProviderEl ? modelProviderEl.value : 'gemini';
      const model = modelProvider === 'claude' && document.getElementById('claudeModel') 
          ? document.getElementById('claudeModel').value 
          : 'gemini';

      const starterCode = starterCodeTextarea ? starterCodeTextarea.value.trim() : '';
      const isCompletionMode = starterCode.length > 0;
      const completionFormat = completionFormatSelect ? completionFormatSelect.value : 'snippet';
      
      if (!problem) {
        alert("Please paste a problem statement first!");
        return;
      }

      // --- AMAZONML Mode: route to chat instead ---
      if (amazonMlModeActive) {
        sendMlssMessage(problem);
        if (problemTextarea) problemTextarea.value = '';
        return;
      }
      
      // UI State
      analyzeBtn.disabled = true;
      loading.style.display = 'flex';
      resultsContainer.style.display = 'none';
      resultsContainer.innerHTML = '';
      
      try {
        const res = await fetch(`${apiBase}/api/practice/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            problem,
            language,
            constraints,
            userAttempt: "",
            environment,
            verbosity,
            namingStyle,
            verify_code: verifyCode,
            isCompletionMode,
            starterCode,
            completionOutputFormat: completionFormat,
            model
          })
        });
        
        if (!res.ok) {
          throw new Error(`API Error: ${await res.text()}`);
        }
        
        const data = await res.json();
        
        // Reset and save as version 1
        sessionHistory = {
          activeVersionIdx: 0,
          versions: [{
            code: data.solutionCode,
            error: null,
            responseData: data
          }]
        };

        if (resetBtn) resetBtn.classList.remove('hidden');
        renderResults(data, language);
        resultsContainer.style.display = 'block';
        
      } catch (err) {
        console.error(err);
        alert("Failed to analyze problem: " + err.message);
        resultsContainer.style.display = 'block';
      } finally {
        analyzeBtn.disabled = false;
        loading.style.display = 'none';
      }
    });
  }

  // Helper to highlight a traceback error link
  function formatTraceback(err) {
    if (!err) return '';
    const safeErr = err.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return safeErr.replace(/(line|Line)\s+(\d+)/g, (match, word, num) => {
      return `<a href="#" class="traceback-line-link" data-line="${num}" style="color:var(--brand); text-decoration:underline; font-weight:600; cursor:pointer;">${match}</a>`;
    });
  }

  function highlightCodeLine(lineNum) {
    document.querySelectorAll('.ln-num').forEach(el => {
      el.style.background = '';
      el.style.color = '';
      el.style.fontWeight = '';
    });
    const targetLn = document.getElementById(`ln-${lineNum}`);
    if (targetLn) {
      targetLn.style.background = 'rgba(239, 68, 68, 0.3)';
      targetLn.style.color = '#ef4444';
      targetLn.style.fontWeight = '700';
      targetLn.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  // 6. Dynamic results renderer
  function renderResults(data, language) {
    let html = '';
    
    // Render Version Swapper if history has versions
    if (sessionHistory.versions.length > 1) {
      html += `<div class="version-selector-bar" style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; border-bottom:1px solid var(--border); padding-bottom:12px;">`;
      sessionHistory.versions.forEach((v, idx) => {
        const isActive = idx === sessionHistory.activeVersionIdx;
        const label = idx === 0 ? 'v1 (Original)' : `v${idx + 1} (Patched)`;
        const isError = v.error !== null;
        
        html += `
          <button class="ver-tab-btn ${isActive ? 'active' : ''}" data-idx="${idx}" style="padding:6px 12px; font-size:0.8rem; border-radius:6px; border:1px solid ${isActive ? 'var(--brand)' : 'var(--border)'}; background:${isActive ? 'var(--brand-light)' : 'var(--bg-2)'}; color:${isActive ? 'var(--brand)' : 'var(--text-2)'}; font-weight:600; cursor:pointer; transition:all 0.15s; display:inline-flex; align-items:center; gap:6px;">
            <span>${isError ? '⚠️' : '💻'}</span> ${label}
          </button>
        `;
      });
      html += `</div>`;
    }

    html += `<div class="tabs">`;
    const tabs = [];
    
    // Determine which tabs to show
    const isOaModeActive = envSelect && envSelect.value === 'oa';
    
    if (!isOaModeActive && (data.constraintsCheck || data.complexity || data.naiveApproach || data.optimizedApproach)) {
      tabs.push({ id: 'tab-breakdown', label: '🧠 Breakdown' });
    }
    if (data.solutionCode) {
      tabs.push({ id: 'tab-code', label: '💻 Code' });
    }
    if (data.verification && data.verification.length > 0) {
      tabs.push({ id: 'tab-verify', label: '✅ Verification' });
    }
    if (!isOaModeActive && data.comparisonTable && data.comparisonTable.length > 0) {
      tabs.push({ id: 'tab-compare', label: '🤖 AI vs Human' });
    }
    if (!isOaModeActive && (data.feedback || data.rederivePrompt)) {
      tabs.push({ id: 'tab-next', label: '🎯 Next Steps' });
    }
    
    // Default to 'tab-code' first if available
    const defaultActiveTabId = tabs.find(t => t.id === 'tab-code') ? 'tab-code' : (tabs[0] ? tabs[0].id : '');
    
    tabs.forEach((t) => {
      html += `<button class="tab-btn ${t.id === defaultActiveTabId ? 'active' : ''}" data-target="${t.id}">${t.label}</button>`;
    });
    html += `</div>`;
    
    // Tab 1: Breakdown
    if (tabs.find(t => t.id === 'tab-breakdown')) {
      html += `<div id="tab-breakdown" class="tab-content ${defaultActiveTabId === 'tab-breakdown' ? 'active' : ''}" style="animation: slideUp 0.3s ease;">`;
      if (data.constraintsCheck) html += `<h4 style="font-weight: 700; margin-bottom: 8px;">Constraints</h4><div style="margin-bottom: 24px; color: var(--text-2);">${marked.parse(data.constraintsCheck)}</div>`;
      if (data.complexity) {
        html += `<div style="margin-bottom: 24px; display: flex; gap: 8px; flex-wrap: wrap;">
          <span class="complexity-pill">⏱️ Time: ${data.complexity.time || 'O(?)'}</span>
          <span class="complexity-pill">💾 Space: ${data.complexity.space || 'O(?)'}</span>
        </div>`;
      }
      if (data.naiveApproach) html += `<h4 style="font-weight: 700; margin-bottom: 8px;">Naive Approach</h4><div style="margin-bottom: 24px; color: var(--text-2);">${marked.parse(data.naiveApproach)}</div>`;
      if (data.optimizedApproach) html += `<h4 style="font-weight: 700; margin-bottom: 8px;">Optimized Approach</h4><div style="margin-bottom: 24px; color: var(--text-2);">${marked.parse(data.optimizedApproach)}</div>`;
      if (data.pseudocode) html += `<h4 style="font-weight: 700; margin-bottom: 8px;">Pseudocode</h4><div style="margin-bottom: 24px; color: var(--text-2);">${marked.parse(data.pseudocode)}</div>`;
      html += `</div>`;
    }
    
    // Tab 2: Code
    if (tabs.find(t => t.id === 'tab-code')) {
      html += `<div id="tab-code" class="tab-content ${defaultActiveTabId === 'tab-code' ? 'active' : ''}">`;
      
      const currentVersion = sessionHistory.versions[sessionHistory.activeVersionIdx];
      
      html += `
        <div class="code-showcase-card" style="background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-md); position: relative; margin-top: 10px;">
          <div class="code-card-header" style="padding: 12px 20px; background: var(--bg-2); border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <span style="font-weight: 600; font-size: 0.95rem; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 8px;">
              💻 Optimal Code
            </span>
            <div style="display: flex; align-items: center; gap: 12px;">
              <div style="display: flex; border: 1px solid var(--border); border-radius: 6px; overflow: hidden; background: var(--surface-1);">
                <button id="fontSizeDec" style="background:none; border:none; padding:4px 8px; color:var(--text-3); font-size:0.8rem; cursor:pointer; border-right:1px solid var(--border);" title="Decrease font size">Aa-</button>
                <button id="fontSizeInc" style="background:none; border:none; padding:4px 8px; color:var(--text-3); font-size:0.8rem; cursor:pointer;" title="Increase font size">Aa+</button>
              </div>
              <button id="exportCodeBtn" style="background:var(--surface-0); border:1px solid var(--border); border-radius:6px; padding:4px 10px; font-size:0.8rem; font-weight:600; color:var(--text-2); cursor:pointer; display:inline-flex; align-items:center; gap:4px;" title="Download source file">
                <i class="ti ti-download" style="font-size:12px;"></i> Export
              </button>
              <span style="font-size: 0.85rem; font-family: var(--font-mono); color: var(--brand); font-weight: 600; background: var(--brand-light); padding: 4px 8px; border-radius: 4px;">
                ${language === 'cpp' ? 'C++' : language.charAt(0).toUpperCase() + language.slice(1)}
              </span>
            </div>
          </div>
          
          <div class="code-container" style="position: relative; display: flex; background: var(--code-bg); overflow: hidden;">
            <div class="line-numbers-gutter" style="padding: 20px 12px; font-family: var(--font-mono); font-size: ${currentFontSize}rem; line-height: 1.5; color: var(--text-4); text-align: right; user-select: none; border-right: 1px solid var(--border); background: rgba(0, 0, 0, 0.15); min-width: 45px; box-sizing: border-box;">
              ${Array.from({length: data.solutionCode.split('\n').length}, (_, i) => `<div class="ln-num" id="ln-${i + 1}" style="line-height: 1.5;">${i + 1}</div>`).join('')}
            </div>
            <div class="code-content-wrapper" style="flex: 1; overflow-x: auto;">
              <pre style="margin: 0; background: transparent; border: none; padding: 20px 24px; box-sizing: border-box;"><code class="language-${language}" style="background: transparent; border: none; padding: 0; font-family: var(--font-mono); font-size: ${currentFontSize}rem; line-height: 1.5; display: block; white-space: pre; overflow: visible;">${data.solutionCode.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</code></pre>
            </div>
            <button class="copy-btn" title="Copy code" style="position: absolute; top: 12px; right: 12px; background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.3); color: #fff; padding: 6px 12px; border-radius: 6px; cursor: pointer; z-index: 1000; display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 0.8rem; font-weight: 500; backdrop-filter: blur(4px); opacity: 1 !important; transition: all 0.2s;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              <span>Copy</span>
            </button>
          </div>
        </div>
      `;

      // Render Runtime Terminal if active version has a saved error
      if (currentVersion && currentVersion.error) {
        html += `
          <div class="terminal-card" style="background:#09090b; border:1px solid rgba(239,68,68,0.3); border-radius:12px; padding:16px; margin-top:20px; font-family:var(--font-mono); font-size:0.85rem; box-shadow:0 8px 24px rgba(239, 68, 68, 0.05); position:relative;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(239,68,68,0.15); padding-bottom:8px; margin-bottom:12px;">
              <span style="color:#ef4444; font-weight:700; font-family:var(--font-sans); display:flex; align-items:center; gap:6px;">
                ⚠️ Runtime / Compile Error Output
              </span>
              <span style="color:var(--text-4); font-size:0.75rem;">Process exited with errors</span>
            </div>
            <div class="terminal-content" style="color:#fca5a5; white-space:pre-wrap; line-height:1.6; max-height:220px; overflow-y:auto; font-family:var(--font-mono);">
              ${formatTraceback(currentVersion.error)}
            </div>
          </div>
        `;
      }

      html += `
        <!-- Error Debugger Section -->
        <div class="error-debugger-card" style="background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 20px; box-shadow: var(--shadow-sm); margin-top: 24px;">
          <h4 style="font-size: 1rem; font-weight: 700; color: var(--text-1); margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
            ⚠️ Got a Runtime or Compilation Error?
          </h4>
          <p style="font-size: 0.85rem; color: var(--text-3); margin-bottom: 12px;">Paste the error details or stdout/stderr logs below and AI will debug & fix the code for you.</p>
          <textarea id="executionErrorInput" placeholder="Paste error message or console output here..." style="width: 100%; min-height: 80px; padding: 10px 12px; font-size: 0.85rem; font-family: var(--font-mono); background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius); color: var(--text-1); resize: vertical; margin-bottom: 12px; outline: none; transition: all 0.2s ease;"></textarea>
          <button id="fixErrorBtn" class="submit-btn" style="padding: 10px 20px; font-size: 0.9rem; max-width: 200px; height: 38px; border-radius: var(--radius); cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px;">
            🐞 Debug & Fix Code
          </button>
        </div>
      `;
      html += `</div>`;
    }

    // Tab 3: Verification
    if (tabs.find(t => t.id === 'tab-verify')) {
      html += `<div id="tab-verify" class="tab-content ${defaultActiveTabId === 'tab-verify' ? 'active' : ''}">`;
      
      let passedCount = 0;
      let totalCount = data.verification.length;
      let accordionHtml = '';
      
      data.verification.forEach((tc, idx) => {
        if (tc.passed) passedCount++;
        
        accordionHtml += `
          <details style="border: 1px solid var(--border); border-radius: 8px; margin-bottom: 8px; background: var(--bg-2); overflow: hidden;">
            <summary style="padding: 12px 16px; font-size: 0.85rem; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: space-between; list-style: none; user-select: none; color: ${tc.passed ? '#22c55e' : '#ef4444'};">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span>${tc.passed ? '✅' : '❌'}</span>
                <span>Test Case ${idx + 1}: ${tc.passed ? 'PASSED' : 'FAILED'}</span>
              </div>
              <span style="font-size: 0.75rem; color: var(--text-3); transition: transform 0.2s;">▶</span>
            </summary>
            <div style="padding: 16px; border-top: 1px solid var(--border); font-size: 0.82rem; font-family: var(--font-mono); color: var(--text-2); line-height: 1.5; background: var(--card);">
              <div><strong>Input:</strong> ${JSON.stringify(tc.inputs || tc.input || 'N/A')}</div>
              <div style="margin-top: 8px;"><strong>Expected:</strong> ${tc.expected || 'N/A'}</div>
              <div style="margin-top: 8px; color: ${tc.passed ? 'var(--text-2)' : 'var(--brand)'};"><strong>Actual:</strong> ${tc.actual || 'N/A'}</div>
            </div>
          </details>
        `;
      });

      const passRatio = totalCount > 0 ? (passedCount / totalCount) : 0;
      const statusText = passRatio === 1 
        ? 'All Tests Passed Successfully' 
        : `Tests: ${passedCount}/${totalCount} Passed`;
      
      html += `
        <div class="verification-status-panel" style="background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 16px 20px; display: flex; flex-direction: column; gap: 14px; box-shadow: var(--shadow-sm); margin-bottom: 20px; margin-top: 10px;">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.2rem;">${passRatio === 1 ? '🎉' : '⚠️'}</span>
            <span style="font-weight: 600; font-size: 0.95rem; color: var(--text-1);">${statusText}</span>
          </div>
          <div style="display: flex; flex-direction: column;">
            ${accordionHtml}
          </div>
        </div>
      `;
      html += `</div>`;
    }
    
    // Tab 4: Comparison
    if (tabs.find(t => t.id === 'tab-compare')) {
      html += `<div id="tab-compare" class="tab-content ${defaultActiveTabId === 'tab-compare' ? 'active' : ''}">`;
      html += `
        <div class="comparison-card" style="background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 24px; box-shadow: var(--shadow-sm); margin-top: 10px; overflow-x: auto;">
          <h3 style="font-size: 1.15rem; font-weight: 700; color: var(--text-1); margin-bottom: 16px;">🤖 AI vs Human Coding Style</h3>
          <table style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr>
                <th style="padding: 12px; border-bottom: 2px solid var(--border); text-align: left; font-weight: 600; color: var(--text-2);">Feature</th>
                <th style="padding: 12px; border-bottom: 2px solid var(--border); text-align: left; font-weight: 600; color: var(--text-2);">Robotic/AI Style</th>
                <th style="padding: 12px; border-bottom: 2px solid var(--border); text-align: left; font-weight: 600; color: var(--text-2);">Human/Interview Style</th>
              </tr>
            </thead>
            <tbody>
              ${data.comparisonTable.map(row => `
                <tr>
                  <td style="padding: 12px; border-bottom: 1px solid var(--border); font-weight: 600; color: var(--text-1);">${row.feature}</td>
                  <td style="padding: 12px; border-bottom: 1px solid var(--border); color: var(--text-3);">${row.aiStyle}</td>
                  <td style="padding: 12px; border-bottom: 1px solid var(--border); color: var(--text-2); font-weight: 500;">${row.humanStyle}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `;
      html += `</div>`;
    }
    
    // Tab 5: Next Steps
    if (tabs.find(t => t.id === 'tab-next')) {
      html += `<div id="tab-next" class="tab-content ${defaultActiveTabId === 'tab-next' ? 'active' : ''}">`;
      html += `<div class="next-steps-card" style="background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 24px; box-shadow: var(--shadow-sm); margin-top: 10px;">`;
      if (data.feedback) html += `<h4 style="font-weight: 700; margin-bottom: 8px;">Feedback</h4><div style="margin-bottom: 20px; color: var(--text-2);">${marked.parse(data.feedback)}</div>`;
      if (data.rederivePrompt) html += `<h4 style="font-weight: 700; margin-bottom: 8px; margin-top: 20px;">Try it yourself</h4><div style="color: var(--text-2);">${marked.parse(data.rederivePrompt)}</div>`;
      html += `</div></div>`;
    }
    
    resultsContainer.innerHTML = html;
    
    // Apply highlight.js to dynamically inserted code blocks
    resultsContainer.querySelectorAll('pre code').forEach((block) => {
      if (window.hljs) {
        hljs.highlightElement(block);
      }
    });
    
    // Setup Version Tabs click events
    resultsContainer.querySelectorAll('.ver-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.getAttribute('data-idx'), 10);
        sessionHistory.activeVersionIdx = idx;
        renderResults(sessionHistory.versions[idx].responseData, language);
      });
    });

    // Setup tab switching
    const tabBtns = resultsContainer.querySelectorAll('.tab-btn');
    const tabContents = resultsContainer.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        const targetId = btn.getAttribute('data-target');
        const targetContent = resultsContainer.querySelector(`#${targetId}`);
        if (targetContent) {
          targetContent.classList.add('active');
        }
      });
    });
    
    // Setup Font size scaling listeners
    const decBtn = resultsContainer.querySelector('#fontSizeDec');
    const incBtn = resultsContainer.querySelector('#fontSizeInc');
    if (decBtn && incBtn) {
      const codeBlock = resultsContainer.querySelector('pre code');
      const gutter = resultsContainer.querySelector('.line-numbers-gutter');
      
      decBtn.addEventListener('click', () => {
        currentFontSize = Math.max(0.75, currentFontSize - 0.05);
        if (codeBlock) codeBlock.style.fontSize = `${currentFontSize}rem`;
        if (gutter) gutter.style.fontSize = `${currentFontSize}rem`;
      });
      incBtn.addEventListener('click', () => {
        currentFontSize = Math.min(1.3, currentFontSize + 0.05);
        if (codeBlock) codeBlock.style.fontSize = `${currentFontSize}rem`;
        if (gutter) gutter.style.fontSize = `${currentFontSize}rem`;
      });
    }

    // Setup Download Source Export listener
    const exportBtn = resultsContainer.querySelector('#exportCodeBtn');
    if (exportBtn) {
      exportBtn.addEventListener('click', () => {
        const code = data.solutionCode;
        const extensionMap = { python: 'py', python3: 'py', python2: 'py', cpp: 'cpp', cpp14: 'cpp', cpp17: 'cpp', cpp20: 'cpp', java: 'java', java11: 'java', java8: 'java', javascript: 'js', typescript: 'ts', sql: 'sql', go: 'go', rust: 'rs' };
        const ext = extensionMap[language] || 'txt';
        const blob = new Blob([code], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `solution.${ext}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    }

    // Setup Copy Buttons
    resultsContainer.querySelectorAll('.copy-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const codeElement = btn.closest('.code-container').querySelector('code');
        if (codeElement) {
          navigator.clipboard.writeText(codeElement.innerText).then(() => {
            const oldHtml = btn.innerHTML;
            btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg> <span>Copied!</span>';
            setTimeout(() => btn.innerHTML = oldHtml, 2000);
          });
        }
      });
    });

    // Setup Traceback line links click events
    resultsContainer.querySelectorAll('.traceback-line-link').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const lineNum = parseInt(link.getAttribute('data-line'), 10);
        highlightCodeLine(lineNum);
      });
    });

    // Setup Error Debugger submit handler
    const fixErrorBtn = resultsContainer.querySelector('#fixErrorBtn');
    if (fixErrorBtn) {
      const errorInput = resultsContainer.querySelector('#executionErrorInput');
      if (errorInput) {
        errorInput.addEventListener('focus', () => {
          errorInput.style.borderColor = 'var(--brand)';
          errorInput.style.boxShadow = '0 0 0 3px var(--brand-light)';
        });
        errorInput.addEventListener('blur', () => {
          errorInput.style.borderColor = 'var(--border)';
          errorInput.style.boxShadow = 'none';
        });
      }

      fixErrorBtn.addEventListener('click', async () => {
        const errorVal = resultsContainer.querySelector('#executionErrorInput').value.trim();
        if (!errorVal) {
          alert("Please paste the error message or output logs first!");
          return;
        }

        // Save error message on the active version
        const activeVer = sessionHistory.versions[sessionHistory.activeVersionIdx];
        if (activeVer) {
          activeVer.error = errorVal;
        }

        const problem = problemTextarea ? problemTextarea.value.trim() : '';
        const language = document.getElementById('language').value;
        const environment = document.getElementById('environment').value;
        const verbosity = document.getElementById('verbosity').value;
        const namingStyleEl = document.getElementById('namingStyle');
        const namingStyle = namingStyleEl ? namingStyleEl.value : 'short';
        const constraints = document.getElementById('constraints') ? document.getElementById('constraints').value.trim() : '';
        const verifyCode = document.getElementById('verifyCode') ? document.getElementById('verifyCode').checked : true;
        
        const modelProvider = modelProviderEl ? modelProviderEl.value : 'gemini';
        const model = modelProvider === 'claude' && document.getElementById('claudeModel') 
            ? document.getElementById('claudeModel').value 
            : 'gemini';

        const starterCode = starterCodeTextarea ? starterCodeTextarea.value.trim() : '';
        const isCompletionMode = starterCode.length > 0;
        const completionFormat = completionFormatSelect ? completionFormatSelect.value : 'snippet';

        // UI State
        fixErrorBtn.disabled = true;
        fixErrorBtn.innerHTML = '<div class="spinner" style="width: 14px; height: 14px; border-width: 2px; border-top-color: #fff; margin-right: 6px; display: inline-block; vertical-align: middle; animation: spin 1s linear infinite;"></div> Debugging...';
        
        loading.style.display = 'flex';
        resultsContainer.style.display = 'none';

        try {
          const res = await fetch(`${apiBase}/api/practice/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              problem,
              language,
              constraints,
              userAttempt: activeVer ? activeVer.code : '', // Send active version's code as userAttempt
              errorMessage: errorVal,
              environment,
              verbosity,
              namingStyle,
              verify_code: verifyCode,
              isCompletionMode,
              starterCode,
              completionOutputFormat: completionFormat,
              model
            })
          });

          if (!res.ok) {
            throw new Error(`API Error: ${await res.text()}`);
          }

          const responseData = await res.json();
          
          // Save new version
          sessionHistory.versions.push({
            code: responseData.solutionCode,
            error: null,
            responseData: responseData
          });
          sessionHistory.activeVersionIdx = sessionHistory.versions.length - 1;

          renderResults(responseData, language);
          resultsContainer.style.display = 'block';

        } catch (err) {
          console.error(err);
          alert("Failed to debug & fix: " + err.message);
          resultsContainer.style.display = 'block';
        } finally {
          loading.style.display = 'none';
        }
      });
    }
  }

  // 7. Starter Code Gutter Line Synchronization
  const starterCodeEl = document.getElementById('starterCode');
  const starterGutterEl = document.getElementById('starterCodeGutter');
  if (starterCodeEl && starterGutterEl) {
    const updateStarterGutter = () => {
      const lines = starterCodeEl.value.split('\n');
      const count = Math.max(1, lines.length);
      let gutterHtml = '';
      for (let i = 1; i <= count; i++) {
        gutterHtml += `<div style="line-height: 1.5;">${i}</div>`;
      }
      starterGutterEl.innerHTML = gutterHtml;
    };

    starterCodeEl.addEventListener('input', updateStarterGutter);
    
    // Sync scroll
    starterCodeEl.addEventListener('scroll', () => {
      starterGutterEl.scrollTop = starterCodeEl.scrollTop;
    });

    updateStarterGutter(); // Run initially
  }
});

// ─── LLM History Dropdown (global scope for onclick) ───────────────────────
let _llmHistoryOpen = false;

function toggleLlmHistory() {
  const dropdown = document.getElementById('llmHistoryDropdown');
  if (!dropdown) return;
  _llmHistoryOpen = !_llmHistoryOpen;
  dropdown.style.display = _llmHistoryOpen ? 'block' : 'none';
  if (_llmHistoryOpen) {
    refreshLlmHistory();
    // Close when clicking outside
    setTimeout(() => {
      document.addEventListener('click', _closeLlmHistoryOutside, { once: true });
    }, 0);
  }
}

function _closeLlmHistoryOutside(e) {
  const wrapper = document.getElementById('llmHistoryWrapper');
  if (wrapper && !wrapper.contains(e.target)) {
    const dropdown = document.getElementById('llmHistoryDropdown');
    if (dropdown) dropdown.style.display = 'none';
    _llmHistoryOpen = false;
  }
}

function refreshLlmHistory() {
  const list = document.getElementById('llmHistoryList');
  if (!list) return;
  list.innerHTML = '<div style="padding:16px;text-align:center;color:#a5b4fc;font-size:0.8rem;">Loading...</div>';

  const apiBase = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:8000' : '';

  fetch(`${apiBase}/api/practice/llm-history`)
    .then(r => r.json())
    .then(data => {
      const entries = data.history || [];
      if (!entries.length) {
        list.innerHTML = '<div style="padding:20px 16px;text-align:center;color:#555;font-size:0.8rem;">No LLM calls recorded yet.<br><span style="font-size:0.72rem;opacity:0.6">Submit a question to see activity</span></div>';
        return;
      }

      const providerColors = {
        'Google Gemini (Direct)': { bg: 'rgba(66,133,244,0.15)', color: '#60a5fa', label: '🔵 Gemini' },
        'OpenRouter (Paid)':      { bg: 'rgba(124,58,237,0.15)', color: '#a78bfa', label: '🟣 OpenRouter' },
        'OpenRouter (Free)':      { bg: 'rgba(124,58,237,0.1)',  color: '#c4b5fd', label: '🟣 OR Free' },
        'Groq':                   { bg: 'rgba(249,115,22,0.15)', color: '#fb923c', label: '🟠 Groq' },
        'Anthropic':              { bg: 'rgba(236,72,153,0.15)', color: '#f472b6', label: '🩷 Anthropic' },
      };

      const typeColors = {
        'analysis':  { bg: 'rgba(16,185,129,0.15)', color: '#34d399' },
        'mlss-chat': { bg: 'rgba(99,102,241,0.15)', color: '#818cf8' },
      };

      list.innerHTML = entries.map((e, idx) => {
        const pc = providerColors[e.provider] || { bg: 'rgba(255,255,255,0.08)', color: '#ccc', label: e.provider };
        const tc = typeColors[e.type] || { bg: 'rgba(255,255,255,0.06)', color: '#aaa' };
        const ts = e.timestamp ? e.timestamp.replace('T', ' ').replace('Z', ' UTC') : '';
        const modelShort = (e.model || '').replace('google/', '').replace(':free', ' (free)');
        return `
          <div style="padding: 10px 16px; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; flex-direction: column; gap: 5px; ${idx === 0 ? 'background: rgba(99,102,241,0.06);' : ''}">
            <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
              <span style="font-size: 0.65rem; font-weight: 800; padding: 2px 7px; border-radius: 4px; background: ${pc.bg}; color: ${pc.color}; letter-spacing: 0.04em;">${pc.label}</span>
              <span style="font-size: 0.65rem; font-weight: 700; padding: 2px 7px; border-radius: 4px; background: ${tc.bg}; color: ${tc.color}; letter-spacing: 0.04em; text-transform: uppercase;">${e.type}</span>
              ${idx === 0 ? '<span style="font-size:0.6rem;background:rgba(52,211,153,0.18);color:#34d399;padding:2px 7px;border-radius:4px;font-weight:700;">LATEST</span>' : ''}
            </div>
            <div style="font-size: 0.78rem; font-weight: 600; color: #e2e8f0; font-family: var(--font-mono, monospace);">${modelShort}</div>
            <div style="font-size: 0.68rem; color: #4b5563;">${ts}</div>
          </div>`;
      }).join('');
    })
    .catch(err => {
      list.innerHTML = `<div style="padding:16px;text-align:center;color:#ef4444;font-size:0.8rem;">Failed to load history<br><span style="font-size:0.7rem;opacity:0.7">${err.message}</span></div>`;
    });
}

