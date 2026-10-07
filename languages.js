// Real links work without JavaScript. Preserve the current section when switching.
document.querySelectorAll('.language-switch a').forEach(link => {
  if (location.hash) link.hash = location.hash;
});
window.addEventListener('hashchange', () => {
  document.querySelectorAll('.language-switch a').forEach(link => {
    link.hash = location.hash;
  });
});
