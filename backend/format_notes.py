import os
import re

def process_file(filepath, tab_id, subject, title, color):
    with open(filepath, 'r') as f:
        lines = f.read().split('\n')
        
    html = []
    html.append(f'<div id="{tab_id}" class="nb-page">')
    html.append('  <div class="page-frame">')
    html.append('    <div class="page-top">')
    html.append(f'      <div class="page-dot" style="background:{color}"></div>')
    html.append('      <div>')
    html.append(f'        <div class="page-subject">{subject}</div>')
    html.append(f'        <div class="page-title">{title}</div>')
    html.append('      </div>')
    html.append('      <div class="page-date">Today</div>')
    html.append('    </div>')
    html.append('    <div class="ruled">')
    
    line_num = 1
    for line in lines:
        if not line.strip():
            html.append(f'      <div class="line blank"><span class="line-num">{line_num}</span><span class="line-content"></span></div>')
        else:
            # Escape HTML
            line_escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            # Highlight headings
            if re.match(r'^#{1,3}\s', line_escaped):
                line_escaped = f'<span class="hl-purple">{line_escaped}</span>'
            elif line_escaped.startswith('---'):
                line_escaped = f'<span class="hl-teal">{line_escaped}</span>'
            elif line_escaped.startswith('**'):
                # Bold to coral
                line_escaped = re.sub(r'\*\*(.*?)\*\*', r'<span class="hl-coral">\1</span>', line_escaped)
            
            # Additional bold parsing
            line_escaped = re.sub(r'\*(.*?)\*', r'<b>\1</b>', line_escaped)
            
            html.append(f'      <div class="line"><span class="line-num">{line_num}</span><span class="line-content">{line_escaped}</span></div>')
        line_num += 1
        
    html.append('    </div>')
    html.append('  </div>')
    html.append('</div>')
    return '\n'.join(html)

def update_notebook():
    guide_html = process_file('/Users/8teen/Downloads/04_/Active/GrindOS/backend/scratch_notes_guide.txt', 'tab-guide', 'Complete Guide', 'DEV + DSA + AI/ML + INTERVIEW PREP', '#534AB7')
    playbook_html = process_file('/Users/8teen/Downloads/04_/Active/GrindOS/backend/scratch_notes_playbook.txt', 'tab-playbook', 'Fresher Playbook', 'Everything in one place', '#993C1D')
    
    nb_path = '/Users/8teen/Downloads/04_/Active/GrindOS/interview_notes_notebook.html'
    with open(nb_path, 'r') as f:
        content = f.read()
        
    # Remove existing guide/playbook tabs if they were injected wrong before
    content = re.sub(r'<div id="tab-guide".*?(?=<div id="tab-playbook"|</div>\n\n<script>)', '', content, flags=re.DOTALL)
    content = re.sub(r'<div id="tab-playbook".*?(?=</div>\n\n<script>)', '', content, flags=re.DOTALL)
    
    # Inject right before the closing div of nb-wrap
    # In the file, the end is:
    #     </div>
    #   </div>
    # </div>
    # 
    # </div>
    # 
    # <script>
    
    parts = content.split('</div>\n\n<script>')
    if len(parts) == 2:
        new_content = parts[0] + '\n' + guide_html + '\n\n' + playbook_html + '\n</div>\n\n<script>' + parts[1]
        with open(nb_path, 'w') as f:
            f.write(new_content)
        print("Successfully updated notebook.")
    else:
        print("Could not find insertion point.")

if __name__ == '__main__':
    update_notebook()
