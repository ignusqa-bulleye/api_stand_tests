import sender_stand_request
import data


# esta función cambia los valores en el parámetro "firstName"
def get_user_body(first_name):
    # el diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_body = data.user_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body

# Función de prueba positiva
def positive_assert(first_name):
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(first_name)
    # El resultado de la solicitud para crear un/a nuevo/a usuario/a se guarda en la variable user_response
    user_response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    print(user_response.status_code)
    # Comprueba que el campo authToken está en la respuesta y contiene un valor
    assert user_response.json()["authToken"] != ""
    print(user_response.json()["authToken"])

    # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"
    users_table_response = sender_stand_request.get_users_table()

    # String que debe estar en el cuerpo de respuesta
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1


# Prueba 1. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene dos caracteres

#Declara la siguiente función: negative_assert_symbol(first_name).
def negative_assert_symbol(first_name):
    #Guarda el resultado de llamar a la función get_user_body(first_name) a la variable response.
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    # Verificar el código en el JSON ⭐ ESTA LÍNEA FALTA
    assert response.json()["code"] == 400

    assert response.json()["message"] == "Has introducido un nombre de usuario no válido. " \
                                         "El nombre solo puede contener letras del alfabeto latino, " \
                                         "la longitud debe ser de 2 a 15 caracteres."

def test_create_user_2_letter_in_first_name_get_success_response():
    # La versión actualizada del cuerpo de solicitud con el nombre "Aa" se guarda en la variable "user_body"
      positive_assert("Aa")

def test_create_user_15_letter_in_first_name_get_success_response():
    # La versión actualizada del cuerpo de solicitud con el nombre "Aaaaaaaaaaaaaaa" se guarda en la variable "user_body"
        positive_assert("Aaaaaaaaaaaaaaa")

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aa")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\\")

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

def negative_assert_no_firstname(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

def test_create_user_no_first_name_get_error_response():
    #se usa una copia para evitar perdidas y ediciones del json original
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_firstname(user_body)

def test_create_user_empty_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body("")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    #negative_assert_no_firstname(user_body)
    #print(response.status_code)
