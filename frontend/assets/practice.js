document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyzeBtn');
  const resultsContainer = document.getElementById('results');
  const loading = document.getElementById('loading');
  
  const apiBase = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
      ? 'http://localhost:8000' 
      : '';

  if (!analyzeBtn) return;

  analyzeBtn.addEventListener('click', async () => {
    const problem = document.getElementById('problem').value.trim();
    const language = document.getElementById('language').value;
    const constraints = document.getElementById('constraints').value.trim();
    const environment = document.getElementById('environment').value;
    const verbosity = document.getElementById('verbosity').value;
    const attemptedFirst = document.getElementById('attemptedFirst').checked;
    
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
          attemptedFirst,
          environment,
          verbosity
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
      html += `<button class="tab-btn ${i===0 ? 'active' : ''}" data-target="${t.id}">${t.label}</button>`;
    });
    html += `</div>`;
    
    // Tab 1: Breakdown
    if (tabs.find(t => t.id === 'tab-breakdown')) {
      html += `<div id="tab-breakdown" class="tab-content ${tabs[0].id === 'tab-breakdown' ? 'active' : ''}">`;
      if (data.constraintsCheck) html += `<h4>Constraints</h4><p>${marked.parse(data.constraintsCheck)}</p>`;
      if (data.complexity) {
        html += `<div style="margin-bottom: 20px;">
          <span class="complexity-pill">⏱️ ${data.complexity.time || '?'}</span>
          <span class="complexity-pill">💾 ${data.complexity.space || '?'}</span>
        </div>`;
      }
      if (data.naiveApproach) html += `<h4>Naive Approach</h4><p>${marked.parse(data.naiveApproach)}</p>`;
      if (data.optimizedApproach) html += `<h4>Optimized Approach</h4><p>${marked.parse(data.optimizedApproach)}</p>`;
      if (data.pseudocode) html += `<h4>Pseudocode</h4><p>${marked.parse(data.pseudocode)}</p>`;
      html += `</div>`;
    }
    
    // Tab 2: Code
    if (tabs.find(t => t.id === 'tab-code')) {
      html += `<div id="tab-code" class="tab-content ${tabs[0].id === 'tab-code' ? 'active' : ''}">`;
      html += `<h4>Optimal Code</h4>
               <div class="code-container">
                 <button class="copy-btn">Copy</button>
                 <pre><code class="language-${language}">${data.solutionCode.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</code></pre>
               </div>`;
      html += `</div>`;
    }
    
    // Tab 3: Verification
    if (tabs.find(t => t.id === 'tab-verify')) {
      html += `<div id="tab-verify" class="tab-content ${tabs[0].id === 'tab-verify' ? 'active' : ''}">`;
      html += `<h4>Execution Verification (Judge0)</h4><div class="badge-container">`;
      let passedAll = true;
      data.verification.forEach((tc, idx) => {
         const pass = tc.passed;
         if (!pass) passedAll = false;
         html += `<div class="test-badge ${pass ? 'pass' : 'fail'}">${pass ? '✅' : '❌'} Test ${idx + 1}</div>`;
      });
      html += `</div>`;
      if (!passedAll) {
        html += `<p style="color:var(--error);font-size:0.9rem;">Warning: Some test cases failed during automated verification.</p>`;
      }
      html += `</div>`;
    }
    
    // Tab 4: Comparison
    if (tabs.find(t => t.id === 'tab-compare')) {
      html += `<div id="tab-compare" class="tab-content ${tabs[0].id === 'tab-compare' ? 'active' : ''}">`;
      let tableHtml = `<table><tr><th>Feature</th><th>Robotic/AI Style</th><th>Human/Interview Style</th></tr>`;
      data.comparisonTable.forEach(row => {
        tableHtml += `<tr><td>${row.feature}</td><td>${row.aiStyle}</td><td>${row.humanStyle}</td></tr>`;
      });
      tableHtml += `</table>`;
      html += tableHtml + `</div>`;
    }
    
    // Tab 5: Next Steps
    if (tabs.find(t => t.id === 'tab-next')) {
      html += `<div id="tab-next" class="tab-content ${tabs[0].id === 'tab-next' ? 'active' : ''}">`;
      if (data.feedback) html += `<h4>Feedback</h4><p>${marked.parse(data.feedback)}</p>`;
      if (data.rederivePrompt) html += `<h4>Try it yourself</h4><p>${marked.parse(data.rederivePrompt)}</p>`;
      html += `</div>`;
    }
    
    resultsContainer.innerHTML = html;
    
    // Setup tab switching
    const tabBtns = resultsContainer.querySelectorAll('.tab-btn');
    const tabContents = resultsContainer.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.getAttribute('data-target')).classList.add('active');
      });
    });
    
    // Setup Copy Buttons
    resultsContainer.querySelectorAll('.copy-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const codeElement = e.target.parentElement.querySelector('code');
        if (codeElement) {
          navigator.clipboard.writeText(codeElement.innerText).then(() => {
            const oldText = btn.innerText;
            btn.innerText = 'Copied!';
            setTimeout(() => btn.innerText = oldText, 2000);
          });
        }
      });
    });
  }
});
