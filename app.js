(() => {
  const STORAGE_KEY = 'embuilded-card-v1';
  const fields = ['nameEn', 'nameZh', 'title', 'phone', 'email', 'website', 'qrUrl', 'company', 'tagline', 'footer'];
  const defaults = Object.fromEntries(fields.map(id => [id, document.getElementById(id).value]));
  const form = document.getElementById('cardForm');
  const front = document.getElementById('cardFront');
  const back = document.getElementById('cardBack');
  const scaler = document.getElementById('cardScaler');
  const stage = document.querySelector('.preview-stage');
  const saveStatus = document.getElementById('saveStatus');
  const toast = document.getElementById('toast');
  // Data-backed SVG images are also supported by the PNG/PDF renderer.
  document.querySelectorAll('.business-card svg').forEach(svg => {
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    const box = svg.viewBox.baseVal;
    svg.setAttribute('width', box.width); svg.setAttribute('height', box.height);
    svg.style.color = '#111820';
    const img = document.createElement('img');
    img.className = svg.getAttribute('class'); img.alt = '';
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(new XMLSerializer().serializeToString(svg));
    svg.replaceWith(img);
  });
  let currentSide = 'front';
  let toastTimer;

  const getData = () => Object.fromEntries(fields.map(id => [id, document.getElementById(id).value.trim()]));

  function cleanWebsite(value) {
    return value.replace(/^https?:\/\//i, '').replace(/\/$/, '');
  }

  function setData(data) {
    fields.forEach(id => {
      if (typeof data[id] === 'string') document.getElementById(id).value = data[id];
    });
    updatePreview(false);
  }

  function updateText(key, value) {
    document.querySelectorAll(`[data-output="${key}"]`).forEach(node => {
      node.textContent = value || '—';
    });
  }

  function drawQr(value) {
    document.querySelectorAll('[data-qr]').forEach(container => {
      container.replaceChildren();
      if (window.QRCode) {
        const qr = new QRCode(container, {
          text: value || defaults.qrUrl,
          width: 512,
          height: 512,
          colorDark: '#101820',
          colorLight: '#ffffff',
          correctLevel: QRCode.CorrectLevel.H
        });
        // Integer-sized modules and four clear modules on every side remain crisp in exports.
        const count = qr._oQRCode.getModuleCount();
        const unit = 12;
        const canvas = document.createElement('canvas');
        canvas.width = canvas.height = (count + 8) * unit;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#fff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#101820';
        for (let y = 0; y < count; y++) for (let x = 0; x < count; x++) {
          if (qr._oQRCode.isDark(y, x)) ctx.fillRect((x + 4) * unit, (y + 4) * unit, unit, unit);
        }
        const size = Math.floor(count * .28) * unit;
        const start = (canvas.width - size) / 2;
        ctx.fillStyle = '#fff';
        ctx.fillRect(start, start, size, size);
        ctx.save();
        ctx.translate(start + size * .16, start + size * .12);
        ctx.scale(size * .7 / 40, size * .76 / 46);
        ctx.fillStyle = '#f5ad00';
        ctx.fillRect(0, 0, 34, 5); ctx.fillRect(0, 0, 5, 46); ctx.fillRect(0, 41, 14, 5);
        ctx.fillRect(14, 11, 5, 28); ctx.fillRect(14, 11, 21, 5);
        ctx.fillRect(14, 22, 18, 5); ctx.fillRect(14, 34, 21, 5);
        ctx.restore();
        container.replaceChildren(canvas);
      } else {
        container.textContent = 'QR';
      }
    });
  }

  function updatePreview(save = true) {
    const data = getData();
    fields.forEach(key => {
      if (!['website', 'qrUrl'].includes(key)) updateText(key, data[key]);
    });
    updateText('websiteDisplay', cleanWebsite(data.website));
    const footer = document.querySelector('[data-output="footer"]');
    const pieces = data.footer.split(/\s*[·|]\s*/);
    if (pieces.length > 1) {
      const left = document.createElement('span'); left.textContent = pieces.shift();
      const divider = document.createElement('i'); divider.className = 'footer-divider';
      const right = document.createElement('span'); right.textContent = pieces.join(' · ');
      footer.replaceChildren(left, divider, right);
    }
    fitText();
    drawQr(data.qrUrl || data.website);
    if (save) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      saveStatus.textContent = '儲存中…';
      window.setTimeout(() => { saveStatus.textContent = '已自動儲存'; }, 280);
    }
  }

  function showToast(message) {
    window.clearTimeout(toastTimer);
    toast.textContent = message;
    toast.classList.add('show');
    toastTimer = window.setTimeout(() => toast.classList.remove('show'), 2200);
  }

  function switchSide(side) {
    currentSide = side;
    front.hidden = side !== 'front';
    back.hidden = side !== 'back';
    document.querySelectorAll('.side-button').forEach(button => {
      button.classList.toggle('active', button.dataset.side === side);
    });
  }

  function fitCard() {
    const padding = parseFloat(getComputedStyle(stage).paddingLeft) * 2;
    const maxWidth = Math.max(1, stage.clientWidth - padding);
    const scale = Math.min(1, maxWidth / 720);
    [front, back].forEach(card => { card.style.transformOrigin = 'top left'; card.style.transform = `scale(${scale})`; });
    scaler.style.width = `${720 * scale}px`;
    scaler.style.height = `${348 * scale}px`;
  }

  function fitText() {
    [['.name-en', 34, 337], ['.job-title', 20, 337], ['.contact-row span', 17, 284], ['.company-name', 12, 185], ['.website', 12, 185], ['.front-tagline strong', 10, 572], ['.back-footer p', 12, 533]].forEach(([selector, base, max]) => {
      document.querySelectorAll(selector).forEach(node => {
        node.style.fontSize = `${base}px`;
        // Measure a clone so hidden reverse-side text can also be fitted.
        const probe = node.cloneNode(true);
        probe.style.cssText = `${getComputedStyle(node).cssText};position:fixed;visibility:hidden;width:max-content;font:${getComputedStyle(node).font};letter-spacing:${getComputedStyle(node).letterSpacing};white-space:nowrap;display:flex;gap:18px`;
        document.body.append(probe);
        const width = probe.getBoundingClientRect().width;
        probe.remove();
        if (width > max) node.style.fontSize = `${base * max / width}px`;
      });
    });
  }

  async function renderCard(element) {
    if (!window.html2canvas) throw new Error('輸出工具尚未載入，請確認網絡連線。');
    if (!window.CARD_EXPORT_RESOURCES) throw new Error('缺少匯出素材，請確認 assets/export-resources.js 與網頁在同一資料夾。');
    // Use an inherited about:blank document, never clone/navigate the file:// page.
    // Every image is embedded; local-file opaque origins cannot taint this canvas.
    const frame = document.createElement('iframe');
    frame.setAttribute('aria-hidden', 'true');
    frame.tabIndex = -1;
    frame.style.cssText = 'position:fixed;left:0;top:0;width:720px;height:348px;opacity:0;pointer-events:none;border:0;z-index:-1';
    document.body.append(frame);
    try {
      const doc = frame.contentDocument;
      doc.open();
      doc.write('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>');
      doc.close();
      const style = doc.createElement('style');
      style.textContent = CARD_EXPORT_RESOURCES.css + '\nhtml,body{margin:0;padding:0;background:transparent}';
      doc.head.append(style);
      document.querySelectorAll('link[href*="fonts.googleapis.com"]').forEach(link => doc.head.append(link.cloneNode(true)));
      const card = element.cloneNode(true);
      card.hidden = false;
      card.style.cssText = 'position:relative;transform:none;box-shadow:none;margin:0';
      card.querySelectorAll('img').forEach(img => {
        const path = img.getAttribute('src');
        if (CARD_EXPORT_RESOURCES.images[path]) img.src = CARD_EXPORT_RESOURCES.images[path];
        else if (!path.startsWith('data:')) throw new Error('匯出素材未內嵌：' + path);
      });
      card.querySelectorAll('canvas').forEach((canvas, index) => {
        const img = doc.createElement('img');
        img.src = element.querySelectorAll('canvas')[index].toDataURL('image/png');
        canvas.replaceWith(img);
      });
      doc.body.append(card);
      // Force layout before waiting for fonts; all images must succeed, not merely complete.
      card.getBoundingClientRect();
      await Promise.all(Array.from(card.querySelectorAll('img')).map(img => new Promise((resolve, reject) => {
        if (img.complete) return img.naturalWidth ? resolve() : reject(new Error('無法載入匯出圖片。'));
        img.onload = resolve; img.onerror = () => reject(new Error('無法載入匯出圖片。'));
      })));
      await doc.fonts.ready;
      return await html2canvas(card, {
        backgroundColor: null,
        scale: 1063 / 720,
        logging: false,
        width: 720,
        height: 348
      });
    } finally {
      frame.remove();
    }
  }

  function safeFilename() {
    const name = document.getElementById('nameEn').value.trim().replace(/[^a-z0-9\u3400-\u9fff]+/gi, '-');
    return name || 'business-card';
  }

  function downloadUrl(url, filename) {
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = filename;
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
  }

  form.addEventListener('input', () => updatePreview(true));
  document.querySelectorAll('.side-button').forEach(button => button.addEventListener('click', () => switchSide(button.dataset.side)));
  window.addEventListener('resize', fitCard);

  document.getElementById('downloadPng').addEventListener('click', async () => {
    const button = document.getElementById('downloadPng');
    try {
      button.disabled = true;
      button.textContent = '製作中…';
      const card = currentSide === 'front' ? front : back;
      const canvas = await renderCard(card);
      downloadUrl(canvas.toDataURL('image/png', 1), `${safeFilename()}-${currentSide}.png`);
      showToast('PNG 已下載');
    } catch (error) {
      showToast(error.message);
    } finally {
      button.disabled = false;
      button.textContent = '下載 PNG';
    }
  });

  document.getElementById('downloadPdf').addEventListener('click', async () => {
    const button = document.getElementById('downloadPdf');
    try {
      if (!window.jspdf) throw new Error('PDF 工具尚未載入，請確認網絡連線。');
      button.disabled = true;
      button.textContent = '製作中…';
      const frontCanvas = await renderCard(front);
      const backCanvas = await renderCard(back);
      const { jsPDF } = window.jspdf;
      const pdf = new jsPDF({ orientation: 'landscape', unit: 'mm', format: [90, 43.5], compress: true });
      pdf.addImage(frontCanvas.toDataURL('image/png'), 'PNG', 0, 0, 90, 43.5);
      pdf.addPage([90, 43.5], 'landscape');
      pdf.addImage(backCanvas.toDataURL('image/png'), 'PNG', 0, 0, 90, 43.5);
      pdf.save(`${safeFilename()}-business-card.pdf`);
      showToast('雙面 PDF 已下載');
    } catch (error) {
      showToast(error.message);
    } finally {
      button.disabled = false;
      button.textContent = '下載雙面 PDF';
    }
  });

  document.getElementById('copyLink').addEventListener('click', async () => {
    const encoded = btoa(unescape(encodeURIComponent(JSON.stringify(getData()))));
    const url = `${location.href.split('#')[0]}#card=${encoded}`;
    try {
      await navigator.clipboard.writeText(url);
      showToast('分享連結已複製');
    } catch {
      window.prompt('請複製以下連結：', url);
    }
  });

  document.getElementById('exportData').addEventListener('click', () => {
    const blob = new Blob([JSON.stringify(getData(), null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    downloadUrl(url, `${safeFilename()}-data.json`);
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    showToast('資料檔已匯出');
  });

  document.getElementById('importData').addEventListener('change', async event => {
    const file = event.target.files[0];
    if (!file) return;
    try {
      setData(JSON.parse(await file.text()));
      localStorage.setItem(STORAGE_KEY, JSON.stringify(getData()));
      showToast('資料已匯入');
    } catch {
      showToast('無法讀取這個資料檔');
    }
    event.target.value = '';
  });

  document.getElementById('resetButton').addEventListener('click', () => {
    if (!confirm('確定要還原範例資料嗎？')) return;
    localStorage.removeItem(STORAGE_KEY);
    history.replaceState(null, '', location.href.split('#')[0]);
    setData(defaults);
    showToast('已還原範例資料');
  });

  function loadInitialData() {
    const hash = location.hash.match(/^#card=(.+)$/);
    if (hash) {
      try {
        setData(JSON.parse(decodeURIComponent(escape(atob(hash[1])))));
        showToast('已載入分享的名片資料');
        return;
      } catch { /* fall through */ }
    }
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
      if (saved) setData(saved);
      else updatePreview(false);
    } catch {
      updatePreview(false);
    }
  }

  loadInitialData();
  if (new URLSearchParams(location.search).get('side') === 'back') switchSide('back');
  fitCard();
  document.fonts.ready.then(fitText);
  if ('ResizeObserver' in window) new ResizeObserver(fitCard).observe(stage);
  if (new URLSearchParams(location.search).get('export-test') === '1') {
    const script = document.createElement('script');
    script.src = 'tools/export-smoke.js';
    document.body.append(script);
  }
})();
