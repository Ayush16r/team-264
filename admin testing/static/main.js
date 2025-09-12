const evtSource = new EventSource('/stream');

// ---------- Helpers ----------
function escapeHtml(s) {
  return (s || '').replace(/[&<>"']/g, function(m){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m];
  });
}

// ---------- Render ----------
function renderStats(data) {
  document.getElementById('queueLength').innerText = data.queue_length;
  document.getElementById('estWait').innerText = `${data.estimated_wait_min} min`;
  document.getElementById('completed').innerText = data.completed_today;
  renderCurrentlyServing(data.in_progress);
  renderLiveQueue(data.waiting, data.service_time_map);
}

function renderCurrentlyServing(item) {
  const container = document.getElementById('currentCard');
  const completeWrap = document.getElementById('completeBtnContainer');
  container.innerHTML = '';
  completeWrap.innerHTML = '';

  if (!item) {
    container.innerHTML = `<div class="muted">No one is being served right now</div>`;
    return;
  }

  container.innerHTML = `<div><strong>${escapeHtml(item.name)}</strong>
    <div class="muted">${escapeHtml(item.department)} (Booking: ${escapeHtml(item.booking_id)})</div></div>`;

  const btn = document.createElement('button');
  btn.type = "button";
  btn.className = 'btn-complete';
  btn.innerText = 'Complete Visit';

  btn.addEventListener('click', async () => {
    try {
      const resp = await fetch('/api/complete/' + encodeURIComponent(item.id), { method: 'POST' });
      const data = await resp.json();
      if (resp.ok && data.stats) {
        renderStats(data.stats); // ✅ instant refresh
      } else {
        fetch('/api/stats').then(r => r.json()).then(renderStats);
      }
    } catch (err) {
      console.error("Complete error:", err);
      fetch('/api/stats').then(r => r.json()).then(renderStats);
    }
  });

  completeWrap.appendChild(btn);
}

function renderLiveQueue(list, service_map) {
  const el = document.getElementById('liveQueue');
  el.innerHTML = '';
  if (!list || list.length === 0) {
    el.innerHTML = `<div class="muted">No patients in queue</div>`;
    return;
  }
  list.forEach((p) => {
    const div = document.createElement('div');
    div.className = 'item';
    const st = service_map[p.department] || service_map["General"] || 10;
    div.innerHTML = `<strong>${escapeHtml(p.name)}</strong> 
      <small>${escapeHtml(p.department)} · est ${st} min (Booking: ${escapeHtml(p.booking_id)})</small>`;
    el.appendChild(div);
  });
}

// ---------- SSE ----------
evtSource.addEventListener('update', function(e) {
  try {
    const data = JSON.parse(e.data);
    renderStats(data);
  } catch (err) {
    console.error("Invalid SSE data", err);
  }
});

// ---------- Initial fetch ----------
fetch('/api/stats').then(r => r.json()).then(renderStats);

// ---------- Search ----------
document.getElementById('searchForm').addEventListener('submit', function(ev) {
  ev.preventDefault();
  const booking_id = document.getElementById('booking_id').value.trim();
  if (!booking_id) { alert('Please enter Booking ID'); return; }

  fetch('/api/search', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({booking_id})
  })
  .then(r => r.json())
  .then(resp => {
    if (resp.error) {
      alert(resp.error);
    } else {
      fetch('/api/stats').then(r => r.json()).then(renderStats);
    }
    document.getElementById('booking_id').value = '';
  });
});
