const addAccount = document.querySelectorAll('.add-account');
const renameAccount = document.querySelectorAll('.rename-account');

if (addAccount.length) {
    addAccount.forEach(element => {
        element.addEventListener('change', () => {

            console.log('add account');
        });
    });
}