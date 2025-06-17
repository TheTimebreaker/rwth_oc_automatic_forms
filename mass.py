import tkinter as tk
import os
import urllib
import urllib.error
from datetime import date, datetime

import cirpy #type:ignore
import molmass
from PIL import Image

import main

def freetext_fields(fields:list[str]) -> dict:
    """Function that opens a window for all the freetext fields

    Args:
        fields (list[str])

    Returns:
        dict: Results
    """
    def submit_and_close():
        for fielddd in fields:
            results[fielddd] = entries[fielddd].get()
        root.quit()
        root.destroy()
    entries = {}

    root = tk.Tk()
    root.title("Enter the values for the freetext fields.")
    for field in fields:
        label = tk.Label(root, text=f"Enter: {field.replace('_', ' ')}:")
        label.pack(pady=2)
        entry = tk.Entry(root, width=40)
        entry.pack(pady=2)
        entries[field] = entry

    # Button to trigger input handling
    results:dict[str,str] = {}
    submit_button = tk.Button(root, text="Submit", command=submit_and_close)
    submit_button.pack(pady=10)

    # Run the main loop
    root.mainloop()
    return results

def checkbox_fields(fields:list[str]) -> dict:
    """Function that opens a window for all checkbox fields

    Args:
        fields (list[str])

    Returns:
        dict: Results
    """
    def submit_and_close():
        for label, var in checkboxes.items():
            results[label] = var.get()
        root.quit()
        root.destroy()

    root = tk.Tk()
    root.title("Select Options")

    results:dict[str, str] = {}
    checkboxes = {}
    for field in fields:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(root, text=field, variable=var)
        cb.pack(anchor="w")
        checkboxes[field] = var

    submit_btn = tk.Button(root, text="Submit", command=submit_and_close)
    submit_btn.pack(pady=10)

    root.mainloop()
    return results

def checkbox_methods() -> dict:
    """Function that opens a window for conditional checkboxes

    Args:
        fields (list[str])

    Returns:
        dict: Results
    """
    def submit_and_close():
        def submit_recursively(option:dict[str, dict]):
            for label, var in option.items():
                assert isinstance(var['main'], tk.IntVar)
                results[label] = var['main'].get()
                if 'subs' in var.keys():
                    assert isinstance(var['subs'], dict)
                    submit_recursively(var['subs'])
        submit_recursively(options)
        root.quit()
        root.destroy()
    def add_checkbox(option:dict[str, dict], indent:int = 0):
        for name, content in option.items():
            checkbox = tk.Checkbutton(
                root,
                text = name,
                variable = content['main'],
                command = update_condition_state_entry
            )
            checkbox.pack(anchor='w', padx= indent)
            if 'subs' in content.keys():
                add_checkbox(content['subs'], indent= indent+20)
    def update_condition_state_entry():
        """Recursively updates the checkboxes to respect the conditional relationship"""
        def update_condition_state(
                option:dict[str, dict[str, tk.IntVar|dict]],
                parent_value:int|bool
            ):
            for content in option.values():
                assert isinstance(content['main'], tk.IntVar)
                if not parent_value:
                    content['main'].set(0)
                if 'subs' in content.keys():
                    assert isinstance(content['subs'], dict)
                    update_condition_state(content['subs'], parent_value= content['main'].get())
        update_condition_state(options, True)

    root = tk.Tk()
    root.title("Select Options")

    options = {
        'gcms': {
            'main': tk.IntVar(),
            'subs': {
                'gcms_ei': {
                    'main': tk.IntVar(),
                },
                'gcms_ci': {
                    'main': tk.IntVar(),
                    'subs': {
                        'gcms_ci_methan': {
                            'main': tk.IntVar(),
                        },
                        'gcms_ci_isobutan': {
                            'main': tk.IntVar(),
                        },
                    },
                },
            }
        },
        'direct': {
            'main': tk.IntVar(),
            'subs': {
                'direct_ei': {
                    'main': tk.IntVar(),
                },
                'direct_ci': {
                    'main': tk.IntVar(),
                    'subs': {
                        'direct_ci_methan': {
                            'main': tk.IntVar(),
                        },
                        'direct_ci_isobutan': {
                            'main': tk.IntVar(),
                        },
                    },
                },
                'direct_dip': {
                    'main': tk.IntVar(),
                },
                'direct_dci': {
                    'main': tk.IntVar(),
                },
            },
        },
        'lcms': {
            'main': tk.IntVar(),
            'subs': {
                'lcms_esi': {
                    'main': tk.IntVar(),
                },
                'lcms_ci': {
                    'main': tk.IntVar(),
                    'subs': {
                        'lcms_ci_pos': {
                            'main': tk.IntVar(),
                        },
                        'lcms_ci_neg': {
                            'main': tk.IntVar(),
                        },
                    },
                },
            },
        },
        'hrms': {
            'main': tk.IntVar(),
            'subs': {
                'hrms_ei': {
                    'main': tk.IntVar(),
                },
                'hrms_lcms': {
                    'main': tk.IntVar(),
                }
            }
        }
    }

    results:dict = {}
    add_checkbox(options)

    submit_btn = tk.Button(root, text="Submit", command=submit_and_close)
    submit_btn.pack(pady=10)

    root.mainloop()
    return results


