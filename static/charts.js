

$('.Bar_Chart').each(function(index,element){
    var endpoint = element.attributes['url-endpoint'].value;
    var final_data = [];
    var labels = [];
    var title = [];

    $.ajax({
        method: "GET",
        url: endpoint,
        success: function(data){
            labels = data.labels
            final_data = data.values
            title = data.question
            var ctx = element.getContext("2d");
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'n° de respuestas',
                        backgroundColor: "#26B99A",
                        data: final_data
                    }]
                },

                options: {
                    title: {
                        display: true,
                        text: title
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        },
        error: function(error_data){
            console.log('error')
            console.log(error_data)
        }
    });
});

$('.Pie_Chart').each(function(index,element){
    var endpoint = element.attributes['url-endpoint'].value;
    var final_data = [];
    var labels = [];
    var title = [];

    $.ajax({
        method: "GET",
        url: endpoint,
        success: function(data){
            labels = data.labels
            final_data = data.values
            title = data.question
            var ctx = element.getContext("2d");
            var data = {
                labels: labels,
                datasets: [{
                    data: final_data,
                    backgroundColor: [
                        "#455C73",
                        "#9B59B6",
                        "#BDC3C7",
                        "#26B99A",
                        "#3498DB"
                    ],
                    label: 'My dataset' // for legend
                }]
            };
            new Chart(ctx, {
                data: data,
                type: 'doughnut',
                options: {
                    title: {
                        display: true,
                        text: title
                    },
                    legend: true
                }
            });
        },
        error: function(error_data){
            console.log('error')
            console.log(error_data)
        }
    });
});