document.querySelector('.container-rewards-available').addEventListener('click', function(event) {
  if (event.target.classList.contains('redeem-btn')) {
    var rewardId = event.target.dataset.rewardId;
    if (confirm('Are you sure you want to redeem this reward?')) {
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/redeem/' + rewardId, true);
      xhr.onload = function() {
        if (xhr.status === 200) {
          alert(xhr.responseText);
          location.reload();
        } else {
          alert('Error redeeming reward.');
        }
      };
      xhr.send();
    }
  }
});