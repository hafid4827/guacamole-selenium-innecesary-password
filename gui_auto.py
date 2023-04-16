from constant import FLAG_SELENIUM
from selenium_auto import exe
from PySimpleGUI import (
    Text,
    theme,
    Button,
    Window,
    InputText,
    Checkbox,
    Slider,
    WIN_CLOSED
)


from multiprocessing import Pipe, Process

# LOOK_AND_FEEL_TABLE

# All the stuff inside your window.


def layout_main():
    layout = [
        [Text('seguridad:'), Text('', key="-output_security-")],
        [Text('longitud:'), Text('', key="-len_password-")],
        [Text('contrasena:'), InputText("", key="-output_password-")],
        [
            Checkbox(text="lo que sea", default=False, key="-ABC-"),
            Checkbox(text="lo que sea", default=False, key="-abc-"),
            Checkbox(text="lo que sea", default=False, key="-number-"),
            Checkbox(text="lo que sea", default=False, key="-specials-")
        ],
        [
            Slider(
                range=(1, 50),
                default_value=15,
                enable_events=True,
                orientation="horizontal",
                expand_x=True
            )
        ],
        [
            Button('start', key="-start-"),
            Button('update data', key="-update_data-"),
            Button('new data', key="-new_data-"),
            Button('reload permanent', key="-reload_permanent-"),
        ]
    ]
    return layout


def windows_object(
    layout: list,
    title: str = "Window Title",
    select_theme: str = "DarkAmber"
):
    theme(select_theme)   # Add a touch of color
    window = Window(title, layout)
    return window

# Create the Window

# Event Loop to process "events" and get the "values" of the inputs


def rendering_logic():
    layout = layout_main()
    window = windows_object(layout=layout)
    receptor, transmisor = Pipe()
    while True:
        event, values = window.read()

        if event == "-start-":
            target = Process(target=exe, args=(transmisor,))
            target.start()
            # window['-start-'].update(disabled=True)
            # window['-update-'].update(disabled=True)

        if event == "-update_data-":
            result = receptor.recv()
            print(result, "=> esto es qui el print XD")
            result_selected_id = result['_CHECKBOX_LIST_ID']
            for item_result_selected in result_selected_id:
                extract_password = result_selected_id[item_result_selected]
                if extract_password == "true":
                    window[f"-{item_result_selected}-"].update(value=True)
                else:
                    window[f"-{item_result_selected}-"].update(value=False)

            result_checkbox_child = result['_CHECKBOX_LIST']
            for item_result_checkbox in result_checkbox_child:
                text_value = result_checkbox_child[item_result_checkbox]
                window[f'-{item_result_checkbox}-'].update(text=text_value)

            result_selected_child = result['_SELECT_DICT']
            for item_result_selected in result_selected_child:
                extract_password = result_selected_child[item_result_selected]
                window[f"-{item_result_selected}-"].update(extract_password)

        if event == WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break

    window.close()


if __name__ == "__main__":
    rendering_logic()
