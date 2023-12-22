let previewContainer = document.querySelector('.food-preview');
let previewBox = previewContainer.querySelectorAll('.food-preview');

document.querySelectorAll('.food-container .food').forEach(food =>{
    food.onclick = () =>{
        previewContainer.style.display = 'flex';
        let name = food.getAttribute('data-name');
        previewBox.forEach(preview =>{
            let target = preview.getAttribute('data-target');
            if(name == target){
                preview.classList.add('active');
                }
        });
    };

});

previewBox.forEach(close =>{
    close.querySelector('.fa-times').onclick = () =>{
        close.classList.remove('active');
        previewContainer.style.display = 'none';
    };
});