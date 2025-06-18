import io
import tkinter as tk
from typing import Callable
import molmass #type:ignore
import chemdraw #type:ignore
from PIL import Image, ImageDraw, ImageFont, ImageChops


def translate_by_dict(text:str, translation_map:dict[str, str]) -> str:
    """Translates a string by using a dictionary as a translation map.

    Returns:
        str: Translated string.
    """
    trans = str.maketrans(
    ''.join(translation_map.keys()),
    ''.join(translation_map.values()))
    return text.translate(trans)
def subscript(text:str) -> str:
    """Turns any string inputted into subscript (ₛᵤ♭ₛ꜀ᵣᵢₚₜ)."""
    subscript_map = {
        "0": "\u2080", "1": "\u2081", "2": "\u2082", "3": "\u2083", "4": "\u2084", "5": "\u2085", "6": "\u2086",
        "7": "\u2087", "8": "\u2088", "9": "\u2089", "a": "ₐ", "b": "♭", "c": "꜀", "d": "ᑯ",
        "e": "ₑ", "f": "բ", "g": "₉", "h": "ₕ", "i": "ᵢ", "j": "ⱼ", "k": "ₖ",
        "l": "ₗ", "m": "ₘ", "n": "ₙ", "o": "ₒ", "p": "ₚ", "q": "૧", "r": "ᵣ",
        "s": "ₛ", "t": "ₜ", "u": "ᵤ", "v": "ᵥ", "w": "w", "x": "ₓ", "y": "ᵧ",
        "z": "₂", "A": "ₐ", "B": "₈", "C": "C", "D": "D", "E": "ₑ", "F": "բ",
        "G": "G", "H": "ₕ", "I": "ᵢ", "J": "ⱼ", "K": "ₖ", "L": "ₗ", "M": "ₘ",
        "N": "ₙ", "O": "ₒ", "P": "ₚ", "Q": "Q", "R": "ᵣ", "S": "ₛ", "T": "ₜ",
        "U": "ᵤ", "V": "ᵥ", "W": "w", "X": "ₓ", "Y": "ᵧ", "Z": "Z", "+": "₊",
        "-": "₋", "=": "₌", "(": "₍", ")": "₎"}
    return translate_by_dict(text, subscript_map)
def superscript(text:str) -> str:
    """Turns any string inputted into superscript (ˢᵘᵖᵉʳˢᶜʳᶦᵖᵗ)."""
    superscript_map = {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
        "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
        "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
        "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
        "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
        "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
        "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
        "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
        "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
        "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"}
    return translate_by_dict(text, superscript_map)


def draw_text(
        img:Image.Image,
        position:tuple[int,int] | tuple[int,int,int,int] = (0,0),
        text:str = "hello world",
        text_color:tuple[int,int,int]|str = "black",
        text_size:int = 100,
        text_alignment:str = 'la'
        ) -> None:
    """Draws text onto an image at given position. Changes image in-place, so no returns.

    Args:
        img (Image.Image): Image object
        position (tuple[int,int], optional): X/Y position where the text gets drawn. Defaults to (0,0).
        text (str, optional): The actual text. Defaults to "hello world".
        text_color (tuple[int,int,int] | str, optional): Color of drawn text. Defaults to "black".
        text_size (int, optional): Font size of drawn text. Defaults to 100.
    """
    draw = ImageDraw.Draw(img)
    draw_text_font:ImageFont.FreeTypeFont = ImageFont.truetype('fonts/DejaVuSans.ttf', size= text_size)

    draw.text(
        position,
        text,
        fill = text_color,
        font = draw_text_font,
        anchor= text_alignment
    )

def crop_to_content(img:Image.Image, bg_color="white"):
    """Crops an image to the content, cutting off background that extends beyond the non-bg pixels.

    Args:
        img (Image.Image): Image object
        bg_color (str, optional): Background color that the image should get afterwards. Defaults to "white".

    Returns:
        _type_: _description_
    """
    # Create a background image of the same size and color
    bg = Image.new("RGB", img.size, bg_color)

    # Find the bounding box of the difference between the image and background
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()

    if bbox:
        cropped = img.crop(bbox)
        return cropped
    return img

