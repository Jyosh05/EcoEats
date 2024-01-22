function submitRating() {
    const stars = document.getElementsByName('rating');
    let ratingValue = 0;

    for (let i = 0; i < stars.length; i++) {
        if (stars[i].checked) {
            ratingValue = stars[i].value;
            break;
        }
    }

    // You can use the ratingValue to perform any action, such as sending it to a server
    // For simplicity, let's just log the rating for now
    console.log("You submitted a rating of " + ratingValue + " stars.");