import requests
import json
# from ascii_magic import AsciiArt, from_image,Back
from PIL import Image
import tempfile
import climage


BASE_URL = "https://celuzador.online/celuzadorApi.php"

def fetch_phone_info(phone_number):
    headers = {
        'User-Agent': 'CeludeitorAPI-TuCulitoSacaLlamaAUFAUF'
    }
    response = requests.post(BASE_URL, data={"txttlf": phone_number},headers=headers)
    data = response.json()
    
    if not data['error']:
        phone_info = json.loads(data['data'])

        # Display info
        if phone_info['fuente']:
            for fuente in phone_info['fuente']:
                print(f"Nombre: {fuente['nombre']}")
        else:
            print("Lo sentimos, No encontramos informacion en la fuente principal.")

        if phone_info['whatsapp']:
            tiene_whatsapp = 'Si tiene' if phone_info['whatsapp']['tiene_whatsapp'] else 'No tiene'
            print(f"WhatsApp: {tiene_whatsapp}")

            if phone_info['whatsapp']['foto_perfil']:
                profile_pic_url = phone_info['whatsapp']['foto_perfil']
                image_response = requests.get(profile_pic_url, stream=True)
                image = Image.open(image_response.raw)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                    image.save(temp_file, format="JPEG")
                    output = climage.convert(temp_file.name)
                    image.show()
                    print (output)

                whatsapp_status = json.loads(phone_info['whatsapp']['estado'])
                print(f"Estado: {whatsapp_status['status']}")
                print(f"Ultima Actualizacion: {whatsapp_status['setAt']}")
        else:
            print("WhatsApp: No tiene")
        
        print(phone_info['_cva'])
    else:
        print("El numero indicado es invalido, intenta nuevamente.")


# # Para usar la función:
phone_number = input("Introduce el número de teléfono: ")
fetch_phone_info(phone_number)


