const host = 'https://search.exeami.com/api/v1/search/'
const site = 'exeami.com'
async function search(query) {
  if (query.length > 0) {
    const response = await fetch(`${host}/?query=${query}&site=${site}`)
    const result_div = document.getElementById('search-results')
    const results = await response.json()
    if (results.length == 0) {
      const div = document.createElement('div')
      div.classList.add('is-text-center', 'title', 'is-padding-1')
      div.innerText = `No search results found for "${query}"`
      result_div.appendChild(div)
      return
    }
    const title = document.createElement('h2')
    title.classList.add('is-text-center', 'title', 'is-padding-1')
    title.innerText = `Search results for "${query}"`
    result_div.appendChild(title)

    for (let result of results) {
      const a = document.createElement('a')
      a.classList.add('search-box')
      a.href = result.url

      const div = document.createElement('div')
      div.classList.add('media-content')
      a.appendChild(div)

      const h2 = document.createElement('h2')
      h2.classList.add('title')
      h2.innerHTML = highlight(result.title, query)
      div.appendChild(h2)

      const h4 = document.createElement('h4')
      h4.classList.add('url')
      h4.innerHTML = highlight(result.url, query)
      div.appendChild(h4)

      const h3 = document.createElement('h3')
      h3.classList.add('subtitle')
      h3.innerHTML = highlight(result.summary, query)
      div.appendChild(h3)

      const p = document.createElement('p')
      p.innerHTML = highlight(result.content, query)
      div.appendChild(p)

      result_div.appendChild(a)
    }
  }
}

function highlight(content, search_text) {
  const paragraph = content
  const regex = new RegExp(String.raw`.*${search_text}.*`, 'i')
  const found = paragraph.match(regex)
  if (!found) return paragraph.substr(0, 150)
  const exactMatch = new RegExp(String.raw`(${search_text})`, 'i')
  return found[0].replace(exactMatch, '<mark>$1</mark>')
}
const search_text = new URLSearchParams(window.location.search).get('q')
const search_element = document.getElementById('search')
search_element.value = search_text
search(search_text)
