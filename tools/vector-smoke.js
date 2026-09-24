(() => {
  const report = document.createElement('main');
  report.style.cssText = 'position:fixed;inset:0;z-index:9999;background:#eee;padding:16px;overflow:auto;font:14px monospace';
  try {
    const downloads = [];
    const originalClick = HTMLAnchorElement.prototype.click;
    HTMLAnchorElement.prototype.click = function () { downloads.push({name:this.download, url:this.href, attached:this.isConnected}); };
    const views = ['front', 'back'].map(side => {
      document.getElementById(side === 'front' ? 'downloadFrontSvg' : 'downloadBackSvg').click();
      const download = downloads.shift();
      if (!download || !download.attached || !download.name.endsWith(`-${side}-print.svg`)) throw new Error(`${side} SVG download did not start`);
      const svg = window.cardVector.build(side);
      if (svg.includes('<image') || !svg.includes('<path') || !svg.includes('<text')) throw new Error(`${side} is not self-contained vector artwork`);
      const img = document.createElement('img');
      img.src = URL.createObjectURL(new Blob([svg], {type:'image/svg+xml'}));
      img.style.cssText = 'display:block;width:720px;margin:16px 0;background:#fff';
      return img;
    });
    HTMLAnchorElement.prototype.click = originalClick;
    const status = document.createElement('p');
    status.textContent = 'PASS: independent front/back downloads are self-contained SVG vector artwork';
    report.append(status, ...views);
  } catch (error) {
    report.textContent = 'FAIL: ' + error.stack;
  }
  document.body.append(report);
})();
