import { postData } from "./main.js";

const accountID = document.getElementById("account-id");
const addAccount = document.querySelectorAll(".add-account");
const renameAccount = document.querySelectorAll(".rename-account");
const accountForm = document.querySelector(".account-form");
const accountType = document.querySelector("#account_type");
const currency = document.querySelector("#currency");
const CreateAccountBtn = document.querySelector("#create-account-btn");
const unreadNotification = document.querySelector(".unread-notifications > span");
const unreadNotifications = document.querySelector(".unread-notifications");
const notificationCount = document.querySelector(".notification-count");
const CancelOverlayBtn = document.querySelectorAll(".cancel-overlay-btn");

CancelOverlayBtn.forEach((elements) => {
  elements.addEventListener("click", () => {
    elements.parentNode.parentNode.parentNode.parentElement.classList.add(
      "d-none"
    );
  });
});

if (addAccount.length) {
  addAccount.forEach((element) => {
    element.addEventListener("change", () => {
      CreateAccountBtn.onclick = () => {
        const form = new FormData();

        form.append("name", element.value);
        form.append("account_type", accountType.value);
        form.append("currency", currency.value);

        postData("/accounts/create/", form, true, true);
      };
      accountForm.classList.remove("d-none");
    });
  });

  renameAccount.forEach((element) => {
    element.addEventListener("change", () => {
      const form = new FormData();
      form.append("id", accountID.innerText);
      form.append("name", element.value);
      postData("/accounts/rename-account/", form);
    });
  });
}

if (notificationCount) {
  unreadNotification.addEventListener("click", (e) => {
    const element = e.target.closest(".unread-notification");
    element.addEventListener("click", () => {
      const id = element
        .querySelector(".unread_notification_id")
        .innerText.trim();
      const form = new FormData();
      form.append("id", id);
      postData("/notifications/read-notification/", form);
      element.style.display = "none";
      notificationCount.innerText = Number(notificationCount.innerText) - 1;
      if (!Number(notificationCount.innerText)) {
        unreadNotifications.classList.add("d-none");
        notificationCount.classList.add("d-none");
      }
    });
  });
}
