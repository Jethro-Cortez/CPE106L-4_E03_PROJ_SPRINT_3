document.addEventListener("DOMContentLoaded", () => {
  // Form validation for login form
  const loginForm = document.getElementById("login-form")
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      const username = document.getElementById("username").value.trim()
      const password = document.getElementById("password").value.trim()
      let isValid = true

      if (!username) {
        showError("username", "Username is required")
        isValid = false
      } else {
        clearError("username")
      }

      if (!password) {
        showError("password", "Password is required")
        isValid = false
      } else {
        clearError("password")
      }

      if (!isValid) {
        e.preventDefault()
      }
    })
  }

  // Form validation for registration form
  const registerForm = document.getElementById("register-form")
  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      const username = document.getElementById("username").value.trim()
      const email = document.getElementById("email").value.trim()
      const password = document.getElementById("password").value.trim()
      const confirmPassword = document.getElementById("confirm_password").value.trim()
      let isValid = true

      if (!username) {
        showError("username", "Username is required")
        isValid = false
      } else if (username.length < 3) {
        showError("username", "Username must be at least 3 characters")
        isValid = false
      } else {
        clearError("username")
      }

      if (!email) {
        showError("email", "Email is required")
        isValid = false
      } else if (!isValidEmail(email)) {
        showError("email", "Please enter a valid email address")
        isValid = false
      } else {
        clearError("email")
      }

      if (!password) {
        showError("password", "Password is required")
        isValid = false
      } else if (password.length < 6) {
        showError("password", "Password must be at least 6 characters")
        isValid = false
      } else {
        clearError("password")
      }

      if (password !== confirmPassword) {
        showError("confirm_password", "Passwords do not match")
        isValid = false
      } else {
        clearError("confirm_password")
      }

      if (!isValid) {
        e.preventDefault()
      }
    })
  }

  // Helper functions
  function showError(fieldId, message) {
    const field = document.getElementById(fieldId)
    const errorElement = field.nextElementSibling?.classList.contains("error-message")
      ? field.nextElementSibling
      : document.createElement("div")

    if (!errorElement.classList.contains("error-message")) {
      errorElement.classList.add("error-message")
      errorElement.style.color = "#ef4444"
      errorElement.style.fontSize = "0.875rem"
      errorElement.style.marginTop = "0.5rem"
      field.parentNode.insertBefore(errorElement, field.nextSibling)
    }

    errorElement.textContent = message
    field.style.borderColor = "#ef4444"
  }

  function clearError(fieldId) {
    const field = document.getElementById(fieldId)
    const errorElement = field.nextElementSibling

    if (errorElement && errorElement.classList.contains("error-message")) {
      errorElement.textContent = ""
    }

    field.style.borderColor = ""
  }

  function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }
})

