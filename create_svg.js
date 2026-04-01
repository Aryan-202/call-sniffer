import fs from 'fs';
import path from 'path';

const pngPath = path.join(process.cwd(), 'public', 'image.png');
const svgPath = path.join(process.cwd(), 'public', 'favicon.svg');

// Read the PNG and convert to base64
const pngData = fs.readFileSync(pngPath);
const base64Data = pngData.toString('base64');

// Create the SVG content wrapping the PNG
const svgContent = `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <image href="data:image/png;base64,${base64Data}" width="100%" height="100%" />
</svg>`;

// Write the SVG file
fs.writeFileSync(svgPath, svgContent);
console.log('Successfully created favicon.svg from image.png');
