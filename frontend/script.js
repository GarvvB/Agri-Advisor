async function loadModelStats(){
    const res = await fetch("http://127.0.0.1:8000/model-stats");
    const stats = await res.json();

    new Chart(document.getElementById("modelChart"), {
        type:'bar',
        data:{
            labels:['Accuracy','Precision','Recall','F1 Score'],
            datasets:[{
                label:'Model Performance',
                data:[stats.accuracy, stats.precision, stats.recall, stats.f1]
            }]
        }
    });
}

window.onload = loadModelStats;