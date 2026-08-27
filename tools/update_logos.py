import os
import glob
import re

def update_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Add Favicon to head if missing
    favicon_tag = '<link rel="icon" type="image/png" href="verifyreviews-logo.png">'
    if 'rel="icon"' not in content and '<head>' in content:
        content = content.replace('</head>', f'    {favicon_tag}\n</head>')

    # 2. Update Header logo in index.html
    index_header_old = '<a href="/" class="text-2xl font-extrabold text-primary tracking-tight">Verify<span class="text-secondary">Reviews</span></a>'
    index_header_new = '''<a href="/" class="flex items-center space-x-3 text-2xl font-extrabold text-primary tracking-tight group">
                    <img src="verifyreviews-logo.png" alt="VerifyReviews Logo" class="h-10 w-10 object-contain">
                    <span>Verify<span class="text-secondary">Reviews</span></span>
                </a>'''
    if index_header_old in content:
        content = content.replace(index_header_old, index_header_new)

    # Index Hero logo insertion
    if 'Independent Tech & Software Reviews' in content and 'verifyreviews-logo.png' not in content[max(0, content.find('Independent Tech & Software Reviews')-300):content.find('Independent Tech & Software Reviews')]:
        hero_target = '<h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight mb-6">\n                    Independent Tech & Software Reviews'
        hero_replacement = '''<div class="flex justify-center mb-6">
                    <img src="verifyreviews-logo.png" alt="VerifyReviews Logo" class="h-20 w-20 sm:h-24 sm:w-24 object-contain rounded-full bg-white/10 p-1.5 backdrop-blur-sm border border-white/20 shadow-lg">
                </div>
                <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight mb-6">
                    Independent Tech & Software Reviews'''
        if hero_target in content:
            content = content.replace(hero_target, hero_replacement)

    # Index footer brand:
    index_footer_old = '<a href="/" class="text-2xl font-extrabold text-white tracking-tight mb-4 inline-block">Verify<span class="text-secondary">Reviews</span></a>'
    index_footer_new = '''<a href="/" class="flex items-center space-x-3 text-2xl font-extrabold text-white tracking-tight mb-4 inline-flex">
                        <img src="verifyreviews-logo.png" alt="VerifyReviews Logo" class="h-9 w-9 object-contain bg-white rounded-full p-0.5">
                        <span>Verify<span class="text-secondary">Reviews</span></span>
                    </a>'''
    if index_footer_old in content:
        content = content.replace(index_footer_old, index_footer_new)

    # 3. Update Header logo in article/guide landing pages
    pattern_a_old = '''<a href="/" class="text-xl font-extrabold text-slate-900 flex items-center">
                <span class="text-secondary mr-1">Verify</span>Reviews
            </a>'''
    pattern_a_new = '''<a href="/" class="text-xl font-extrabold text-slate-900 flex items-center space-x-2">
                <img src="verifyreviews-logo.png" alt="VerifyReviews Logo" class="h-8 w-8 object-contain">
                <span><span class="text-secondary mr-1">Verify</span>Reviews</span>
            </a>'''
    if pattern_a_old in content:
        content = content.replace(pattern_a_old, pattern_a_new)

    pattern_b_old = '''<span class="text-xl font-extrabold text-slate-900 flex items-center">
                    <span class="text-secondary mr-1">Verify</span>Reviews
                </span>'''
    pattern_b_new = '''<a href="/" class="text-xl font-extrabold text-slate-900 flex items-center space-x-2">
                    <img src="verifyreviews-logo.png" alt="VerifyReviews Logo" class="h-8 w-8 object-contain">
                    <span><span class="text-secondary mr-1">Verify</span>Reviews</span>
                </a>'''
    if pattern_b_old in content:
        content = content.replace(pattern_b_old, pattern_b_new)

    pattern_c_old = '''<span class="text-xl font-extrabold text-slate-900 flex items-center">
                    <span class="text-secondary mr-1">Proxy</span>Scout
                </span>'''
    pattern_c_new = '''<a href="/" class="text-xl font-extrabold text-slate-900 flex items-center space-x-2">
                    <img src="verifyreviews-logo.png" alt="VerifyReviews Logo" class="h-8 w-8 object-contain">
                    <span><span class="text-secondary mr-1">Verify</span>Reviews</span>
                </a>'''
    if pattern_c_old in content:
        content = content.replace(pattern_c_old, pattern_c_new)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {os.path.basename(filepath)}")

def main():
    root_dir = "/Users/claudetest/Documents/Hệ thống kiếm tiền online/Affiliate Global"
    html_files = glob.glob(os.path.join(root_dir, "*.html")) + glob.glob(os.path.join(root_dir, "landing-pages", "*.html"))
    for hf in html_files:
        update_html_file(hf)

if __name__ == "__main__":
    main()
