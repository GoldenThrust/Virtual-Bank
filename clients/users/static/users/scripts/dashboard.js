import { postData, createElement } from "./main.js";
const lineChart = document.getElementById("transactionChart");
const accountBalance = document.querySelector(".account-cards .account-balance > span")
const accountNumber = document.querySelector(".account-cards .account-number")
const income = document.querySelector("#income .deposit")
const spending = document.querySelector("#spending div:last-child");
const notificationCount = document.querySelector(".notification-count");
const unreadNotifications = document.querySelector('.unread-notifications');
const notification = document.querySelector('.unread-notifications > span');

const socket = new WebSocket('ws://localhost:8000/ws/transactions/');
socket.addEventListener("open", (e) => {
  socket.send('{"hello": "world"}')
})
let currentChartData = {
  deposit_data: [],
  transfer_data: [],
  debit_card_data: []
};

console.log(accountNumber.textContent)

socket.addEventListener("message", (e) => {
  const data = JSON.parse(e.data);

  if (data.event === "transaction") {
    if (data.content.type == "DEPOSIT") {
      updateChart({ deposit_data: [data.content] });
    } else if (data.content.type == "TRANSFER") {
      updateChart({ transfer_data: [data.content] });
    } else if (data.content.type == "DEBIT_CARD") {
      updateChart({ debit_card_data: [data.content] });
    }

    if (accountNumber.textContent == data.content.account_number) {
      if (data.content.payer) {
        if (data.content.payer === "You") {
          spending.textContent = `${spending.textContent[0]}${Number(spending.textContent.slice(1, -1)) + Number(data.content.amount)}`;
        } else {
          income.textContent = `${income.textContent[0]}${Number(income.textContent.slice(1, -1)) + Number(data.content.amount)}`;
        }
      }

      accountBalance.innerText = data.content.account_balance;
    }
  } else if (data.event === "notification") {
    notificationCount.classList.remove('d-none');
    unreadNotifications.classList.remove('d-none');
    notificationCount.textContent = Number(notificationCount.textContent) + 1;

    const unreadNotification = createElement(notification, 'div', { class: "unread-notification mb-2 pb-2" }, '', true);
    createElement(unreadNotification, 'div', { class: "unread_notification_id d-none" });
    createElement(unreadNotification, 'div', { class: "fw-lighter" }, data.content.notification);
    const div = createElement(unreadNotification, 'div');
    createElement(div, 'span', {}, data.content.notification_type);
    const text = document.createTextNode(' - ');
    div.appendChild(text);
    createElement(div, 'span', {}, 'now');
  }
});

const createSeriesData = (entries, hasUser = true) => {
  return entries.map(entry => ({
    x: new Date(entry.date),
    y: entry.amount,
    payer: hasUser ? entry.payer : '',
    payee: hasUser ? entry.payee : ''
  }));
};

function updateChart(newData) {
  if (newData.deposit_data) {
    currentChartData.deposit_data = [
      ...currentChartData.deposit_data,
      ...newData.deposit_data
    ];
  }
  if (newData.transfer_data) {
    currentChartData.transfer_data = [
      ...currentChartData.transfer_data,
      ...newData.transfer_data
    ];
  }
  if (newData.debit_card_data) {
    currentChartData.debit_card_data = [
      ...currentChartData.debit_card_data,
      ...newData.debit_card_data
    ];
  }

  const depositData = createSeriesData(currentChartData.deposit_data, false);
  const transferData = createSeriesData(currentChartData.transfer_data);
  const debitCardData = createSeriesData(currentChartData.debit_card_data);

  const datasets = [
    { name: "Deposit", data: depositData, color: '#FF0000' },
    { name: "Transfer", data: transferData, color: '#00FF00' },
    { name: "Debit Card", data: debitCardData, color: '#0000FF' },
  ].filter(dataset => dataset.data.length > 0);

  chart.updateSeries(datasets);
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
          <li><strong>Date: </strong> ${date}</li>
          <li><strong>Amount: </strong> ${data.y}</li>
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
chart.render();


const addAccount = document.querySelectorAll(".add-account");
const WelcomeCreateAccountBtn = document.querySelector(
  "#welcome-create-account-btn"
);

if (WelcomeCreateAccountBtn) {
  WelcomeCreateAccountBtn.addEventListener("click", () => {
    addAccount[1].focus();
  });
}

let data = {};
fetch("../transactions/transactions_chart")
  .then((response) => {
    if (response.ok) {
      return response.json();
    }
  })
  .then((response) => {
    updateChart(response);
  })
  .catch((error) => console.error("Error:", error));



const quickTransfer = document.querySelector(".quick-transfer");
const quickDeposit = document.querySelector(".quick-deposit");
const quickTransferForm = document.querySelector(".quick-transfer-form");
const quickDepositForm = document.querySelector(".quick-deposit-form");
const quickTransferBtn = document.getElementById("quick-transfer-btn");
const quickDepositBtn = document.getElementById("quick-deposit-btn");

// const quickAccountNumber = document.getElementById("quick-account_number");
// const quickAmount = document.getElementById("quick-amount");

quickDepositForm.querySelector('form').addEventListener("submit", (e) => {
  e.preventDefault()
});

quickTransferForm.querySelector('form').addEventListener("submit", (e) => {
  e.preventDefault()
});

quickTransfer.addEventListener("click", () => {
  quickTransferForm.classList.remove("d-none");
});

quickDeposit.addEventListener("click", () => {
  quickDepositForm.classList.remove("d-none");
});


quickTransferBtn.addEventListener("click", async (e) => {
  const form = new FormData(e.target.closest('form'));

  const response = await postData("/transfers/create/", form, true, true);
  quickTransferForm.classList.add("d-none");
});

quickDepositBtn.addEventListener("click", (e) => {
  const form = new FormData(e.target.closest('form'));

  postData("/deposits/create/", form, true, true);
  quickDepositForm.classList.add("d-none");
});