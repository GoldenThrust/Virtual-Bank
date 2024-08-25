import { postData } from "./main.js";

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
const lineChart = document.getElementById("transactionChart");
fetch("../transactions/transactions_chart")
  .then((response) => {
    if (response.ok) {
      return response.json();
    }
  })
  .then((response) => {
    drawChart(response);
  })
.catch((error) => console.error("Error:", error));

function drawChart(data) {
  const createSeriesData = (entries, hasUser = true) => {
    return entries.map(entry => ({
      x: new Date(entry.date), // Ensure entry.date is a valid date string
      y: entry.amount,
      user: hasUser ? entry.user : ''
    }));
  };

  const depositData = createSeriesData(data.deposit_data, false);
  const transferData = createSeriesData(data.transfer_data);
  const debitCardData = createSeriesData(data.debit_card_data);

  const datasets = [
    { name: "Deposit", data: depositData, color: '#FF0000' },
    { name: "Transfer", data: transferData, color: '#00FF00' },
    { name: "Debit Card", data: debitCardData, color: '#0000FF' },
  ].filter(dataset => dataset.data.length > 0);

  let options = {
    chart: {
      type: "area",
      animations: {
        easing: "easeInOutQuad",
      },
    },
    series: datasets,
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
            ${data.user ? '<li><strong>Payer: </strong>' + data.user + '</li>' : ''}
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
}




const quickTransfer = document.querySelector(".quick-transfer");
const quickDeposit = document.querySelector(".quick-deposit");
const quickTransferForm = document.querySelector(".quick-transfer-form");
const quickDepositForm = document.querySelector(".quick-deposit-form");
const quickTransferBtn = document.getElementById("quick-transfer-btn");
const quickDepositBtn = document.getElementById("quick-deposit-btn");

const quickAccountNumber = document.getElementById("quick-account_number");
const quickAmount = document.getElementById("quick-amount");

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

  const response = await postData("/transfers/create/", form, false, true);
  console.log(response);
});

quickDepositBtn.addEventListener("click", (e) => {
  const form = new FormData(e.target.closest('form'));

  postData("/deposits/create/", form, false, true);
});



const socket = new WebSocket('ws://localhost:8000/ws/transactions/');
socket.addEventListener("open", (e)=> {
  socket.send('{"hello": "world"}')
})

socket.addEventListener("message", (e)=>{
  const data = JSON.parse(e.data);

  console.log(data)
})