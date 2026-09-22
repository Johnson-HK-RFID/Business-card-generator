// Opt-in same-page smoke test: works under ordinary file:// security settings.
(async () => {
  const report = document.createElement('pre');
  report.id = 'export-test-result';
  report.style.cssText = 'position:fixed;inset:0;z-index:9999;background:#eee;padding:16px;margin:0;overflow:auto;white-space:pre-wrap';
  report.textContent = 'Running export checks under ' + location.protocol;
  document.body.append(report);
  const downloads = [];
  const saveFiles = new URLSearchParams(location.search).get('save-test-files') === '1';
  const originalClick = HTMLAnchorElement.prototype.click;
  const originalPdf = window.jspdf?.jsPDF;
  const initialSide = document.getElementById('cardFront').hidden ? 'back' : 'front';
  let pdfInfo;
  async function waitFor(test) {
    for (let i = 0; i < 200; i++) {
      if (test()) return;
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    throw new Error('Timed out: ' + document.getElementById('toast').textContent);
  }
  try {
    HTMLAnchorElement.prototype.click = function () { downloads.push({url:this.href, name:this.download, attached:this.isConnected}); if(saveFiles) originalClick.call(this); };
    for (const side of ['front', 'back']) {
      report.firstChild.textContent = 'Rendering ' + side;
      document.querySelector(`[data-side="${side}"]`).click();
      document.getElementById('downloadPng').click();
      await waitFor(() => downloads.length);
      const result = downloads.shift();
      if (!result.attached || !result.name.endsWith('.png')) throw new Error('Invalid download anchor');
      const img = new Image();
      await new Promise((resolve, reject) => {img.onload=resolve;img.onerror=reject;img.src=result.url;});
      if (img.naturalWidth !== 1063 || img.naturalHeight !== 513) throw new Error('Wrong image size');
      img.style.cssText = 'display:block;width:720px;margin:16px 0';
      report.append(img);
    }
    window.jspdf.jsPDF = function (...args) {
      const pdf = new originalPdf(...args);
      const save = pdf.save.bind(pdf);
      pdf.save = () => {
        const bytes = pdf.output('arraybuffer');
        pdfInfo = {pages:pdf.getNumberOfPages(), width:pdf.internal.pageSize.getWidth(), height:pdf.internal.pageSize.getHeight(), bytes:bytes.byteLength};
        if(saveFiles) save('export-smoke-business-card.pdf');
      };
      return pdf;
    };
    document.getElementById('downloadPdf').click();
    await waitFor(() => pdfInfo);
    if (pdfInfo.pages !== 2 || Math.abs(pdfInfo.height - 43.5) > .01 || pdfInfo.bytes < 10000) throw new Error('Invalid PDF');
    if(document.querySelectorAll('iframe').length) throw new Error('Export iframe leaked');
    report.firstChild.textContent = 'PASS: ordinary '+location.protocol+'; PNG front/back 1063×513; PDF '+JSON.stringify(pdfInfo);
  } catch(error) {
    report.firstChild.textContent = 'FAIL: ' + error.stack;
  } finally {
    HTMLAnchorElement.prototype.click = originalClick;
    if (originalPdf) window.jspdf.jsPDF = originalPdf;
    document.querySelector(`[data-side="${initialSide}"]`).click();
  }
})();
