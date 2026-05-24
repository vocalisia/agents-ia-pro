#!/usr/bin/env python3
"""Fix GA4 issues on agents-ia.pro:
1. Inject cookie banner into all pages missing it
2. Add GA4 tag to newsletter page
3. Fix app.js: accept button missing gtag consent update
4. Remove deprecated anonymize_ip from GA4 config
"""
import re
from pathlib import Path

BASE = Path(__file__).parent

GA_ID = 'G-B5627RD3TF'

GA4_SNIPPET = f'''<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
window.gtag = gtag;
var _c = (typeof localStorage !== 'undefined') ? localStorage.getItem('ai_cookies') : null;
gtag('consent', 'default', {{ analytics_storage: _c === 'rejected' ? 'denied' : 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 }});
(function(){{var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id={GA_ID}';document.head.appendChild(s);}})();
gtag('js', new Date());
gtag('config', '{GA_ID}');
</script>'''

BANNER_ROOT = '''<div class="cookie-banner" id="cookieBanner"><div class="cookie-content"><p>🍪 Ce site utilise des cookies pour analyser le trafic. <a href="/confidentialite" style="color:var(--primary-light);">Politique de confidentialité</a>.</p><div class="cookie-actions"><button class="cookie-btn cookie-accept" id="cookieAccept">Accepter</button><button class="cookie-btn cookie-decline" id="cookieDecline">Refuser</button></div></div></div>'''

BANNER_BLOG = '''<div class="cookie-banner" id="cookieBanner"><div class="cookie-content"><p>🍪 Ce site utilise des cookies pour analyser le trafic. <a href="../confidentialite.html" style="color:var(--primary-light);">Politique de confidentialité</a>.</p><div class="cookie-actions"><button class="cookie-btn cookie-accept" id="cookieAccept">Accepter</button><button class="cookie-btn cookie-decline" id="cookieDecline">Refuser</button></div></div></div>'''

# Pages missing cookie banner
ROOT_MISSING_BANNER = [
    'agent-intelligence-artificielle-pro.html',
    'contact.html',
    'marketplace-agent-ia.html',
    'merci.html',
    'vocalis-pro.html',
]

BLOG_MISSING_BANNER = [
    'blog/agent-ia-vs-employe.html',
    'blog/agent-vocal-cabinet-dentaire.html',
    'blog/choisir-agent-ia.html',
    'blog/claude-code-seo-battre-concurrents-google.html',
    'blog/deployer-agent-ia-30-minutes.html',
    'blog/rgpd-agents-ia.html',
    'blog/top-10-agents-ia-mars-2025.html',
]

def inject_banner(path: Path, banner: str):
    content = path.read_text(encoding='utf-8')
    if 'cookieBanner' in content:
        print(f'  SKIP (already has banner): {path.name}')
        return
    # Insert banner before </body>
    if '</body>' not in content:
        print(f'  WARN no </body> in {path.name}')
        return
    content = content.replace('</body>', f'\n{banner}\n</body>', 1)
    path.write_text(content, encoding='utf-8')
    print(f'  FIXED banner: {path.name}')

def add_ga4_to_newsletter():
    path = BASE / 'newsletter-issue-13-2026-04-29.html'
    content = path.read_text(encoding='utf-8')
    if GA_ID in content:
        print('  SKIP newsletter GA4 already present')
        return
    content = content.replace('<head>', f'<head>\n{GA4_SNIPPET}', 1)
    path.write_text(content, encoding='utf-8')
    print('  FIXED GA4: newsletter-issue-13-2026-04-29.html')

def fix_app_js():
    path = BASE / 'js' / 'app.js'
    content = path.read_text(encoding='utf-8')

    # Fix 1: accept button should call gtag consent update
    old_accept = """    acceptBtn.addEventListener('click', () => {
        localStorage.setItem('ai_cookies', 'accepted');
        banner.classList.add('hidden');
    });"""
    new_accept = """    acceptBtn.addEventListener('click', () => {
        localStorage.setItem('ai_cookies', 'accepted');
        banner.classList.add('hidden');
        if (typeof gtag === 'function') {
            gtag('consent', 'update', { analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
        }
    });"""

    if old_accept in content:
        content = content.replace(old_accept, new_accept)
        print('  FIXED app.js: accept button now calls gtag consent update')
    else:
        print('  WARN app.js: accept pattern not matched (already fixed or changed)')

    path.write_text(content, encoding='utf-8')

def remove_deprecated_anonymize_ip():
    """Remove anonymize_ip:true from all HTML files — deprecated in GA4."""
    count = 0
    for html_file in BASE.rglob('*.html'):
        content = html_file.read_text(encoding='utf-8', errors='ignore')
        new_content = re.sub(r',\s*anonymize_ip:\s*true', '', content)
        new_content = re.sub(r"'config',\s*'" + GA_ID + r"',\s*\{\s*\}\s*\)", f"'config', '{GA_ID}')", new_content)
        # Clean up empty config objects: gtag('config', 'G-xxx', { }) → gtag('config', 'G-xxx')
        new_content = re.sub(r"gtag\('config',\s*'" + GA_ID + r"',\s*\{\s*\}\)", f"gtag('config', '{GA_ID}')", new_content)
        if new_content != content:
            html_file.write_text(new_content, encoding='utf-8', errors='ignore')
            count += 1
    print(f'  FIXED anonymize_ip removed from {count} files')

def main():
    print('=== Fix GA4 banners + app.js ===')

    print('\n[1] Add banner to root pages...')
    for name in ROOT_MISSING_BANNER:
        inject_banner(BASE / name, BANNER_ROOT)

    print('\n[2] Add banner to blog pages...')
    for name in BLOG_MISSING_BANNER:
        inject_banner(BASE / name, BANNER_BLOG)

    print('\n[3] Add GA4 to newsletter...')
    add_ga4_to_newsletter()

    print('\n[4] Fix app.js accept button...')
    fix_app_js()

    print('\n[5] Remove deprecated anonymize_ip...')
    remove_deprecated_anonymize_ip()

    print('\nDone.')

if __name__ == '__main__':
    main()
