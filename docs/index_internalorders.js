import {subscript_numbers, get_today_date, get_exact_mass} from './centrals.js'
import {
  form,
  setupFormEventListeners,
  getFormData,
  drawImage,
  drawText
} from './index.js'

setupFormEventListeners(submitAndDrawForm);

function submitAndDrawForm(event) {
  if (event){
    event.preventDefault(); // prevents page reload
  };
  const formData = getFormData(form);
  drawForm(formData);
}

function drawForm(formData) {
  const src = 'base_forms/internal-orders.png';
  const container = document.getElementById('img-container');
  container.classList.add("printable")
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

    const x_coordinates = [0, 2620];
    const y_coordinates = [0, 1750];
    const offsets = x_coordinates.flatMap(x => y_coordinates.map(y => [x, y]));

    for (const offset_xy of offsets) {
      let offset_x = offset_xy[0];
      let offset_y = offset_xy[1];


      svg.appendChild(drawText(svgNS, h, offset_x + 1150, offset_y + 730, formData.product, 70));
      svg.appendChild(drawText(svgNS, h, offset_x + 710, offset_y + 1080, formData.amount, 70));
      svg.appendChild(drawText(svgNS, h, offset_x + 2100, offset_y + 1080, formData.price, 70));
      svg.appendChild(drawText(svgNS, h, offset_x + 885, offset_y + 1420, formData.name, 70));
      svg.appendChild(drawText(svgNS, h, offset_x + 1870, offset_y + 1420, formData_workgroup, 70));
      


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
        svg.appendChild(drawText(svgNS, h, offset_x +320,offset_y+1420, selected_date.join("-") , 70))
      };
    };


    
    // clear container and append svg
    container.innerHTML = '';
    container.appendChild(svg);
  };
};