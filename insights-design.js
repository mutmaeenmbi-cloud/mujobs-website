(() => {
  const filters = [...document.querySelectorAll('[data-blog-filter]')];
  const search = document.querySelector('[data-blog-search]');
  const items = [...document.querySelectorAll('[data-blog-item]')];
  if (!search || !items.length) return;
  document.querySelector('.journal-filters').hidden = false;
  document.querySelector('.journal-search').hidden = false;
  let selected = 'all';
  const normalise = value => value.toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const apply = () => {
    const query = normalise(search.value.trim());
    let shown = 0;
    items.forEach(item => {
      const visible = (selected === 'all' || item.dataset.topic === selected) && normalise(item.textContent).includes(query);
      item.hidden = !visible;
      if (visible) shown++;
    });
    const de = document.documentElement.lang === 'de';
    document.querySelector('[data-blog-count]').textContent = `${shown} ${de ? 'Artikel' : (shown === 1 ? 'article' : 'articles')}`;
    document.querySelector('.journal-empty').hidden = shown !== 0;
  };
  filters.forEach(button => button.addEventListener('click', () => {
    selected = button.dataset.blogFilter;
    filters.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
    apply();
  }));
  search.addEventListener('input', apply);
})();
