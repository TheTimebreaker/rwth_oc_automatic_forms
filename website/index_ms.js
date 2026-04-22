import {subscript_numbers, get_today_date, get_exact_mass} from './centrals.js'
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
methodWarningListener();

function methodWarningListener(submitFunction) {
  const method_warnings = document.getElementById('method-warnings');
  form.addEventListener('input', () => {
    const formData = getFormData(form);
    let msg = [];

    if (formData.gcms || formData.gcms_ei || formData.gcms_ci) {
      msg.push('⚠️ Because you have selected GCMS options: Even though the form sheet claims that you have to submit a GC spectrum before the mass spectra department can measure a GCMS spectrum, this is outdated and you don\' need to do this.')
      
    };

    if (formData.hrms_ei) {
      msg.push('⚠️ Because you have selected HRMS EI: Submit an EI spectrum to the mass spectra department together with this form, if you have one.')
    };

    if (msg) {
      method_warnings.innerHTML = msg.join('<br>')
    }
    
  });
};

function submitAndDrawForm(event) {
  if (event){
    event.preventDefault(); // prevents page reload
  };
  const formData = getFormData(form);
  drawForm(formData);
}

function drawForm(formData) {
  const src = 'base_forms/ms.png';
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
    svg.appendChild(drawText(svgNS, h, 1500,820, name_workgroup_str, 50));

    svg.appendChild(drawText(svgNS, h, 1110, 1030, formData.sample, 50));
    svg.appendChild(drawText(svgNS, h, 3460, 1030, formData.phone, 50));
    

    if (formData.stateofmatter == 'solid') {
      svg.appendChild(drawText(svgNS, h, 875,1298, 'x', 70)); // solid
    } else if (formData.stateofmatter == 'liquid') {
      svg.appendChild(drawText(svgNS, h, 875,1424, 'x', 70)); // liquid
    } else if (formData.stateofmatter == 'sirup') {
      svg.appendChild(drawText(svgNS, h, 875,1550, 'x', 70)); // sirup
    };
    
    if (formData.otherproperties_hygroscopic) {
      svg.appendChild(drawText(svgNS, h, 875,1674, 'x', 70)); // hygroscopic
    };
    if (formData.otherproperties_volatile) {
      svg.appendChild(drawText(svgNS, h, 875,1800, 'x', 70)); // volatile
    };

    if (formData.mp) {
      svg.appendChild(drawText(svgNS, h, 1550,1318, formData.mp, 55)); // melting point
    };
    if (formData.bp) {
      svg.appendChild(drawText(svgNS, h, 1550,1444, formData.bp, 55)); // boiling point
    };

   
    if (formData.dangers_toxic) {
      svg.appendChild(drawText(svgNS, h, 2786,1298, 'x', 70)); // toxic
    };
    if (formData.dangers_skinirritant) {
      svg.appendChild(drawText(svgNS, h, 2786,1424, 'x', 70)); // skin-irritating
    };
    if (formData.dangers_eyeirritant) {
      svg.appendChild(drawText(svgNS, h, 2786,1550, 'x', 70)); // eye-irritating
    };


    if (formData.solvent) {
      svg.appendChild(drawText(svgNS, h, 2766,1820, formData.solvent, 50)); // solvent
    }
    

    if (formData.purity) {
      svg.appendChild(drawText(svgNS, h, 900,2075, formData.purity, 50)); // purity
    };
    if (formData.puritymethod) {
      svg.appendChild(drawText(svgNS, h, 2040,2075, formData.puritymethod, 50)); // purity method
    };

    if (formData.sumformula) {
      let SUMFORMULA_LIST = JSON.parse(formData.sum_formula_array);
      let REMAINING_SUMFORMULA_LIST = {...SUMFORMULA_LIST};

      let chn_coordinate_X = 2930
      let chn_coordinate_Y = 2675;
      let chn_letter_offset_X = 168;
      let chn_letter_offset_Y = 0;
      for (const letter of ['C', 'H', 'N', 'O']) {
        svg.appendChild(
          drawText(
            svgNS,
            h,
            chn_coordinate_X,
            chn_coordinate_Y,
            SUMFORMULA_LIST[letter] || "0",
            40
          )
        );
        if (REMAINING_SUMFORMULA_LIST[letter]) {
          delete REMAINING_SUMFORMULA_LIST[letter];
        };
        chn_coordinate_X = chn_coordinate_X + chn_letter_offset_X;
        chn_coordinate_Y = chn_coordinate_Y + chn_letter_offset_Y;
      };
      const REMAINING_SUMFORMULA_STRING = subscript_numbers(sum_formula_to_string(REMAINING_SUMFORMULA_LIST));
      svg.appendChild(drawText(svgNS, h, 3580,2610, REMAINING_SUMFORMULA_STRING, 50)); // remaining elements

      svg.appendChild(drawText(svgNS, h, 3200,2950, get_exact_mass(formData.sumformula).toFixed(5), 50));
    };


    // Methods
    if (formData.gcms) {
      svg.appendChild(drawText(svgNS, h, 327,3760, 'x', 70));
    };
    if (formData.gcms_ei) {
      svg.appendChild(drawText(svgNS, h, 2295,3760, 'x', 70));
    };
    if (formData.gcms_ci) {
      svg.appendChild(drawText(svgNS, h, 2739,3760, 'x', 70));
    };
    if (formData.gcms_ci_methane) {
      svg.appendChild(drawText(svgNS, h, 3092,3774, 'x', 70));
    };
    if (formData.gcms_ci_isobutane) {
      svg.appendChild(drawText(svgNS, h, 3486,3774, 'x', 70));
    };

    if (formData.directevap) {
      svg.appendChild(drawText(svgNS, h, 327,4077, 'x', 70));
    };
    if (formData.directevap_dip) {
      svg.appendChild(drawText(svgNS, h, 524,4229, 'x', 70));
    };
    if (formData.directevap_dci) {
      svg.appendChild(drawText(svgNS, h, 1115,4229, 'x', 70));
    };
    if (formData.directevap_ei) {
      svg.appendChild(drawText(svgNS, h, 2295,4074, 'x', 70));
    };
    if (formData.directevap_ci) {
      svg.appendChild(drawText(svgNS, h, 2739,4074, 'x', 70));
    };
    if (formData.directevap_ci_methane) {
      svg.appendChild(drawText(svgNS, h, 3092,4088, 'x', 70));
    };
    if (formData.directevap_ci_isobutane) {
      svg.appendChild(drawText(svgNS, h, 3486,4088, 'x', 70));
    };

    if (formData.lcms) {
      svg.appendChild(drawText(svgNS, h, 327,4399, 'x', 70));
    };
    if (formData.lcms_esi) {
      svg.appendChild(drawText(svgNS, h, 2295,4399, 'x', 70));
    };
    if (formData.lcms_apci) {
      svg.appendChild(drawText(svgNS, h, 2739,4399, 'x', 70));
    };
    if (formData.lcms_apci_pos) {
      svg.appendChild(drawText(svgNS, h, 3181,4408, 'x', 70));
    };
    if (formData.lcms_apci_neg) {
      svg.appendChild(drawText(svgNS, h, 3464,4408, 'x', 70));
    };
    
    if (formData.hrms) {
      svg.appendChild(drawText(svgNS, h, 327,4814, 'x', 70));
    };
    if (formData.hrms_ei) {
      svg.appendChild(drawText(svgNS, h, 1650,4814, 'x', 70));
    };
    if (formData.hrms_lcms) {
      svg.appendChild(drawText(svgNS, h, 1950,4814, 'x', 70));
    };



    const molecule_image = document.getElementById("molecule-image");
    if (!(molecule_image.classList.contains('placeholder')) && molecule_image.src) {
      svg.appendChild(drawImage(svgNS, 280, 2530, 2290, 870, molecule_image.src));
    };    

    if (formData.automaticdate) {
      svg.appendChild(drawText(svgNS, h, 280,5090, get_today_date(), 60))
    };
    
    // clear container and append svg
    container.innerHTML = '';
    container.appendChild(svg);
  };
};