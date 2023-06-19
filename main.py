import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
import shutil as copy_files
from PyQt5.QtGui import QPixmap
from tkinter import messagebox, filedialog
from PyQt5.uic import loadUi
import database as db
import qr
import re
import os

print('\033[2J')  # Borrar la terminal / secuencia de escape


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        try:
            loadUi('./PYQT5_interfaz_grafica_moderna/diseño.ui', self)
        except FileNotFoundError:
            print('\033[38;5;196m' + ' El archivo de la interfaz gráfica NO existe')
            quit()
        else:
            if os.path.isdir('./codigos_qr'):
                pass
            else:
                os.mkdir('./codigos_qr')
        messagebox.showinfo('Conexión', db.conexion_base_de_datos())
        self.setWindowTitle('Manejo de asistencia')
        self.setWindowIcon(QtGui.QIcon('./icos/icono principal.png'))
        self.directorio = './codigos_qr'
        self.boton_aadir.clicked.connect(self.agregar_registros)
        self.boton_eliminar_registro.clicked.connect(self.eliminar_registros)
        self.boton_actualizar.clicked.connect(self.editar_registros)
        self.boton_consultar_registro.clicked.connect(self.consultar_registros)
        self.ver_codigo_boton.clicked.connect(self.ver_codigo_qr)
        self.ver_info_qr_btn.clicked.connect(self.info_qr)
        self.llamar_a_lista_btn.clicked.connect(self.llamar_a_asistencia)
        self.boton_de_asistencia_id.clicked.connect(self.asistencia_id)
        self.consultar_asistencia_qr.clicked.connect(self.asistencia_qr)
        self.save_image.clicked.connect(self.guardar_imagen_codigo_qr)
        self.alterar_asistencia_btn.clicked.connect(self.cambiar_valores_combobox_asistencia)
        self.comboBox_fechas.activated[str].connect(self.combochanged)
        self.cambiar_asistencia_btn.clicked.connect(self.cambiar_asistencia)

        self.boton_nuevo.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.NUEVO))
        self.boton_eliminar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ELIMINAR))
        self.boton_editar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.EDITAR))
        self.boton_consultar.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.CONSULTAR))
        self.boton_verqr.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.VER_QR))
        self.boton_asistencia.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ASISTENCIA))
        self.boton_informacion.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.INFORMACION))
        self.ver_asistencia_id.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.VER_ASISTENCIA_USANDO_ID))
        self.ver_asistencia_qr.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.ver_asistencia_usando_qr))
        self.alterar_lista.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Alterar_asistencia))

    def agregar_registros(self):
        """Agregar registros a la base de datos de los estudiantes

        Se toman los valores de id, nombre y curso del estudiante que fueron proporcionados por el usuario, 
        se convierten a mayúscula para estandarizar y se llama a la función de agregar registros y de crear 
        código qr, si las funciones devuelven 1 (fallo) se indica al usuario lo sucedido. De lo contrario se 
        le indica al usuario lo contrario (logrado).
        """
        try:
            id = int(self.identrada.text().upper())
            nombre = str(self.nombreentrada.text().upper())
            curso = int(self.cursoentrada.text().upper())
        except ValueError:
            self.identrada.clear()
            self.nombreentrada.clear()
            self.cursoentrada.clear()
            messagebox.showerror('ERROR', 'Los datos ingresados son inconsistentes, verifique e intente de nuevo')
        else:
            if id != '' and nombre != '' and curso != '' and db.consultar(id) == None:
                if db.crear_registro(id, nombre, curso) == 1 or qr.crearqr((id, nombre, curso), self.directorio) == 1:
                    messagebox.showerror('ERROR',
                                         'Error al conectar con la base de datos, los registros no fueron guardados')
                else:
                    self.identrada.clear()
                    self.nombreentrada.clear()
                    self.cursoentrada.clear()
                    messagebox.showinfo('Proceso logrado', 'Los registros fueron guardados en la base de datos')
            else:
                messagebox.showerror('ERROR', 'Los datos ingresados son inconsistentes, verifique e intente de nuevo')

    def eliminar_registros(self):
        """Eliminar registros de la base de datos de los estudiantes

        Se tomael valor de id del estudiante que fue proporcionado por el usuario, se llama a la función borrar registro
        de la base de datos y se elimina el registro de la base de datos y el código qr que fue generado. En caso tal las
        funciones devuelvan un valor de 1 (fallo) se indica al usuario lo sucedido. De lo contrario (logrado) se indica al
        usuario el proceso.
        """
        try:
            id = int(self.ingresar_id_eliminar.text().upper())
        except ValueError:
            messagebox.showerror('ERROR', 'Verifique el id ingresado, el registro no pudo ser eliminado.')
        else:
            if id != '':
                if db.borrar_registro(id, self.directorio) == 1:
                    messagebox.showerror('ERROR',
                                         'Error al conectar con la base de datos, los registros no fueron guardados')
                else:
                    messagebox.showinfo('Proceso logrado', 'Los registros fueron eliminados de la base de datos')
                    self.ingresar_id_eliminar.clear()
            else:
                messagebox.showerror('ERROR', 'Verifique el id ingresado, el registro no pudo ser eliminado.')

    def editar_registros(self):
        """Editar registros de la base de datos.

        Se le solicitan al usuario los registros id, nombre y curso, se editan en la base de datos. Si el proceso falla
        devuelve 1 y se indica al usuario el problema, de lo contrario se le indica al usuario que el proceso fue exitoso.
        """
        try:
            id = int(self.entrada_id.text().upper())
            nombre = str(self.entrada_nombre.text().upper())
            curso = int(self.entrada_curso.text().upper())
        except ValueError:
            messagebox.showerror('ERROR', 'Verifique los datos ingresados, el registro no pudo ser actualizado.')
        else:
            if id != '' and nombre != '' and curso != '':
                if db.actualizar(id, nombre, curso) == 1:
                    messagebox.showerror('ERROR',
                                         'Error al conectar con la base de datos, los registros no fueron guardados')
                else:
                    self.entrada_id.clear()
                    self.entrada_nombre.clear()
                    self.entrada_curso.clear()
                    messagebox.showinfo('Proceso logrado', 'Los datos fueron actualizados con exito')
            else:
                messagebox.showerror('ERROR', 'Verifique los datos ingresados, el registro no pudo ser actualizado.')

    def consultar_registros(self):
        """Consultar registros de la base de datos.

        Se solicita al usuario el id de estudiante y se consulta por el registro en la base de datos, si la función
        devuelve 1 (fallo) se le indica al usuario lo sucedido, de lo contrario se le dice que esto fue logrado.
        Los datos se muestran en una ventana pop up de sistema creada a través de QMessageBox.about.
        """
        try:
            id = int(self.ingresar_id_consultar.text().upper())
        except ValueError:
            messagebox.showerror('ERROR', 'El id de usuario ingresado no es válido, verifiquelo e intente de nuevo')
        else:
            if id != '':
                datos = db.consultar(id)
                if datos == 1:
                    messagebox.showerror('Error', 'El registro no se pudo consultar, ha ocurrido un error')
                else:
                    try:
                        self.ingresar_id_consultar.clear()
                        messagebox.showinfo('Datos', f'id: {datos[0]}, nombre: {datos[1]}, curso: {datos[2]}')
                    except:
                        messagebox.showinfo('Error', 'verifique los datos ingresados, el registro no se pudo consultar')
            else:
                messagebox.showinfo('ERROR', 'El id de usuario ingresado no es válido, verifiquelo e intente de nuevo')

    def ver_codigo_qr(self):
        """Función para generar el codigo qr de estudiante

        Se busca el código qr de la persona a través del id, si este es encontrado se muestra como fondo a
        través de un label, en caso contrario se indica al usuario que el código no pudo ser encontrado.
        """
        try:
            id = int(self.Ingresar_id_ver_qr.text().upper())
            ruta_del_archivo = f'{self.directorio}/{id}.png'
        except ValueError:
            messagebox.showinfo('ERROR', 'Verifique el id ingresado, los datos no son válidos')
        else:
            try:
                handle_temporal = open(ruta_del_archivo)
                handle_temporal.close()
            except FileNotFoundError:
                self.label_mostrar_qr.clear()
                self.Ingresar_id_ver_qr.clear()
                messagebox.showerror('Error', 'El estudiante no se encuentra registrado en la base de datos')
            else:
                imagen = QPixmap(ruta_del_archivo)
                self.label_mostrar_qr.setPixmap(imagen)

    def info_qr(self):
        """Visualizar la información de los códigos qr
        """
        lectura = str(qr.lectura_qr())
        lectura = lectura.strip('[]').split(',')
        informacion = db.consultar(lectura[0])
        try:
            messagebox.showinfo('info', f'id: {informacion[0]} \n nombre: {informacion[1]} \n curso:{informacion[2]}')
        except TypeError:
            messagebox.showerror('Error', 'El estudiante no se encuentra en la base de datos')

    def llamar_a_asistencia(self):
        """Llamado de asistencia 
        """
        valores = qr.lectura_asistencia_qr()
        valores_sin_repetir = []
        for item in valores:
            if item not in valores_sin_repetir:
                valores_sin_repetir.append(item)
        for i in valores_sin_repetir:
            valor = str(i)
            valor = valor.strip('[]').split(',')
            informacion = db.consultar(valor[0])
            if informacion == None:
                messagebox.showerror('Error', f'El estudiante {valor[0]} no se encuentra en la base de datos')
            else:
                db.llamar_asistencia(informacion[0])

    def asistencia_id(self):
        id_consultar = self.ingresar_id_asistencia.text().upper()
        respuestas = db.ver_asistencia(id_consultar)
        if respuestas == 1:
            messagebox.showerror('ERROR', 'Por favor verifique los datos ingresados')
        else:
            string_general = ''
            for i in respuestas:
                string_general += i
                string_general += '\n'
            self.label_informacion.setText(string_general)

    def asistencia_qr(self):
        lectura = str(qr.lectura_qr())
        lectura = lectura.strip('[]').split(',')
        try:
            if db.consultar(lectura[0]) == None: raise TypeError
            respuestas = db.ver_asistencia(lectura[0])
        except TypeError:
            messagebox.showerror('Error', 'El estudiante no se encuentra en la base de datos')
        else:
            if respuestas == 1:
                messagebox.showerror('ERROR', 'Ha ocurrido un error al recopilar los datos')
            else:
                string_general = ''
                for i in respuestas:
                    string_general += i
                    string_general += '\n'
                self.label_info_qr.setText(string_general)

    def guardar_imagen_codigo_qr(self):
        try:
            id = int(self.Ingresar_id_ver_qr.text().upper())
            ruta_del_archivo = filedialog.askdirectory()
            if db.consultar(id) == 1:
                messagebox.showerror('Error', 'El id no se encontró en la base de datos.')
                self.Ingresar_id_ver_qr.clear()
        except:
            messagebox.showerror('Error', 'Ha ocurrido un error, verifique la información proporcionada.')
        else:
            try:
                copy_files.copy(f'{self.directorio}/{id}.png', f'{ruta_del_archivo}/{id}.png')
            except FileNotFoundError:
                messagebox.showerror('Error', 'El estudiante no está en la base de datos')
                self.Ingresar_id_ver_qr.clear()
            else:
                messagebox.showinfo('Proceso Exitoso', 'El código ha sido guardado con exito')

    def cambiar_valores_combobox_asistencia(self):
        try:
            id = int(self.id_consulta_asistencia.text().upper())
            if db.consultar(id) == None: raise ValueError
        except ValueError:
            messagebox.showerror('Error', 'El ID ingresado no es válido')
        else:
            fechas = db.ver_fechas()
            for i in range(len(fechas)):
                self.comboBox_fechas.addItem(fechas[i])

    def combochanged(self):
        id = int(self.id_consulta_asistencia.text().upper())
        valor_combobox = self.comboBox_fechas.currentText()
        asistencia = db.ver_asistencia(id)
        for i in asistencia:
            value = re.search(valor_combobox, i)
            if value != None:
                String = i
                break
        self.label_info_asistencia_cambiar.setText(String)

    def cambiar_asistencia(self):
        try:
            id = int(self.id_consulta_asistencia.text().upper())
            valor_combobox = self.comboBox_fechas.currentText()
            db.alterar_asistencia_segun_fecha(id, valor_combobox)
        except:
            messagebox.showerror('ERROR', 'El registro no pudo ser actualizado')
        else:
            messagebox.showinfo('PROCESO LOGRADO', 'El registro se actualizó con exito')
        finally:
            self.id_consulta_asistencia.clear()
            self.comboBox_fechas.clear()
            self.label_info_asistencia_cambiar.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = VentanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())
