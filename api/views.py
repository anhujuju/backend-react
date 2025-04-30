from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from pymongo import MongoClient
from django.contrib.auth.hashers import make_password, check_password

# 🔐 Conexión segura a MongoDB Atlas usando variable de entorno
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["react"]
users_collection = db["users"]

@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            raw_body = request.body.decode('utf-8')
            print(f"📩 Cuerpo recibido: {raw_body}")

            if not raw_body:
                return JsonResponse({"error": "El cuerpo de la solicitud está vacío."}, status=400)

            data = json.loads(raw_body)
            email = data.get("email")
            password = data.get("password")
            gender = data.get("gender")
            username = data.get("username")
            score = data.get("score", 0)

            if not email or not password or not gender or not username:
                return JsonResponse({"error": "Todos los campos son obligatorios."}, status=400)

            print(f"🔍 Verificando si el correo {email} ya está registrado...")
            existing_user = users_collection.find_one({"email": email})
            if existing_user:
                print("🚨 Correo ya registrado:", email)
                return JsonResponse({"error": "Este correo ya está registrado."}, status=400)

            hashed_password = make_password(password)

            new_user = {
                "email": email,
                "username": username,
                "password": hashed_password,
                "gender": gender,
                "score": score
            }

            users_collection.insert_one(new_user)
            print("✅ Registro exitoso para:", email)

            return JsonResponse({
                "message": "Registro exitoso",
                "email": email,
                "username": username,
                "score": score
            })

        except json.JSONDecodeError:
            print(f"❌ Error: JSON mal formado. Cuerpo recibido: {raw_body}")
            return JsonResponse({"error": "Formato JSON inválido."}, status=400)
        except Exception as e:
            print(f"🔥 Error inesperado en el servidor: {str(e)}")
            return JsonResponse({"error": f"Error en el servidor: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            raw_body = request.body.decode('utf-8')
            print(f"📩 Cuerpo recibido en login: {raw_body}")

            if not raw_body:
                return JsonResponse({"error": "El cuerpo de la solicitud está vacío."}, status=400)

            data = json.loads(raw_body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"error": "Correo y contraseña son obligatorios."}, status=400)

            print(f"🔑 Intentando iniciar sesión: {email}")
            user = users_collection.find_one({"email": email})

            if user and check_password(password, user["password"]):
                print("✅ Inicio de sesión exitoso:", email)
                return JsonResponse({
                    "message": "Inicio de sesión exitoso",
                    "email": user["email"],
                    "username": user.get("username", ""),
                    "score": user.get("score", 0)
                })

            print("❌ Credenciales incorrectas:", email)
            return JsonResponse({"error": "Credenciales incorrectas"}, status=400)

        except json.JSONDecodeError:
            print("❌ Error: JSON mal formado")
            return JsonResponse({"error": "Formato JSON inválido."}, status=400)
        except Exception as e:
            print(f"🔥 Error inesperado en el servidor: {str(e)}")
            return JsonResponse({"error": f"Error en el servidor: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def update_score(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get("email")
            new_score = data.get("score")

            if not email or not isinstance(new_score, (int, float)):
                return JsonResponse({"error": "Faltan datos o el puntaje no es válido."}, status=400)

            print("📥 Datos recibidos para actualizar score:", data)

            result = users_collection.update_one(
                {"email": email},
                {"$set": {"score": new_score}}
            )

            if result.matched_count == 0:
                return JsonResponse({"error": "Usuario no encontrado."}, status=404)

            return JsonResponse({"message": "Puntaje actualizado exitosamente."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def get_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get("email")

            if not email:
                return JsonResponse({"error": "Falta el correo."}, status=400)

            user = users_collection.find_one({"email": email})
            if not user:
                return JsonResponse({"error": "Usuario no encontrado."}, status=404)

            return JsonResponse({
                "email": user.get("email"),
                "username": user.get("username"),
                "score": user.get("score", 0)
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)
