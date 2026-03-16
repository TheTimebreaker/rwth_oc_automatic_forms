import chemcalc from 'https://cdn.jsdelivr.net/npm/chemcalc@3.4.1/+esm';

export function sum_formula_to_string(sum_formula_dict) {
    let result = ''
    for (const [key, value] of Object.entries(sum_formula_dict)) {
        result = `${result}${key}${value}`;
    };
    return result;
};
window.sum_formula_to_string = sum_formula_to_string;

export function getMolecularFormulaDict(molecule) {
  let molecular_formula_dict = {};
  for (let i = 0; i < molecule.getAllAtoms(); i++) {
    const label = molecule.getAtomLabel(i);      // "C", "H", "O", ...

    molecular_formula_dict[label] = (molecular_formula_dict[label] || 0) + 1; // adds 1 to its element count
    let hydrogen_count = molecule.getImplicitHydrogens(i);
    molecular_formula_dict['H'] = (molecular_formula_dict['H'] || 0) + hydrogen_count;
  };
  return molecular_formula_dict;
};
window.getMolecularFormulaDict = getMolecularFormulaDict;

export function getElementalMassContributionDict(sum_formula) {
  let per_element_mass_dict = {};
  chemcalc.analyseMF(sum_formula).ea.forEach(entry => {
    const element = entry.element;
    const percentage = entry.percentage;
    per_element_mass_dict[element] = percentage
  });
  return per_element_mass_dict;
};

export function subscript_numbers(string) {
  const subscript = {
    '0': '₀',
    '1': '₁',
    '2': '₂',
    '3': '₃',
    '4': '₄',
    '5': '₅',
    '6': '₆',
    '7': '₇',
    '8': '₈',
    '9': '₉',
  }
  let result = []
  for (let i = 0; i < string.length; i++) {
    const letter = string.charAt(i);
    let newletter
    if (letter in subscript) {
      newletter = subscript[letter];
    } else {
      newletter = letter;
    };
    result.push(newletter);
  };
  return result.join('')
}

export function get_today_date() {
  const today = new Date();

  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0'); // months are 0-based
  const day = String(today.getDate()).padStart(2, '0');

  const formatted = `${year}-${month}-${day}`;
  return formatted
}

export function get_molar_mass(sum_formula) {
  const result = chemcalc.analyseMF(sum_formula);
  return result.mw;
}

export function get_exact_mass(sum_formula) {
  const result = chemcalc.analyseMF(sum_formula);
  return result.em;
}

export function process_CHN(molecule) {
    const molecular_formula_dict = getMolecularFormulaDict(molecule);
    const molecular_formula_str = sum_formula_to_string(molecular_formula_dict);

    const elemental_avrg_mass_contribution_dict = getElementalMassContributionDict(molecular_formula_str);
    
    return [molecular_formula_dict, elemental_avrg_mass_contribution_dict] 
};
