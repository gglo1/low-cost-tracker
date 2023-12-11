document.addEventListener('DOMContentLoaded', function() {
    update_stats();
    setInterval(update_stats, 5000);
});

function update_stats() {
    fetch("/api/status")
    .then(response => response.json())
    .then(data => {
        document.querySelector('#ml').innerHTML = data['my_count'];
        document.querySelector('#al').innerHTML = data['active_count'];
    })
}