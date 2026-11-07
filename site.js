document.querySelectorAll('.mobile-nav a').forEach(link => {
  link.addEventListener('click', () => {
    link.closest('details').open = false;
  });
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') {
    const menu = document.querySelector('.mobile-nav[open]');
    if (menu) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  }
});
document.querySelector('.contact-form')?.addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  const body = `${data.get('message')}\n\nFrom: ${data.get('name')}\nEmail: ${data.get('email')}`;
  window.location.href = `mailto:raghav.sharma481@gmail.com?subject=${encodeURIComponent(data.get('subject'))}&body=${encodeURIComponent(body)}`;
});

const latestWork = document.querySelector('#projects');
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
if (latestWork && 'IntersectionObserver' in window && !motionPreference.matches) {
  const targets = [...latestWork.querySelectorAll(':scope > .section-head, :scope > .grid > .card')];
  const activeAnimations = new Set();
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      observer.unobserve(entry.target);
      if (motionPreference.matches || typeof entry.target.animate !== 'function') return;
      const index = targets.indexOf(entry.target);
      const animation = entry.target.animate([
        { opacity: 0, transform: 'translateY(64px) scale(0.97)' },
        { opacity: 1, transform: 'translateY(0) scale(1)' }
      ], {
        duration: 900,
        delay: index > 0 ? ((index - 1) % 3) * 100 : 0,
        easing: 'cubic-bezier(0.16, 1, 0.3, 1)',
        fill: 'backwards'
      });
      activeAnimations.add(animation);
      animation.onfinish = () => activeAnimations.delete(animation);
      animation.oncancel = () => activeAnimations.delete(animation);
    });
  }, { rootMargin: '0px 0px -24px 0px', threshold: 0.08 });
  targets.forEach(target => observer.observe(target));
  motionPreference.addEventListener('change', () => {
    if (motionPreference.matches) {
      observer.disconnect();
      activeAnimations.forEach(animation => animation.cancel());
    }
  });
}