if __name__ == '__main__':
    freetexts = freetext_fields([
            "name",
            "workgroup",
            "sample_name",
            "phone_number",
            'solvent',
            'melting_point',
            'boiling_point',
            'purity',
            'purity_method',
            'smiles'
        ])
    if not freetexts['workgroup'].lower().startswith('ak '):
        freetexts['workgroup'] = f'AK {freetexts['workgroup']}'

    properties = checkbox_fields([
            'solid',
            'liquid',
            'sirup',
            'hygroscopic',
            'volatile',
            'toxic',
            'skin-irritating',
            'eye-irritating'
        ])

    analysis_method = checkbox_methods()


    with Image.open('base_forms/ms.png') as image:
        image = image.convert('RGBA')
        main.draw_text(image, (1514,810), f'{freetexts['name']} / {freetexts['workgroup']}', 'black', 80) # Name und Arbeitskreis
        main.draw_text(image, (1110,1015), freetexts['sample_name'], 'black', 80) # Substanzbezeichnung
        main.draw_text(image, (3455,810), '', 'black', 80) # lfd. nummer
        main.draw_text(image, (3455,1015), freetexts['phone_number'], 'black', 80) # Tel.Nr.


        # Eigenschaften
        if properties['solid']: main.draw_text(image, (880,1300), 'x', 'black', 80)
        if properties['liquid']: main.draw_text(image, (880,1425), 'x', 'black', 80)
        if properties['sirup']: main.draw_text(image, (880,1548), 'x', 'black', 80)
        if properties['hygroscopic']: main.draw_text(image, (880,1675), 'x', 'black', 80)
        if properties['volatile']: main.draw_text(image, (880,1800), 'x', 'black', 80)
        if properties['toxic']: main.draw_text(image, (2795,1300), 'x', 'black', 80)
        if properties['skin-irritating']: main.draw_text(image, (2795,1425), 'x', 'black', 80)
        if properties['eye-irritating']: main.draw_text(image, (2795,1548), 'x', 'black', 80)


        main.draw_text(image, (1550,1310), f'{freetexts['melting_point']}°C' if freetexts['melting_point'] else '', 'black', 80) # melting point
        main.draw_text(image, (1550,1435), f'{freetexts['boiling_point']}°C' if freetexts['boiling_point'] else '', 'black', 80) # boiling point


        main.draw_text(image, (2750,1810), freetexts['solvent'], 'black', 80) # Lösungsmittel


        # Reinheitsgrad
        main.draw_text(image, (910,2060), freetexts['purity'], 'black', 80) # Reinheit
        main.draw_text(image, (2050,2060), freetexts['purity_method'], 'black', 80) # Methode


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
            main.draw_molecule(image, (400, 2800), (2100, 810), SMILES)

            # Molmasse
            if FORMULA:
                mass = molmass.Formula(FORMULA).monoisotopic_mass
                main.draw_text(image, (3200,2920), str(round(mass, 5)), 'black', 80)


            # C H N O ...
            if 'C' in FORMULA_BY_ATOMS:
                main.draw_text(image, (2945,2650), str(FORMULA_BY_ATOMS['C']), 'black', 60)
            if 'H' in FORMULA_BY_ATOMS:
                main.draw_text(image, (3110,2650), str(FORMULA_BY_ATOMS['H']), 'black', 60)
            if 'N' in FORMULA_BY_ATOMS:
                main.draw_text(image, (3275,2650), str(FORMULA_BY_ATOMS['N']), 'black', 60)
            if 'O' in FORMULA_BY_ATOMS:
                main.draw_text(image, (3440,2650), str(FORMULA_BY_ATOMS['O']), 'black', 60)
            BONUS_STRING = ''
            for element, count in FORMULA_BY_ATOMS.items():
                if element in ('C', 'H', 'N', 'O'):
                    continue
                BONUS_STRING += element + (main.subscript(str(count)) if count > 1 else "")
            main.draw_text(image, (3600,2610), BONUS_STRING, 'black', 80)


        # Analysemethoden
        if analysis_method['gcms']: main.draw_text(image, (335,3758), 'x', 'black', 80) # GC/MS
        if analysis_method['gcms_ei']: main.draw_text(image, (2304,3758), 'x', 'black', 80) # GC/MS EI
        if analysis_method['gcms_ci']: main.draw_text(image, (2746,3758), 'x', 'black', 80) # GC/MS CI
        if analysis_method['gcms_ci_methan']: main.draw_text(image, (3100,3773), 'x', 'black', 80) # GC/MS CI Methan
        if analysis_method['gcms_ci_isobutan']: main.draw_text(image, (3493,3773), 'x', 'black', 80) # GC/MS CI Isobutan

        if analysis_method['direct']: main.draw_text(image, (335,4074), 'x', 'black', 80) # Direktverdampfung
        if analysis_method['direct_dip']: main.draw_text(image, (532,4226), 'x', 'black', 80) # Direktverdampfung DIP
        if analysis_method['direct_dci']: main.draw_text(image, (1122,4226), 'x', 'black', 80) # Direktverdampfung DCI
        if analysis_method['direct_ei']: main.draw_text(image, (2304,4074), 'x', 'black', 80) # Direktverdampfung EI
        if analysis_method['direct_ci']: main.draw_text(image, (2746,4074), 'x', 'black', 80) # Direktverdampfung CI
        if analysis_method['direct_ci_methan']: main.draw_text(image, (3100,4088), 'x', 'black', 80) # Direktverdampfung CI Methan
        if analysis_method['direct_ci_isobutan']: main.draw_text(image, (3493,4088), 'x', 'black', 80) # Direktverdampfung CI Isobutan

        if analysis_method['lcms']: main.draw_text(image, (335,4397), 'x', 'black', 80) # LC/MS
        if analysis_method['lcms_esi']: main.draw_text(image, (2304,4397), 'x', 'black', 80) # LC/MS ESI
        if analysis_method['lcms_ci']: main.draw_text(image, (2746,4397), 'x', 'black', 80) # LC/MS CI
        if analysis_method['lcms_ci_pos']: main.draw_text(image, (3188,4407), 'x', 'black', 80) # LC/MS CI pos
        if analysis_method['lcms_ci_neg']: main.draw_text(image, (3472,4407), 'x', 'black', 80) # LC/MS CI neg

        if analysis_method['hrms']: main.draw_text(image, (335,4815), 'x', 'black', 80) # HRMS
        if analysis_method['hrms_ei']: main.draw_text(image, (1657,4815), 'x', 'black', 80) # HRMS EI
        if analysis_method['hrms_lcms']: main.draw_text(image, (1958,4815), 'x', 'black', 80) # HRMS LC/MS


        date_today = date.today().isoformat()
        main.draw_text(image, (300,5100), date_today, 'black', 80) # Date


        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        output_path = os.path.join('output', f'mass_form_filled_{timestamp}.png')
        image.save(output_path)
        print(f'Image saved at {output_path}')
