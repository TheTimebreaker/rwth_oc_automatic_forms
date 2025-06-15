from PIL import Image, ImageDraw, ImageFont, ImageChops
import time, molmass, chemdraw, io, cirpy

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
        position:tuple[int,int] = (0,0),
        text:str = "hello world",
        text_color:tuple[int,int,int]|str = "black",
        text_size:int = 100
        ) -> None:
    draw = ImageDraw.Draw(img)
    draw_text_font:ImageFont.FreeTypeFont = ImageFont.truetype('fonts/arial.ttf', size= text_size)

    draw.text(
        position,
        text,
        fill= text_color,
        font = draw_text_font
    )

def crop_to_content(img:Image.Image, bg_color="white"):
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

    with Image.open(io.BytesIO(molecule_bytes)) as b:
        overlay_img = b.convert('RGB')
        overlay_img = crop_to_content(overlay_img, 'white')

        # resizes to make sure image does not exceed the maximum allowed height/width
        max_width, max_height = max_width_height
        original_width, original_height = overlay_img.size
        ratio = min(max_width / original_width, max_height / original_height)
        ratio = min(ratio, 2) #limits maximum scale up
        new_size = (int(original_width * ratio), int(original_height * ratio))
        overlay_img = overlay_img.resize(new_size, Image.LANCZOS)

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

