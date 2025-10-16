let currentTrips = [];
const totalTripsEl = document.getElementById('totalTrips');
const avgDistanceEl = document.getElementById('avgDistance');
const avgSpeedEl = document.getElementById('avgSpeed');

const distanceChartCtx = document.getElementById('distanceChart').getContext('2d');
const vendorChartCtx = document.getElementById('vendorChart').getContext('2d');
let distanceChart, vendorChart;

const topTripsBody = document.querySelector('#topTripsTable tbody');
const sortSelect = document.getElementById('sortBy');

// Fetch trips with optional filters
async function fetchTrips(filters = {}) {
    let url = '/api/trips?';
    if (filters.min_distance) url += `min_distance=${filters.min_distance}&`;
    if (filters.max_distance) url += `max_distance=${filters.max_distance}&`;

    try {
        const response = await fetch(url);
        const trips = await response.json();
        currentTrips = trips;
        renderSummary(trips);
        renderCharts(trips);
        renderTopTrips(trips, sortSelect.value);
    } catch (err) {
        console.error('Error fetching trips:', err);
    }
}

// Render summary stats
function renderSummary(trips) {
    if (!trips.length) {
        totalTripsEl.textContent = '--';
        avgDistanceEl.textContent = '-- km';
        avgSpeedEl.textContent = '-- km/h';
        return;
    }
    const total = trips.length;
    const avgDistance = (trips.reduce((sum,t)=>sum+t.trip_distance_km,0)/total).toFixed(2);
    const avgSpeed = (trips.reduce((sum,t)=>sum+t.speed_kmph,0)/total).toFixed(2);

    totalTripsEl.textContent = total;
    avgDistanceEl.textContent = `${avgDistance} km`;
    avgSpeedEl.textContent = `${avgSpeed} km/h`;
}

// Render charts
function renderCharts(trips) {
    // Distance distribution
    const distances = trips.map(t => t.trip_distance_km);
    const bins = [0,1,2,5,10,20,50];
    const labels = ['0-1','1-2','2-5','5-10','10-20','20-50'];
    const counts = labels.map((_,i)=>distances.filter(d=>d>=bins[i] && d< (bins[i+1] || Infinity)).length);

    if(distanceChart) distanceChart.destroy();
    distanceChart = new Chart(distanceChartCtx, {
        type: 'bar',
        data: { labels, datasets: [{ label: 'Trips per Distance (km)', data: counts, backgroundColor:'#007BFF' }] },
        options: { responsive:true }
    });

    // Vendor distribution
    const vendorCounts = {};
    trips.forEach(t => vendorCounts[t.vendor_id] = (vendorCounts[t.vendor_id] || 0) + 1);
    const vendorLabels = Object.keys(vendorCounts);
    const vendorData = Object.values(vendorCounts);

    if(vendorChart) vendorChart.destroy();
    vendorChart = new Chart(vendorChartCtx, {
        type: 'pie',
        data: { labels: vendorLabels, datasets:[{ label:'Trips by Vendor', data: vendorData, backgroundColor:['#007BFF','#28A745','#FFC107','#DC3545','#6F42C1'] }] },
        options: { responsive:true }
    });
}

// Render Top 10 trips
function renderTopTrips(trips, sortBy='trip_distance_km') {
    if(!trips.length){
        topTripsBody.innerHTML = `<tr><td colspan="4">No trips found.</td></tr>`;
        return;
    }

    const sortedTrips = [...trips].sort((a,b)=>b[sortBy]-a[sortBy]).slice(0,10);
    topTripsBody.innerHTML = sortedTrips.map(t=>`
        <tr>
            <td>${t.trip_distance_km.toFixed(2)}</td>
            <td>${t.speed_kmph.toFixed(2)}</td>
            <td>${t.pickup_hour}</td>
            <td>${t.pickup_dayofweek}</td>
        </tr>
    `).join('');
}

// Apply filters
document.getElementById('applyFilters').addEventListener('click', ()=>{
    const filters = {
        min_distance: document.getElementById('minDistance').value,
        max_distance: document.getElementById('maxDistance').value
    };
    fetchTrips(filters);
});

// Reset filters
document.getElementById('resetFilters').addEventListener('click', ()=>{
    document.getElementById('minDistance').value = 0;
    document.getElementById('maxDistance').value = 50;
    document.getElementById('peakHours').value = '';
    fetchTrips();
});

// Sort Top Trips
sortSelect.addEventListener('change', ()=>{
    renderTopTrips(currentTrips, sortSelect.value);
});

// Initial load
fetchTrips();
