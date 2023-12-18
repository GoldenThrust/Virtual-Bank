const addAccount = document.querySelectorAll('.add-account');
const renameAccount = document.querySelectorAll('.rename-account');
const accountForm = document.querySelector('.account-form');
const accountType = document.querySelector('#account_type');
const currency = document.querySelector('#currency');
const CreateAccountBtn = document.querySelector('#create-account-btn');

if (addAccount.length) {
    addAccount.forEach(element => {
        element.addEventListener('change', () => {
            CreateAccountBtn.onclick = () => {
                createAccount(element.value);
            }
            accountForm.classList.remove('d-none');
        });
    });
}


function createAccount(account_name) {
    console.log( JSON.stringify({
        name: account_name,
        account_type: accountType.value,
        currency: currency.value
    }));
    // fetch('/api/accounts/', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({
    //         name: account_name,
    //         account_type: accountType.value,
    //         currency: currency.value
    //     })
    // })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.status === 'success') {
    //             window.location.reload();
    //         }
    // })
}