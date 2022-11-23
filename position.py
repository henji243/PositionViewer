import PySimpleGUI as sg
from pyautogui import position as mouse_position
import pyperclip
import keyboard


module_name = [[sg.T("PyAutoGUIの名前:"),
                sg.Input(default_text="pyautogui", s=(15, 1), font=("meiryo", 10),
                         k="-MODULE_NAME-", disabled=True, use_readonly_for_disable=True)],
               [sg.T("カスタム:"),
                sg.Column([[sg.Input(s=(15, 1), disabled_readonly_background_color="grey70",
                            font=("meiryo", 10), k="-CUSTOM_FUNC-")]], justification="right")],
               [sg.Button("コピーを一時停止", k="-PAUSED-")]
]

FUNC_NAMES = ("click", "rightClick", "doubleClick", "moveTo", "dragTo",
                "scroll", "tripleClick", "screenshot", "カスタム...")
options_layout = [
    [sg.Listbox(FUNC_NAMES, default_values="click", s=(12, 4), font=("meiryo", 12),
                k="-COPY_OPTION-", highlight_background_color="#0078d7"),
     sg.Column(module_name, vertical_alignment="top")]
]

layout = [[sg.T("現在のカーソルの座標", font=("meiryo", 14))],
          [sg.Column([[sg.T(font=("meiryo", 22), k="-POSITION-")]],
                     justification="c")],
          [sg.Frame("コピー設定", options_layout)],
          [sg.Quit(k="-QUIT-")]]

window = sg.Window("Position Viewer", layout, resizable=True, keep_on_top=True, finalize=True)

paused = False
pause_button_pushed = False
window["-MODULE_NAME-"].block_focus()

while True:
    event, values = window.read(timeout=0)
    if event == sg.WIN_CLOSED or event == "-QUIT-":
        break

    position = str(mouse_position())[5:]
    window["-POSITION-"].update(position)

    if event == "-PAUSED-":
        pause_button_pushed = not pause_button_pushed
        if pause_button_pushed:
            window["-MODULE_NAME-"].update(disabled=False)
            window["-MODULE_NAME-"].set_focus()
            window["-PAUSED-"].update("一時停止中")
        else:
            window["-MODULE_NAME-"].update(disabled=True)
            window["-MODULE_NAME-"].block_focus()
            window["-PAUSED-"].update("コピーを一時停止")

    # 関数名を変えるときの処理
    customized = values["-COPY_OPTION-"][0] == "カスタム..."
    if not values["-CUSTOM_FUNC-"] == "":
        selected_text = values["-CUSTOM_FUNC-"]
        paused = False
    elif customized:
        paused = True
    else:
        selected_text = values["-COPY_OPTION-"][0]
        paused = False

    window["-CUSTOM_FUNC-"].update(disabled=not customized)

    if (keyboard.is_pressed("c")) and (not paused) and (not pause_button_pushed):
        copy_text = f"{values['-MODULE_NAME-']}.{selected_text}{position}"
        if not pyperclip.paste() == copy_text:
            pyperclip.copy(copy_text)

window.close()
