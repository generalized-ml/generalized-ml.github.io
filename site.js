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
  let previousTime = 0;
  const positions = new Map();
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  function updateDepth(timestamp = 0) {
    frame = 0;
    if (motionPreference.matches) return;
    const delta = previousTime ? clamp(timestamp - previousTime, 1, 50) : 16.67;
    previousTime = timestamp;
    const blend = 1 - Math.exp(-delta / 90);
    const height = window.innerHeight;
    const progress = clamp(-introStage.getBoundingClientRect().top / Math.max(height * 0.85, 1), 0, 1);
    const strength = compact.matches ? 0.4 : 1;
    const targets = [
      [title, -progress * 64 * strength, 1],
      [copy, -progress * 30 * strength, 1],
      [portrait, progress * 32 * strength, 1 + progress * 0.035 * strength]
    ];
    // Read all geometry before applying styles to avoid repeated layout work.
    if (grid) {
      const gridTop = grid.getBoundingClientRect().top;
      cards.forEach(card => {
        const center = gridTop + card.offsetTop + card.offsetHeight / 2;
        const cardProgress = clamp((height / 2 - center) / Math.max(height, 1), -1, 1);
        targets.push([card, -cardProgress * 36 * strength, 1]);
      });
    }
    images.forEach(image => {
      const rect = image.parentElement.getBoundingClientRect();
      if (rect.bottom < -100 || rect.top > height + 100) return;
      const imageProgress = clamp((height / 2 - rect.top - rect.height / 2) / Math.max(height, 1), -1, 1);
      targets.push([image, imageProgress * 48 * strength, 1.04]);
    });
    let moving = false;
    targets.forEach(([element, targetY, targetScale]) => {
      const current = positions.get(element) || { y: 0, scale: 1 };
      current.y += (targetY - current.y) * blend;
      current.scale += (targetScale - current.scale) * blend;
      if (Math.abs(targetY - current.y) < 0.02) current.y = targetY;
      if (Math.abs(targetScale - current.scale) < 0.0001) current.scale = targetScale;
      moving ||= current.y !== targetY || current.scale !== targetScale;
      positions.set(element, current);
      element.style.setProperty('--depth-y', `${current.y.toFixed(2)}px`);
      element.style.setProperty('--depth-scale', current.scale.toFixed(4));
    });
    const targetOpacity = 1 - clamp(progress * 3, 0, 1);
    const previousOpacity = cue.style.opacity === '' ? 1 : Number(cue.style.opacity ?? 1);
    let opacity = previousOpacity + (targetOpacity - previousOpacity) * blend;
    if (Math.abs(targetOpacity - opacity) < 0.002) opacity = targetOpacity;
    moving ||= opacity !== targetOpacity;
    cue.style.opacity = String(opacity);
    cue.style.visibility = opacity < 0.01 ? 'hidden' : '';
    if (moving) frame = requestAnimationFrame(updateDepth);
    else previousTime = 0;
  }
  function requestDepth() {
    if (!frame && !motionPreference.matches) frame = requestAnimationFrame(updateDepth);
  }
  function configureDepth() {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    previousTime = 0;
    positions.clear();
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
