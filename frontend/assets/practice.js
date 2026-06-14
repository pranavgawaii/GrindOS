document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyzeBtn');
  const resultsContainer = document.getElementById('results');
  const loading = document.getElementById('loading');
  
  const apiBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
      ? 'http://localhost:8000' 
      : '';

  if (!analyzeBtn) return;

  // Claude model toggling logic
  const modelProviderEl = document.getElementById('modelProvider');
  const claudeModelGroupEl = document.getElementById('claudeModelGroup');

  if (modelProviderEl && claudeModelGroupEl) {
    modelProviderEl.addEventListener('change', () => {
      if (modelProviderEl.value === 'claude') {
        claudeModelGroupEl.classList.remove('hidden');
      } else {
        claudeModelGroupEl.classList.add('hidden');
      }
    });
  }
  
  // OCR Logic
  const ocrTrigger = document.getElementById('ocrTrigger');
  const ocrInput = document.getElementById('ocrInput');
  const problemTextarea = document.getElementById('problem');

  if (ocrTrigger && ocrInput) {
    ocrTrigger.addEventListener('click', (e) => {
      e.preventDefault();
      ocrInput.click();
    });

    ocrInput.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      ocrTrigger.disabled = true;
      ocrTrigger.innerHTML = '<div class="spinner" style="width: 14px; height: 14px; border-width: 2px; border-top-color: var(--text-2); margin-right: 4px;"></div> Extracting...';

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
          problemTextarea.value = data.extracted_text + "\\n\\n" + problemTextarea.value;
          
        } catch (err) {
          console.error(err);
          alert(err.message);
        } finally {
          ocrTrigger.disabled = false;
          ocrTrigger.innerHTML = '<span class="premium-star">✨</span> Extract from Image';
          ocrInput.value = ''; // reset
        }
      };
      reader.readAsDataURL(file);
    });
  }

  analyzeBtn.addEventListener('click', async () => {
    const problem = document.getElementById('problem').value.trim();
    const language = document.getElementById('language').value;
    
    const modelProvider = document.getElementById('modelProvider').value;
    const model = modelProvider === 'claude' ? document.getElementById('claudeModel').value : 'gemini';
    
    const constraints = '';
    const environment = 'auto';
    const verbosity = 'concise';
    const verifyCode = false;
    
    const starterCode = document.getElementById('starterCode').value.trim();
    const isCompletionMode = starterCode.length > 0;
    const completionFormat = document.getElementById('completionFormat').value;
    
    if (!problem) {
      alert("Please paste a problem statement first!");
      return;
    }
    
    // UI state
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
      // Syntax highlighting
      document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
      });
      
    } catch (err) {
      console.error(err);
      alert("Failed to analyze problem: " + err.message);
    } finally {
      analyzeBtn.disabled = false;
      loading.style.display = 'none';
    }
  });
   function renderResults(data, language) {
    let verificationBadgeRow = '';
    if (data.verification && data.verification.length > 0) {
      let passedCount = 0;
      let totalCount = data.verification.length;
      let badgeHtml = '';
      
      data.verification.forEach((tc, idx) => {
        if (tc.passed) passedCount++;
        badgeHtml += `
          <div class="test-badge ${tc.passed ? 'pass' : 'fail'}" style="padding: 6px 12px; font-size: 0.8rem; font-weight: 600; border-radius: 6px; display: inline-flex; align-items: center; gap: 6px;">
            ${tc.passed ? '✅' : '❌'} Test ${idx + 1}
          </div>
        `;
      });

      const passRatio = passedCount / totalCount;
      const statusText = passRatio === 1 
        ? 'All Tests Passed Successfully' 
        : `Tests: ${passedCount}/${totalCount} Passed`;
      
      verificationBadgeRow = `
        <div class="verification-status-panel" style="background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; box-shadow: var(--shadow-sm); margin-bottom: 20px;">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.2rem;">${passRatio === 1 ? '🎉' : '⚠️'}</span>
            <span style="font-weight: 600; font-size: 0.95rem; color: var(--text-1);">${statusText}</span>
          </div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            ${badgeHtml}
          </div>
        </div>
      `;
    }

    let complexityPills = '';
    if (data.complexity) {
      complexityPills = `
        <div style="display: flex; gap: 8px;">
          <span class="complexity-pill" style="margin-right: 0; padding: 6px 12px; font-size: 0.85rem;">⏱️ Time: ${data.complexity.time || 'O(?)'}</span>
          <span class="complexity-pill" style="margin-right: 0; padding: 6px 12px; font-size: 0.85rem;">💾 Space: ${data.complexity.space || 'O(?)'}</span>
        </div>
      `;
    }

    let html = `
      <div class="results-layout" style="display: flex; flex-direction: column; gap: 24px; animation: slideUp 0.4s ease;">
        <!-- Verification Header -->
        ${verificationBadgeRow}

        <!-- Code Showcase Card -->
        <div class="code-showcase-card" style="background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-md); position: relative;">
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

        <!-- Explanation & Complexity Card -->
        <div class="explanation-card" style="background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 24px; box-shadow: var(--shadow-sm); margin-bottom: 24px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; border-bottom: 1px solid var(--border); padding-bottom: 16px;">
            <h3 style="font-size: 1.15rem; font-weight: 700; color: var(--text-1); margin: 0; display: flex; align-items: center; gap: 8px;">
              💡 Complexity & Explanation
            </h3>
            ${complexityPills}
          </div>
          
          <div class="explanation-content" style="color: var(--text-2); font-size: 1rem; line-height: 1.65;">
            ${marked.parse(data.explanation || 'No explanation provided.')}
          </div>
        </div>
      </div>
    `;

    resultsContainer.innerHTML = html;

    // Apply highlight.js to dynamically inserted code blocks
    resultsContainer.querySelectorAll('pre code').forEach((block) => {
      if (window.hljs) {
        hljs.highlightElement(block);
      }
    });

    // Setup Copy Buttons
    resultsContainer.querySelectorAll('.copy-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const codeElement = btn.closest('.code-container').querySelector('code');
        if (codeElement) {
          navigator.clipboard.writeText(codeElement.innerText).then(() => {
            const labelSpan = btn.querySelector('span');
            const oldHtml = btn.innerHTML;
            btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg> <span>Copied!</span>';
            setTimeout(() => btn.innerHTML = oldHtml, 2000);
          });
        }
      });
    });
  }
});
