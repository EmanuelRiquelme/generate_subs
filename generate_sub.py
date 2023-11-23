import json
import textwrap

def create_subtitle(name_file):
    title = name_file 
    fontname = "Arial"
    fontsize = 20
    primary_color = "&H00FFFFFF"
    secondary_color = "&H0000FFFF"
    tertiary_color = "&H00000000"
    back_color = "&H80000000"

    ssa_content = textwrap.dedent(f"""\
        [Script Info]
        Title: {title}
        ScriptType: v4.00+

        [V4+ Styles]
        Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, TertiaryColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, AlphaLevel, Encoding
        Style: Default,{fontname},{fontsize},{primary_color},{secondary_color},{tertiary_color},{back_color},-1,0,1,3,0,2,20,20,10,0,0
        [Events]
        Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
    """)

    with open('name_file.ssa', 'w', encoding='utf-8') as file:
        file.write(ssa_content)

    print("SSA file created successfully.")

def add_subtitle(name_file,json_file):
    json_file = json.loads(json_file)
    start = json_file['Start']
    end = json_file['End']
    text = json_file['Text']
    subtitle = textwrap.dedent(f"""\
    Dialogue: 0,{start},{end},Default,,0000,0000,0000,,{text}
        """)
    with open(f'{name_file}.ssa', 'a', encoding='utf-8') as file:
        file.write(subtitle)
    print('subtitle added!')

def format_seconds(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{int(hours):d}:{int(minutes):02d}:{seconds:05.2f}'

def generate_json(start,end,text):
    start,end = format_seconds(start),format_seconds(end)
    json_file = {
       "Start": start, 
       "End":  end,
       'Text': text,
       }
    return json.dumps(json_file, indent=2)
