function createElement(name, { attributes, classes } = {}) {
  let element = document.createElement(name);
  if (attributes) {
    attributes.forEach((attribute) => {
      element.setAttribute(attribute.name, attribute.value);
    });
  }
  if (classes) {
    element.classList.add(...classes);
  }
  return element;
}

export { createElement };
