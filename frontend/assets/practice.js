document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyzeBtn');
  const resultsContainer = document.getElementById('results');
  const loading = document.getElementById('loading');
  const problemTextarea = document.getElementById('problem');
  const starterCodeTextarea = document.getElementById('starterCode');
  const completionFormatSelect = document.getElementById('completionFormat');
  const ocrTrigger = document.getElementById('ocrTrigger');
  const ocrInput = document.getElementById('ocrInput');
  const modelProviderEl = document.getElementById('modelProvider');
  const claudeModelGroupEl = document.getElementById('claudeModelGroup');
  
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
        if (ocrInput) ocrInput.value = ''; // reset file input
      }
    };
    reader.readAsDataURL(file);
  }

  // 5. Solve & Explain submission API call
  if (analyzeBtn) {
    analyzeBtn.addEventListener('click', async () => {
      const problem = problemTextarea ? problemTextarea.value.trim() : '';
      const language = document.getElementById('language').value;
      const environment = document.getElementById('environment').value;
      const verbosity = document.getElementById('verbosity').value;
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
        renderResults(data, language);
        
        resultsContainer.style.display = 'block';
        
      } catch (err) {
        console.error(err);
        alert("Failed to analyze problem: " + err.message);
      } finally {
        analyzeBtn.disabled = false;
        loading.style.display = 'none';
      }
    });
  }

  // 6. Dynamic results renderer
  function renderResults(data, language) {
    let html = `<div class="tabs">`;
    const tabs = [];
    
    // Determine which tabs to show
    if (data.constraintsCheck || data.complexity || data.naiveApproach || data.optimizedApproach) {
      tabs.push({ id: 'tab-breakdown', label: '🧠 Breakdown' });
    }
    if (data.solutionCode) {
      tabs.push({ id: 'tab-code', label: '💻 Code' });
    }
    if (data.verification && data.verification.length > 0) {
      tabs.push({ id: 'tab-verify', label: '✅ Verification' });
    }
    if (data.comparisonTable && data.comparisonTable.length > 0) {
      tabs.push({ id: 'tab-compare', label: '🤖 AI vs Human' });
    }
    if (data.feedback || data.rederivePrompt) {
      tabs.push({ id: 'tab-next', label: '🎯 Next Steps' });
    }
    
    tabs.forEach((t, i) => {
      html += `<button class="tab-btn ${i === 0 ? 'active' : ''}" data-target="${t.id}">${t.label}</button>`;
    });
    html += `</div>`;
    
    // Tab 1: Breakdown
    if (tabs.find(t => t.id === 'tab-breakdown')) {
      html += `<div id="tab-breakdown" class="tab-content ${tabs[0].id === 'tab-breakdown' ? 'active' : ''}" style="animation: slideUp 0.3s ease;">`;
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
      html += `<div id="tab-code" class="tab-content ${tabs[0].id === 'tab-code' ? 'active' : ''}">`;
      html += `
        <div class="code-showcase-card" style="background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-md); position: relative; margin-top: 10px;">
          <div class="code-card-header" style="padding: 16px 20px; background: var(--bg-2); border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between;">
            <span style="font-weight: 600; font-size: 0.95rem; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; gap: 8px;">
              💻 Optimal Code
            </span>
            <span style="font-size: 0.85rem; font-family: var(--font-mono); color: var(--brand); font-weight: 600; background: var(--brand-light); padding: 4px 8px; border-radius: 4px;">
              ${language === 'cpp' ? 'C++' : language.charAt(0).toUpperCase() + language.slice(1)}
            </span>
          </div>
          
          <div class="code-container" style="position: relative; display: flex; background: var(--code-bg); overflow: hidden;">
            <div class="line-numbers-gutter" style="padding: 20px 12px; font-family: var(--font-mono); font-size: 0.95rem; line-height: 1.5; color: var(--text-4); text-align: right; user-select: none; border-right: 1px solid var(--border); background: rgba(0, 0, 0, 0.15); min-width: 45px; box-sizing: border-box;">
              ${Array.from({length: data.solutionCode.split('\n').length}, (_, i) => `<div style="line-height: 1.5;">${i + 1}</div>`).join('')}
            </div>
            <div class="code-content-wrapper" style="flex: 1; overflow-x: auto;">
              <pre style="margin: 0; background: transparent; border: none; padding: 20px 24px; box-sizing: border-box;"><code class="language-${language}" style="background: transparent; border: none; padding: 0; font-family: var(--font-mono); font-size: 0.95rem; line-height: 1.5; display: block; white-space: pre; overflow: visible;">${data.solutionCode.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</code></pre>
            </div>
            <button class="copy-btn" title="Copy code" style="position: absolute; top: 12px; right: 12px; background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.3); color: #fff; padding: 6px 12px; border-radius: 6px; cursor: pointer; z-index: 1000; display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 0.8rem; font-weight: 500; backdrop-filter: blur(4px); opacity: 1 !important; transition: all 0.2s;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              <span>Copy</span>
            </button>
          </div>
        </div>

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
      html += `<div id="tab-verify" class="tab-content ${tabs[0].id === 'tab-verify' ? 'active' : ''}">`;
      
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
      html += `<div id="tab-compare" class="tab-content ${tabs[0].id === 'tab-compare' ? 'active' : ''}">`;
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
      html += `<div id="tab-next" class="tab-content ${tabs[0].id === 'tab-next' ? 'active' : ''}">`;
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

        const problem = problemTextarea ? problemTextarea.value.trim() : '';
        const language = document.getElementById('language').value;
        const environment = document.getElementById('environment').value;
        const verbosity = document.getElementById('verbosity').value;
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
        const originalBtnText = fixErrorBtn.innerHTML;
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
              userAttempt: data.solutionCode, // Pass the previous generated code as the attempt
              errorMessage: errorVal,        // Pass the error message
              environment,
              verbosity,
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
});
