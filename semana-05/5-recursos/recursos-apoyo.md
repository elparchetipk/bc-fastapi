# Recursos de Apoyo - Semana 5

## 📚 Documentación y Referencias

### **JWT (JSON Web Tokens)**

- [JWT.io](https://jwt.io/) - Decodificador y documentación oficial
- [RFC 7519 - JWT Standard](https://tools.ietf.org/html/rfc7519) - Especificación técnica
- [JWT Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/) - Mejores prácticas de seguridad

### **Python-JOSE**

- [Python-JOSE Documentation](https://python-jose.readthedocs.io/) - Librería para JWT en Python
- [Python-JOSE GitHub](https://github.com/mpdavis/python-jose) - Código fuente y ejemplos
- [JOSE Standards](https://jose.readthedocs.io/) - Estándares JOSE/JWT

### **Passlib (Password Hashing)**

- [Passlib Documentation](https://passlib.readthedocs.io/) - Documentación completa
- [Bcrypt Documentation](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html) - Algoritmo bcrypt
- [Password Hashing Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) - OWASP Guide

### **FastAPI Security**

- [FastAPI Security Tutorial](https://fastapi.tiangolo.com/tutorial/security/) - Tutorial oficial
- [OAuth2 with Password](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) - OAuth2 + JWT
- [Dependencies Security](https://fastapi.tiangolo.com/tutorial/dependencies/) - Inyección de dependencias

### **HTTP Authentication**

- [HTTP Authentication RFC](https://tools.ietf.org/html/rfc7235) - Estándar HTTP Auth
- [Bearer Token RFC](https://tools.ietf.org/html/rfc6750) - Esquema Bearer
- [OAuth2 RFC](https://tools.ietf.org/html/rfc6749) - Protocolo OAuth2

---

## 🛠️ Herramientas Útiles

### **Testing de Autenticación**

- **Postman**: Para probar endpoints con Bearer tokens
- **httpie**: Cliente HTTP con soporte para Authorization headers
- **curl**: Testing básico de autenticación
- **JWT Debugger**: Para verificar contenido de tokens

### **Comandos Básicos para Testing**

```bash
# Login y obtener token
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=secret"

# Usar token en requests
curl -X GET "http://localhost:8000/protected" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Con httpie
http POST localhost:8000/token username=admin password=secret
http GET localhost:8000/protected "Authorization:Bearer TOKEN"
```

### **Generadores Útiles**

- **Secret Key Generator**: Para generar SECRET_KEY seguras
- **Password Generator**: Para crear passwords de prueba
- **JWT Decoder**: Para verificar contenido de tokens

---

## 🔧 Configuración de Desarrollo

### **Variables de Entorno**

```bash
# Crear archivo .env
SECRET_KEY=your-super-secret-key-here-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### **Validación de Seguridad**

```bash
# Instalar herramientas de testing
pip install pytest-asyncio httpx

# Testing básico
pytest tests/test_auth.py -v

# Verificar hashing
python -c "from passlib.context import CryptContext; ctx = CryptContext(schemes=['bcrypt']); print(ctx.hash('test'))"
```

---

## 📖 Conceptos Clave para Estudio

### **Autenticación vs Autorización**

- **Autenticación**: ¿Quién eres? (login)
- **Autorización**: ¿Qué puedes hacer? (permisos)
- **Sesiones**: Estado del usuario autenticado

### **JWT Componentes**

- **Header**: Algoritmo y tipo de token
- **Payload**: Datos del usuario (claims)
- **Signature**: Verificación de integridad

### **Seguridad Básica**

- **Hash de passwords**: Nunca guardar passwords en texto plano
- **Secret keys**: Mantener secretas las claves de firma
- **Expiración**: Los tokens deben tener tiempo límite
- **HTTPS**: Siempre usar en producción

---

## 🚀 Comandos Rápidos

### **Instalación de Dependencias**

```bash
# Instalar librerías de autenticación
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# Actualizar requirements.txt
pip freeze > requirements.txt
```

### **Testing Manual Rápido**

```bash
# Iniciar servidor
uvicorn main:app --reload

# En otra terminal - Login
curl -X POST localhost:8000/token -d "username=admin&password=secret"

# Usar el token obtenido
curl -H "Authorization: Bearer TOKEN_AQUI" localhost:8000/users/me
```

### **Verificación de Setup**

```bash
# Verificar instalación de librerías
python -c "import jose; import passlib; print('✅ Auth libraries installed')"

# Test de hashing
python -c "from passlib.context import CryptContext; print('✅ Bcrypt working')"

# Verificar FastAPI security
python -c "from fastapi.security import HTTPBearer; print('✅ FastAPI security ready')"
```

---

## 📝 Checklist Final

### **Configuración Básica**

- [ ] `python-jose`, `passlib`, `python-multipart` instalados
- [ ] Archivo `auth.py` con funciones de hashing y JWT
- [ ] SECRET_KEY configurada
- [ ] Modelos de usuario listos

### **Funcionalidad Mínima**

- [ ] Hash de passwords funcionando
- [ ] Generación de tokens JWT
- [ ] Verificación de tokens
- [ ] Endpoint de login
- [ ] Protección básica de rutas

### **Testing Manual**

- [ ] Login exitoso retorna token
- [ ] Token válido permite acceso
- [ ] Token inválido rechaza acceso
- [ ] Password incorrecta rechaza login
- [ ] Endpoints protegidos funcionan

---

## 🎯 Para Continuar Aprendiendo

### **Temas Avanzados (Opcional)**

- Refresh tokens para sesiones largas
- Roles y permisos granulares
- OAuth2 con proveedores externos
- Rate limiting para seguridad
- Logging de eventos de autenticación

### **Recursos Adicionales**

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT Security Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
- [FastAPI Advanced Security](https://fastapi.tiangolo.com/advanced/security/)

---

## 🎉 ¡Éxito en la implementación de autenticación! 🔐✨
