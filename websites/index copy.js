import {Molecule} from 'https://cdn.jsdelivr.net/npm/openchemlib@9.7/+esm'
import {process_CHN, subscript_numbers, get_today_date} from './centrals.js'
import {downloadSVG, downloadPNG} from './download.js'
document.addEventListener("DOMContentLoaded", () => {
  setDisabledTooltip();
  enableEasyDoubleclick();
});



const downloadSVGButton = document.getElementById('downloadSVG')
downloadSVGButton.addEventListener('click', () => {
  console.log('Downloading svg...');
  const svg = document.getElementById('img-container')?.querySelector('svg') || document.querySelector('svg')
  downloadSVG(svg);
});
const downloadPNGButton = document.getElementById('downloadPNG')
downloadPNGButton.addEventListener('click', () => {
  console.log('Downloading png...');
  const svg = document.getElementById('img-container')?.querySelector('svg') || document.querySelector('svg')
  downloadPNG(svg);
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

// File picker for molfiles
// Formats that WORK:       MDL SDfile (V2000), Molfile (V2000)
// Formats that DONT WORK:  MSI ChemNote,MDL RDfile, MDL RDfile V2000, .cml, .cdx, .cdxml
const molfileElement = document.getElementById('molfile');
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


const form = document.getElementById('inputfields');
const submit_btn = document.getElementById('submit');
form.addEventListener('submit', (event) => {
  submitAndDrawForm(event);
  submit_btn.value = 'Update Preview';
  downloadPNGButton.disabled = false;
  downloadPNGButton.title = '';
  downloadSVGButton.disabled = false;
  downloadSVGButton.title = '';
});
form.addEventListener('input', () => {
  // window.previewIsCurrent = false;
  const msg = "Downloading is disabled, once the preview is out-of-date with your inputs. Generate a new preview to enable download.";
  downloadPNGButton.disabled = true;
  downloadPNGButton.title = msg;
  downloadSVGButton.disabled = true;
  downloadSVGButton.title = msg;
})

function getFormData(formElement) {
  console.log('submitted');
  const formData = Object.fromEntries(new FormData(formElement));
  return formData;
}


export function set_sum_formula(sumformula) {
  document.getElementById("sumformula").value = sum_formula_to_string(sumformula);
  const c_element = document.getElementById("c_count");
  if (c_element) c_element.value = sumformula['C'] || 0;
  const h_element = document.getElementById("h_count");
  if (h_element) h_element.value = sumformula['H'] || 0;
  const n_element = document.getElementById("n_count");
  if (n_element) n_element.value = sumformula['N'] || 0;
  const o_element = document.getElementById("o_count");
  if (o_element) o_element.value = sumformula['O'] || 0;
};
window.set_sum_formula = set_sum_formula;
export function set_molecule_smiles(smiles) {
  document.getElementById("smiles").value = smiles;
};
window.set_molecule_smiles = set_molecule_smiles;

export function set_elemental_contribution(sumcontribution) {
  document.getElementById("c_percent").value = (100*(sumcontribution['C']?.[1] ?? 0)).toFixed(2);
  document.getElementById("h_percent").value = (100*(sumcontribution['H']?.[1] ?? 0)).toFixed(2);
  document.getElementById("n_percent").value = (100*(sumcontribution["N"]?.[1] ?? 0)).toFixed(2);
};
window.set_elemental_contribution = set_elemental_contribution;

export function set_molecule_image_svg(image_svg) {
  const svgBase64 = 'data:image/svg+xml;base64,' + btoa(image_svg);
  const imgelement = document.getElementById("molecule-image");
  imgelement.src = svgBase64;
  imgelement.classList.remove("placeholder");
  imgelement.removeAttribute('title')
};
window.set_molecule_image_svg = set_molecule_image_svg;

function drawText(svgNS, svg_height, positionX, positionY, text, text_size) {
  const textElement = document.createElementNS(svgNS, 'text');
  textElement.setAttribute('x', positionX);
  textElement.setAttribute('y', positionY);
  textElement.setAttribute('fill', 'black');
  textElement.setAttribute('textAlign', 'center');
  textElement.setAttribute('font-size', Math.max(12, svg_height * text_size/4000));
  textElement.setAttribute('dominant-baseline', 'hanging');
  textElement.textContent = text;
  return textElement;
};
function drawImage(svgNS, positionX, positionY, maxWidth, maxHeight, image) {
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










function submitAndDrawForm(event) {
  if (event){
    event.preventDefault(); // prevents page reload
  };
  const formData = getFormData(form);
  drawFormCHN(formData);
}

function drawFormCHN(formData) {
  const src = 'base_forms/chn.png';
  const container = document.getElementById('img-container');
  if (!container) {
    return false
  };

  let formData_workgroup = formData.workgroup;
  if (formData_workgroup && !(formData_workgroup.substring(0,3).toLowerCase() == 'ak ')){
    formData_workgroup = `AK ${formData_workgroup}`;
  };


  const img = new Image();
  img.src = src;
  img.onload = () => {
    const w = img.naturalWidth;
    const h = img.naturalHeight;

    // create SVG sized to the image natural dimensions (viewBox) so coordinates are stable
    const svgNS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(svgNS, 'svg');
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
    svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    svg.style.width = '100%';
    svg.style.height = 'auto';

    // add image element
    const imageEl = document.createElementNS(svgNS, 'image');
    imageEl.setAttributeNS('http://www.w3.org/1999/xlink', 'href', src);
    imageEl.setAttribute('x', '0');
    imageEl.setAttribute('y', '0');
    imageEl.setAttribute('width', w);
    imageEl.setAttribute('height', h);
    svg.appendChild(imageEl);

    let name_workgroup_str = ''
    if (formData.name && formData_workgroup) {
      name_workgroup_str = `${formData.name} / ${formData_workgroup}`
    } else {
      name_workgroup_str = `${formData.name}${formData_workgroup}`
    };
    svg.appendChild(drawText(svgNS, h, 800,825, name_workgroup_str, 80));

    let sample_coordinate_X = 1470;
    let sample_coordinate_Y = 1160;
    let sample_letter_offset_X = 155;
    let sample_letter_offset_Y = 0;
    for (let i = 0; i < formData.sample.length; i++) {
      svg.appendChild(drawText(svgNS, h, sample_coordinate_X, sample_coordinate_Y, formData.sample.charAt(i), 100));
      sample_coordinate_X = sample_coordinate_X + sample_letter_offset_X;
      sample_coordinate_Y = sample_coordinate_Y + sample_letter_offset_Y;
    };
    svg.appendChild(drawText(svgNS, h, 2900, 825, formData.phone, 80));

    if (formData.stateofmatter == 'solid') {
      svg.appendChild(drawText(svgNS, h, 1716,1765, 'x', 70)); // solid
    } else if (formData.stateofmatter == 'liquid') {
      svg.appendChild(drawText(svgNS, h, 1716,1913, 'x', 70)); // liquid
    } else if (formData.stateofmatter == 'sirup') {
      svg.appendChild(drawText(svgNS, h, 1716,2061, 'x', 70)); // sirup
    };
    
    if (formData.otherproperties_sublimates) {
      svg.appendChild(drawText(svgNS, h, 3377,1765, 'x', 70)); // sublimated
    };
    if (formData.otherproperties_volatile) {
      svg.appendChild(drawText(svgNS, h, 3377,1912, 'x', 70)); // volatile
    };


    if (formData.sensitivity_airhumidity) {
      svg.appendChild(drawText(svgNS, h, 1716,2200, 'x', 70)); // sensitive to air humidity
    };
    if (formData.sensitivity_airoxygen) {
      svg.appendChild(drawText(svgNS, h, 2483,2200, 'x', 70)); // sensitive to air oxygen
    };
    if (formData.sensitivity_rt) {
      svg.appendChild(drawText(svgNS, h, 3377,2484, 'x', 70)); // decomposes at room temperature
    };

   
    if (formData.dangers_toxic) {
      svg.appendChild(drawText(svgNS, h, 1690,2484, 'x', 70)); // toxic
    };
    if (formData.dangers_skinirritant) {
      svg.appendChild(drawText(svgNS, h, 2483,2484, 'x', 70)); // skin-irritating
    };
    if (formData.dangers_eyeirritant) {
      svg.appendChild(drawText(svgNS, h, 3377,2484, 'x', 70)); // eye-irritating
    };
    

    if (formData.mp) {
      svg.appendChild(drawText(svgNS, h, 2100,1765, formData.mp, 55)); // melting point
    };
    if (formData.bp) {
      svg.appendChild(drawText(svgNS, h, 2100,1913, formData.bp, 55)); // boiling point
    };

    if (formData.purity) {
      svg.appendChild(drawText(svgNS, h, 1180,2630, formData.purity, 55)); // purity
    };
    if (formData.puritymethod) {
      svg.appendChild(drawText(svgNS, h, 1740,2630, formData.puritymethod, 55)); // purity method
    };

    if (formData.sumformula) {
      let SUMFORMULA_LIST = []
      for (let i = 0; i < formData.sumformula.length; i++) {
        SUMFORMULA_LIST.push(formData.sumformula.charAt(i))
      };
      const SUMFORMULA_STRING = subscript_numbers(SUMFORMULA_LIST.join(''));
      svg.appendChild(drawText(svgNS, h, 550,2920, SUMFORMULA_STRING, 70));

      let chn_coordinate_X = 1810;
      let chn_coordinate_Y = 4410;
      let chn_letter_offset_X = 635;
      let chn_letter_offset_Y = 0;
      for (const letter of ['C', 'H', 'N']) {
        svg.appendChild(
          drawText(
            svgNS,
            h,
            chn_coordinate_X,
            chn_coordinate_Y,
            formData[letter],
            50
          )
        );
        chn_coordinate_X = chn_coordinate_X + chn_letter_offset_X;
        chn_coordinate_Y = chn_coordinate_Y + chn_letter_offset_Y;
      };
    };



    const molecule_image = document.getElementById("molecule-image");
    if (!(molecule_image.classList.contains('placeholder')) && molecule_image.src) {
      svg.appendChild(drawImage(svgNS, 410, 3340, 3200, 900, molecule_image.src))
    };    

    if (formData.automaticdate) {
      svg.appendChild(drawText(svgNS, h, 460,5060, get_today_date(), 65))
    };
    
    // clear container and append svg
    container.innerHTML = '';
    container.appendChild(svg);
  };
};