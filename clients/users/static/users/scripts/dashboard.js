const addAccount = document.querySelectorAll('.add-account');
const WelcomeCreateAccountBtn = document.querySelector('#welcome-create-account-btn');

WelcomeCreateAccountBtn.addEventListener('click', () => {
    addAccount[1].focus()
})