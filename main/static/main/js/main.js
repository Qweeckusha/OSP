document.addEventListener('DOMContentLoaded', function() {
    var button = document.getElementById('button');

    button.addEventListener('click', async function() {
        const perm = await Notification.requestPermission()

        if (perm === 'granted') {
            new Notification('ВВГУ.Заселение', {
                body: 'Вас пригласили на обработку документов для заселения!',
                tag: 'notif'
            })
        };
    });
});
