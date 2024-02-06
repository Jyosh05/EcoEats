//document.addEventListener('DOMContentLoaded', function () {
//    const stars = document.querySelectorAll('.star');
//    const starsInput = document.getElementById('stars-input');
//
//    stars.forEach(star => {
//        star.addEventListener('click', function () {
//            const value = this.getAttribute('data-value');
//            updateStars(value);
//        });
//        star.addEventListener('mouseover', function () {
//            const value = this.getAttribute('data-value');
//            highlightStars(value);
//        });
//
//        star.addEventListener('mouseout', function () {
//            highlightStars(starsInput.value);
//        });
//    });
//
//    function updateStars(value) {
//        starsInput.value = value;
//        highlightStars(value);
//    }
//
//    function highlightStars(value) {
//        stars.forEach(star => {
//            const starValue = star.getAttribute('data-value');
//            star.classList.toggle('active', starValue <= value);
//        });
//    }
//});


document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.star');
    const starsInput = document.getElementById('stars-input');
    const starRatingContainer = document.getElementById('star-rating-container');

    stars.forEach(star => {
        star.addEventListener('click', function () {
            const value = this.getAttribute('data-value');
            updateStars(value);
        });
        star.addEventListener('mouseover', function () {
            const value = this.getAttribute('data-value');
            highlightStars(value);
        });

        star.addEventListener('mouseout', function () {
            highlightStars(starsInput.value);
        });
    });

    function updateStars(value) {
        starsInput.value = value;
        highlightStars(value);

        // Display stars in the starRatingContainer based on the selected value
        starRatingContainer.innerHTML = '';
        for (let i = 1; i <= value; i++) {
            const starElement = document.createElement('span');
            starElement.innerHTML = '&#9733;'; // Unicode character for a filled star
            starRatingContainer.appendChild(starElement);
        }
    }

    function highlightStars(value) {
        stars.forEach(star => {
            const starValue = star.getAttribute('data-value');
            star.classList.toggle('active', starValue <= value);
        });
    }
});
