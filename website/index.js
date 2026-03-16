import {Molecule} from 'https://cdn.jsdelivr.net/npm/openchemlib@9.7/+esm'
import {process_CHN} from './centrals.js'
import {downloadSVG, downloadPNG} from './download.js'

export const downloadSVGButton = document.getElementById('downloadSVG');
export const downloadPNGButton = document.getElementById('downloadPNG');
export const molfileElement = document.getElementById('molfile');
export const form = document.getElementById('inputfields');
export const submit_btn = document.getElementById('submit');


// General comfort code for all subpages
document.addEventListener("DOMContentLoaded", () => {
  setDisabledTooltip();
  enableEasyDoubleclick();
});
function setDisabledTooltip() {
  function set_message(element) {
    element.setAttribute('title', 'This field cannot be edited manually. It will adjust automatically, whenever you change the structure above.')
  };
  Array.from(document.getElementsByClassName('disabled')).forEach((element) => {
    set_message(element);
  });
  Array.from(document.getElementsByClassName('disabled-tooltip')).forEach((element) => {
    set_message(element);
  });
};
function enableEasyDoubleclick() {
  const elements = document.getElementsByClassName('easydoubleclick');
  Array.from(elements).forEach((element) => {
    element.addEventListener('dblclick', (e) => {
      e.preventDefault();
      element.select();
    });
  });
};


export function getFormData(formElement) {
  console.log('submitted');
  const formData = Object.fromEntries(new FormData(formElement));
  return formData;
}


// Submit & Download button code
downloadSVGButton.addEventListener('click', () => {
  console.log('Downloading svg...');
  const svg = document.getElementById('img-container')?.querySelector('svg') || document.querySelector('svg')
  downloadSVG(svg);
});
downloadPNGButton.addEventListener('click', () => {
  console.log('Downloading png...');
  const svg = document.getElementById('img-container')?.querySelector('svg') || document.querySelector('svg')
  downloadPNG(svg);
});
export function setupFormEventListeners(submitFunction) {
  form.addEventListener('input', () => {
    // window.previewIsCurrent = false;
    const msg = "Downloading is disabled, once the preview is out-of-date with your inputs. Generate a new preview to enable download.";
    downloadPNGButton.disabled = true;
    downloadPNGButton.title = msg;
    downloadSVGButton.disabled = true;
    downloadSVGButton.title = msg;
  });
  form.addEventListener('submit', (event) => {
    if (event){
      event.preventDefault(); // prevents page reload
    };
    submitFunction(event);
    submit_btn.value = 'Update Preview';
    downloadPNGButton.disabled = false;
    downloadPNGButton.title = '';
    downloadSVGButton.disabled = false;
    downloadSVGButton.title = '';
  });
}


// Filepicker event listener
export function setupFilepickerEventListener() {
  // Formats that WORK:       MDL SDfile (V2000), Molfile (V2000)
  // Formats that DONT WORK:  MSI ChemNote,MDL RDfile, MDL RDfile V2000, .cml, .cdx, .cdxml
  molfileElement.addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();

    // This event fires when reading is complete
    reader.onload = async function(e) {
      const contents = e.target.result;
      const molecule = Molecule.fromMolfile(contents);
      const [molecular_formula_dict, elemental_avrg_mass_contribution_dict] = await process_CHN(molecule);
      const svg = molecule.toSVG(200, 200, null, {
        autoCrop : true
      });
      window.submitDrawStructure(
          molecular_formula_dict,
          molecule.toSmiles(),
          elemental_avrg_mass_contribution_dict,
          svg
      );
    };

    reader.readAsText(file);
  });
}


// Elemental contribution functions
window.set_sum_formula = function set_sum_formula(sumformula) {
  document.getElementById("sumformula").value = sum_formula_to_string(sumformula);
  const c_element = document.getElementById("c_count");
  if (c_element) c_element.value = sumformula['C'] || 0;
  const h_element = document.getElementById("h_count");
  if (h_element) h_element.value = sumformula['H'] || 0;
  const n_element = document.getElementById("n_count");
  if (n_element) n_element.value = sumformula['N'] || 0;
  const o_element = document.getElementById("o_count");
  if (o_element) o_element.value = sumformula['O'] || 0;

  const array_elem = document.getElementById("sum_formula_array")
  if (array_elem) array_elem.value = JSON.stringify(sumformula);
};
window.set_molecule_smiles = function set_molecule_smiles(smiles) {
  document.getElementById("smiles").value = smiles;
};
window.set_elemental_contribution = function set_elemental_contribution(sumcontribution) {
  document.getElementById("c_percent").value = ((sumcontribution['C'] ?? 0)).toFixed(2);
  document.getElementById("h_percent").value = ((sumcontribution['H'] ?? 0)).toFixed(2);
  document.getElementById("n_percent").value = ((sumcontribution["N"] ?? 0)).toFixed(2);
};
window.set_molecule_image_svg = function set_molecule_image_svg(image_svg) {
  const svgBase64 = 'data:image/svg+xml;base64,' + btoa(image_svg);
  const imgelement = document.getElementById("molecule-image");
  imgelement.src = svgBase64;
  imgelement.classList.remove("placeholder");
  imgelement.removeAttribute('title')
};


// Drawing functions for text and images
export function drawText(svgNS, svg_height, positionX, positionY, text, text_size, anchor = "start") {
  const textElement = document.createElementNS(svgNS, 'text');
  textElement.setAttribute('x', positionX);
  textElement.setAttribute('y', positionY);
  textElement.setAttribute('fill', "black");
  textElement.setAttribute('textAlign', 'center');
  textElement.setAttribute("text-anchor", anchor)
  textElement.setAttribute('font-size', Math.max(12, svg_height * text_size/4000));
  textElement.setAttribute('dominant-baseline', 'hanging');
  textElement.textContent = text;
  return textElement;
};
export function drawImage(svgNS, positionX, positionY, maxWidth, maxHeight, image) {
  const scaledW = maxWidth;
  const scaledH = maxHeight;
  const svgImg = document.createElementNS(svgNS, 'image');
  svgImg.setAttributeNS('http://www.w3.org/1999/xlink', 'href', image);
  svgImg.setAttribute('x', positionX);
  svgImg.setAttribute('y', positionY);
  svgImg.setAttribute('width', scaledW);
  svgImg.setAttribute('height', scaledH);
  return svgImg;
}

export function drawDebug(svgNS, positionX, positionY, maxWidth, maxHeight, image) {
  const scaledW = maxWidth;
  const scaledH = maxHeight;

  // group container so we can return one node

  // debug rectangle (shows allowed drawing area)
  const debugRect = document.createElementNS(svgNS, 'rect');
  debugRect.setAttribute('x', positionX);
  debugRect.setAttribute('y', positionY);
  debugRect.setAttribute('width', maxWidth);
  debugRect.setAttribute('height', maxHeight);
  debugRect.setAttribute('fill', 'none');
  debugRect.setAttribute('stroke', 'black');
  debugRect.setAttribute('stroke-width', '4');
  return debugRect;
}