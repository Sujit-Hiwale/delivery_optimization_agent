let map = L.map('map', {
    center: [40.7549, -73.9840],
    zoom: 14,
    dragging: false
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let orderMarkers = [];
let vehicleMarkers = [];
let warehouseMarkers = [];

let chart = new Chart(document.getElementById("chart"), {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Reward",
            data: []
        }]
    }
});

function drawState(data) {
    orderMarkers.forEach(m => map.removeLayer(m));
    vehicleMarkers.forEach(m => map.removeLayer(m));
    warehouseMarkers.forEach(m => map.removeLayer(m));

    orderMarkers = [];
    vehicleMarkers = [];
    warehouseMarkers = [];

    data.orders.forEach(o => {
        let m = L.circleMarker([o.lat, o.lon], {
            color: o.picked ? "green" : "red",
            radius: 5
        }).addTo(map);
        orderMarkers.push(m);
    });

    data.vehicles.forEach(v => {
        let icon = L.divIcon({
            html: '<div style="font-size:20px;">🚚</div>',
            className: "",
            iconSize: [50, 50],
            iconAnchor: [25, 25]
        });

        let m = L.marker([v.lat, v.lon], { icon }).addTo(map);
        vehicleMarkers.push(m);
    });

    data.warehouses.forEach(w => {
       let icon = L.divIcon({
            html: '<div style="font-size:50px;">🏭</div>',
            className: "",
            iconSize: [30, 30],
            iconAnchor: [25, 25]
        });

        let m = L.marker([w.lat, w.lon], { icon }).addTo(map);
        warehouseMarkers.push(m);
    });

    updateMetrics(data.metrics);
}

function updateMetrics(m) {
    if (!m) return;

    document.getElementById("reward").innerText = m.reward || 0;
    document.getElementById("score").innerText = (m.score || 0).toFixed(2);
    document.getElementById("delivery").innerText =
        (m.delivery_rate || 0).toFixed(2);

    const statsDiv = document.getElementById("vehicleStats");
    statsDiv.innerHTML = "";

    if (m.vehicle_stats) {
        for (let vid in m.vehicle_stats) {
            const div = document.createElement("div");
            div.innerText = `Vehicle ${vid}: ${m.vehicle_stats[vid]} deliveries`;
            statsDiv.appendChild(div);
        }
    }

    if (m.time !== undefined) {
        chart.data.labels.push(m.time);
        chart.data.datasets[0].data.push(m.reward || 0);
        chart.update();
    }
}

async function stepSimulation() {
    const res = await fetch("/step");
    const data = await res.json();

    drawState(data);

    setTimeout(stepSimulation, 500);
}

async function resetSimulation() {
    const vehicles = parseInt(document.getElementById("vehicles").value);

    await fetch("/reset", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ vehicles })
    });

    orderMarkers.forEach(m => map.removeLayer(m));
    vehicleMarkers.forEach(m => map.removeLayer(m));
    warehouseMarkers.forEach(m => map.removeLayer(m));

    orderMarkers = [];
    vehicleMarkers = [];
    warehouseMarkers = [];

    document.getElementById("reward").innerText = 0;
    document.getElementById("score").innerText = 0;
    document.getElementById("delivery").innerText = 0;

    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    chart.update();
}

map.on("click", async function(e) {
    await fetch("/add_order", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            lat: e.latlng.lat,
            lon: e.latlng.lng
        })
    });
});

stepSimulation();