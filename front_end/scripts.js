function signup(event) {
    event.stopPropagation();
    event.preventDefault();

    let signup_data = JSON.stringify({
            username : document.getElementById('sign_username').value,
            email : document.getElementById('sign_email').value,
            password : document.getElementById('sign_password').value
        });


    fetch("http://127.0.0.1:8000/signup/",
    {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body : signup_data
        })
    .then(function(res){ return res.json(); })
    .then(function(data){ alert( JSON.stringify( data ) ) });
}

function logout() {
    window.localStorage.removeItem("token");
    alert("Bye-bye");
    hide_all();
}


function login(event) {
    event.stopPropagation();
    event.preventDefault();

    let login_data = JSON.stringify({
            username : document.getElementById('login_username').value,
            password : document.getElementById('login_password').value
        });

    fetch("http://127.0.0.1:8000/login/",
        {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body : login_data
        }).then(function(response) { return response.json(); })
        .then(function(data) {
            save_token_in_local_storage(data['data']['token']);
        });

    function save_token_in_local_storage(token) {
        window.localStorage.setItem('token', token);
        alert("You logger in!");
        hide_all();
    }
}


function show_user() {
    hide_all();
    document.getElementById("user_page").style.display = "inline";
    fetch("http://127.0.0.1:8000/api/user/",
        {
            method: "GET",
            headers: {
                'Authorization': window.localStorage.getItem('token')
            },
        }).then(function(response) { return response.json(); })
        .then(function(data) {
            display_info(data);
        });

    function display_info(data) {
        document.getElementById("user_username").innerHTML = data['username'];
        document.getElementById("user_email").innerHTML = data['email'];
    }
}


function load_reports() {

   fetch("http://127.0.0.1:8000/api/load/",
        {
            method: "GET",
            headers: {
                'Authorization': window.localStorage.getItem('token')
            }
        }).then(response => [response.status, response.blob()])
        .then(res => {
            if (res[0] !== 200)
                alert("You don't have a permission to load reports!");
            else {
                res[1].then(blob => {
                    let url = window.URL.createObjectURL(blob);
                    let a = document.createElement('a');
                    a.href = url;
                    a.download = "Reports.xls";
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                });
            }
        });
}

function hide_all() {
    document.getElementById("signup_form").style.display = "none";
    document.getElementById("login_form").style.display = "none";
    document.getElementById("templates").style.display = "none";
    document.getElementById("templates").innerHTML = "";
    document.getElementById("user_page").style.display = "none";
    document.getElementById("create_report").style.display = "none";
    document.getElementById("reports").style.display = "none";
    document.getElementById("report_items").innerHTML = "";
    if (document.contains(document.getElementById("report_create_item"))) {
        document.getElementById("report_create_item").remove();
    }
}

function show_signup() {
    hide_all();
    document.getElementById("signup_form").style.display = "block";
}

function show_login() {
    hide_all();
    document.getElementById("login_form").style.display = "block";
}

function show_reports(username="") {
    hide_all();
    document.getElementById("reports").style.display = "block";
    fetch(`http://127.0.0.1:8000/api/reports/?user=${username}`,
        {
            method: "GET",
            headers: {
                'Authorization': window.localStorage.getItem('token')
            },
        }).then(function(response) { return response.json(); })
        .then(function(data) {
            append_reports(data);
        });

}

function show_templates() {
    hide_all();
    document.getElementById("templates").style.display = "block";
    fetch("http://127.0.0.1:8000/api/templates/",
        {
            method: "GET",
            headers: {
                'Authorization': window.localStorage.getItem('token')
            },
        }).then(function(response) { return response.json(); })
        .then(function(data) {
            append_templates(data);
        });

}

function append_templates(data) {
        for (let template of data) {
            let div = document.createElement('div');
            let hr = document.createElement('hr');
            div.innerHTML = `<h3>Name: </h3>${template["label"]} ` +
                            `<h4>Description: </h4>${template["description"]}` +
                            `<h4>Inputs: </h4>${template["inputs"].join(', ')}`;
            div.setAttribute('onmouseover', 'this.bgColor="grey"');
            div.appendChild(hr);
            div.addEventListener('click', function(){make_report(template);});
            document.getElementById("templates").appendChild(div)
        }
}

function append_reports(data) {
        for (let report of data) {
            let div = document.createElement('div');
            div.setAttribute("id", "report_item");
            let hr = document.createElement('hr');
            let user = document.createElement('i');
            div.innerHTML = `<h3>Name: </h3>${report["template"]["label"]} ` +
                            `<h4>Description: </h4>${report["template"]["description"]}`;
            for (let i = 0; i < report["template"]["inputs"].length; i++){
                let h4 = document.createElement('h4');
                let p = document.createElement('p');
                h4.innerHTML = report["template"]["inputs"][i];
                p.innerHTML = report["answers"][i];
                user.innerText = `Created by: ${report["user"]["username"]} at ${report["date"]}`;
                div.appendChild(h4);
                div.appendChild(p);
                div.appendChild(user);
                div.appendChild(hr);
            }
            document.getElementById("report_items").appendChild(div);
        }
}

function make_report(template) {
        hide_all();
        let form = document.createElement('form');
        form.setAttribute("id", "report_create_item");
        document.getElementById("template_name").innerHTML = template['label'];
        document.getElementById("template_description").innerHTML = template['description'];
        let input = document.createElement('input');
        for (let i = 0; i < template["inputs"].length; i++){
            let p = document.createElement('p');
            let input = document.createElement('input');
            p.innerHTML = template["inputs"][i];
            input.setAttribute("type", "text");
            input.setAttribute("name", template["inputs"][i]);
            form.appendChild(p);
            form.appendChild(input);
        }
        input.setAttribute("type", "submit");
        input.addEventListener('click', function(){
            let formData = new FormData(document.querySelector('#report_create_item'));
            let obj = {};
            let answers = [];
            formData.forEach((value, key) => {answers.push(value)});
            obj["template"] = {"id": template['id']};
            obj["answers"] = answers;
            let json = JSON.stringify(obj);
            fetch("http://127.0.0.1:8000/api/reports/",
                {
                        method: "POST",
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': window.localStorage.getItem('token')
                        },
                        body : json
                }).then(response => alert(response.json()));
        });
        form.appendChild(input);
        document.getElementById("create_report").appendChild(form);
        document.getElementById("create_report").style.display = "block";
}

function post_report(form) {

}

