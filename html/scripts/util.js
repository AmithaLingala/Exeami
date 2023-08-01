// function to set a given theme/color-scheme
function selectTheme(themeName) {
  localStorage.setItem('theme', themeName)
  document.documentElement.className = themeName
}

window.onload = function () {
  const themeButtons = document.querySelectorAll('.theme-button')
  themeButtons.forEach((themeButton) => {
    themeButton.onclick = () =>
      selectTheme(themeButton.getAttribute('data-theme'))
  })
  const theme = localStorage.getItem('theme') || 'black-theme'
  selectTheme(theme)
}
