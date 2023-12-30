var ctxPie = document.getElementById('transactionTypePieChart').getContext('2d')
var ctxLine = document.getElementById('transactionLineChart').getContext('2d')

var depositData = JSON.parse('{{ deposit_data|safe }}')
var transferData = JSON.parse('{{ transfer_data|safe }}')
var debitCardData = JSON.parse('{{ debit_card_data|safe }}')

// Transaction Type Pie Chart
var typePieChartData = {
  labels: ['Deposit', 'Transfer', 'Debit Card'],
  datasets: [
    {
      label: 'Transaction Type',
      backgroundColor: ['blue', 'green', 'red'],
      data: [depositData.length, transferData.length, debitCardData.length]
    }
  ]
}

var typePieChart = new Chart(ctxPie, {
  type: 'pie',
  data: typePieChartData,
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'right'
      },
      title: {
        display: true,
        text: 'Transaction Type Distribution',
        padding: 20
      }
    }
  }
})

var depositDates = depositData.map(function (entry) {
  return entry.date
})
var depositAmounts = depositData.map(function (entry) {
  return entry.amount
})

var transferDates = transferData.map(function (entry) {
  return entry.date
})
var transferAmounts = transferData.map(function (entry) {
  return entry.amount
})

var debitCardDates = debitCardData.map(function (entry) {
  return entry.date
})
var debitCardAmounts = debitCardData.map(function (entry) {
  return entry.amount
})

var myChart = new Chart(ctxLine, {
  type: 'line',
  data: {
    labels: depositDates,
    datasets: [
      {
        label: 'Deposit',
        data: depositAmounts,
        borderColor: 'rgba(75, 192, 192, 1)',
        fill: false
      },
      {
        label: 'Transfer',
        data: transferAmounts,
        borderColor: 'rgba(255, 99, 132, 1)',
        fill: false
      },
      {
        label: 'Debit Card',
        data: debitCardAmounts,
        borderColor: 'rgba(255, 205, 86, 1)',
        fill: false
      }
    ]
  },
  options: {
    animation: {
      easing: 'easeInOutQuad'
    }
  }
})