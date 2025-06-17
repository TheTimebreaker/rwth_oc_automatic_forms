import tkinter as tk
import os
import urllib
import urllib.error
from datetime import date, datetime

import cirpy #type:ignore
import molmass
from PIL import Image

import main


# def checkbox_methods() -> dict:
#     """Function that opens a window for conditional checkboxes

#     Args:
#         fields (list[str])

#     Returns:
#         dict: Results
#     """
#     def submit_and_close():
#         def submit_recursively(option:dict[str, dict]):
#             for label, var in option.items():
#                 assert isinstance(var['main'], tk.IntVar)
#                 results[label] = var['main'].get()
#                 if 'subs' in var.keys():
#                     assert isinstance(var['subs'], dict)
#                     submit_recursively(var['subs'])
#         submit_recursively(options)
#         root.quit()
#         root.destroy()
#     def add_checkbox(option:dict[str, dict], indent:int = 0):
#         for name, content in option.items():
#             checkbox = tk.Checkbutton(
#                 root,
#                 text = name,
#                 variable = content['main'],
#                 command = update_condition_state_entry
#             )
#             checkbox.pack(anchor='w', padx= indent)
#             if 'subs' in content.keys():
#                 add_checkbox(content['subs'], indent= indent+20)
#     def update_condition_state_entry():
#         """Recursively updates the checkboxes to respect the conditional relationship"""
#         def update_condition_state(
#                 option:dict[str, dict[str, tk.IntVar|dict]],
#                 parent_value:int|bool
#             ):
#             for content in option.values():
#                 assert isinstance(content['main'], tk.IntVar)
#                 if not parent_value:
#                     content['main'].set(0)
#                 if 'subs' in content.keys():
#                     assert isinstance(content['subs'], dict)
#                     update_condition_state(content['subs'], parent_value= content['main'].get())
#         update_condition_state(options, True)

#     root = tk.Tk()
#     root.title("Select Options")

#     options = {
#         'gcms': {
#             'main': tk.IntVar(),
#             'subs': {
#                 'gcms_ei': {
#                     'main': tk.IntVar(),
#                 },
#                 'gcms_ci': {
#                     'main': tk.IntVar(),
#                     'subs': {
#                         'gcms_ci_methan': {
#                             'main': tk.IntVar(),
#                         },
#                         'gcms_ci_isobutan': {
#                             'main': tk.IntVar(),
#                         },
#                     },
#                 },
#             }
#         },
#         'direct': {
#             'main': tk.IntVar(),
#             'subs': {
#                 'direct_ei': {
#                     'main': tk.IntVar(),
#                 },
#                 'direct_ci': {
#                     'main': tk.IntVar(),
#                     'subs': {
#                         'direct_ci_methan': {
#                             'main': tk.IntVar(),
#                         },
#                         'direct_ci_isobutan': {
#                             'main': tk.IntVar(),
#                         },
#                     },
#                 },
#                 'direct_dip': {
#                     'main': tk.IntVar(),
#                 },
#                 'direct_dci': {
#                     'main': tk.IntVar(),
#                 },
#             },
#         },
#         'lcms': {
#             'main': tk.IntVar(),
#             'subs': {
#                 'lcms_esi': {
#                     'main': tk.IntVar(),
#                 },
#                 'lcms_ci': {
#                     'main': tk.IntVar(),
#                     'subs': {
#                         'lcms_ci_pos': {
#                             'main': tk.IntVar(),
#                         },
#                         'lcms_ci_neg': {
#                             'main': tk.IntVar(),
#                         },
#                     },
#                 },
#             },
#         },
#         'hrms': {
#             'main': tk.IntVar(),
#             'subs': {
#                 'hrms_ei': {
#                     'main': tk.IntVar(),
#                 },
#                 'hrms_lcms': {
#                     'main': tk.IntVar(),
#                 }
#             }
#         }
#     }

#     results:dict = {}
#     add_checkbox(options)

#     submit_btn = tk.Button(root, text="Submit", command=submit_and_close)
#     submit_btn.pack(pady=10)

#     root.mainloop()
#     return results


