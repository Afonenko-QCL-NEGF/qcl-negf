// OOD 4.2.5: editor.js applies this preference during its DOM-ready callback.
document.addEventListener('DOMContentLoaded', () => {
  const theme = document.querySelector('#theme');
  if (!document.querySelector('#editor') || !theme) return;
  localStorage.setItem('ood_editor_store_ood_editor_store_theme', 'ace/theme/chrome');
  const dark = theme.querySelector('optgroup[label="Dark"]');
  if (dark) dark.remove();
});
