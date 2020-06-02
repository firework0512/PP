# El tercer clon - Gui
# Se han considerado los estándares de nomenclatura del Python en la realización de esta práctica :
# https://www.python.org/dev/peps/pep-0008/
# autores : Mario Ramos Diez
#           Weihua Weng
# Github link de este proyecto : https://github.com/firework0512/PP
# Branch gui-version
import os

import wx

from GameConfig import GameConfig
from GameOperations import create_random_obstacles, do_pie_operation, change_mode, save, read_file, is_possible_move
from Widgets import NewGameDialog, ClonGridSizer


class ClonFrame(wx.Frame):
    # Solo lo guardamos en formato .txt
    WILDCARD = "Text file (*.txt)|*.txt|" \
               "All files (*.*)|*.*"

    def __init__(self, game_config: GameConfig):
        # begin wxGlade: ClonFrame.__init__
        super(ClonFrame, self).__init__(None)
        self.game_config = game_config
        self.SetSize((450, 450))

        # Tool Bar
        self.toolbar = wx.ToolBar(self, -1)
        self.SetToolBar(self.toolbar)
        self.toolbar.AddTool(1, "new_game", wx.Bitmap("Images/new.png", wx.BITMAP_TYPE_ANY),
                             wx.NullBitmap, wx.ITEM_NORMAL, "", "Creates a new game")
        self.toolbar.AddTool(2, "open_file", wx.Bitmap("Images/open.png", wx.BITMAP_TYPE_ANY),
                             wx.NullBitmap,
                             wx.ITEM_NORMAL, "", "Opens a saved game")
        self.toolbar.AddTool(3, "save_game", wx.Bitmap("Images/save.png", wx.BITMAP_TYPE_ANY),
                             wx.NullBitmap,
                             wx.ITEM_NORMAL, "", "Saves the current game.")
        # Tool Bar end
        self.splitter_window = wx.SplitterWindow(self, wx.ID_ANY)
        self.left_panel = wx.Panel(self.splitter_window, wx.ID_ANY)
        self.mode_radio_box = wx.RadioBox(self.left_panel, wx.ID_ANY, "Modo",
                                          choices=[u"Alfabético", "Level", "1024", "2048"], majorDimension=1,
                                          style=wx.RA_SPECIFY_COLS)
        self.thanos = wx.Button(self.left_panel, wx.ID_ANY, "Thanos")
        self.right_panel = wx.Panel(self.splitter_window, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TOOL, self._new_game, id=1)
        self.Bind(wx.EVT_TOOL, self._open_file, id=2)
        self.Bind(wx.EVT_TOOL, self._save_game, id=3)
        self.Bind(wx.EVT_RADIOBOX, self._game_mode_changed, self.mode_radio_box)
        self.Bind(wx.EVT_CHAR_HOOK, self._on_key_clicked)
        self.Bind(wx.EVT_BUTTON, self.on_thanos_clicked, self.thanos)
        self.SetFocus()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ClonFrame.__set_properties
        self.SetTitle("CLON3-GUI")
        self.SetBackgroundColour("white")
        self.toolbar.Realize()
        self.mode_radio_box.SetSelection(0)
        self.splitter_window.SetMinimumPaneSize(100)
        self.splitter_window.SetSashGravity(0.5)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ClonFrame.__do_layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        right_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_static_box_sizer = wx.StaticBoxSizer(wx.StaticBox(self.right_panel, wx.ID_ANY, "Tablero"), wx.HORIZONTAL)
        self.grid_sizer = ClonGridSizer(self.right_panel, self.game_config)
        vertical_box_sizer = wx.BoxSizer(wx.VERTICAL)
        game_status_sizer = wx.StaticBoxSizer(wx.StaticBox(self.left_panel, wx.ID_ANY, "Game Status"), wx.VERTICAL)
        record_sizer = wx.BoxSizer(wx.HORIZONTAL)
        movements_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vertical_box_sizer.Add((20, 20), 0, 0, 0)
        vertical_box_sizer.Add(self.mode_radio_box, 0, 0, 0)
        vertical_box_sizer.Add(self.thanos, 2, wx.EXPAND, 0)
        movements_text = wx.StaticText(self.left_panel, wx.ID_ANY, "Movimientos : ", style=wx.ALIGN_LEFT)
        movements_sizer.Add(movements_text, 0, wx.ALIGN_CENTER, 0)
        self.movements_count_text = wx.StaticText(self.left_panel, wx.ID_ANY, str(self.game_config.get_moves()))
        movements_sizer.Add(self.movements_count_text, 0, wx.ALIGN_CENTER, 0)
        game_status_sizer.Add(movements_sizer, 1, wx.EXPAND, 0)
        record_hint_ext = wx.StaticText(self.left_panel, wx.ID_ANY, u"Puntuación :   ", style=wx.ALIGN_LEFT)
        record_sizer.Add(record_hint_ext, 0, wx.ALIGN_CENTER, 0)
        self.record_count_text = wx.StaticText(self.left_panel, wx.ID_ANY, str(self.game_config.get_record()), style=wx.ALIGN_RIGHT)
        record_sizer.Add(self.record_count_text, 0, wx.ALIGN_CENTER | wx.RIGHT, 0)
        game_status_sizer.Add(record_sizer, 1, wx.EXPAND, 0)
        vertical_box_sizer.Add(game_status_sizer, 1, wx.EXPAND | wx.FIXED_MINSIZE, 0)
        self.left_panel.SetSizer(vertical_box_sizer)
        right_vertical_sizer.Add((20, 20), 1, wx.EXPAND, 0)
        grid_static_box_sizer.Add(self.grid_sizer, 0, wx.ALIGN_CENTER, 0)
        right_vertical_sizer.Add(grid_static_box_sizer, 0, 0, 0)
        right_vertical_sizer.Add((20, 20), 1, wx.EXPAND, 0)
        self.right_panel.SetSizer(right_vertical_sizer)
        self.splitter_window.SplitVertically(self.left_panel, self.right_panel, 180)
        main_sizer.Add(self.splitter_window, 1, wx.EXPAND, 0)
        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre()
        self._show_info_dialog()
        # end wxGlade

    def _refresh_right_panel(self):
        """
        Actualizamos el grid y el panel derecho
        :return: None
        """
        self.grid_sizer.update_grid()
        self.right_panel.Layout()
        return None

    def _new_game(self, event):
        """
        Creamos un nuevo tablero del juego
        :param event: evento
        :return: None
        """
        # Nuevo custom dialogo
        dialog = NewGameDialog(self.game_config)
        # Mostramos el diálogo y comprobamos que el usuario haya elegido el botón OK
        if dialog.ShowModal() == wx.ID_OK:
            # Buscamos el spinner de dimensiones y obstáculos mediante su Id
            dimens_spinner = wx.FindWindowById(1, dialog)
            obstacles_spinner = wx.FindWindowById(2, dialog)
            # Obtenemos el valor del spinner de dimensiones y obstáculos
            new_table_dimens = dimens_spinner.GetValue()
            new_table_obstacles = obstacles_spinner.GetValue()
            # Comprobamos que los obstáculos siempre sea menor que el tamaño del tablero
            if new_table_obstacles > new_table_dimens ** 2:
                self._show_prohibited_dialog(title="Algo mal ha ocurrido",
                                             content="El número de obstáculos debe ser menor que el tamaño del tablero!")
                return
            # Actualizamos la dimensión y obstaculos de la matriz
            self.game_config.set_matrix_size(new_table_dimens)
            self.game_config.set_obstacles(new_table_obstacles)
            # Creamos los obstáculos aleatorios
            create_random_obstacles(self.game_config.get_matrix(), new_table_obstacles)
            # Insertamos un nuevo bloque
            if new_table_obstacles != new_table_dimens ** 2:
                do_pie_operation("Z", self.game_config)
            # Actualizamos el grid y el panel derecho
            self._refresh_right_panel()
            # Actualizamos la puntuación y los movimientos
            self.game_config.set_moves(0)
            self.game_config.set_record(0)
            self.record_count_text.SetLabelText(str(self.game_config.get_record()))
            self.movements_count_text.SetLabelText(str(self.game_config.get_moves()))
        return None

    def _open_file(self, event):
        """
        Leemos un archivo y cargamos la partida guardada
        :param event: evento
        :return: None
        """
        # Creamos el diálogo de selección de la ruta del archivo
        # Por defecto el archivo se usará el nombre "partida" y solo aceptará archivos en formato txt
        dlg = wx.FileDialog(self, message="Elija la partida guardada...", defaultDir="", defaultFile="partida", wildcard=self.WILDCARD,
                            style=wx.FD_OPEN | wx.FD_CHANGE_DIR)
        # Comprobamos que el usuario haya pulsado el botón OK
        if dlg.ShowModal() == wx.ID_OK:
            # Obtenemos la ruta seleccionada
            path = dlg.GetPath()
            # Leemos el archivo y le cargamos
            read_file(path, self.game_config)
            # Actualizamos el grid y el panel derecho
            self._refresh_right_panel()
            # Actualizamos los movimientos
            self.movements_count_text.SetLabelText(str(self.game_config.get_moves()))
            # Actualizamos la puntuación
            self.record_count_text.SetLabelText(str(self.game_config.get_record()))
        dlg.Destroy()
        return None

    def _save_game(self, event):
        """
        Intentamos guardar el tablero en un archivo mediante [wx.FileDialog]
        :param event: evento
        :return: None
        """
        # Creamos el diálogo de selección de la ruta del archivo
        # Por defecto el archivo se usará el nombre "partida" y solo aceptará archivos en formato txt
        dlg = wx.FileDialog(self, message="Guardar partida...", defaultDir="", defaultFile="partida", wildcard=self.WILDCARD, style=wx.FD_SAVE)
        # Comprobamos que el usuario haya pulsado el botón OK
        if dlg.ShowModal() == wx.ID_OK:
            # Obtenemos la ruta seleccionada
            path = dlg.GetPath()
            # Guardamos el archivo
            save(path, self.game_config)
        # Destruimos el diálogo
        dlg.Destroy()
        return None

    def _game_mode_changed(self, event):
        """
        Cambiamos el modo del tablero
        :param event: evento
        :return: None
        """
        # Obtenemos el radio box seleccionado
        selection = self.mode_radio_box.GetSelection()
        # Cambiamos de modo
        change_mode(selection, self.game_config)
        # Actualizamos el grid y el panel derecho
        self._refresh_right_panel()
        return None

    def _on_key_clicked(self, event):
        """
        Callback que se ejecuta cuando el usuario pulsa una tecla del teclado
        :param event: el evento
        :return: None
        """
        # La tecla pulsada en unicode
        keycode = event.GetUnicodeKey()
        # Comprobamos que no sea una tecla especial
        if keycode != wx.WXK_NONE:
            # Comprobamos que la tecla pulsada corresponde con alguna de W, A, S, D en (Ascii)
            if keycode in [65, 68, 83, 87]:
                # Comprobamos si podemos realizar el movimiento (quedan huecos libres)
                if not is_possible_move(self.game_config.get_matrix()):
                    # Mostramos el diálogo de error
                    self._show_prohibited_dialog(title="Ahhhh!!!", content="Has perdido!")
                    # Salimos de la función
                    return
                # La tecla pulsada es un W
                if keycode == 87:
                    do_pie_operation("S", self.game_config)
                elif keycode == 83:  # La tecla pulsada es un S
                    do_pie_operation("B", self.game_config)
                elif keycode == 65:  # La tecla pulsada es una A
                    do_pie_operation("I", self.game_config)
                elif keycode == 68:  # La tecla pulsada es una D
                    do_pie_operation("D", self.game_config)
                # Actualizamos los movimientos y la puntuación
                self.record_count_text.SetLabelText(str(self.game_config.get_record()))
                self.movements_count_text.SetLabelText(str(self.game_config.get_moves()))
                # Actualizamos el grid y el panel derecho
                self._refresh_right_panel()
                # Comprobamos si podemos realizar el movimiento (quedan huecos libres)
                if not is_possible_move(self.game_config.get_matrix()):
                    # Mostramos el diálogo de error
                    self._show_prohibited_dialog(title="Ahhhh!!!", content="Has perdido!")
                    return
        event.Skip()
        return None

    def on_thanos_clicked(self, event):
        print("Event handler 'on_thanos_clicked' not implemented!")
        event.Skip()
        return None

    def _show_info_dialog(self):
        """
        Creamos un diálogo de información y lo mostramos
        :return:
        """
        wx.MessageBox(
            "Las teclas W,A,S,D corresponden con desplazamientos hacia arriba, izquierda, abajo y derecha respectivamente. Debe usted hacer click "
            "en una posición de la ventana primero",
            "Sobre los controles", wx.OK | wx.ICON_WARNING)
        return None

    def _show_prohibited_dialog(self, title="", content=""):
        """
        Creamos un diálog de error y lo mostramos
        :return:
        """
        wx.MessageBox(content, title, wx.OK | wx.ICON_WARNING)
        return None


# end of class ClonFrame


class MyApp(wx.App):
    # Configuración principal del juego
    game_config = GameConfig()

    def __init__(self):
        super().__init__(redirect=False, filename=None, useBestVisual=False, clearSigInt=True)
        self.game_config.set_matrix_size(3)
        self.clon_3 = ClonFrame(self.game_config)
        self.SetTopWindow(self.clon_3)
        self.clon_3.Show()


# end of class MyApp

# Creamos el App y empezamos el bucle de eventos
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
