from datetime import date, datetime
import os

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
    if not freetexts['workgroup'].lower().startswith('ak '):
        freetexts['workgroup'] = f'AK {freetexts['workgroup']}'

    properties = main.checkbox_fields([
            'solid',
            'liquid',
            'sirup',
            'hygroscopic',
            'volatile',
            'toxic',
            'skin-irritating',
            'eye-irritating'
        ])

    analysis_method = main.mixed_fields({
        'Capillary': bool,
        'KBr': bool,
        'U-ATR': bool,
        'In Solution: CDCl3': bool,
        'In Solution: CHCl3': bool,
        'Other solvent': str,
      }
    )


    with Image.open('base_forms/ir.png') as image:
        image = image.convert('RGBA')
        main.draw_text(image, (1514,727), f'{freetexts['name']} / {freetexts['workgroup']}', 'black', 80) # Name und Arbeitskreis
        main.draw_text(image, (1110,932), freetexts['sample_name'], 'black', 80) # Substanzbezeichnung
        main.draw_text(image, (3455,727), '', 'black', 80) # lfd. nummer
        main.draw_text(image, (3455,932), freetexts['phone_number'], 'black', 80) # Tel.Nr.


        # Eigenschaften
        if properties['solid']: main.draw_text(image, (880,1195), 'x', 'black', 80)
        if properties['liquid']: main.draw_text(image, (880,1320), 'x', 'black', 80)
        if properties['sirup']: main.draw_text(image, (880,1443), 'x', 'black', 80)
        if properties['hygroscopic']: main.draw_text(image, (880,1570), 'x', 'black', 80)
        if properties['volatile']: main.draw_text(image, (880,1695), 'x', 'black', 80)
        if properties['toxic']: main.draw_text(image, (2792,1192), 'x', 'black', 80)
        if properties['skin-irritating']: main.draw_text(image, (2792,1317), 'x', 'black', 80)
        if properties['eye-irritating']: main.draw_text(image, (2792,1441), 'x', 'black', 80)


        main.draw_text(image, (1550,1210), f'{freetexts['melting_point']}°C' if freetexts['melting_point'] else '', 'black', 80) # melting point
        main.draw_text(image, (1550,1330), f'{freetexts['boiling_point']}°C' if freetexts['boiling_point'] else '', 'black', 80) # boiling point


        # Reinheitsgrad
        main.draw_text(image, (910,2125), freetexts['purity'], 'black', 80) # Reinheit
        main.draw_text(image, (2050,2125), freetexts['purity_method'], 'black', 80) # Methode


        # Molekül
        SMILES = freetexts['smiles']
        if not SMILES:
            print('ERROR - No SMILES code given, you need to do draw the structure yourself!')
        else:
            main.draw_molecule(image, (300, 2600), (2100, 810), SMILES)


        # Analysemethoden
        if analysis_method['Capillary']: main.draw_text(image, (922,4261), 'x', 'black', 80)

        if analysis_method['KBr']: main.draw_text(image, (922,4428), 'x', 'black', 80)

        if analysis_method['U-ATR']: main.draw_text(image, (922,4596), 'x', 'black', 80)

        if analysis_method['In Solution: CDCl3']: main.draw_text(image, (3088,4262), 'x', 'black', 80)

        if analysis_method['In Solution: CHCl3']: main.draw_text(image, (3088,4428), 'x', 'black', 80)

        if analysis_method['Other solvent']:
            main.draw_text(image, (3088,4596), 'x', 'black', 80)
            main.draw_text(image, (2950,4670), analysis_method['Other solvent'], 'black', 80, text_alignment= 'rb')


        date_today = date.today().isoformat()
        main.draw_text(image, (290,5090), date_today, 'black', 80) # Date

        # image.show()

        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        output_path = os.path.join('output', f'infrared_form_filled_{timestamp}.png')
        image.save(output_path)
        print(f'Image saved at {output_path}')
