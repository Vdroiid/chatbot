import wx
import threading
from funciones_chatbot import grabar_sintoma, leer_texto, validar_diagnostico, recomendar, sintomas_gripa, sintomas_resfriado, sintomas_alergia, numero_ordinal
""" Falta ponerle una bienvenida. """

class AutoCloseDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(AutoCloseDialog, self).__init__(*args, **kw)
        panel = wx.Panel(self)
        message = wx.StaticText(panel, label="Activando el micrófono, espere...")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(message, 0, wx.ALL, 10)
        panel.SetSizer(sizer)
    def set_timeout(self, milliseconds):
        wx.CallLater(milliseconds, self.Destroy)

class DiagnosticoFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(DiagnosticoFrame, self).__init__(*args, **kw)
        panel = wx.Panel(self)
        self.sintomas = []
        self.contador = 0

        # Crear la interfaz
        self.static_text = wx.StaticText(panel, label=f"Ingrese la {numero_ordinal[self.contador]} síntoma:")
        self.txt_sintoma = wx.TextCtrl(panel, size=(300, -1))
        self.btn_agregar = wx.Button(panel, label="Agregar síntoma")
        self.grabar_button = wx.Button(panel, label="Decir síntoma")
        self.list_sintomas = wx.ListBox(panel, size=(300, 90))
        self.btn_diagnosticar = wx.Button(panel, label="Diagnosticar")

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.static_text, 0, wx.ALL, 5)
        sizer.Add(self.txt_sintoma, 0, wx.ALL, 5)
        sizer.Add(self.btn_agregar, 0, wx.ALL, 5)
        sizer.Add(self.grabar_button, 0, wx.ALL, 5)
        sizer.Add(self.list_sintomas, 0, wx.ALL, 5)
        sizer.Add(self.btn_diagnosticar, 0, wx.ALL, 5)
        panel.SetSizer(sizer)

        # Establecer un tamaño fijo para la pantalla
        self.SetSize((300, 300))  # Tamaño fijo
        self.SetMinSize((300, 300))  # Tamaño mínimo
        self.SetMaxSize((300, 300))  # Tamaño máximo para evitar redimensionamiento
        # Eventos
        self.btn_agregar.Bind(wx.EVT_BUTTON, self.on_agregar_sintoma)
        self.btn_diagnosticar.Bind(wx.EVT_BUTTON, self.on_diagnosticar)
        self.grabar_button.Bind(wx.EVT_BUTTON, self.on_grabar)

        # Mostrar el mensaje de bienvenida en un hilo separado
        threading.Thread(target=self.welcome).start()

    def welcome(self):
        # Leer el texto de bienvenida y mostrar el cuadro de mensaje en el hilo principal
        texto = "¡Hola! Soy DiagnosAI\n\nTe haré un diagnóstico.Para empezar, por favor ingresa tus síntomas."
        wx.CallAfter(self.mostrar_cuadro_mensaje, texto)

    def mostrar_cuadro_mensaje(self, texto):
        wx.MessageBox(leer_texto(texto), "Información", wx.OK | wx.ICON_INFORMATION, parent=self)

    def on_agregar_sintoma(self, event):
        respuesta = self.txt_sintoma.GetValue().strip().capitalize()
        if respuesta in self.sintomas:
            wx.MessageBox("Síntoma ya agregado.", "Advertencia", wx.OK | wx.ICON_WARNING)
            self.txt_sintoma.Clear()
        elif respuesta == "Fin":
            self.on_diagnosticar(self)
        elif  len(self.sintomas) == 7:
            print("Se alcanzó el límite")
            wx.MessageBox("Ya no se acepta más síntomas. Pulse el botón diagnosticar, por favor.", "Advertencia", wx.OK | wx.ICON_WARNING)
            self.txt_sintoma.Clear()
        elif respuesta and respuesta not in self.sintomas:
            print("Agregando síntoma")
            if respuesta in sintomas_gripa or respuesta in sintomas_resfriado or respuesta in sintomas_alergia:
                self.sintomas.append(respuesta)
                self.list_sintomas.Append(respuesta)
                self.txt_sintoma.Clear()
                self.contador += 1
                if len(self.sintomas) <= 7:
                    # Actualizar el texto estático
                    self.static_text.SetLabel(f"Ingrese la {numero_ordinal[self.contador]} síntoma:")
            else:
                wx.MessageBox("Síntoma no válido. Inténtelo de nuevo.", "Advertencia", wx.OK | wx.ICON_WARNING)
                self.txt_sintoma.Clear()
        else:
            wx.MessageBox("El campo está vacío.", "Advertencia", wx.OK | wx.ICON_WARNING)
    def on_diagnosticar(self, event):
        if not self.sintomas:
            texto = "No se han ingresado síntomas."
            leer_texto(texto)
            wx.MessageBox(texto, "Advertencia", wx.OK | wx.ICON_WARNING)
            return
        diagnostico = validar_diagnostico(self.sintomas, sintomas_gripa, sintomas_resfriado, sintomas_alergia)
        leer_texto(diagnostico)
        if diagnostico.endswith("Gripa.") or diagnostico.endswith("Resfriado.") or diagnostico.endswith("Alergia."):
            leer_texto(recomendar())
            wx.MessageBox(diagnostico + " " + recomendar(), "Diagnóstico", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox(diagnostico, "Diagnóstico", wx.OK | wx.ICON_INFORMATION)
        self.list_sintomas.Clear()
        self.sintomas.clear()
        self.contador = 0
        self.static_text.SetLabel(f"Ingrese la {numero_ordinal[self.contador]} síntoma:")
    def on_grabar(self, event):
        # Mostrar diálogo
        self.dialog = AutoCloseDialog(self, title="Escuchando...", size=(250, 100))
        self.dialog.Show()

        # Ejecutar la función en un hilo separado
        threading.Thread(target=self.grabar_sintoma).start()
    def grabar_sintoma(self):
        respuesta = grabar_sintoma(self.contador)
        if respuesta in self.sintomas:
            wx.MessageBox("Síntoma ya agregado.", "Advertencia", wx.OK | wx.ICON_WARNING)
        elif  len(self.sintomas) == 7:
            wx.MessageBox("Ya no se acepta más síntomas. Pulse el botón diagnosticar, por favor.", "Advertencia", wx.OK | wx.ICON_WARNING)
        elif  respuesta == "Finalizar":
            self.on_diagnosticar(self)
        elif respuesta and respuesta not in self.sintomas:
            if respuesta in sintomas_gripa or respuesta in sintomas_resfriado or respuesta in sintomas_alergia:
                self.sintomas.append(respuesta)
                self.list_sintomas.Append(respuesta)
                self.contador += 1
                if len(self.sintomas) <=7:
                    # Actualizar el contador del texto estático
                    self.static_text.SetLabel(f"Ingrese la {numero_ordinal[self.contador]} síntoma:")
        else:
            wx.MessageBox("Lo siento, no pude escucharte. Intente de nuevo.", "Advertencia", wx.OK | wx.ICON_WARNING)
        wx.CallAfter(self.dialog.Destroy)

# Función principal
def main():
    app = wx.App(False)
    frame = DiagnosticoFrame(None, title="DiagnosAI", size=(400, 400))
    frame.Show()
    app.MainLoop()
if __name__ == "__main__":
    main()
