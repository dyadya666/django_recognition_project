(function () {
    // Глобальні змінні `VIDEO_PK` та `STATUS_URL` мають бути визначені в шаблоні
    const pk = window.VIDEO_PK;
    const statusUrl = window.STATUS_URL;

  if (!statusUrl) {
    console.error('STATUS_URL not defined');
    return;
  }

    const statusEl = document.getElementById('status');
    const errorEl = document.getElementById('error');
    const resultsEl = document.getElementById('results');
    const resultsList = document.getElementById('results-list');
    const detailLink = document.getElementById('detail-link');

    let stopped = false;

    async function fetchStatus() {
        if (stopped) return;

        try {
            const res = await fetch(statusUrl, { cache: 'no-store' });
            if (!res.ok) throw new Error('Network error: ' + res.status);
            const data = await res.json();

            if (statusEl) statusEl.textContent = data.status || 'unknown';

            if (data.status === 'processing' || data.status === 'pending') {
                setTimeout(fetchStatus, 2000);
                return;
            }
            
            if (data.status === 'done') {
                stopped = true;
                renderResults(data.result || []);
                if (detailLink) detailLink.style.display = 'inline';
                return;
            }
            
            if (data.status === 'error') {
                stopped = true;
                if (errorEl) {
                    errorEl.style.display = 'block';
                    errorEl.textContent = data.error || 'Unknown error';
                }
                if (detailLink) detailLink.style.display = 'inline';
                return;
            }

            setTimeout(fetchStatus, 3000);

        } catch (error) {
            console.error('status fetch failed', error);
            setTimeout(fetchStatus, 3000);
        }
    }

  function parseLabelAndConfidence(item) {
    let label = item.label || item.result || item.name || '-';
    let confidence = item.confidence;
    if (confidence === undefined || confidence === null) {
      const m = String(label).match(/\(([0-9]+(?:\.[0-9]+)?)\s*%?\)/);
      if (m) {
        confidence = parseFloat(m[1]) / 100;
        label = label.replace(m[0], '').trim();
      }
    }
    return { label, confidence };
  }

    function renderResults(results) {
        if (!resultsEl || !resultsList) return;

        resultsEl.style.display = results.length ? 'block' : 'none';
        resultsList.innerHTML = '';
        for (const r of results) {
            const li = document.createElement('li');
            const parsed = parseLabelAndConfidence(r);
            const confText = (parsed.confidence !== undefined) ? ` — ${(parsed.confidence * 100).toFixed(1)}%` : '';
            li.textContent = `Кадр ${r.frame} : ${parsed.label}${confText}`;
            resultsList.appendChild(li);
        }
    }

    fetchStatus();
})();
