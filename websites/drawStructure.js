import {CanvasEditor} from 'https://cdn.jsdelivr.net/npm/openchemlib@9.7/+esm'
import {process_CHN} from './centrals.js'


document.addEventListener("DOMContentLoaded", () => {
    const editorDiv = document.getElementsByClassName('molecule-editor')[0];
    window.canvas = new CanvasEditor(editorDiv);
});

export async function sendToParent() {
    const molecule = window.canvas.getMolecule();
    const [molecular_formula_dict, elemental_avrg_mass_contribution_dict] = await process_CHN(molecule);
    const svg = molecule.toSVG(200, 200, null, {
        autoCrop : true
    });

    if (window.opener) {
        window.opener.submitDrawStructure(
            molecular_formula_dict,
            molecule.toSmiles(),
            elemental_avrg_mass_contribution_dict,
            svg
        );
        window.close();
    }
};
window.sendToParent = sendToParent;

