// ================= LOAD CSV =================
async function loadData() {
  const res = await fetch("../data/processed/cleaned_train.csv");
  const txt = await res.text();
  const rows = txt.trim().split("\n").slice(1);

  return rows.map(r => {
    const c = r.split(",");
    return {
      id: c[0],
      vendor: c[1],
      pickup: new Date(c[2]),
      dropoff: new Date(c[3]),
      pas: Number(c[4]),
      pickup_lon: Number(c[5]),
      pickup_lat: Number(c[6]),
      dropoff_lon: Number(c[7]),
      dropoff_lat: Number(c[8]),
      store_flag: c[9],
      trip_duration: Number(c[10]),
      trip_distance_km: Number(c[11]),
      speed_kmph: Number(c[12]),
      pickup_hour: Number(c[13])
    };
  });
}

// ================= FILTERING =================
function filterData(data) {
  const minD = Number(document.getElementById("minDistance").value);
  const maxD = Number(document.getElementById("maxDistance").value);
  const peak = document.getElementById("peakHours").value;

  return data.filter(d => {
    const validDist = d.trip_distance_km >= minD && d.trip_distance_km <= maxD;
    const validSpeed = d.speed_kmph <= 60;

    let validPeak = true;
    if (peak === "8-10") validPeak = d.pickup_hour >= 8 && d.pickup_hour <= 10;
    else if (peak === "17-19") validPeak = d.pickup_hour >= 17 && d.pickup_hour <= 19;

    return validDist && validSpeed && validPeak;
  });
}

// ================= SUMMARY =================
function computeSummary(data) {
  const total = data.length;
  const avg = total>0 ? data.reduce((s,d)=>s+d.trip_duration,0)/total : 0;

  const counts={};
  data.forEach(d=>counts[d.pas]=(counts[d.pas]||0)+1);

  let common="--", max=0;
  for(const [k,v] of Object.entries(counts)) if(v>max){max=v; common=k;}

  return { totalTrips: total, avgDuration: avg, commonPassenger: common };
}

// ================= CHARTS =================
let tripsChart, durationChart;

function renderCharts(filteredData) {
  // Trips per date
  const tripsPerDay = {};
  filteredData.forEach(d=>{
    const day=d.pickup.toISOString().split("T")[0];
    tripsPerDay[day]=(tripsPerDay[day]||0)+1;
  });
  const dayLabels=Object.keys(tripsPerDay).sort();
  const dayValues=dayLabels.map(d=>tripsPerDay[d]);

  // Avg trip duration per hour
  const durationPerHour={}, countPerHour={};
  filteredData.forEach(d=>{
    const h=d.pickup_hour;
    durationPerHour[h]=(durationPerHour[h]||0)+d.trip_duration;
    countPerHour[h]=(countPerHour[h]||0)+1;
  });
  const hourLabels=[...Array(24).keys()];
  const hourValues=hourLabels.map(h=>countPerHour[h]?durationPerHour[h]/countPerHour[h]:0);

  // Update summary
  const { totalTrips, avgDuration, commonPassenger } = computeSummary(filteredData);
  document.getElementById("totalTrips").textContent = totalTrips;
  document.getElementById("avgDuration").textContent = avgDuration.toFixed(0)+" sec";
  document.getElementById("commonPassenger").textContent = commonPassenger;

  // Draw charts
  if(!tripsChart){
    tripsChart=new Chart(document.getElementById("tripsChart"),{
      type:"bar",
      data:{labels:dayLabels, datasets:[{label:"Trips per Day", data:dayValues, backgroundColor:"rgba(75,192,192,0.6)"}]},
      options:{responsive:true}
    });
  } else { tripsChart.data.labels=dayLabels; tripsChart.data.datasets[0].data=dayValues; tripsChart.update(); }

  if(!durationChart){
    durationChart=new Chart(document.getElementById("durationChart"),{
      type:"line",
      data:{labels:hourLabels, datasets:[{label:"Avg Trip Duration (sec)", data:hourValues, borderColor:"rgba(153,102,255,1)", fill:false, tension:0.2}]},
      options:{responsive:true}
    });
  } else { durationChart.data.datasets[0].data=hourValues; durationChart.update(); }
}

// ================= TOP 10 TRIPS =================
function renderTopTrips(filteredData) {
  const sortBy = document.getElementById("sortBy").value;
  const sorted = [...filteredData].sort((a,b)=>b[sortBy]-a[sortBy]).slice(0,10);

  const tbody = document.getElementById("topTripsBody");
  tbody.innerHTML = "";
  sorted.forEach(d=>{
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${d.id}</td><td>${d.trip_distance_km.toFixed(2)}</td><td>${d.speed_kmph.toFixed(2)}</td><td>${d.trip_duration}</td><td>${d.pickup_hour}</td>`;
    tbody.appendChild(tr);
  });
}

// ================= INIT =================
let globalData=[];

async function initDashboard() {
  globalData = await loadData();
  const filtered = filterData(globalData);
  renderCharts(filtered);
  renderTopTrips(filtered);
}

// ============== Event listeners ==============
document.getElementById("applyFilters").addEventListener("click",()=>{
  const filtered = filterData(globalData);
  renderCharts(filtered);
  renderTopTrips(filtered);
});

document.getElementById("resetFilters").addEventListener("click",()=>{
  document.getElementById("minDistance").value="2";
  document.getElementById("maxDistance").value="10";
  document.getElementById("peakHours").value="";
  const filtered = filterData(globalData);
  renderCharts(filtered);
  renderTopTrips(filtered);
});

document.getElementById("sortBy").addEventListener("change",()=>{
  const filtered = filterData(globalData);
  renderTopTrips(filtered);
});

// Start
initDashboard();
