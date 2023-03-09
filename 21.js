var ctx = document.getElementById('myChart').getContext('2d');
ctx.canvas.parentNode.style.height = 200;
ctx.canvas.parentNode.style.weight = 200;
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'pie',

    // The data for our dataset
    data: {
        labels: ["jeep", "audi", "DMW"],
        datasets: [{
                label: "Вес зверей",
                backgroundColor: ['lightgreen', 'lightblue', 'lightyellow'],
                borderColor: 'rgb(255, 99, 132)',
                data: [5, 45, 20],
            }

        ]

    },

    // Configuration options go here
    options: {
        maintainAspectRatio: false,
    }
});

function btnClick() {
    vl += 5;
    alert(vl);
}