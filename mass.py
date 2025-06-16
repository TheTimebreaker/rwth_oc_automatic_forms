import tkinter as tk
import urllib
import urllib.error
from datetime import date, datetime
from main import *

def freetext_fields(fields:list[str]):
    def handle_tkiner():
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
    submit_button = tk.Button(root, text="Submit", command=handle_tkiner)
    submit_button.pack(pady=10)

    # Run the main loop
    root.mainloop()
    return results

def checkbox_fields(fields:list[str]):
    def submit_and_close():
        for label, var in checkboxes.items():
            results[label] = var.get()
        root.quit()
        root.destroy()

    root = tk.Tk()
    root.title("Select Options")
    
    results = {}
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

# def checkbox_properties():
#     """Window for properties"""
#     options = [
#         'solid',
#         'liquid',
#         'sirup',
#         'hygroscopic',
#         'volatile',
#         'toxic',
#         'skin-irritating',
#         'eye-irritating'
#     ]
#     selected = {}

#     def submit_and_close():
#         selected["choice"] = var.get()
#         root.quit()
#         root.destroy()

#     root = tk.Tk()
#     root.title("Choose an Option")

#     var = tk.StringVar(value=options[0])  # Default selection

#     for option in options:
#         rb = tk.Radiobutton(root, text=option, variable=var, value=option)
#         rb.pack(anchor="w")

#     submit_btn = tk.Button(root, text="Submit", command=submit_and_close)
#     submit_btn.pack(pady=10)

#     root.mainloop()
#     return selected["choice"]

