import {subscript_numbers, get_today_date} from './centrals.js'
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