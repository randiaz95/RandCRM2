$(document).ready(()=> {
    // Constructor code
    let domain = "http://localhost:8000";
    let state = {};

    $("#authenticated-navbar").hide();
    $("#signup").hide();
    $("#faq").hide();
    $("#confirm").hide();
    $("#engine").hide();
    $("#login-button").css("color", "#FFF");
    // Constructor endcode

    // Navbar code
    $("#login-button").click(()=> {
        $("#signup").hide();
        $("#signup-button").css("color", "#818181");

        $("#faq").hide();
        $("#faq-button").css("color", "#818181");

        $("#login").show();
        $("#login-button").css("color", "#FFF");
    });

    $("#signup-button").click(()=> {
        $("#login").hide();
        $("#login-button").css("color", "#818181");

        $("#faq").hide();
        $("#faq-button").css("color", "#818181");

        $("#signup").show();
        $("#signup-button").css("color", "#FFF");
    });

    $("#faq-button").click(()=> {
        $("#signup").hide();
        $("#signup-button").css("color", "#818181");

        $("#login").hide();
        $("#login-button").css("color", "#818181");

        $("#faq").show();
        $("#faq-button").css("color", "#FFF");
    });
    // Navbar endcode


    // Login code
    $("#login-submit").click(()=> {
        fetch(`${domain}/login`, {
            method: "POST",
            headers: { "content-type": "application/json"},
            body: JSON.stringify({
                email: $("#login-email").val(),
                password: $("#login-password").val(),
            }),
        })
        .then((response)=> response.json())
        .then((data)=> {
            if (data.status=="success") {
                state.id = data.id;
                $("#anonymous-navbar").hide();
                $("#authenticated-navbar").show();
                $("#login").hide();
                $("#engine").show();
            } else {
                $("#login-error").html(data.message);
            }
        }).catch((error)=> {
            console.log(error);
        });
    });
    // Login endcode

    // Signup code
    $("#signup-submit").click(()=> {
        console.log($("#signup-password1").val());
        console.log($("#signup-password2").val());

        if ($("#signup-password1").val() != $("#signup-password2").val()) {
            $("#signup-error").html("Passwords do not match.");
            return;
        }

        fetch(`${domain}/signup`, {
            method: "POST",
            headers: { "content-type": "application/json"},
            body: JSON.stringify({
                email: $("#signup-email").val(),
                password: $("#signup-password1").val(),
            }),
        })
        .then((response)=> response.json())
        .then((data)=> {
            if (data.status=="success") {
                state.id = data.id;
                $("#signup").hide();
                $("#confirm").show();
            } else {
                $("#login-error").html(data.message);
            }
        }).catch((error)=> {
            console.log(error);
        });

    });
    // Signup endcode

    // Signup code
    $("#confirm-submit").click(()=> {
        fetch(`${domain}/confirm`, {
            method: "POST",
            headers: { "content-type": "application/json"},
            body: JSON.stringify({
                id: state.id,
                code: $("#code").val(),
            }),
        })
        .then((response)=> response.json())
        .then((data)=> {
            if (data.status=="success") {
                $("#confirm").hide();
                $("#anonymous-navbar").hide();
                $("#authenticate-navbar").show();
                $("#engine").show();
                $("#engine").html(state.id + data.id);
            } else {
                $("#confirm-error").html(data.message);
            }
        }).catch((error)=> {
            console.log(error);
        });
    });
    // Signup endcode

});
