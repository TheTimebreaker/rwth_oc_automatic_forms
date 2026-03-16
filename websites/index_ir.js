import {get_today_date} from './centrals.js'
import {
  form,
  setupFormEventListeners,
  setupFilepickerEventListener,
  getFormData,
  drawImage,
  drawText
} from './index.js'

setupFormEventListeners(submitAndDrawForm);
setupFilepickerEventListener();

function submitAndDrawForm(event) {
  if (event){
    event.preventDefault(); // prevents page reload
  };
  const formData = getFormData(form);
  drawForm(formData);
}

function drawForm(formData) {
  const src = 'base_forms/ir.png';
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
    svg.appendChild(drawText(svgNS, h, 1500, 745, name_workgroup_str, 50));

    svg.appendChild(drawText(svgNS, h, 1110, 955, formData.sample, 50));
    svg.appendChild(drawText(svgNS, h, 3460, 955, formData.phone, 50));
    

    if (formData.stateofmatter == 'solid') {
      svg.appendChild(drawText(svgNS, h, 875, 1195, 'x', 70)); // solid
    } else if (formData.stateofmatter == 'liquid') {
      svg.appendChild(drawText(svgNS, h, 875, 1321, 'x', 70)); // liquid
    } else if (formData.stateofmatter == 'sirup') {
      svg.appendChild(drawText(svgNS, h, 875, 1447, 'x', 70)); // sirup
    };
    
    if (formData.otherproperties_hygroscopic) {
      svg.appendChild(drawText(svgNS, h, 875, 1571, 'x', 70)); // hygroscopic
    };
    if (formData.otherproperties_volatile) {
      svg.appendChild(drawText(svgNS, h, 875, 1697, 'x', 70)); // volatile
    };

    if (formData.mp) {
      svg.appendChild(drawText(svgNS, h, 1550,1215, formData.mp, 55)); // melting point
    };
    if (formData.bp) {
      svg.appendChild(drawText(svgNS, h, 1550,1341, formData.bp, 55)); // boiling point
    };

    if (formData.dangers_toxic) {
      svg.appendChild(drawText(svgNS, h, 2786, 1195, 'x', 70)); // toxic
    };
    if (formData.dangers_skinirritant) {
      svg.appendChild(drawText(svgNS, h, 2786, 1321, 'x', 70)); // skin-irritating
    };
    if (formData.dangers_eyeirritant) {
      svg.appendChild(drawText(svgNS, h, 2786, 1447, 'x', 70)); // eye-irritating
    };
    

    if (formData.purity) {
      svg.appendChild(drawText(svgNS, h, 900, 2140, formData.purity, 50)); // purity
    };
    if (formData.puritymethod) {
      svg.appendChild(drawText(svgNS, h, 2040, 2140, formData.puritymethod, 50)); // purity method
    };

    // analytic method - method
    if (formData.methods == 'capillary') {
      svg.appendChild(drawText(svgNS, h, 918, 4262, 'x', 70));
    } else if (formData.methods == 'kbr') {
      svg.appendChild(drawText(svgNS, h, 918, 4433, 'x', 70));
    } else if (formData.methods == 'uatr') {
      svg.appendChild(drawText(svgNS, h, 918, 4599, 'x', 70));
    };
    // analytic method - solvent
    if (formData.in_solution == 'cdcl3') {
      svg.appendChild(drawText(svgNS, h, 3083, 4262, 'x', 70));
    } else if (formData.in_solution == 'chcl3') {
      svg.appendChild(drawText(svgNS, h, 3083, 4433, 'x', 70));
    } else if (formData.in_solution == 'custom') {
      svg.appendChild(drawText(svgNS, h, 3083, 4599, 'x', 70));
      if (formData.in_solution_custom_solvent) {
        svg.appendChild(drawText(svgNS, h, 2970, 4610, formData.in_solution_custom_solvent, 50, "end"));
      };      
    };

    const molecule_image = document.getElementById("molecule-image");
    if (!(molecule_image.classList.contains('placeholder')) && molecule_image.src) {
      svg.appendChild(drawImage(svgNS, 280, 2580, 3470, 1200, molecule_image.src));
    };    

    if (formData.automaticdate) {
      svg.appendChild(drawText(svgNS, h, 280,5090, get_today_date(), 60))
    };
    
    // clear container and append svg
    container.innerHTML = '';
    container.appendChild(svg);
  };
};