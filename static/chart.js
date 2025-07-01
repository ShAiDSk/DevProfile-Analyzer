let chartInstance = null;

document.getElementById("form").addEventListener("submit", async function(e) {
  e.preventDefault();

  const formData = new FormData(this);
  const response = await fetch("/analyze", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  const resultDiv = document.getElementById("result");
  const chartContainer = document.getElementById("chart-container");
  resultDiv.innerHTML = "";
  chartContainer.classList.add("hidden");

  if (data.error) {
    resultDiv.innerHTML = `<p class="text-red-600 font-semibold text-center">${data.error}</p>`;
    return;
  }

  let html = `
    <div class="bg-gray-50 p-4 rounded-md shadow-sm border border-gray-200">
      <h3 class="text-xl font-bold text-indigo-600 mb-3">${data.platform} Profile - ${data.handle}</h3>
      <ul class="space-y-1 text-sm">
  `;

  for (let key in data) {
    if (key !== "platform" && key !== "handle") {
      html += `<li><strong class="capitalize">${key}:</strong> ${data[key]}</li>`;
    }
  }

  html += `</ul></div>`;
  resultDiv.innerHTML = html;

  // Chart
  const ratingData = Object.keys(data).filter(k => !["platform", "handle", "rank", "maxRank", "stars"].includes(k));
  const numericValues = ratingData.map(k => Number(data[k])).filter(v => !isNaN(v));

  if (numericValues.length > 0) {
    chartContainer.classList.remove("hidden");
    const ctx = document.getElementById("myChart").getContext("2d");

    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ratingData,
        datasets: [{
          label: 'Stat Value',
          data: numericValues,
          backgroundColor: 'rgba(99, 102, 241, 0.7)',
          borderRadius: 6,
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 100
            }
          }
        }
      }
    });
  }
});
