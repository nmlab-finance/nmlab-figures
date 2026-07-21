// Génère inline-button-{fr,en}.html (SVG inline pour le MDX, placeholder COLAB_URL).
// Usage : FONTCONFIG_FILE=fonts.conf node gen-inline.js
const sharp = require("sharp");
const fs = require("fs");

const LABELS = {
  fr: "Générer/Modifier l'image dans Google Colab",
  en: "Generate/Edit the image in Google Colab",
};

const official = fs.readFileSync(__dirname + "/colab-badge-official.svg", "utf8");
const inner = official.match(/<svg x="4px"[\s\S]*?<\/svg>/)[0];
const logo = [...inner.matchAll(/<path style="fill:(#\w+);" d="([^"]+)"\/>/g)]
  .map(m => `<path fill="${m[1]}" d="${m[2]}"/>`).join("");

async function textWidth1x(text) {          // mesure à 30 px (2×) puis /2
  const probe = `<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="100">
    <rect width="1600" height="100" fill="#000"/>
    <text x="10" y="60" font-family="Inter" font-weight="600" font-size="30" fill="#fff">${text.replace(/'/g, "&apos;")}</text></svg>`;
  const { info } = await sharp(Buffer.from(probe)).trim().toBuffer({ resolveWithObject: true });
  return Math.round(info.width / 2) + 2;    // +2 px de marge de rendu navigateur
}

(async () => {
  for (const [lang, label] of Object.entries(LABELS)) {
    const tw = await textWidth1x(label);
    const arrowX = 54 + tw + 10;
    const W = arrowX + 12 + 16;
    const esc = label.replace(/'/g, "&apos;");
    const snippet =
      `<a href="COLAB_URL" target="_blank" rel="noopener noreferrer" aria-label="${esc}">` +
      `<svg width="${W}" height="44" viewBox="0 0 ${W} 44" role="img">` +
      `<title>${esc}</title>` +
      `<rect x="0.5" y="0.5" width="${W - 1}" height="43" rx="9" fill="#17233a" stroke="#31405c"/>` +
      `<g transform="translate(18,10)">${logo}</g>` +
      `<text x="54" y="27.5" font-family="Inter, system-ui, sans-serif" font-size="15" font-weight="600" fill="#f3f6fb">${esc}</text>` +
      `<g transform="translate(${arrowX},16)" stroke="#8ba0bd" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round">` +
      `<path d="M0 12 L12 0 M3.5 0 H12 V8.5"/></g>` +
      `</svg></a>`;
    fs.writeFileSync(`${__dirname}/inline-button-${lang}.html`, snippet);
    const preview = snippet.replace(/^<a [^>]*>/, "").replace(/<\/a>$/, "");
    await sharp(Buffer.from(preview), { density: 192 }).png().toFile(`${__dirname}/preview-${lang}.png`);
    console.log(`${lang} : W=${W}, texte=${tw}, flèche à x=${arrowX}`);
  }
})();
