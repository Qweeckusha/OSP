function updateQueue() {
    $.ajax({
        url: "/admin_panel/api/users/",
        method: "GET",
        success: function(response) {
            // Разделим данные на две части: для 'Университет' и 'Колледж'
            var univData = response.filter(function(queue) {
                return queue.queue_id.slice(0, 1) == 'У';
            });
            var colData = response.filter(function(queue) {
                return queue.queue_id.slice(0, 1) == 'К';
            });

            updateTable('#univ', univData);
            updateTable('#col', colData);
        },
        error: function(xhr, status, error) {
            console.error(status, error);
        }
    });
}

function updateTable(tableID, data) {
    $(tableID).empty();
    data.forEach(function(queue) {

        var row = document.createElement('tr');
        row.innerHTML = '<td>' + queue.queue_id + '</td>';
        if (queue.called) {
            row.classList.add(tableID === '#univ' ? 'called' : 'called_c');
        }
        $(tableID).append(row);
    });
}

// Обновлять каждые 2 секунды
setInterval(updateQueue, 5000);
$(document).ready(updateQueue);