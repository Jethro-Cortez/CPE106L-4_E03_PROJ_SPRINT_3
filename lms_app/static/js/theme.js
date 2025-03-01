// Theme Toggle Functionality
document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.querySelector(".theme-toggle")
  const htmlElement = document.documentElement
  const themeIcon = themeToggle.querySelector("i")

  // Check for saved theme preference or use system preference
  const savedTheme = localStorage.getItem("theme")
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches

  // Set initial theme
  if (savedTheme === "dark" || (savedTheme === null && prefersDark)) {
    htmlElement.setAttribute("data-theme", "dark")
    themeIcon.classList.remove("fa-moon")
    themeIcon.classList.add("fa-sun")
    themeToggle.setAttribute("aria-pressed", "true")
  } else {
    htmlElement.setAttribute("data-theme", "light")
    themeIcon.classList.remove("fa-sun")
    themeIcon.classList.add("fa-moon")
    themeToggle.setAttribute("aria-pressed", "false")
  }

  // Toggle theme on button click
  themeToggle.addEventListener("click", () => {
    const currentTheme = htmlElement.getAttribute("data-theme")
    const newTheme = currentTheme === "light" ? "dark" : "light"

    htmlElement.setAttribute("data-theme", newTheme)
    localStorage.setItem("theme", newTheme)

    // Update icon and aria-pressed
    if (newTheme === "dark") {
      themeIcon.classList.remove("fa-moon")
      themeIcon.classList.add("fa-sun")
      themeToggle.setAttribute("aria-pressed", "true")
    } else {
      themeIcon.classList.remove("fa-sun")
      themeIcon.classList.add("fa-moon")
      themeToggle.setAttribute("aria-pressed", "false")
    }
  })

  // Mobile navigation toggle
  const navbarToggler = document.querySelector(".navbar-toggler")
  const navLinks = document.querySelector(".nav-links")

  if (navbarToggler) {
    navbarToggler.addEventListener("click", () => {
      navLinks.classList.toggle("active")
      const expanded = navbarToggler.getAttribute("aria-expanded") === "true" || false
      navbarToggler.setAttribute("aria-expanded", !expanded)
    })
  }

  // Close flash messages
  const closeButtons = document.querySelectorAll(".flash-close")
  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const flashMessage = this.closest(".flash")
      flashMessage.style.opacity = "0"
      setTimeout(() => {
        flashMessage.style.display = "none"
      }, 300)
    })
  })

  // Auto-hide flash messages after 5 seconds
  const flashMessages = document.querySelectorAll(".flash")
  flashMessages.forEach((message) => {
    setTimeout(() => {
      message.style.opacity = "0"
      setTimeout(() => {
        message.style.display = "none"
      }, 300)
    }, 5000)
  })
})

