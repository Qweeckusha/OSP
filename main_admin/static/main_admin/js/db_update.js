$(document).ready(function() {
    // Обновлять каждые 5 секунд
    setInterval(updateQueue, 5000);
    updateQueue(); // Запустить обновление сразу при загрузке страницы

    // Обработчик для отправки формы
    $('#callForm').on('submit', function(event) {
        event.preventDefault(); // Предотвратить стандартное поведение отправки формы

        // Отправить AJAX-запрос
        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: $(this).serialize(), // Включает данные формы, включая CSRF-токен
            success: function(response) {
                updateQueue(); // Обновить данные после успешного выполнения запроса
            },
            error: function(xhr, status, error) {
                console.error('Ошибка при отправке запроса: ', status, error);
            }
        });
    });
});

function updateQueue() {
            $.ajax({
                url: "/admin_panel/api/users/",
                method: "GET",
                success: function(response) {

                    var univData = response.filter(queue => queue.queue_id.startsWith('У'));
                    var colData = response.filter(queue => queue.queue_id.startsWith('К'));

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
        row.innerHTML = tableID === '#admin_panel' ?
                        '<td>' + queue.id + '</td>' +
                        '<td>' + queue.queue_id + '</td>' +
                        '<td>' + queue.last_name + '</td>' +
                        '<td>' + queue.first_name + '</td>' +
                        '<td>' + queue.middle_name + '</td>' +
                        '<td>' + queue.affiliation + '</td>' :
                        tableID === '#admin_u' || tableID === '#admin_c' ?
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