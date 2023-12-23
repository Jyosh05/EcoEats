let previewContainer = document.querySelector('.food-preview');
let previewBox = previewContainer.querySelectorAll('.preview');

document.querySelectorAll('.food-container .food').forEach(food => {
    food.onclick = () => {
        let name = food.getAttribute('data-name');
        previewBox.forEach(preview => {
            let target = preview.getAttribute('data-target');
            if (name === target) {
                preview.classList.add('active');
            } else {
                preview.classList.remove('active');
            }
        });
        previewContainer.style.display = 'flex';
    };
});

// Attach click event to the close buttons inside the previewContainer
previewContainer.querySelectorAll('.btn-close').forEach(btnClose => {
    btnClose.onclick = () => {
        previewBox.forEach(preview => {
            preview.classList.remove('active');
        });
        previewContainer.style.display = 'none';
    };
});
