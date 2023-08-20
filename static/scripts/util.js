let themes = []

function swapThemeButtons() {
  const currentTheme = getTheme()
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
    logo.setAttribute('src', '/images/logos/exeami.webp')
    if (profilePhoto !== null)
      profilePhoto.setAttribute('src', '/images/logos/exeami.webp')
  } else {
    logo.setAttribute('src', '/images/logos/exeami-light.webp')
    if (profilePhoto !== null)
      profilePhoto.setAttribute('src', '/images/logos/exeami-light.webp')
  }

  let old_logo = document.getElementById('logo-old')
  let new_logo = document.getElementById('logo-new')
  if (old_logo !== null && new_logo !== null) {
    if (themeName === 'white-theme') {
      old_logo.setAttribute('src', '/images/logos/logo-old.svg')
      new_logo.setAttribute('src', '/images/logos/exeami.webp')
    } else {
      old_logo.setAttribute('src', '/images/logos/logo-old-light.svg')
      new_logo.setAttribute('src', '/images/logos/exeami-light.webp')
    }
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
  const themeSwitcher = document.querySelector('.theme-switcher-button')
  const newThemeIcon = document.querySelector(`.theme-box .${themeName}-button`)
    .children[0]

  themeSwitcher.className = themeSwitcher.className.replace(
    /[a-z]+-theme-button/,
    `${themeName}-button`
  )

  const themeSwitcherIcon = themeSwitcher.children[0]
  themeSwitcherIcon.src = newThemeIcon.src
  themeSwitcherIcon.setAttribute('alt', newThemeIcon.getAttribute('alt'))

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
  target.textContent = target.getAttribute('data-copy-value')

  setTimeout(() => {
    target.textContent = target.getAttribute('data-original-value')
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
