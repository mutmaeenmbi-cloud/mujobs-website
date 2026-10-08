const menu = document.querySelector('.menu');
if (menu) {
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { menu.open = false; }));
  document.addEventListener('click', e => { if (!menu.contains(e.target)) menu.open = false; });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu.open) { menu.open = false; menu.querySelector('summary').focus(); }
  });
}
function syncLanguageLinks() {
  document.querySelectorAll('.language-switch a').forEach(a => { a.hash = location.hash; });
}
syncLanguageLinks();
window.addEventListener('hashchange', syncLanguageLinks);
const filters = document.querySelector('.filters');
if (filters) {
  const cards = [...document.querySelectorAll('.work-card')];
  const buttons = [...filters.querySelectorAll('button')];
  const count = document.querySelector('.result-count');
  function select(value) {
    if (!buttons.some(b => b.dataset.filter === value)) value = 'all';
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.filter === value)));
    cards.forEach(card => { card.hidden = value !== 'all' && card.dataset.sector !== value; });
    const n = cards.filter(card => !card.hidden).length;
    count.textContent = document.documentElement.lang === 'de' ? `${n} ${n === 1 ? 'Projekt' : 'Projekte'}` : `${n} ${n === 1 ? 'project' : 'projects'}`;
  }
  filters.hidden = false;
  buttons.forEach(b => b.addEventListener('click', () => select(b.dataset.filter)));
  select('all');
}

// Motion is an optional layer: every page remains readable without it.
(() => {
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (preference.matches || !('IntersectionObserver' in window)) return;
  const root = document.documentElement;
  const header = document.querySelector('.header');
  const progress = document.createElement('div');
  progress.className = 'reading-progress';
  progress.setAttribute('aria-hidden', 'true');
  document.body.appendChild(progress);
  root.classList.add('motion-enabled');

  const revealSelector = '.section-heading, .service-deliverables article, .market-card, .work-card, .insight-card, .reading > section, .sector-roles, .closing, .footer-grid';
  const targets = [...document.querySelectorAll(revealSelector)];
  const groups = ['.service-deliverables', '.market-grid', '.work-grid'];
  groups.forEach(selector => {
    document.querySelectorAll(selector).forEach(group => {
      [...group.children].forEach((item, index) => {
        item.style.setProperty('--reveal-delay', `${Math.min(index % 3, 2) * 90}ms`);
      });
    });
  });
  targets.forEach(target => target.classList.add('motion-reveal'));
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('motion-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
  targets.forEach(target => observer.observe(target));

  // Trigger the complete sequence once the funnel or method reaches the viewport.
  const sequences = document.querySelectorAll('.pipeline, .method-cards');
  const sequenceObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('sequence-visible');
      sequenceObserver.unobserve(entry.target);
    });
  }, { threshold: 0.12 });
  sequences.forEach(sequence => {
    [...sequence.children].forEach((item, index) => {
      item.style.setProperty('--sequence-delay', `${index * 130}ms`);
    });
    sequenceObserver.observe(sequence);
  });

  let frame = 0;
  const updateScroll = () => {
    frame = 0;
    const distance = root.scrollHeight - window.innerHeight;
    progress.style.transform = `scaleX(${distance > 0 ? Math.min(window.scrollY / distance, 1) : 0})`;
    header?.classList.toggle('header-scrolled', window.scrollY > 24);
  };
  const onScroll = () => {
    if (!frame) frame = window.requestAnimationFrame(updateScroll);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  updateScroll();
  preference.addEventListener('change', event => {
    if (!event.matches) return;
    root.classList.remove('motion-enabled');
    observer.disconnect();
    sequenceObserver.disconnect();
    window.removeEventListener('scroll', onScroll);
    window.removeEventListener('resize', onScroll);
    if (frame) window.cancelAnimationFrame(frame);
    progress.remove();
  });
})();
