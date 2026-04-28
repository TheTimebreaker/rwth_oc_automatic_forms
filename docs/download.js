export async function downloadPNG(svg) {
  // const svg = document.getElementById('img-container')?.querySelector('svg') || document.querySelector('svg')
  if (!svg) {
    console.error('SVG element not found');
    return;
  }

  // Work on a clone so the live SVG isn’t modified
  const clone = svg.cloneNode(true);
  if (!clone.getAttribute("xmlns")) clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  if (!clone.getAttribute("xmlns:xlink")) clone.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");

  // Inline external <image> hrefs (reuses your helper)
  if (typeof inlineExternalImages === 'function') {
    await inlineExternalImages(clone);
  }

  // Determine output pixel size: prefer viewBox, then bbox, then displayed size
  let width, height;
  const viewBox = clone.getAttribute('viewBox');
  if (viewBox) {
    const parts = viewBox.trim().split(/\s+/);
    if (parts.length >= 4) {
      width = Math.round(Number(parts[2]));
      height = Math.round(Number(parts[3]));
    }
  }

  if ((!width || !height) && typeof svg.getBBox === 'function') {
    try {
      const bb = svg.getBBox();
      if (bb.width && bb.height) {
        width = Math.round(bb.width);
        height = Math.round(bb.height);
      }
    } catch (e) {
      // ignore
    }
  }

  if ((!width || !height) && svg.getBoundingClientRect) {
    const rect = svg.getBoundingClientRect();
    width = Math.round(rect.width) || width;
    height = Math.round(rect.height) || height;
  }

  if (!width || !height) {
    console.error('Could not determine SVG pixel size.');
    return;
  }

  // Ensure clone has explicit pixel dimensions so rasterizer uses them
  clone.setAttribute('width', width);
  clone.setAttribute('height', height);

  const svgString = new XMLSerializer().serializeToString(clone);
  const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(svgBlob);

  const img = new Image();
  img.crossOrigin = 'anonymous'; // safe for same-origin/blob URLs and avoids tainting the canvas
  await new Promise((resolve, reject) => {
    img.onload = resolve;
    img.onerror = (e) => {
      URL.revokeObjectURL(url);
      reject(e);
    };
    img.src = url;
  });

  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0, width, height);
  URL.revokeObjectURL(url);

  // Use toBlob and download the resulting PNG blob
  canvas.toBlob((blob) => {
    if (!blob) {
      console.error('Failed to create PNG blob from canvas');
      return;
    }
    const pngUrl = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = pngUrl;
    a.download = 'image.png';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(pngUrl);
  }, 'image/png');
};

export async function downloadSVG(svg) {
  // const svg = document.getElementById('img-container').querySelector('svg');
  if (!svg) {
    console.error("SVG element not found");
    return;
  }

  // Work on a clone so the live SVG isn’t modified
  const clone = svg.cloneNode(true);

  // Ensure namespaces exist (helps some viewers)
  if (!clone.getAttribute("xmlns")) {
    clone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  }
  if (!clone.getAttribute("xmlns:xlink")) {
    clone.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
  }

  // Inline all <image> hrefs as data URLs
  await inlineExternalImages(clone);

  const svgString = new XMLSerializer().serializeToString(clone);
  const blob = new Blob([svgString], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = 'form_chn.svg';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

async function inlineExternalImages(svgRoot) {
  const XLINK_NS = "http://www.w3.org/1999/xlink";
  const images = Array.from(svgRoot.querySelectorAll("image"));

  await Promise.all(
    images.map(async (img) => {
      let href =
        img.getAttribute("href") ||
        img.getAttributeNS(XLINK_NS, "href");

      if (!href || href.startsWith("data:")) return;

      // Resolve relative URLs against the document
      const absUrl = new URL(href, document.baseURI).href;

      try {
        // Requires the image to be same-origin or CORS-enabled
        const res = await fetch(absUrl, { mode: "cors" });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const blob = await res.blob();

        const dataUrl = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => resolve(reader.result);
          reader.onerror = reject;
          reader.readAsDataURL(blob);
        });

        // Set both SVG2 and legacy xlink hrefs
        img.setAttribute("href", dataUrl);
        img.setAttributeNS(XLINK_NS, "href", dataUrl);
      } catch (err) {
        console.warn("Could not inline image:", absUrl, err);
      }
    })
  );
}