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

  const response = await postData("/transfers/create/", form, false, true);
  quickTransferForm.classList.add("d-none");
});

quickDepositBtn.addEventListener("click", (e) => {
  const form = new FormData(e.target.closest('form'));

  postData("/deposits/create/", form, false, true);
  quickDepositForm.classList.add("d-none");
});