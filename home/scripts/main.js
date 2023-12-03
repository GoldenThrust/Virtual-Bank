const signin = document.getElementById('signin');
const signup = document.getElementById('signup');
const host = 'http://' + window.location.hostname + ':8000';

signin.onclick = () => {
    window.location = host + '/users/login/';
}
signup.onclick = () => {
    window.location = host + '/users/register/';
}