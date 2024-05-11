document.addEventListener("DOMContentLoaded", function() {

        var button = document.getElementById("delete");
        var form = document.getElementById("editingForm");
        var btn2 = document.getElementById('editing');
        var btn3 = document.getElementById('editing');


        button.addEventListener("click", function() {
        // Применяем стили напрямую к кнопке
        button.style.backgroundColor = "#1d6ea3"; // Например, устанавливаем красный цвет фона
        button.style.color = "white"; // Устанавливаем белый цвет текста


        // Применяем стили напрямую к кнопке btn2
        btn2.style.backgroundColor = "#fff"; // Например, устанавливаем синий цвет фона
        btn2.style.color = "#000"; // Устанавливаем белый цвет текста


        // Заменяем содержимое формы
        form.innerHTML = `
            {% csrf_token %}
            <div class="input" id="first_input">
                <input required type="text" name="queue_id" placeholder="Номер участника">
            </div>
            <button id="edit" type="submit">Удалить</button>
        `;
        // Устанавливаем атрибут action для формы
        form.action = "{% url 'deleting' %}";
        console.log("Кнопка была нажата!");
    });
    btn2.addEventListener("click", function() {
        // Применяем стили напрямую к кнопке
        btn2.style.backgroundColor = "#1d6ea3"; // Например, устанавливаем красный цвет фона
        btn2.style.color = "white"; // Устанавливаем белый цвет текста


        // Применяем стили напрямую к кнопке btn2
        button.style.backgroundColor = "#fff"; // Например, устанавливаем синий цвет фона
        button.style.color = "#000"; // Устанавливаем белый цвет текста


        // Заменяем содержимое формы
        form.innerHTML = `
            {% csrf_token %}
            <div>
                <div class="input" id="first_input">
                    <input required type="text" name="ID" placeholder="ID">
                </div>
                <div class="input">
                    <input required type="text" name="last_name" placeholder="Фамилия">
                </div>
                <div class="input">
                    <input required type="text" name="first_name" placeholder="Имя">
                </div>
                <div class="input">
                    <input type="text" name="middle_name" placeholder="Отчество">
                </div>
            </div>
            <button id="edit" type="submit">Изменить</button>
        `;
        // Устанавливаем атрибут action для формы
        form.action = "{% url 'editing' %}";
        console.log("Кнопка была нажата!");
        });
    });