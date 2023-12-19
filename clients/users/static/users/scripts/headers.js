import { postData, con } from './main.js'

const accountID = document.getElementById('account-id')
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
                const form = new FormData();

                form.append('name', element.value);
                form.append('account_type', accountType.value);
                form.append('currency', currency.value);

                postData('/accounts/create-account/', form, true);
            }
            accountForm.classList.remove('d-none');
        });
    });

    renameAccount.forEach(element => {
        element.addEventListener('change', () => {
            const form = new FormData();
            form.append('id', accountID.innerText)
            form.append('name', element.value)
            postData('/accounts/rename-account/', form)
        });
    })
}

con()