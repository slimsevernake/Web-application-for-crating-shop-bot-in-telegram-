window.addEventListener('load', function() {
    let inputs = document.querySelectorAll('.main-form__field');
    let restorePassword = document.querySelector('.main-form__restore-password');
    let login = document.querySelector('.main-form__field[name="username"]');
    let button = document.querySelector('#signup');
    
    changeInputView();

    for (let i = 0 ; i < inputs.length; i++) {
        inputs[i].addEventListener('focusout', changeInputView);
    }

    function changeInputView() {
        for (let i = 0 ; i < inputs.length; i++) {
            if(inputs[i].value) {
                inputs[i].classList.add('used');
            } else {
                inputs[i].classList.remove('used');
            }
        }
    }
    
    if(login.value) {
        restorePassword.classList.remove('main-form__restore-password--disable');
    } else {
        restorePassword.classList.add('main-form__restore-password--disable');
    }

    login.addEventListener('focusout', function(event) {
        if(event.target.value) {
            restorePassword.classList.remove('main-form__restore-password--disable');
        } else {
            restorePassword.classList.add('main-form__restore-password--disable');
        }
    });

    button.addEventListener('click', (event) => {
        event.target.classList.add('isActive');
    });
});