def checkbox_methods():
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
            checkbox = tk.Checkbutton(root, text= name, variable= content['main'], command= update_condition_state_entry)
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
                'hrms_esi': {
                    'main': tk.IntVar(),
                },
                'hrms_ci': {
                    'main': tk.IntVar(),
                }
            }
        }
    }

    results = {}
    add_checkbox(options)


    submit_btn = tk.Button(root, text="Submit", command=submit_and_close)
    submit_btn.pack(pady=10)

    root.mainloop()
    return results


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
    draw_text(image, (1580,1100), f'{freetexts['name']} / {freetexts['workgroup']}', 'black', 80) # Name und Arbeitskreis
    draw_text(image, (1150,1370), freetexts['sample_name'], 'black', 80) # Substanzbezeichnung
    draw_text(image, (3140,1100), '', 'black', 80) # lfd. nummer
    draw_text(image, (3140,1370), freetexts['phone_number'], 'black', 80) # Tel.Nr.


    # Eigenschaften
    if properties['solid']: draw_text(image, (1075,1586), 'x', 'black', 80)
    if properties['liquid']: draw_text(image, (1075,1730), 'x', 'black', 80)
    if properties['sirup']: draw_text(image, (1075,1874), 'x', 'black', 80)
    if properties['hygroscopic']: draw_text(image, (1075,2018), 'x', 'black', 80)
    if properties['volatile']: draw_text(image, (1075,2161), 'x', 'black', 80)
    if properties['toxic']: draw_text(image, (2657,1586), 'x', 'black', 80)
    if properties['skin-irritating']: draw_text(image, (2657,1730), 'x', 'black', 80)
    if properties['eye-irritating']: draw_text(image, (2657,1874), 'x', 'black', 80)


    draw_text(image, (2000,1580), f'{freetexts['melting_point']}°C' if freetexts['melting_point'] else '', 'black', 80) # melting point
    draw_text(image, (2000,1725), f'{freetexts['boiling_point']}°C' if freetexts['boiling_point'] else '', 'black', 80) # boiling point


    draw_text(image, (3050,2155), freetexts['solvent'], 'black', 80) # Lösungsmittel


    # Reinheitsgrad
    draw_text(image, (990,2380), freetexts['purity'], 'black', 80) # Reinheit
    draw_text(image, (2165,2380), freetexts['purity_method'], 'black', 80) # Methode


    # Molekül
    SMILES = freetexts['smiles']
    if not SMILES:
        print('ERROR - No SMILES code given, you need to do sumformula and molar mass yourself!')
    else:
        try:
            FORMULA = cirpy.resolve(SMILES, 'formula')
        except urllib.error.HTTPError:
            print('ERROR - Cirpy server unavailable, you need to do sumformula and molar mass yourself!')
            FORMULA = ''
        FORMULA_BY_ATOMS = molecule_sumformula_by_atom(FORMULA)
        draw_molecule(image, (400, 2800), (2100, 810), SMILES)

        # C H N O ...
        if 'C' in FORMULA_BY_ATOMS:
            draw_text(image, (2720,2920), str(FORMULA_BY_ATOMS['C']), 'black', 60)
        if 'H' in FORMULA_BY_ATOMS:
            draw_text(image, (2960,2920), str(FORMULA_BY_ATOMS['H']), 'black', 60)
        if 'N' in FORMULA_BY_ATOMS:
            draw_text(image, (3210,2920), str(FORMULA_BY_ATOMS['N']), 'black', 60)
        if 'O' in FORMULA_BY_ATOMS:
            draw_text(image, (3440,2920), str(FORMULA_BY_ATOMS['O']), 'black', 60)
        BONUS_STRING = ''
        for element, count in FORMULA_BY_ATOMS.items():
            if element in ('C', 'H', 'N', 'O'):
                continue
            BONUS_STRING += element + (str(count) if count > 1 else "") + " "
        draw_text(image, (2660,3020), BONUS_STRING, 'black', 80)

        # Molmasse
        mass = molmass.Formula(FORMULA).monoisotopic_mass
        draw_text(image, (3050,3230), str(round(mass, 5)), 'black', 80)


    # Analysemethoden
    if analysis_method['gcms']: draw_text(image, (350,3977), 'x', 'black', 80) # GC/MS
    if analysis_method['gcms_ei']: draw_text(image, (2426,3977), 'x', 'black', 80) # GC/MS EI
    if analysis_method['gcms_ci']: draw_text(image, (2820,3977), 'x', 'black', 80) # GC/MS CI
    if analysis_method['gcms_ci_methan']: draw_text(image, (3129,3981), 'x', 'black', 80) # GC/MS CI Methan
    if analysis_method['gcms_ci_isobutan']: draw_text(image, (3457,3981), 'x', 'black', 80) # GC/MS CI Isobutan

    if analysis_method['direct']: draw_text(image, (350,4198), 'x', 'black', 80) # Direktverdampfung
    if analysis_method['direct_dip']: draw_text(image, (513,4308), 'x', 'black', 80) # Direktverdampfung DIP
    if analysis_method['direct_dci']: draw_text(image, (1388,4308), 'x', 'black', 80) # Direktverdampfung DCI
    if analysis_method['direct_ei']: draw_text(image, (2426,4198), 'x', 'black', 80) # Direktverdampfung EI
    if analysis_method['direct_ci']: draw_text(image, (2820,4198), 'x', 'black', 80) # Direktverdampfung CI
    if analysis_method['direct_ci_methan']: draw_text(image, (3129,4202), 'x', 'black', 80) # Direktverdampfung CI Methan
    if analysis_method['direct_ci_isobutan']: draw_text(image, (3457,4202), 'x', 'black', 80) # Direktverdampfung CI Isobutan

    if analysis_method['lcms']: draw_text(image, (350,4418), 'x', 'black', 80) # LC/MS
    if analysis_method['lcms_esi']: draw_text(image, (2426,4418), 'x', 'black', 80) # LC/MS ESI
    if analysis_method['lcms_ci']: draw_text(image, (2820,4418), 'x', 'black', 80) # LC/MS CI
    if analysis_method['lcms_ci_pos']: draw_text(image, (3129,4422), 'x', 'black', 80) # LC/MS CI pos
    if analysis_method['lcms_ci_neg']: draw_text(image, (3457,4422), 'x', 'black', 80) # LC/MS CI neg

    if analysis_method['hrms']: draw_text(image, (350,4748), 'x', 'black', 80) # HRMS
    if analysis_method['hrms_esi']: draw_text(image, (1598,4748), 'x', 'black', 80) # HRMS EI
    if analysis_method['hrms_ci']: draw_text(image, (1875,4748), 'x', 'black', 80) # HRMS LC/MS


    date_today = date.today().isoformat()
    draw_text(image, (400,5050), date_today, 'black', 80) # Date


    image.show()
    time.sleep(10)
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    image.save(f'output/mass_form_filled_{timestamp}.png')
