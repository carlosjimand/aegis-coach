# ☁️ Cloudflare Worker para Monitorización 24/7 (PC Apagado)

Este Worker gratuito de Cloudflare ejecuta un **Cron Trigger cada 4 horas en los servidores de Cloudflare**. Revisa automáticamente si has subido un nuevo entrenamiento desde tu Garmin a Intervals.icu, sin necesidad de que tu ordenador esté encendido.

---

## 🚀 Despliegue en 2 Pasos

1. **Instalar Wrangler (si no lo tienes):**
   ```bash
   npm install -g wrangler
   ```

2. **Hacer login y desplegar:**
   ```bash
   cd cloudflare
   npx wrangler login
   npx wrangler deploy
   ```

3. **(Opcional) Notificaciones en el Móvil vía Telegram:**
   Si quieres que te mande un mensaje a Telegram cuando detecte un entreno nuevo:
   ```bash
   npx wrangler secret put TELEGRAM_BOT_TOKEN
   npx wrangler secret put TELEGRAM_CHAT_ID
   ```
