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
    if (profilePhoto !== null)
      profilePhoto.setAttribute('src', '/images/logos/exeami.png')
  } else {
    logo.setAttribute('src', '/images/logos/exeami-light.png')
    if (profilePhoto !== null)
      profilePhoto.setAttribute('src', '/images/logos/exeami-light.png')
  }
}

function switchIcons(themeName) {
  let envolopeIcon = document.getElementById('envelope-icon')
  let gitHubIcon = document.getElementById('github-icon')
  let linkedinIcon = document.getElementById('linkedin-icon')
  if (envolopeIcon !== null && gitHubIcon !== null && linkedinIcon !== null) {
    if (themeName === 'white-theme') {
      envolopeIcon.setAttribute('src', '/images/contact/envelope.svg')
      gitHubIcon.setAttribute('src', '/images/contact/github.svg')
      linkedinIcon.setAttribute('src', '/images/contact/linkedin.svg')
    } else {
      envolopeIcon.setAttribute('src', '/images/contact/envelope-white.svg')
      gitHubIcon.setAttribute('src', '/images/contact/github-white.svg')
      linkedinIcon.setAttribute('src', '/images/contact/linkedin-white.svg')
    }
  }
}

function selectTheme(themeName) {
  const themeButton = document.querySelector(`.theme-box .${themeName}-button`)
  const themeSwitcher = document.querySelector('.theme-switcher-button')

  themeSwitcher.classList.replace(`${getTheme()}-button`, `${themeName}-button`)
  themeSwitcher.textContent = themeButton.textContent

  document.documentElement.className = themeName
  switchLogo(themeName)
  switchIcons(themeName)
  localStorage.setItem('theme', themeName)
}

function getTheme() {
  return document.documentElement.className
}

function isDisplayed(element) {
  return window.getComputedStyle(element).display !== 'none'
}

function copyPath(target, path) {
  const value = target.textContent
  target.textContent = 'Copied link!'

  setTimeout(() => {
    target.textContent = value
  }, 1000)
  url = `${window.location.host}${path}`
  navigator.clipboard.writeText(url)
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
