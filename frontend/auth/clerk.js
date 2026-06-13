/**
 * GrindOS — Clerk Auth Guard
 *
 * Include this script on any page you want to protect.
 * Uses absolute paths for all redirects (required for Vercel cleanUrls).
 *
 * Usage (add to <head> of protected pages):
 *   <script src="/auth/clerk.js"></script>
 *   OR (with relative path from nested pages):
 *   <script src="../../auth/clerk.js"></script>
 */

// ── CONFIG ────────────────────────────────────────────────────────────────────
const CLERK_PUBLISHABLE_KEY = window.__CLERK_PUBLISHABLE_KEY__ || 'pk_test_Z29yZ2VvdXMtamF3ZmlzaC0zMy5jbGVyay5hY2NvdW50cy5kZXYk';

// ── CLERK INIT ────────────────────────────────────────────────────────────────
(function () {
  if (!CLERK_PUBLISHABLE_KEY || CLERK_PUBLISHABLE_KEY === 'PASTE_YOUR_PUBLISHABLE_KEY_HERE') {
    console.warn('[GrindOS Auth] Clerk publishable key not set. Auth is disabled.');
    return;
  }

  // Inject Clerk script if not already loaded
  if (!window.Clerk) {
    const script = document.createElement('script');
    script.src = `https://cdn.jsdelivr.net/npm/@clerk/clerk-js@4/dist/clerk.browser.js`;
    script.setAttribute('data-clerk-publishable-key', CLERK_PUBLISHABLE_KEY);
    script.async = true;
    script.onload = () => initClerk();
    document.head.appendChild(script);
  } else {
    initClerk();
  }

  async function initClerk() {
    await window.Clerk.load({
      publishableKey: CLERK_PUBLISHABLE_KEY
    });

    // Use session (more reliable than user immediately after sign-in redirect)
    const session = window.Clerk.session;
    const user = window.Clerk.user;
    const isLoginPage = window.location.pathname.includes('/auth/signin');

    if (!session && !isLoginPage) {
      // Not signed in → redirect to sign-in
      window.location.replace('/auth/signin.html');
      return;
    }

    if (session && isLoginPage) {
      // Already signed in on login page → go to dashboard
      window.location.replace('/dashboard.html');
      return;
    }

    // Inject user info into the topbar if element exists
    renderUserWidget(user);
  }

  function renderUserWidget(user) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => renderUserWidget(user));
      return;
    }
    const container = document.getElementById('clerk-user-widget');
    if (!container || !user) return;

    container.innerHTML = '';
    const afterSignOutUrl = window.location.origin + '/';
    const isDark = document.documentElement.classList.contains('dark');

    window.Clerk.mountUserButton(container, {
      afterSignOutUrl: afterSignOutUrl,
      appearance: {
        variables: {
          colorPrimary: '#ea763f',
          colorBackground: 'transparent',
          colorText:            isDark ? '#fafafa'              : '#18181b',
          colorTextSecondary:   isDark ? '#a1a1aa'              : '#71717a',
          colorInputBackground: isDark ? '#0f0f13'              : '#ffffff',
          colorInputText:       isDark ? '#fafafa'              : '#18181b',
          colorBorder:          isDark ? 'rgba(255,255,255,0.08)': '#e2e0d8',
          borderRadius: '10px',
          fontFamily: 'DM Sans, -apple-system, sans-serif',
        },
        elements: {
          userButtonAvatarBox: {
            width: '30px',
            height: '30px',
            border: '1.5px solid rgba(234,118,63,0.5)',
            borderRadius: '50%',
          },
          userButtonPopoverCard: isDark ? {
            background: 'rgba(15,15,18,0.95)',
            backdropFilter: 'blur(20px)',
            WebkitBackdropFilter: 'blur(20px)',
            border: '1px solid rgba(255,255,255,0.08)',
            boxShadow: '0 16px 40px rgba(0,0,0,0.5)',
            borderRadius: '14px',
          } : {
            background: '#ffffff',
            border: '1px solid #e2e0d8',
            boxShadow: '0 8px 28px rgba(0,0,0,0.1)',
            borderRadius: '14px',
          },
          userButtonPopoverActionButton: {
            color: isDark ? '#e4e4e7' : '#27272a',
          },
          userButtonPopoverActionButtonText: { color: 'inherit' },
          userButtonPopoverActionButtonIconBox: { color: 'inherit' },
          userButtonPopoverFooter: { display: 'none' },
        }
      }
    });
  }

  // Re-render widget when theme toggles (light ↔ dark)
  new MutationObserver(() => {
    if (window.Clerk?.user) renderUserWidget(window.Clerk.user);
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
})();
