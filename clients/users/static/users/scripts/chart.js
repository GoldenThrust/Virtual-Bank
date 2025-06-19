import { createElement, getData, currency_mapping } from "./main.js";
const lineChart = document.getElementById("transactionChart");
const accountBalance = document.querySelector(".account-cards .account-balance > span")
const accountNumber = document.querySelector(".account-cards .account-number").textContent
const income = document.querySelector("#income .deposit")
const spending = document.querySelector("#spending div:last-child");
const notificationCount = document.querySelector(".notification-count");
const unreadNotifications = document.querySelector('.unread-notifications');
const notification = document.querySelector('.unread-notifications > span');
const root = document.documentElement;
// Convert API_BASE_URL from http to ws for WebSocket connection
const wsUrl = window.WEBSOCKET_URL ? 
    window.WEBSOCKET_URL + '/ws/socket/' : 
    'ws://localhost:8030/ws/socket/';

const socket = new WebSocket(wsUrl);



socket.addEventListener("open", (e) => {
    root.style.setProperty('--primary', '#5E3FBE');
})

socket.addEventListener("close", (e) => {
    // root.style.setProperty('--primary', 'red');
    // root.style.setProperty('--secondary', 'red');
})

let doubleSignal = false;

socket.addEventListener("message", (e) => {
    const data = JSON.parse(e.data);

    
    if (data.event === "transaction") {
        if (data.content.payee.user.id == data.content.payer.user.id) {
            doubleSignal = !doubleSignal;
        }

        if (!doubleSignal) {
            updateChart([data.content])
            if (accountNumber === data.content.payee.number) {
                const newIncome = Number(income.textContent.slice(1)) + Number(data.content.amount_received);
                income.textContent = `${income.textContent[0]}${newIncome.toFixed(2)}`;
                accountBalance.textContent = Number(data.content.payee.balance).toFixed(2);
            } else if (accountNumber === data.content.payer.number) {
                const newSpending = Number(spending.textContent.slice(1)) + Number(data.content.amount_sent);
                spending.textContent = `${spending.textContent[0]}${newSpending.toFixed(2)}`;
                accountBalance.textContent = Number(data.content.payer.balance).toFixed(2);   
            }
        }
    } else if (data.event === "notification") {
        notificationCount.classList.remove('d-none');
        unreadNotifications.classList.remove('d-none');
        notificationCount.textContent = Number(notificationCount.textContent) + 1;

        const unreadNotification = createElement(notification, 'div', { class: "unread-notification mb-2 pb-2" }, '', true);
        createElement(unreadNotification, 'div', { class: "unread_notification_id d-none" });
        createElement(unreadNotification, 'div', { class: "fw-lighter" }, data.content.content);
        const div = createElement(unreadNotification, 'div');
        createElement(div, 'span', {}, data.content.notification_type);
        const text = document.createTextNode(' - ');
        div.appendChild(text);
        createElement(div, 'span', {}, 'now');
    }
});

let currentChartData = {};

function createSeriesData(entries) {
    const data = {
        deposit: [],
        transfer: [],
        debit_card: []
    };

    entries.forEach(entry => {
        let amount = 0;
        let currency = currency_mapping['NGN']
        let payer = `${entry.payer.user.first_name} ${entry.payer.user.last_name}`
        let payee = `${entry.payee.user.first_name} ${entry.payee.user.last_name}`
        let date = new Date(entry.date);

        if (accountNumber === entry.payee.number) {
            payee = "You"
            amount = entry.amount_received
            currency = entry.currency_received ? currency_mapping[entry.currency_received] : currency_mapping['NGN']
  
        } else if (accountNumber === entry.payer.number){
            payer = "You"
            amount = entry.amount_sent
            currency = entry.currency_sent ? currency_mapping[entry.currency_sent] : currency_mapping['NGN']   
        } else {
            return;
        }


        if (entry.transaction_type === "TRANSFER") {
            data.transfer.push({
                x: date,
                y: amount,
                currency,
                transaction: "TRANSFER",
                payer,
                payee,
            });
        } else if (entry.transaction_type === "DEBIT_CARD") {
            data.debit_card.push({
                x: date,
                y: amount,
                transaction: "DEBIT_CARD",
                currency,
                payer,
                payee,
            });
        } else {
            data.deposit.push({
                x: new Date(entry.date),
                y: amount,
                transaction: "DEPOSIT",
                currency,
                payer: '',
                payee: '',
            });
        }
    });

    return data;
};

async function updateChart(newData) {
    currentChartData = {
        ...newData,
        ...currentChartData,
    };


    const data = createSeriesData(Object.values(currentChartData));

    const datasets = [
        { name: "Deposit", data: data.deposit, color: '#FF0000' },
        { name: "Transfer", data: data.transfer, color: '#00FF00' },
        { name: "Debit Card", data: data.debit_card, color: '#0000FF' },
    ].filter(dataset => dataset.data.length > 0);

    try {
        chart.updateSeries(datasets);
    } catch (e) {
        console.error(e);
    }
}



let options = {
    chart: {
        type: "area",
        animations: {
            easing: "easeInOutQuad",
        },
    },
    series: [],
    stroke: {
        curve: 'smooth',
    },
    tooltip: {
        custom: function ({ series, seriesIndex, dataPointIndex, w }) {
            const data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
            const date = new Date(data.x).toLocaleDateString();

            return `
      <div class="card p-2">
        <ul class="list-unstyled mb-0">
          <li><strong>Transaction: </strong> ${data.transaction}</li>
          <li><strong>Date: </strong> ${date}</li>
          <li><strong>Amount: </strong> ${data.currency}${data.y}</li>
          ${data.payer ? `<li><strong>Payer: </strong>${data.payer}</li>` : ''}
          ${data.payee ? `<li><strong>Payee: </strong>${data.payee}</li>` : ''}
        </ul>
      </div>
      `;
        },
    },
    xaxis: {
        type: 'datetime',
    },
    colors: ["#FF0000", "#00FF00", "#0000FF"],
};

const chart = new ApexCharts(lineChart, options);
try {
    chart.render();
} catch (e) {
    console.error(e);
}

const data = await getData(`/transactions/?account_number=${accountNumber}`, true)
updateChart(data);