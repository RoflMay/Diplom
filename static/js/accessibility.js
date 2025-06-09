const html = document.documentElement;

document.addEventListener('DOMContentLoaded', function () {
  const savedFont = localStorage.getItem('accessibilityFont');
  const savedScheme = localStorage.getItem('accessibilityScheme');
  const savedKerning = localStorage.getItem('accessibilityKerning');
  const isEnabled = localStorage.getItem('accessibilityEnabled');

  if (isEnabled === 'true') {
    if (savedFont) html.classList.add(savedFont);
    if (savedScheme) html.classList.add(savedScheme);
    if (savedKerning) html.classList.add(savedKerning);

    const panel = document.getElementById('accessibility-panel');
    if (panel) panel.style.display = 'block';
    document.body.classList.add('accessibility-enabled');
  }

  const toggleBtn = document.getElementById('toggleAccessibility');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      const panel = document.getElementById('accessibility-panel');
      const isVisible = panel && panel.style.display === 'block';

      if (panel) panel.style.display = isVisible ? 'none' : 'block';
      document.body.classList.toggle('accessibility-enabled');
      localStorage.setItem('accessibilityEnabled', !isVisible);
    });
  }

  updateEyeIcon();
});

function setFontSize(size) {
  ['font-small', 'font-medium', 'font-large'].forEach(cls => html.classList.remove(cls));
  const newClass = 'font-' + size;
  html.classList.add(newClass);
  localStorage.setItem('accessibilityFont', newClass);
}

function setColorScheme(scheme) {
  ['theme-white', 'theme-black', 'theme-blue'].forEach(cls => html.classList.remove(cls));
  const newClass = 'theme-' + scheme;
  html.classList.add(newClass);
  localStorage.setItem('accessibilityScheme', newClass);
  updateEyeIcon();
}

function setLetterSpacing(spacing) {
  ['kerning-normal', 'kerning-wide'].forEach(cls => html.classList.remove(cls));
  const newClass = 'kerning-' + spacing;
  html.classList.add(newClass);
  localStorage.setItem('accessibilityKerning', newClass);
}

function disableAccessibility() {
  ['font-small', 'font-medium', 'font-large',
   'theme-white', 'theme-black', 'theme-blue',
   'kerning-normal', 'kerning-wide'].forEach(cls => html.classList.remove(cls));

  const panel = document.getElementById('accessibility-panel');
  if (panel) panel.style.display = 'none';

  document.body.classList.remove('accessibility-enabled');

  localStorage.removeItem('accessibilityFont');
  localStorage.removeItem('accessibilityScheme');
  localStorage.removeItem('accessibilityKerning');
  localStorage.removeItem('accessibilityEnabled');
  updateEyeIcon();
}

function updateEyeIcon() {
  const eye = document.getElementById('toggleAccessibility');
  if (!eye) return;

  const currentTheme = [...html.classList].find(cls => cls.startsWith('theme-'));
  if (currentTheme === 'theme-white' || currentTheme === 'theme-blue') {
    eye.src = "/static/icons/eye2.png";
  } else {
    eye.src = "/static/icons/eye.png";
  }
}
