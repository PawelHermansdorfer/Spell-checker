from turtle import update
import PySimpleGUI as sg
from spellchaker import SpellChecker


TEXT_FILE_PATH = 'text.txt'
NUMBER_OF_COMBO = 50

sg.SetOptions(font='any 11')
layout = [[sg.Text('Place your text here', key='-TITLE-', font='any 16')],
          [sg.Multiline(key='-INPUT_TEXT-', size=(100, 10))],
          [sg.Button('CHECK', key='-CHECK_BUTTON-', size=(10, 2))],
          [sg.ProgressBar(50, key='-PROGRESS_BAR-', size=(70, 20),
                          border_width=(5), orientation='h', visible=False)]
]

for i in range(NUMBER_OF_COMBO):
    layout.append([
        sg.Column([[
            sg.Text('', key=f'-WORD_{i}-', visible=False),
            sg.Combo('', visible=False, enable_events=True,
                     key=f'-COMBO_{i}-', size=(10, 1))
        ]])
    ])

WINDOW = sg.Window('Spell checker', layout,
                   element_justification='c', margins=(10,2),
                   element_padding=1, finalize=False)

combos_words = {}


def main():   
    while True:
        event, values = WINDOW.read()

        match event:
            case sg.WIN_CLOSED:
                WINDOW.close()
                break
            
            case '-CHECK_BUTTON-':
                for i in range(NUMBER_OF_COMBO):
                    WINDOW[f'-WORD_{i}-'].update(visible=False)
                    WINDOW[f'-COMBO_{i}-'].update(visible=False)
                WINDOW['-PROGRESS_BAR-'].update(current_count=0)
                    
                    
                text_input = values['-INPUT_TEXT-']
                spell_checker = SpellChecker(text_input,
                                             window=WINDOW,
                                             progress_bar_key='-PROGRESS_BAR-')
                corrections = spell_checker.check_text()
                WINDOW['-PROGRESS_BAR-'].update(visible=False)
                
                combo_id = 0
                for i, word in enumerate(text_input.split(' ')):
                    if len(corrections[i]) > 0:
                        WINDOW[f'-WORD_{combo_id}-'].update(value=word,
                                                            visible=True)
                        WINDOW[f'-COMBO_{combo_id}-'].update(
                            values=corrections[i], visible=True)
                        
                        combos_words[f'-COMBO_{combo_id}-'] = i
                        
                        combo_id += 1
                        
                WINDOW['-TITLE-'].update('Check corrections')
            
            case _:
                if event.startswith('-COMBO_'):
                    change_id = combos_words[event]
                    
                    separated_words = values['-INPUT_TEXT-'].split(' ')
                    new_text = separated_words[0:change_id]
                    new_text.append(values[event])
                    if len(separated_words) > change_id:
                        new_text.extend(separated_words[change_id+1:])
                    new_text = ' '.join(new_text)

                    WINDOW['-INPUT_TEXT-'].update(value=new_text)


if __name__ == '__main__':
    main()