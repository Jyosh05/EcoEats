document.addEventListener("DOMContentLoaded", function() {
    const stars = document.querySelectorAll(".star");
    const ratingContainer = document.querySelector(".rating");
    const selectedRatingText = document.getElementById("selected-rating");

    stars.forEach(star => {
        star.addEventListener("mouseover", hoverRating);
        star.addEventListener("mouseout", resetRating);
        star.addEventListener("click", clickRating);
    });

    function hoverRating(e) {
        resetRating();
        const hoverValue = e.target.getAttribute("data-value");
        stars.forEach(star => {
            if (star.getAttribute("data-value") <= hoverValue) {
                star.classList.add("active");
            }
        });
    }

    function resetRating() {
        stars.forEach(star => {
            star.classList.remove("active");
        });
        const currentRating = ratingContainer.getAttribute("data-rating");
        if (currentRating > 0) {
            for (let i = 1; i <= currentRating; i++) {
                stars[i - 1].classList.add("active");
            }
        }
    }

    function clickRating(e) {
        const clickedValue = e.target.getAttribute("data-value");
        ratingContainer.setAttribute("data-rating", clickedValue);
        resetRating();
        selectedRatingText.textContent = `Selected Rating: ${clickedValue}`;
    }

    window.submitRating = function() {
        const selectedRating = ratingContainer.getAttribute("data-rating");

        // Send the selectedRating to the server using AJAX
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/submit_rating", true);
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                alert(response.message); // You can handle the server response here
            }
        };
        xhr.send(`rating=${selectedRating}`);
    };
});