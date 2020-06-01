import wx

from GameConfig import GameConfig, GameModes
from GameOperations import convert_block_to_mode, print_matrix


class NewGameDialog(wx.Dialog):
    def __init__(self, game_config):
        # begin wxGlade: NewGameDialog.__init_
        super(NewGameDialog, self).__init__(None, title="Nuevo Tablero", size=(250, 150))
        self.game_config = game_config
        self.dimens_spin = wx.SpinCtrl(self, 1, "0", min=0, max=100, style=wx.ALIGN_RIGHT | wx.SP_ARROW_KEYS)
        self.obstacles_spin = wx.SpinCtrl(self, 2, "0", min=0, max=100, style=wx.ALIGN_RIGHT | wx.SP_ARROW_KEYS)
        self.__set_properties()
        self.__do_layout()

        # self.Bind(wx.EVT_SPINCTRL, self.on_obstacle_spin_value_changed, self.obstacles_spin)
        # self.Bind(wx.EVT_TEXT_ENTER, self.on_obstacle_spin_value_changed, self.obstacles_spin)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: NewGameDialog.__set_properties
        self.SetSize((250, 150))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        return None
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: NewGameDialog.__do_layout
        vertical_dialog_sizer = wx.BoxSizer(wx.VERTICAL)
        bottom_sizer = wx.WrapSizer(wx.HORIZONTAL)
        top_sizer = wx.WrapSizer(wx.HORIZONTAL)
        vertical_dialog_sizer.Add((20, 20), 0, 0, 0)
        top_sizer.Add((20, 20), 1, wx.EXPAND, 0)
        dimens_hint_text = wx.StaticText(self, wx.ID_ANY, "Dimensiones : ", style=wx.ALIGN_LEFT)
        top_sizer.Add(dimens_hint_text, 0, 0, 0)
        top_sizer.Add(self.dimens_spin, 0, 0, 0)
        vertical_dialog_sizer.Add(top_sizer, 1, wx.EXPAND, 0)
        bottom_sizer.Add((20, 20), 1, wx.EXPAND, 0)
        obstacles_hint_text = wx.StaticText(self, wx.ID_ANY, "Obstáculos :   ", style=wx.ALIGN_LEFT)
        bottom_sizer.Add(obstacles_hint_text, 0, 0, 0)
        bottom_sizer.Add(self.obstacles_spin, 0, 0, 0)
        vertical_dialog_sizer.Add(bottom_sizer, 1, wx.EXPAND, 0)
        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        static_line_1.SetMinSize((220, 2))
        static_line_1.SetBackgroundColour(wx.Colour(122, 122, 122))
        vertical_dialog_sizer.Add(static_line_1, 0, wx.EXPAND, 0)
        buttons = self.CreateSeparatedButtonSizer(wx.OK | wx.CANCEL)
        vertical_dialog_sizer.Add(buttons, 1, wx.EXPAND, 0)
        self.SetSizer(vertical_dialog_sizer)
        self.Layout()
        self.Centre()
        return None
        # end wxGlade


# Grid sizer del Clon 3
class ClonGridSizer(wx.GridSizer):
    # Prefijos de las imágenes
    ALPHABETIC_IMAGES_PREFIX = "0-"
    LEVEL_IMAGES_PREFIX = "1-"
    A_1024_IMAGES_PREFIX = "2-"
    B_2048_IMAGES_PREFIX = "3-"

    def __init__(self, parent, game_config: GameConfig):
        super(ClonGridSizer, self).__init__(3, 3, 0, 0)
        self.game_config = game_config
        self.parent = parent
        # Actualizamos el grid
        self.update_grid()

    def update_grid(self):
        """
        Método que actualiza el grid
        :return: None
        """
        # Limpiamos el contenido del grid previo
        self.Clear(True)
        # Actualizamos el número de columnas y filas
        self.SetRows(self.game_config.get_matrix_size())
        self.SetCols(self.game_config.get_matrix_size())
        # Matriz del juego
        matrix = self.game_config.get_matrix()
        # Modo actual
        current_mode = self.game_config.get_mode()
        # Prefijo del archivo
        prefix = self._get_correct_image_prefix(current_mode)
        # Bucle que recorre por filas y columnas
        for row in range(len(matrix)):
            for column in range(len(matrix[0])):
                # Valor de una posición específica de la matriz
                value = matrix[row][column]
                # Nombre del archivo
                file_name = "Bloque.png"
                # Comprobamos que no sea bloque ni vacío
                if value not in ["*", " "]:
                    # Convertimos el valor al modo nivel
                    value = convert_block_to_mode(value, current_mode, GameModes.LEVEL)
                    # Concatenamos el prefijo + valor + .png obteniendo el nombre del archivo
                    file_name = prefix + value + ".png"
                elif value == "*":  # Es un bloque
                    file_name = "Bloque.png"
                elif value == " ":  # Está vacia
                    file_name = "Vacio.png"
                # Añadimos al grid la imagen
                self.Add(wx.StaticBitmap(self.parent, wx.ID_ANY, wx.Bitmap("Images/" + file_name, wx.BITMAP_TYPE_ANY)), 0, wx.ALIGN_CENTER, 0)
        # Actualizamos el grid
        self.Layout()
        return None

    def _get_correct_image_prefix(self, mode):
        """
        Método que obtiene los prefijos correctos según el tipo de modo
        :param mode: El modo actual del juego
        :return: el prefijo del archivo
        """
        if mode == GameModes.ALPHA:
            return self.ALPHABETIC_IMAGES_PREFIX
        elif mode == GameModes.LEVEL:
            return self.LEVEL_IMAGES_PREFIX
        elif mode == GameModes.A:
            return self.A_1024_IMAGES_PREFIX
        elif mode == GameModes.B:
            return self.B_2048_IMAGES_PREFIX
