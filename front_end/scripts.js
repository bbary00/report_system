function myFunction(event) {
    event.stopPropagation();
    event.preventDefault();

    let signup_data = JSON.stringify({
            username : document.getElementById('username').value,
            email : document.getElementById('email').value,
            password : document.getElementById('password').value
        });
    let login_data = JSON.stringify({
            username : document.getElementById('username').value,
            password : document.getElementById('password').value
        });

    // fetch("http://127.0.0.1:8000/signup/",
    // {
    //     method: "POST",
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body : signup_data
    //     })
    // .then(function(res){ return res.json(); })
    // .then(function(data){ alert( JSON.stringify( data ) ) });

    // fetch("http://127.0.0.1:8000/login/",
    //     {
    //         method: "POST",
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body : login_data
    //     }).then(function(response) { return response.json(); })
    //     .then(function(data) {
    //         save_token_in_local_storage(data['data']['token']);
    //     });
    //
    // function save_token_in_local_storage(token) {
    //     window.localStorage.setItem('token', token);
    // }

    fetch("http://127.0.0.1:8000/api/user/",
        {
            method: "GET",
            headers: {
                'Authorization': window.localStorage.getItem('token')
            },
        }).then(function(response) { return response.json(); })
        .then(function(data) {
            console.log(data);
        });


     fetch("http://127.0.0.1:8000/api/load/",
        {
            method: "GET",
            headers: {
                'Authorization': window.localStorage.getItem('token')
            }
        }).then(response => response.blob())
        .then(blob => {
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = "Reports.xls";
            document.body.appendChild(a);
            a.click();
            a.remove();
        });
}