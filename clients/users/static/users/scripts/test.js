
const socket = new WebSocket('ws://localhost:8000/ws/socket/');
socket.addEventListener("open", (e) => {
  // socket.send('{"hello": "world"}')
})
let currentChartData = {
  deposit_data: [],
  transfer_data: [],
  debit_card_data: []
};


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
  console.log(data)
});
