const addAccount = document.querySelectorAll('.add-account');
const WelcomeCreateAccountBtn = document.querySelector('#welcome-create-account-btn');

if (WelcomeCreateAccountBtn) {
    WelcomeCreateAccountBtn.addEventListener('click', () => {
        addAccount[1].focus()
    })
}

let data = {};
const ctxLine = document.getElementById('transactionLineChart');
fetch('../transactions/transactions_chart').then((response) => {
    if (response.ok) {
        return response.json()
    }
}).then((response) => {
    drawChart(response)
})
// .catch(error => console.error('Error:', error));

function drawChart(data) {
    let depositDates = data.deposit_data.map(entry => entry.date);
    let depositAmounts = data.deposit_data.map(entry => entry.amount);

    let transferDates = data.transfer_data.map(entry => entry.date);
    let transferAmounts = data.transfer_data.map(entry => entry.amount);

    let debitCardDates = data.debit_card_data.map(entry => entry.date);
    let debitCardAmounts = data.debit_card_data.map(entry => entry.amount);

    const longestArrayofDate = () => {
        return (depositDates.length > transferDates.length && depositDates.length > debitCardDates.length)
            ? depositDates
            : (transferDates.length > debitCardDates.length)
                ? transferDates : debitCardDates;
    }

    // Creating datasets for ApexCharts
    let datasets = [
        {
            name: 'Deposit',
            data: depositAmounts
        },
        {
            name: 'Transfer',
            data: transferAmounts
        },
        {
            name: 'Debit Card',
            data: debitCardAmounts
        }
    ];

    let options = {
        chart: {
            type: 'line',
            animations: {
                easing: 'easeInOutQuad'
            }
        },
        series: datasets,
        xaxis: {
            categories: longestArrayofDate()
        }
    };

    let myChart = new ApexCharts(document.getElementById('transactionChart'), options);

    myChart.render();
}