function updateQueue() {
            $.ajax({
                url: "/admin_panel/api/users/",
                method: "GET",
                success: function(response) {

                    var univData = response.filter(function(queue) {
                        return queue.queue_id.slice(0, 1) == 'У';
                    });
                    var colData = response.filter(function(queue) {
                        return queue.queue_id.slice(0, 1) == 'К';
                    });

                    // Функции для обновления на страницах
                    updateTable('#admin_panel', response) // Внутрь admin_panel мы помещаем все записи в БД
                    updateTable('#admin_u', univData)
                    updateTable('#admin_c', colData)

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
        row.innerHTML = (tableID === '#admin_panel') ?
                        '<td>' + queue.id + '</td>' +
                        '<td>' + queue.queue_id + '</td>' +
                        '<td>' + queue.last_name + '</td>' +
                        '<td>' + queue.first_name + '</td>' +
                        '<td>' + queue.middle_name + '</td>' +
                        '<td>' + queue.affiliation + '</td>' :
                        (tableID === '#admin_u' || tableID === '#admin_c') ?
                        '<td>' + queue.id + '</td>' +
                        '<td>' + queue.queue_id + '</td>' +
                        '<td>' + queue.last_name + '</td>' +
                        '<td>' + queue.first_name + '</td>' +
                        '<td>' + queue.middle_name + '</td>' :
                        '<td>' + 'Для данной таблицы не прописан JS (static/main_admin/js/db_update.js)' + '</td>';

        if (queue.called) {
            row.classList.add(queue.queue_id.includes('У') ? 'called' : 'called_c');
        }
        $(tableID).append(row);
    });
}
        // Обновлять каждые 2 секунды
        setInterval(updateQueue, 5000);
        $(document).ready(updateQueue);