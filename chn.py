
import urllib
import urllib.error
from datetime import date, datetime

import cirpy #type:ignore
from PIL import Image

import main

if __name__ == '__main__':
    freetexts = main.freetext_fields([
            "name",
            "workgroup",
            "sample_name",
            "phone_number",
            'melting_point',
            'boiling_point',
            'purity',
            'purity_method',
            'smiles'
        ])
#     freetexts = {
#     "name": "name",
#     "workgroup": "workgroup",
#     "sample_name": "YS187-15999",
#     "phone_number": "phone_number",
#     "melting_point": "100",
#     "boiling_point": "200",
#     "purity": "purity",
#     "purity_method": "purity_method",
#     "smiles": "ClC1=C(C=C)C=C(C(O)=O)C=C1",
# }
    if not freetexts['workgroup'].lower().startswith('ak '):
        freetexts['workgroup'] = f'AK {freetexts['workgroup']}'


    properties = main.checkbox_fields([
            'solid',
            'liquid',
            'sirup',
            'volatile',
            'sublimated',
            'sensitive to air humidity',
            'sensitive to air oxygen',
            'decomposes at room temperature',
            'toxic',
            'skin-irritating',
            'eye-irritating'
        ])
    # properties = {'solid': True,
    # 'liquid': True,
    # 'sirup': True,
    # 'volatile': True,
    # 'sublimated': True,
    # 'sensitive to air humidity': True,
    # 'sensitive to air oxygen': True,
    # 'decomposes at room temperature': True,
    # 'toxic': True,
    # 'skin-irritating': True,
    # 'eye-irritating': True}


    with Image.open(main.resource_path('base_forms/chn.png')) as image:
        image = image.convert('RGBA')
        main.draw_text(image, (800,825), f'{freetexts['name']} / {freetexts['workgroup']}', 'black', 80) # Name und Arbeitskreis
        # main.draw_text(image, (1300,1215), freetexts['sample_name'], 'black', 80) # Substanzbezeichnung
        sample_coordinates = (1529, 1213)
        sample_letter_offset = (155, 0)
        for symbol in freetexts['sample_name']:
            main.draw_text(image, sample_coordinates, symbol, 'black', 150, 'mm')
            sample_coordinates = tuple(map(sum, zip(sample_coordinates, sample_letter_offset)))
        main.draw_text(image, (2900,825), freetexts['phone_number'], 'black', 80) # Tel.Nr.


        # Eigenschaften
        if properties['solid']: main.draw_text(image, (1716,1765), 'x', 'black', 80)
        if properties['liquid']: main.draw_text(image, (1716,1913), 'x', 'black', 80)
        if properties['sirup']: main.draw_text(image, (1716,2057), 'x', 'black', 80)
        if properties['sublimated']: main.draw_text(image, (3377,1765), 'x', 'black', 80)
        if properties['volatile']: main.draw_text(image, (3377,1912), 'x', 'black', 80)

        if properties['sensitive to air humidity']: main.draw_text(image, (1716,2200), 'x', 'black', 80)
        if properties['sensitive to air oxygen']: main.draw_text(image, (2483,2200), 'x', 'black', 80)
        if properties['decomposes at room temperature']: main.draw_text(image, (2483,2342), 'x', 'black', 80)

        if properties['toxic']: main.draw_text(image, (1690,2484), 'x', 'black', 80)
        if properties['skin-irritating']: main.draw_text(image, (2483,2484), 'x', 'black', 80)
        if properties['eye-irritating']: main.draw_text(image, (3377,2484), 'x', 'black', 80)


        main.draw_text(image, (2100,1765), freetexts['melting_point'], 'black', 60) # melting point
        main.draw_text(image, (2100,1913), freetexts['boiling_point'], 'black', 60) # boiling point


        # Reinheitsgrad
        main.draw_text(image, (1180,2640), freetexts['purity'], 'black', 60) # Reinheit
        main.draw_text(image, (1740,2640), freetexts['purity_method'], 'black', 60) # Methode


        # Molekül
        SMILES = freetexts['smiles']
        if not SMILES:
            print('ERROR - No SMILES code given, you need to do sumformula and molar mass yourself!')
        else:
            try:
                FORMULA = cirpy.resolve(SMILES, 'formula')
            except urllib.error.HTTPError as error:
                print('ERROR - Cirpy server unavailable, you need to do sumformula and molar mass yourself!')
                print(error)
                tmp = input('Paste SUM FORMULA (optional):')
                if tmp:
                    FORMULA = tmp
                else:
                    FORMULA = ''
            FORMULA_BY_ATOMS = main.molecule_sumformula_by_atom(FORMULA)
            main.draw_molecule(image, (450, 3350), (3100, 850), SMILES)

            BONUS_STRING = ''
            for element, count in FORMULA_BY_ATOMS.items():
                BONUS_STRING += element + (main.subscript(str(count)) if count > 1 else "")
            main.draw_text(image, (550,2920), BONUS_STRING, 'black', 100)


            # C H N ...
            MASSPERCENT_BY_ATOMS = main.molecule_masspercent_by_atom(FORMULA)
            sample_coordinates = (1810, 4410)
            sample_letter_offset = (635, 0)
            for letter in ('C', 'H', 'N'):
                main.draw_text(
                    image,
                    sample_coordinates,
                    f'{MASSPERCENT_BY_ATOMS[letter]*100 if letter in MASSPERCENT_BY_ATOMS else 0.0:.2f}',
                    'black',
                    60
                )
                sample_coordinates = tuple(map(sum, zip(sample_coordinates, sample_letter_offset)))


        date_today = date.today().isoformat()
        main.draw_text(image, (460,5060), date_today, 'black', 80) # Date

        # image.show()
        # time.sleep(0.5)

        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        output_path = f'chn_form_filled_{timestamp}.png'
        image.save(output_path)
        print(f'Image saved at {output_path}')
