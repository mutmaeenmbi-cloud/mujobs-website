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
