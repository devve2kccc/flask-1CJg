document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/chart-data")
    .then((response) => response.json())
    .then((data) => {
      var ctx = document.getElementById("bankChart").getContext("2d");
      var myChart = new Chart(ctx, {
        type: "doughnut",
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          borderWidth: 0,
        },
      });
    })
    .catch((error) => console.error("Error:", error));
});

document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/total-money")
    .then((response) => response.json())
    .then((data) => {
      // Extract the totalMoney value from the response data
      const totalMoney = data.totalMoney;

      // Prepare the data for the chart (same as before)
      const chartData = {
        labels: ["Cash", "Banks"],
        datasets: [
          {
            data: [data.cash, data.bankTotal],
            backgroundColor: ["#FF6384", "#36A2EB"],
          },
        ],
      };

      // Configure the chart (same as before)
      const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        borderWidth: 0,
      };

      // Get the chart canvas element (same as before)
      const ctx = document.getElementById("totalMoneyChart").getContext("2d");

      // Create the Doughnut chart (same as before)
      const myChart = new Chart(ctx, {
        type: "doughnut",
        data: chartData,
        options: chartOptions,
      });
    })
    .catch((error) => console.error("Error:", error));
});
