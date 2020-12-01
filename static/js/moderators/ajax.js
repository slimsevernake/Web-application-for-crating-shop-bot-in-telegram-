// Script to realize ajax requests with time-outs
$(document).ready(() => {
    // Click on link counter
    let clickCount = 0;
    let ajax_link = $("#ajax-reset-password");

    ajax_link.click(() => {
        // limit the click-through rate of the link
        timeOut(clickCount, ajax_link);
        clickCount++;

        let username_field = $("#id_username");
        // Check if username field has any value
        if (username_field.val().length !== 0) {
            $.ajax({
                type: 'POST',
                async: true,
                url: '/reset_password_ajax/',
                data: {username: username_field.val()},
                dataType: 'json',
                success: (data) => {
                    // Set success message if it does`t exist
                    let success_msg = data['success_msg']
                    if ($("#form").find('#success').length === 0)
                        $("#form").prepend(`<div class="alert alert-success text-center alert-dismissible fade show" role="alert" id="success">${success_msg}
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                          </button></div>`);
                },
                error: (data) => {
                    // Set/reset warning message
                    username_field.addClass("is-invalid");
                    if ($("#form").find('#error-username').length > 0)
                        $("#form").find('#error-username').text(data.responseJSON.error)
                    else
                        username_field.after(`<div id="error-username" class="invalid-feedback">${data.responseJSON.error}</div>`);
                }
            });
        }
        else {
            // Set/reset warning message cause of empty field
            let error_msg = "Введіть поштову скриньку";
            username_field.addClass("is-invalid");
            if ($("#form").find('#error-username').length > 0)
                $("#form").find('#error-username').text(error_msg);
            else
                username_field.after(`<div class="invalid-feedback" id="error-username">${error_msg}</div>`);
        }
    });
});

function timeOut(clickCount, element) {
    // if it`s first clock => do nothing
    if(clickCount === 0) {
        return;
    }

    // Enable/disable click possibility by removing "href" attr
    let location = disable(element)
    // Set timeouts
    if(clickCount === 1) {
        countdown(15);
    }
    else if(clickCount === 2) {
        countdown(30);
    }
    else {
        countdown(60);
    }

    function countdown(seconds) {
        let i = seconds;

        element.after(`<span id="timer" class="text-danger small">Сможете повторить через <span id="counter">${i}</span> секунд</span>`);

        let timerId = setInterval(() => {
            $('#counter').html(--i);
        }, 1000);

        setTimeout(() => { clearInterval(timerId) }, seconds * 1000);
        setTimeout(enable, seconds * 1000, element, location);
    }

    /*let timerId = setInterval(() => alert('tick'), 1000);
    setTimeout(() => { clearInterval(timerId); alert('stop'); }, 5000); */
}

function disable(element) {
    $('#ajax-reset-password').toggleClass('disabled')
    var location= element.attr("href");
    element.removeAttr('href');
    element.css("color", " #999999")
    return location;
}

function enable(element, location) {
    $('#ajax-reset-password').toggleClass('disabled')
    element.attr("href", location);
    element.css("color", " #007bff")
    // remove timer hint
    $("#timer").remove();
}