let themes = []

function swapThemeButtons() {
  const currentTheme = getTheme()
  const themeSwitcher = document.querySelector('.theme-switcher-button')
  themes.forEach((theme) => {
    const themeButton = document.querySelector(`.theme-box .${theme}-button`)
    if (theme === currentTheme) {
      themeButton.classList.add('hide-in-mobile')
    } else {
      themeButton.classList.remove('hide-in-mobile')
    }
  })
}

function switchLogo(themeName) {
  let logo = document.getElementById('logo')
  let profilePhoto = document.getElementById('profile-photo')
  if (themeName === 'white-theme') {
    logo.setAttribute('src', '/images/logos/exeami.png')
    profilePhoto.setAttribute('src', '/images/logos/exeami.png')
  } else {
    logo.setAttribute('src', '/images/logos/exeami-light.png')
    profilePhoto.setAttribute('src', '/images/logos/exeami-light.png')
  }
}

function selectTheme(themeName) {
  const themeButton = document.querySelector(`.theme-box .${themeName}-button`)
  const themeSwitcher = document.querySelector('.theme-switcher-button')

  themeSwitcher.classList.replace(`${getTheme()}-button`, `${themeName}-button`)
  themeSwitcher.textContent = themeButton.textContent

  document.documentElement.className = themeName
  switchLogo(themeName)
  localStorage.setItem('theme', themeName)
}

function getTheme() {
  return document.documentElement.className
}

function isDisplayed(element) {
  return window.getComputedStyle(element).display !== 'none'
}

function getAllThemes() {
  const themes = []
  const themeBox = document.querySelector('.theme-box')
  for (let child of themeBox.children) {
    themes.push(child.classList[0].replace('-button', ''))
  }
  return themes
}

window.onload = function () {
  themes = getAllThemes()

  const themeSwitcher = document.querySelector('.theme-switcher-button')
  const themeName = localStorage.getItem('theme') || themes[0]

  themeSwitcher.classList.add(`${themeName}-button`)
  selectTheme(themeName)

  const themeButtons = document.querySelectorAll('.theme-button')

  themeButtons.forEach((themeButton) => {
    themeButton.onclick = () => {
      selectTheme(themeButton.getAttribute('data-theme'))
      swapThemeButtons()
    }
  })

  themeSwitcher.onclick = () => {
    swapThemeButtons()
    const themeBox = document.querySelector('.theme-box')
    if (themeBox.classList.contains('hide-in-mobile')) {
      themeBox.classList.remove('hide-in-mobile')
    } else {
      themeBox.classList.add('hide-in-mobile')
    }
  }
}
