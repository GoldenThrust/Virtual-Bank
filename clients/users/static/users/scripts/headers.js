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
    const csrftoken = getCookie('csrftoken');
    const form = new FormData();

    form.append('name', account_name);
    form.append('account_type', accountType.value);
    form.append('currency', currency.value);

    fetch('/accounts/create-account/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken 
        },
        body: form
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.status === 'success') {
                window.location.reload();
            }
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log(document.cookie);
    return cookieValue;
}