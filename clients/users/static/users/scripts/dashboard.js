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
  let depositDates = data.deposit_data.map((entry) => entry.date);
  let depositAmounts = data.deposit_data.map((entry) => entry.amount);

  let transferDates = data.transfer_data.map((entry) => entry.date);
  let transferAmounts = data.transfer_data.map((entry) => entry.amount);

  let debitCardDates = data.debit_card_data.map((entry) => entry.date);
  let debitCardAmounts = data.debit_card_data.map((entry) => entry.amount);

  const longestArrayofDate = () => {
    return depositDates.length > transferDates.length &&
      depositDates.length > debitCardDates.length
      ? depositDates
      : transferDates.length > debitCardDates.length
      ? transferDates
      : debitCardDates;
  };

  // Creating datasets for ApexCharts
  let datasets = [
    {
      name: "Deposit",
      data: depositAmounts,
    },
    {
      name: "Transfer",
      data: transferAmounts,
    },
    {
      name: "Debit Card",
      data: debitCardAmounts,
    },
  ];

  let options = {
    chart: {
      type: "line",
      animations: {
        easing: "easeInOutQuad",
      },
    },
    series: datasets,
    xaxis: {
      categories: longestArrayofDate(),
    },
    stroke: {
      // curve: 'smooth',
    },
    colors: ["#F44336", "#E91E63", "#c1311e"],
    fill: {
      type: "gradient",
      gradient: {
        shade: "dark",
        type: "horizontal",
        shadeIntensity: 0.5,
        gradientToColors: undefined,
        inverseColors: true,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 50, 100],
        colorStops: [],
      },
    },
    chart: {
      dropShadow: {
        enabled: true,
        enabledOnSeries: false,
        top: 1,
        left: 1,
        blur: 3,
        color: "#000",
        opacity: 0.35,
      },
    },
  };

  let chart = new ApexCharts(lineChart, options);
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

quickTransfer.addEventListener("click", () => {
  quickTransferForm.classList.remove("d-none");
});

quickDeposit.addEventListener("click", () => {
  quickDepositForm.classList.remove("d-none");
});


quickTransferBtn.addEventListener("click", (e) => {
    const acctNo = quickAccountNumber.value
    const amount = quickAmount.value
    if (amount && acctNo) {
        const form = new FormData();

        form.append("name", acctNo);
        form.append("account_type", amount);
        postData("/transactions/transfer/", form, true);
    }
});

quickDepositBtn.addEventListener("click", (e) => {
    const amount = e.target.parentNode.parentElement.children[1].children[1].value
    if (amount) {
        const form = new FormData();
        form.append("account_type", amount);
        postData("/transactions/deposit/", form, true);
    }
});