def draw_molecule(
        img:Image.Image,
        position:tuple[int,int] = (0,0),
        max_width_height:tuple[int,int] = (2100, 810),
        smiles:str = "CC(C)=O"
    ) -> None:
    """Draws molecule onto an image.

    Args:
        img (Image.Image): Image object of image the molecule will be drawn onto.
        position (tuple[int,int], optional): Position where the molecule will be placed in pixels (x,y). Defaults to (0,0).
        max_width_height (tuple[int,int], optional): Maximum (width, height) that the molecule will be scaled to. Defaults to (2100, 810).
        smiles (str, optional): SMILES code of molecule. Defaults to "CC(C)=O".
    """
    drawer = chemdraw.Drawer(smiles)
    molecule_bytes = drawer.draw().to_image()

    with Image.open(io.BytesIO(molecule_bytes)) as molecule:
        overlay_img = molecule.convert('RGB')
        overlay_img = crop_to_content(overlay_img, 'white')

        # resizes to make sure image does not exceed the maximum allowed height/width
        max_width, max_height = max_width_height
        original_width, original_height = overlay_img.size
        ratio = min(max_width / original_width, max_height / original_height)
        ratio = min(ratio, 2) #limits maximum scale up
        new_size = (int(original_width * ratio), int(original_height * ratio))
        overlay_img = overlay_img.resize(new_size, Image.LANCZOS) #type:ignore #pylint:disable=no-member
        overlay_img = overlay_img.convert('RGBA')

        # img = img.convert('RGBA')
        img.paste(overlay_img, position)

def molecule_sumformula_by_atom(sum_formula:str) -> dict[str, int]:
    """Splits a molecule sum formula into a dictionary, so each element can be easily looked up.

    Args:
        sum_formula (str): Sum formula as string.

    Returns:
        dict[str, int]: Keys: Element (e.g. C). Values: Count of that element in the sum formula.
    """
    res:dict[str, int] = {}
    try:
        formula = molmass.Formula(sum_formula)
        for element in formula.composition():
            res[element] = formula.composition()[element].count
    except molmass.FormulaError:
        print('ERROR - Invalid formula.')
        return {}
    return res

def molecule_masspercent_by_atom(sum_formula:str) -> dict[str, float]:
    """Returns a by-element dict for the mass% of each atom from the total mass (for elemental analysis).

    Args:
        sum_formula (str): Sum formula as string.

    Returns:
        dict[str, int]: Keys: Element (e.g. C). Values: Mass% of element as decimal.
    """
    res:dict[str, float] = {}
    formula = molmass.Formula(sum_formula)
    total_mass = formula.mass
    for element in formula.composition():
        res[element] = (formula.composition()[element].count * molmass.ELEMENTS[element].mass) / total_mass
    return res



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



def mixed_fields(fields:dict[str, Callable]) -> dict:
    """Function that opens a window for mixed fields (checkboxes and text enter fields)

    Args:
        fields (dict[str, Callable]): Dictionary of requested fields. Key: Name of field and key in the results dict. Value: Callable that determines the type of field. Bool = checkbox; str = Text field

    Returns:
        dict: Results dict that uses the fields keys as keys
    """
    def submit_and_close():
        for label, var in field_values.items():
            results[label] = var.get()
        root.quit()
        root.destroy()
    root = tk.Tk()
    root.title("Select Options")

    results:dict[str, str] = {}
    field_values = {}

    for field, fieldtype in fields.items():
        if fieldtype is bool:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(root, text=field, variable=var)
            cb.pack(anchor="w")
            field_values[field] = var
        elif fieldtype is str:
            var = tk.StringVar(root)
            label = tk.Label(root, text= str(field))
            element = tk.Entry(root, textvariable= var)
            label.pack(anchor='w')
            element.pack(anchor='w')
            field_values[field] = var

    submit_btn = tk.Button(root, text="Submit", command=submit_and_close)
    submit_btn.pack(pady=10)

    root.mainloop()
    return results