if __name__ == '__main__':
    # freetexts = main.freetext_fields([
    #         "name",
    #         "workgroup",
    #         "sample_name",
    #         "phone_number",
    #         'melting_point',
    #         'boiling_point',
    #         'purity',
    #         'purity_method',
    #         'smiles'
    #     ])
    freetexts = {
            "name": 'name',
            "workgroup": 'WG',
            "sample_name": 'sample',
            "phone_number": '94681',
            'melting_point': 'MP',
            'boiling_point': 'BP',
            'purity': 'PURITY',
            'purity_method': 'PM',
            'smiles': 'C1=CC=CC=C1'
    }
    if not freetexts['workgroup'].lower().startswith('ak '):
        freetexts['workgroup'] = f'AK {freetexts['workgroup']}'

    # properties = main.checkbox_fields([
    #         'solid',
    #         'liquid',
    #         'sirup',
    #         'hygroscopic',
    #         'volatile',
    #         'toxic',
    #         'skin-irritating',
    #         'eye-irritating'
    #     ])
    properties = {
            'solid':True,
            'liquid':True,
            'sirup':True,
            'hygroscopic':True,
            'volatile':True,
            'toxic':True,
            'skin-irritating':True,
            'eye-irritating':True
    }

    analysis_method = {
        'capillary': True,
        'kbr': True,
        'u-atr': True,
        'solution_cdcl3': True,
        'solution_chcl3': True,
        'solution_solvent': 'DCM',
    }#checkbox_methods()


    with Image.open('base_forms/ir.png') as image:
        image = image.convert('RGBA')
        main.draw_text(image, (1514,810-83), f'{freetexts['name']} / {freetexts['workgroup']}', 'black', 80) # Name und Arbeitskreis
        main.draw_text(image, (1110,1015-83), freetexts['sample_name'], 'black', 80) # Substanzbezeichnung
        main.draw_text(image, (3455,810-83), '', 'black', 80) # lfd. nummer
        main.draw_text(image, (3455,1015-83), freetexts['phone_number'], 'black', 80) # Tel.Nr.


        # Eigenschaften
        if properties['solid']: main.draw_text(image, (880,1300-83-22), 'x', 'black', 80)
        if properties['liquid']: main.draw_text(image, (880,1425-83-22), 'x', 'black', 80)
        if properties['sirup']: main.draw_text(image, (880,1548-83-22), 'x', 'black', 80)
        if properties['hygroscopic']: main.draw_text(image, (880,1675-83-22), 'x', 'black', 80)
        if properties['volatile']: main.draw_text(image, (880,1800-83-22), 'x', 'black', 80)
        if properties['toxic']: main.draw_text(image, (2795,1300-83-22), 'x', 'black', 80)
        if properties['skin-irritating']: main.draw_text(image, (2795,1425-83-22), 'x', 'black', 80)
        if properties['eye-irritating']: main.draw_text(image, (2795,1548-83-22), 'x', 'black', 80)


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
            main.draw_molecule(image, (400, 2800), (2100, 810), SMILES)


        # Analysemethoden
        if analysis_method['capillary']: main.draw_text(image, (907,4270), 'x', 'black', 80)

        if analysis_method['kbr']: main.draw_text(image, (907,4436), 'x', 'black', 80)
 
        if analysis_method['u-atr']: main.draw_text(image, (907,4604), 'x', 'black', 80)

        if analysis_method['solution_cdcl3']: main.draw_text(image, (3065,4270), 'x', 'black', 80)

        if analysis_method['solution_chcl3']: main.draw_text(image, (3065,4436), 'x', 'black', 80)

        if analysis_method['solution_solvent']: main.draw_text(image, (3065,4604), 'x', 'black', 80)
        # if analysis_method['solution_solvent']: main.draw_text(image, (335,4815), 'x', 'black', 80)


        date_today = date.today().isoformat()
        main.draw_text(image, (300,5100), date_today, 'black', 80) # Date

        image.show()
        input('...')

        # timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        # output_path = os.path.join('output', f'infrared_form_filled_{timestamp}.png')
        # image.save(output_path)
        # print(f'Image saved at {output_path}')
