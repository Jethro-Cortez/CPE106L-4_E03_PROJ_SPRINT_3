// ⭐ Star Rating Hover Effect
document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll(".star-rating label");

    stars.forEach((star) => {
        star.addEventListener("mouseover", () => {
            star.classList.add("hover");
            let previous = star.previousElementSibling;
            while (previous) {
                previous.classList.add("hover");
                previous = previous.previousElementSibling;
            }
        });

        star.addEventListener("mouseout", () => {
            stars.forEach(s => s.classList.remove("hover"));
        });
    });
});

// ⭐ Star Rating Hover Effect for Feedback
document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll(".star-rating label");

    stars.forEach((star) => {
        star.addEventListener("mouseover", () => {
            star.classList.add("hover");
            let previous = star.previousElementSibling;
            while (previous) {
                previous.classList.add("hover");
                previous = previous.previousElementSibling;
            }
        });

        star.addEventListener("mouseout", () => {
            stars.forEach(s => s.classList.remove("hover"));
        });
    });
});
