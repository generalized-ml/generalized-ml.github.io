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
// Scroll-linked depth with independent layers and native browser scrolling.
const introStage = document.querySelector('.intro-stage');
if (introStage) {
  const intro = introStage.querySelector('.about');
  const title = intro.querySelector('#about-title');
  const copy = intro.querySelector('.about-copy');
  const portrait = intro.querySelector('.about-portrait');
  const cue = intro.querySelector('.intro-scroll');
  const images = [...document.querySelectorAll('#projects .project-diagram img')];
  const cards = [...document.querySelectorAll('#projects .grid > .card')];
  const grid = latestWork?.querySelector('.grid');
  const layers = [title, copy, portrait, cue, ...cards, ...images];
  const compact = window.matchMedia('(max-width: 760px)');
  let frame = 0;
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const setDepth = (element, y, scale = 1) => {
    element.style.setProperty('--depth-y', `${y.toFixed(2)}px`);
    element.style.setProperty('--depth-scale', scale.toFixed(4));
  };
  function updateDepth() {
    frame = 0;
    if (motionPreference.matches) return;
    const height = window.innerHeight;
    const stageRect = introStage.getBoundingClientRect();
    const progress = clamp(-stageRect.top / Math.max(height * 0.85, 1), 0, 1);
    const strength = compact.matches ? 0.4 : 1;
    setDepth(title, -progress * 100 * strength);
    setDepth(copy, -progress * 42 * strength);
    setDepth(portrait, progress * 60 * strength, 1 + progress * 0.06 * strength);
    cue.style.opacity = String(1 - clamp(progress * 3, 0, 1));
    cue.style.visibility = progress > 0.55 ? 'hidden' : '';
    if (grid) {
      const gridTop = grid.getBoundingClientRect().top;
      cards.forEach(card => {
        // offsetTop is unaffected by transforms, so scrolling reverses cleanly.
        const center = gridTop + card.offsetTop + card.offsetHeight / 2;
        const cardProgress = clamp((height / 2 - center) / Math.max(height, 1), -1, 1);
        setDepth(card, -cardProgress * 36 * strength);
      });
    }
    images.forEach(image => {
      const rect = image.parentElement.getBoundingClientRect();
      if (rect.bottom < -100 || rect.top > height + 100) return;
      const imageProgress = clamp((height / 2 - rect.top - rect.height / 2) / Math.max(height, 1), -1, 1);
      setDepth(image, imageProgress * 48 * strength, 1.04);
    });
  }
  function requestDepth() {
    if (!frame && !motionPreference.matches) frame = requestAnimationFrame(updateDepth);
  }
  function configureDepth() {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    introStage.classList.toggle('has-parallax', !motionPreference.matches);
    if (motionPreference.matches) {
      layers.forEach(element => {
        element.style.removeProperty('--depth-y');
        element.style.removeProperty('--depth-scale');
      });
      cue.style.removeProperty('opacity');
      cue.style.removeProperty('visibility');
    } else {
      requestDepth();
    }
  }
  window.addEventListener('scroll', requestDepth, { passive: true });
  window.addEventListener('resize', requestDepth, { passive: true });
  window.addEventListener('pageshow', requestDepth);
  document.querySelector('.about-portrait img').addEventListener('load', requestDepth);
  motionPreference.addEventListener('change', configureDepth);
  compact.addEventListener('change', requestDepth);
  configureDepth();
}
