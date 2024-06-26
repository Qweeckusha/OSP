document.addEventListener('DOMContentLoaded', function() {
    // Запрашиваем разрешение на отправку уведомлений сразу после загрузки страницы
    Notification.requestPermission().then(function(permission) {
        if (permission === 'granted') {
            console.log('Уведомления разрешены пользователем');
        } else {
            console.log('Уведомления не разрешены пользователем');
        }
    });

    var form = document.getElementById('callForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем стандартное отправление формы

        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            type: 'POST',
            url: form.action, // URL берется из атрибута action формы
            data: {
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (Notification.permission === 'granted') {
                    // Получаем queue_id из cookie
                    var queueId = getCookie('queue_id');

                    response.called_students.forEach(function(student) {
                        if (student.queue_id === queueId) {
                            new Notification('ВВГУ. Заселение', {
                                body: `Вас пригласили на обработку документов для заселения! Студент: ${student.last_name}
                                с номером ${student.queue_id}`,
                                tag: student.queue_id
                            });
                        }
                    });
                } else {
                    console.warn('Уведомления не разрешены');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error calling students:', error);
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function base64DecodeUnicode(str) {
        // Декодируем строку из base64
        return decodeURIComponent(atob(str).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
    }
});
