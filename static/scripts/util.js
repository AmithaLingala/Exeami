function selectTheme(themeName) {
  localStorage.setItem('theme', themeName)
  document.documentElement.className = themeName
  switchLogo(themeName)
}

function switchLogo(themeName) {
  let logo = document.getElementById('logo')
  if (themeName === 'white-theme') {
    logo.setAttribute('src', '/images/logos/exeami.png')
  } else {
    logo.setAttribute('src', '/images/logos/exeami-light.png')
  }
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
