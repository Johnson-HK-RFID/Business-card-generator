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

  function escapeXml(value) {
    return String(value ?? '').replace(/[&<>"']/g, character => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;'
    })[character]);
  }

  function fittedFontSize(selector, fallback) {
    const node = document.querySelector(selector);
    return node ? parseFloat(getComputedStyle(node).fontSize) || fallback : fallback;
  }

  function makeQrVector(value, x, y, size) {
    const container = document.createElement('div');
    const qr = new QRCode(container, {
      text: value || defaults.qrUrl,
      width: 512,
      height: 512,
      colorDark: '#101820',
      colorLight: '#ffffff',
      correctLevel: QRCode.CorrectLevel.H
    });
    const matrix = qr._oQRCode;
    const count = matrix.getModuleCount();
    const moduleSize = size / (count + 8);
    let path = '';
    for (let row = 0; row < count; row++) {
      for (let column = 0; column < count; column++) {
        if (!matrix.isDark(row, column)) continue;
        const px = x + (column + 4) * moduleSize;
        const py = y + (row + 4) * moduleSize;
        path += `M${px.toFixed(3)} ${py.toFixed(3)}h${moduleSize.toFixed(3)}v${moduleSize.toFixed(3)}h-${moduleSize.toFixed(3)}z`;
      }
    }
    const logoSize = Math.floor(count * .28) * moduleSize;
    const logoX = x + (size - logoSize) / 2;
    const logoY = y + (size - logoSize) / 2;
    const sx = logoSize * .7 / 40;
    const sy = logoSize * .76 / 46;
    return `<rect x="${x}" y="${y}" width="${size}" height="${size}" fill="#fff"/>` +
      `<path d="${path}" fill="#101820" shape-rendering="crispEdges"/>` +
      `<rect x="${logoX.toFixed(3)}" y="${logoY.toFixed(3)}" width="${logoSize.toFixed(3)}" height="${logoSize.toFixed(3)}" fill="#fff"/>` +
      `<g transform="translate(${(logoX + logoSize * .16).toFixed(3)} ${(logoY + logoSize * .12).toFixed(3)}) scale(${sx.toFixed(5)} ${sy.toFixed(5)})" fill="#f5ad00">` +
      '<path d="M0 0h34v5H5v36h9v5H0zM14 11h21v5H19v6h13v5H19v7h16v5H14z"/></g>';
  }

  function buildVectorSvg(side) {
    if (!window.CARD_VECTOR_RESOURCES) throw new Error('缺少矢量 Logo 素材。');
    const data = getData();
    const fontFamily = 'Arial, Microsoft JhengHei, Noto Sans TC, sans-serif';
    const common = `<style>text{font-family:${fontFamily}}.card-small{font-size:12px}.lettered{letter-spacing:2.4px}</style>`;
    if (side === 'front') {
      const nameSize = fittedFontSize('.name-en', 34);
      const titleSize = fittedFontSize('.job-title', 20);
      const contactSize = fittedFontSize('.contact-row span', 17);
      const companySize = fittedFontSize('.company-name', 12);
      const websiteSize = fittedFontSize('.website', 12);
      const taglineSize = fittedFontSize('.front-tagline strong', 10);
      return `<?xml version="1.0" encoding="UTF-8"?>\n` +
        `<svg xmlns="http://www.w3.org/2000/svg" width="90mm" height="43.5mm" viewBox="0 0 720 348">` +
        `<title>${escapeXml(data.nameEn)} business card — front</title>${common}` +
        '<rect width="720" height="348" fill="#fff"/>' +
        '<path d="M720 0 600 46v213l108 37v-37l-70-25V82l82-32Z" fill="#f3dfb8"/>' +
        `<svg x="36" y="28" width="350" height="80" viewBox="0 0 1568 358" preserveAspectRatio="xMinYMin meet">${CARD_VECTOR_RESOURCES.embuilded.body}</svg>` +
        `<text x="36" y="158" font-size="${nameSize}" font-weight="700">${escapeXml(data.nameEn || '—')}</text>` +
        `<text x="36" y="185" font-size="21" font-weight="700">${escapeXml(data.nameZh || '—')}</text>` +
        '<rect x="36" y="196" width="43" height="3" fill="#f5ad00"/>' +
        `<text x="36" y="226" font-size="${titleSize}">${escapeXml(data.title || '—')}</text>` +
        '<path d="M5 2 2 4c-1 7 10 18 17 18l3-4-6-4-2 3c-3-1-6-4-7-7l3-2-3-6Z" fill="#101820" transform="translate(36 244) scale(.9)"/>' +
        `<text x="89" y="267" font-size="${contactSize}">${escapeXml(data.phone || '—')}</text>` +
        '<rect x="36" y="279" width="24" height="18" rx="2" fill="#101820"/><path d="m37 280 11 9 11-9" fill="none" stroke="#fff"/>' +
        `<text x="89" y="294" font-size="${contactSize}">${escapeXml(data.email || '—')}</text>` +
        '<line x1="376" y1="132" x2="376" y2="293" stroke="#aeb3b6"/>' +
        makeQrVector(data.qrUrl || data.website, 428.5, 126, 128) +
        `<text x="492.5" y="272" text-anchor="middle" font-size="${companySize}" font-weight="700">${escapeXml(data.company || '—')}</text>` +
        `<text x="492.5" y="291" text-anchor="middle" font-size="${websiteSize}" letter-spacing=".54">${escapeXml(cleanWebsite(data.website) || '—')}</text>` +
        '<rect x="36" y="326" width="46" height="3" fill="#f5ad00"/>' +
        `<text x="96" y="332" font-size="${taglineSize}" font-weight="500" letter-spacing="2.4">${escapeXml(data.tagline || '—')}</text>` +
        '</svg>';
    }

    const footerParts = data.footer.split(/\s*[·|]\s*/);
    const footerLeft = footerParts.shift() || '—';
    const footerRight = footerParts.join(' · ');
    const footerSize = fittedFontSize('.back-footer p', 12);
    const terms = [
      ['TRACKING', 48], ['REPORTING', 173], ['ANALYTICS', 299], ['COMPLIANCE', 425], ['INTELLIGENCE', 563]
    ].map(([label, x]) => `<text x="${x}" y="151" fill="#e6e8e9" font-size="10" letter-spacing="2">${label}</text>`).join('');
    return `<?xml version="1.0" encoding="UTF-8"?>\n` +
      `<svg xmlns="http://www.w3.org/2000/svg" width="90mm" height="43.5mm" viewBox="0 0 720 348">` +
      `<title>${escapeXml(data.nameEn)} business card — back</title>${common}` +
      '<defs><linearGradient id="back" x1="0" x2="1"><stop stop-color="#252b2f"/><stop offset="1" stop-color="#171c1f"/></linearGradient></defs>' +
      '<rect width="720" height="348" fill="url(#back)"/>' +
      '<path d="M720 172 608 209v139h32V233l80-26Z" fill="#fff" fill-opacity=".10"/>' +
      `<svg x="233" y="76" width="254" height="38" viewBox="75 0 1352 202" preserveAspectRatio="xMidYMid meet">${CARD_VECTOR_RESOURCES.traci.body}</svg>` +
      terms +
      '<rect x="141" y="136" width="1" height="20" fill="#f5ad00"/><rect x="267" y="136" width="1" height="20" fill="#f5ad00"/><rect x="393" y="136" width="1" height="20" fill="#f5ad00"/><rect x="531" y="136" width="1" height="20" fill="#f5ad00"/>' +
      '<line x1="42" y1="277" x2="575" y2="277" stroke="#bec3c5"/>' +
      `<text x="42" y="311" fill="#fff" font-size="${footerSize}">${escapeXml(footerLeft)}</text>` +
      '<rect x="190" y="291" width="1" height="20" fill="#f5ad00"/>' +
      `<text x="208" y="311" fill="#fff" font-size="${footerSize}">${escapeXml(footerRight)}</text>` +
      '</svg>';
  }

  function downloadVector(side) {
    const svg = buildVectorSvg(side);
    const blob = new Blob([svg], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    downloadUrl(url, `${safeFilename()}-${side}-print.svg`);
    window.setTimeout(() => URL.revokeObjectURL(url), 1500);
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

  [['downloadFrontSvg', 'front'], ['downloadBackSvg', 'back']].forEach(([buttonId, side]) => {
    document.getElementById(buttonId).addEventListener('click', () => {
      try {
        downloadVector(side);
        showToast(`${side === 'front' ? '正面' : '背面'} SVG 已下載`);
      } catch (error) {
        showToast(error.message);
      }
    });
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
  window.cardVector = { build: buildVectorSvg };
  if (new URLSearchParams(location.search).get('export-test') === '1') {
    const script = document.createElement('script');
    script.src = 'tools/export-smoke.js';
    document.body.append(script);
  }
  if (new URLSearchParams(location.search).get('vector-test') === '1') {
    const script = document.createElement('script');
    script.src = 'tools/vector-smoke.js';
    document.body.append(script);
  }
})();
