import openpyxl

path = 'matriz.xlsx'

workbook = openpyxl.load_workbook(path)

sheet = workbook.active

# Crear un arreglo para almacenar los datos
data = []

# Recorrer las filas de la hoja
for row in sheet.iter_rows(values_only=True):
    # Convertir cada fila en una lista y agregarla al arreglo 'data'
    data.append(list(row))

print(data)

