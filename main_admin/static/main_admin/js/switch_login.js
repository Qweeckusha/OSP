//document.addEventListener("DOMContentLoaded", function() {
//
//    var button = document.getElementById("admin");
//    var form = document.getElementById("login_users");
//
//    button.addEventListener("click", function() {
//        form.innerHTML = `
//            {% csrf_token %}
//            <h3>Вход</h3>
//            {{ form_admin.as_p }}
//
//            <button type="submit">Войти</button>
//            {% if error_message %}
//                <p>{{ error_message }}</p>
//            {% endif %}
//
//       <div class="social">
//           <button id="user">Пользователям</button>
//       </div>
//        `;
//        form.action = "{% url 'login_admins' %}";
//        form.id = "login_admins"
//        console.log("Switch to admin");
//    });
//});
//
//document.addEventListener("DOMContentLoaded", function() {
//
//    var button = document.getElementById("user");
//    var form = document.getElementById("login_admins");
//
//    button.addEventListener("click", function() {
//        form.innerHTML = `
//            {% csrf_token %}
//            <h3>Вход</h3>
//            {{ form.as_p }}
//
//            <button type="submit">Войти</button>
//            {% if error_message %}
//                <p>{{ error_message }}</p>
//            {% endif %}
//
//            <div class="social">
//                <button id="admin">Сотрудникам</button>
//            </div>
//        `;
//        form.action = "{% url 'login' %}";
//        form.id = "login_users"
//        console.log("Switch to login");
//    });
//});

document.addEventListener("DOMContentLoaded", function() {
    var buttonAdmin = document.getElementById("admin");
    var buttonUser = document.getElementById("user");
    var form = document.getElementById("login_users");

    buttonAdmin.addEventListener("click", function() {
        form.innerHTML = `
            <form action="{% url 'login_admins' %}" method="POST">
                {% csrf_token %}
                <h3>Вход</h3>
                {{ form_admin.as_p }}
                <button type="submit">Войти</button>
                {% if error_message %}
                    <p>{{ error_message }}</p>
                {% endif %}
            </form>
        `;
    });

    buttonUser.addEventListener("click", function() {
        form.innerHTML = `
            <form action="/login_users/" method="POST">
                {% csrf_token %}
                <h3>Вход</h3>
                {{ form.as_p }}
                <button type="submit">Войти</button>
                {% if error_message %}
                    <p>{{ error_message }}</p>
                {% endif %}
            </form>
        `;
    });
});