import {process_CHN, subscript_numbers, get_today_date, get_exact_mass} from './centrals.js'
import {
  downloadSVGButton,
  downloadPNGButton,
  form,
  submit_btn,
  molfileElement,
  setupFormEventListeners,
  setupFilepickerEventListener,
  getFormData,
  drawImage,
  drawDebug,
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
      msg.push('⚠️ Because you have selected GCMS options: Submit a GC spectrum to the mass spectra department together with this form.')
      
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
  const src = 'base_forms/nmr.png';
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

    const x_coordinates = [201, 1436, 2672];
    const y_coordinates = [200, 867, 1534, 2203, 2872, 3540, 4208, 4876];
    const offsets = x_coordinates.flatMap(x => y_coordinates.map(y => [x, y]));

    for (const offset_xy of offsets) {
      let offset_x = offset_xy[0];
      let offset_y = offset_xy[1];

      svg.appendChild(drawText(svgNS, h, offset_x + 435, offset_y + 165, formData.name, 30));
      svg.appendChild(drawText(svgNS, h, offset_x + 435, offset_y + 240, formData_workgroup, 30));
      svg.appendChild(drawText(svgNS, h, offset_x + 435, offset_y + 320, formData.sample, 30));

      const formData_solvent_radio = formData.solvent;
      if (formData_solvent_radio && formData_solvent_radio == "selector") {
        const selector = formData.solvent_selector;
        if (selector == "Chloroform-d") {
          svg.appendChild(drawText(svgNS, h, offset_x + 430, offset_y + 373, "x", 100));
        } else {
          svg.appendChild(drawText(svgNS, h, offset_x + 757, offset_y + 373, "x", 100));
          svg.appendChild(drawText(svgNS, h, offset_x + 850, offset_y + 440, formData.solvent_selector, 30));
        }

      } else if (formData_solvent_radio && formData_solvent_radio == "custom") {
          svg.appendChild(drawText(svgNS, h, offset_x + 757, offset_y + 373, "x", 100));
          svg.appendChild(drawText(svgNS, h, offset_x + 850, offset_y + 440, formData.custom_solvent, 30));
      };

      let exp_list = [];
      if (formData.xp_1h) {
        exp_list.push("¹H")
      };
      if (formData.xp_1hq) {
        exp_list.push("¹Hquant")
      };
      if (formData.xp_13c) {
        exp_list.push("¹³C")
      };
      if (formData.xp_13cq) {
        exp_list.push("¹³Cquant")
      };
      if (formData.xp_19f) {
        exp_list.push("¹⁹F")
      };
      if (formData.xp_19fq) {
        exp_list.push("¹⁹Fquant")
      };
      if (formData.xp_31p) {
        exp_list.push("³¹P")
      };
      if (formData.xp_31pq) {
        exp_list.push("³¹Pquant")
      };
      if (formData.xp_hsqc) {
        exp_list.push("HSQC")
      };
      if (formData.xp_hmbc) {
        exp_list.push("HMBC")
      };
      if (formData.xp_cosy) {
        exp_list.push("COSY")
      };
      if (formData.xp_dosy) {
        exp_list.push("DOSY")
      };
      if (formData.xp_noesy) {
        exp_list.push("NOESY")
      };
      
      const exp_str = exp_list.join(",");
      svg.appendChild(drawText(svgNS, h, offset_x + 435, offset_y + 515, exp_str, 30));


      if (formData.automaticdate) {
        const today_fulldate = get_today_date().split("-");
        let selected_date = [];
        if (formData.autodate_year) {
          selected_date.push(today_fulldate[0])
        };
        if (formData.autodate_month) {
          selected_date.push(today_fulldate[1])
        };
        if (formData.autodate_day) {
          selected_date.push(today_fulldate[2])
        };

        svg.appendChild(drawText(svgNS, h, offset_x + 435, offset_y + 635, selected_date.join("-") , 30))
      };
    }

    // clear container and append svg
    container.innerHTML = '';
    container.appendChild(svg);
  };
};