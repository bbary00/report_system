function hide_all() {
    document.getElementById("signup_form").style.display = "none";
    document.getElementById("login_form").style.display = "none";
    document.getElementById("templates").style.display= "none";
    document.getElementById("template_items").innerHTML= "";
    document.getElementById("user_page").style.display = "none";
    document.getElementById("create_report").style.display = "none";
    document.getElementById("create_template").style.display = "none";
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
    .then(function(data){
        let response = data["data"];
        if ('error_msg' in response){
            alert(response["error_msg"]);
        }
        else {
            alert("Account created!");
            window.location.reload();
        }
    });
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
            let response = data["data"];
            if ('error_msg' in response){
                alert(response["error_msg"]);
            }
            else {
                save_token_in_local_storage(response['token']);
            }
        });

    function save_token_in_local_storage(token) {
        window.localStorage.setItem('token', token);
        alert("You logger in!");
        window.location.reload();
    }
}


function download_reports() {

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


function append_templates(data) {
        for (let template of data) {
            let div = document.createElement('div');
            div.setAttribute("id", "template_item");
            let hr = document.createElement('hr');
            div.innerHTML = `<h3 style="display:inline-block">Name:&nbsp;</h3>${template["label"]}<br>` +
                            `<h4 style="display:inline-block">Description:&nbsp;</h4>${template["description"]}<br>` +
                            `<h4 style="display:inline-block">Inputs:&nbsp;</h4>${template["inputs"].join(', ')}<br>`;
            // div.setAttribute('onmouseover', 'this.bgColor="grey"');
            div.appendChild(hr);
            div.addEventListener('click', function(){make_report(template);});
            document.getElementById("template_items").appendChild(div)
        }
}

function append_reports(data) {
        for (let report of data) {
            let div = document.createElement('div');
            div.setAttribute("id", "report_item");
            div.innerHTML = `<h3 style="display:inline-block">Name:&nbsp;</h3>${report["template"]["label"]}<br>` +
                            `<h4 style="display:inline-block">Description:&nbsp;</h4>${report["template"]["description"]}<br>`;
            for (let i = 0; i < report["template"]["inputs"].length; i++){
                div.innerHTML +=
                    `<h4 style="display:inline-block">${report["template"]["inputs"][i]}:&nbsp;</h4>` +
                    `<p style="display:inline-block">&nbsp;${report["answers"][i]}</p><br>`;

            }
            div.innerHTML += `<i>Created&nbsp;by:&nbsp;${report["user"]["username"]}&nbsp;at&nbsp;${report["date"]}</i><hr>`;
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
        input.addEventListener('click', function(event){
            event.stopPropagation();
            event.preventDefault();
            let formData = new FormData(document.querySelector('#report_create_item'));
            let obj = {};
            let answers = [];
            for (let k_v of formData.entries()){
                if (k_v[1] === ""){
                    alert("Please fill all fields!");
                    break;
                }
                answers.push(k_v[1]);
            }
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
                }).then(response => response.json())
                .then(data => {
                    if(!('data' in data)){
                        alert("Report created!");
                        window.location.reload();
                    }
                });
        });
        form.appendChild(input);
        document.getElementById("create_report").appendChild(form);
        document.getElementById("create_report").style.display = "block";
}

function make_template_form() {
    hide_all();
    document.getElementById('create_template').style.display = "block";
}

function create_template(event) {
    event.stopPropagation();
    event.preventDefault();
    let formData = new FormData(document.querySelector('#create_template'));
    let obj = {};
    for (let k_v of formData.entries()){
        if (k_v[1] === ""){
            alert("Please fill all fields!");
            break;
        }
        obj[k_v[0]] = k_v[1];
    }
    obj["inputs"] = obj["inputs"].split(" ");
    let json = JSON.stringify(obj);
    console.log(json);
    fetch("http://127.0.0.1:8000/api/templates/",
    {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': window.localStorage.getItem('token')
            },
            body: json
    }) .then(function(res){ return res })
    .then(function(data){
        if (data.status === 403) {
            alert("You don't have permission to perform this action!");
            window.location.reload();
        }
        else {
            data = data.json();
            if ('data' in data){
            alert(data["data"]["error"]);
            }
            else if ("detail" in data){
                alert(data["detail"]);
            }
            else {
                alert("Template created!");
                window.location.reload();
            }
        }
    });
}

