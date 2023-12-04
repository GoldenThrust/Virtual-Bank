const signin = document.querySelectorAll('.signin');
const signup = document.querySelectorAll('.signup');
const host = 'http://' + window.location.hostname + ':8000';

signin.forEach((button) => {
    button.onclick = () => {
        window.location = host + '/users/login/';
    }
})

signup.forEach((button) => {
    button.onclick = () => {
        window.location = host + '/users/register/';
    }
})