import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# --- 0. CSS para la Estética "Cyberpunk Tierno" ---
def inject_cyber_cuddle_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=VT323&family=Fira+Code&display=swap');
            
            /* Colores Neón Ciber-Tierno */
            :root {
                --color-dark-bg: #1A0033; /* Púrpura Oscuro */
                --color-neon-pink: #FF69B4; /* Rosa Brillante */
                --color-neon-blue: #00FFFF; /* Cian */
                --color-light-purple: #BB86FC; /* Lavanda Cyber */
                --color-text-light: #F0F8FF;
                --color-code: #03DAC6; /* Verde Tierno */
            }

            /* Fondo Principal: Oscuro con Grilla (simulación) */
            .stApp {
                background-color: var(--color-dark-bg);
                color: var(--color-text-light);
                font-family: 'Fira Code', monospace; 
            }
            
            /* Títulos - Fuente Glitch/Retro */
            h1, h2, h3, h4 {
                font-family: 'VT323', monospace;
                color: var(--color-neon-blue);
                text-shadow: 0 0 5px var(--color-neon-pink), 0 0 10px var(--color-neon-blue);
                letter-spacing: 3px;
                text-align: center;
            }

            /* Barra lateral (Estación de Control) */
            .css-1d3s3aw, .st-emotion-cache-1d3s3aw { 
                background-color: #330066; /* Un tono más claro que el fondo */
                border-right: 2px solid var(--color-neon-pink);
            }
            .stSidebar .stTextInput, .stSidebar .stNumberInput {
                border-radius: 8px;
                border: 1px solid var(--color-neon-blue);
                padding: 5px;
            }
            
            /* Botón Principal (Activación) */
            .stButton > button {
                background-color: var(--color-neon-pink);
                color: var(--color-dark-bg);
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                box-shadow: 0 0 15px var(--color-neon-pink), 0 0 5px var(--color-neon-blue);
                transition: all 0.2s;
                font-family: 'VT323', monospace;
                font-size: 1.2em;
            }
            .stButton > button:hover {
                background-color: #FFC1D8;
                transform: scale(1.02);
            }

            /* Contenedores de Alerta/Info (Hologramas) */
            .stAlert, .stInfo, .stSuccess, .stError {
                border-radius: 12px;
                padding: 15px;
                background-color: rgba(255, 105, 180, 0.1); /* Fondo transparente/suave */
                border: 1px solid var(--color-neon-pink);
                color: var(--color-text-light) !important;
            }
            
            /* Métricas de Datos (Indicadores de Vida) */
            [data-testid="stMetric"] {
                background-color: rgba(0, 255, 255, 0.1); /* Cian transparente */
                border: 2px solid var(--color-neon-blue);
                border-radius: 10px;
                padding: 10px;
                text-align: center;
            }
            [data-testid="stMetricLabel"] {
                color: var(--color-neon-pink); /* Etiquetas en rosa */
                font-family: 'VT323', monospace;
                font-size: 1.1em;
            }
            [data-testid="stMetricValue"] {
                color: var(--color-code); /* Valores en verde */
                font-weight: bold;
                font-size: 2em;
            }
        </style>
    """, unsafe_allow_html=True)

# Configuración de la página
st.set_page_config(
    page_title="Consola PetNet",
    page_icon="💖",
    layout="centered"
)
inject_cyber_cuddle_css() # Inyectar el CSS

# Variables de estado
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = None

def get_mqtt_message(broker, port, topic, client_id):
    """Función para obtener un mensaje MQTT (El Latido de Datos)"""
    message_received = {"received": False, "payload": None}
    
    def on_message(client, userdata, message):
        try:
            # Intentar decodificar como JSON
            payload = json.loads(message.payload.decode())
            message_received["payload"] = payload
            message_received["received"] = True
        except:
            # Si no es JSON, guardar como texto simple
            message_received["payload"] = message.payload.decode()
            message_received["received"] = True
    
    try:
        # Usamos un ID único para la conexión
        client = mqtt.Client(client_id=client_id) 
        client.on_message = on_message
        client.connect(broker, port, 60)
        client.subscribe(topic)
        client.loop_start()
        
        # Esperar máximo 5 segundos por el latido
        timeout = time.time() + 5
        while not message_received["received"] and time.time() < timeout:
            time.sleep(0.1)
        
        client.loop_stop()
        client.disconnect()
        
        return message_received["payload"]
        
    except Exception as e:
        return {"error": str(e)}

# Sidebar - Configuración (Estación de Control)
with st.sidebar:
    st.subheader('⚙️ Estación de Control PetNet')
    st.markdown("---")
    
    broker = st.text_input('Broker del Emisor', value='broker.mqttdashboard.com', 
                           help='Dirección del servidor MQTT (El cerebro de la red)')
    
    port = st.number_input('Puerto de Conexión', value=1883, min_value=1, max_value=65535,
                           help='Canal de transmisión (generalmente 1883)')
    
    topic = st.text_input('Tópico (ID de la Mascota)', value='Sensor/THP2',
                          help='Tópico MQTT que identifica a tu Ciber-Mascota')
    
    # Usar un ID de cliente único para evitar conflictos en el broker
    client_id = st.text_input('ID de Cuidador', value='petnet_client_' + str(time.time()),
                              help='Tu identificador único en la red PetNet')

# Título Principal
st.title('💖 Consola de Estabilización PetNet')

# Introducción y Holograma de Información
with st.expander('✨ Protocolo de Inicio', expanded=True):
    st.markdown("""
    ### ¡Bienvenido, Cuidador PetNet!
    
    Tu misión es monitorear los **Latidos de Datos** de tu Ciber-Mascota.
    
    1. **Configura** la conexión en la Estación de Control (panel lateral).
    2. **Activa** el Pulso para interceptar su estado vital.
    3. **Analiza** las métricas para asegurar su bienestar.
    """)
    st.markdown("---")
    st.markdown("**Brokers de Prueba:** `broker.mqttdashboard.com` | `test.mosquitto.org`")
    
st.divider()

# Botón para obtener datos
if st.button('📡 Activar Pulso de Datos (Obtener Latido)', use_container_width=True):
    if not broker or not topic:
        st.error("🚨 Error de Configuración: Ingresa el Broker y el Tópico de la mascota.")
    else:
        with st.spinner('Conectando a la red ciber-física y esperando el Latido...'):
            sensor_data = get_mqtt_message(broker, int(port), topic, client_id)
            st.session_state.sensor_data = sensor_data
            
        # Pequeño mensaje de confirmación antes de mostrar los datos
        if isinstance(sensor_data, dict) and 'error' in sensor_data:
             st.error(f"❌ La Mascota está Desconectada. Error: {sensor_data['error']}")
        elif sensor_data is None:
             st.warning("⚠️ Sin Latido Recibido. La Mascota está en modo Dormancia.")
        else:
             st.success('✅ Latido de Datos Estabilizado. ¡La Mascota está OK!')

# Mostrar resultados
if st.session_state.sensor_data:
    st.divider()
    st.subheader('📊 Lecturas Vitales')
    
    data = st.session_state.sensor_data
    
    # El mensaje de error ya se mostró arriba, aquí solo mostramos los datos si no hay error
    if isinstance(data, dict) and 'error' not in data and data is not None:
        
        # Mostrar cada campo en una métrica
        cols = st.columns(len(data))
        for i, (key, value) in enumerate(data.items()):
            with cols[i]:
                # Usar key.upper() y aplicar formato si es numérico
                label = key.upper().replace('_', ' ')
                display_value = f"{value:.2f}" if isinstance(value, (int, float)) else value
                st.metric(label=f"[{label}]", value=display_value)
                
        # Mostrar JSON completo (Registro Holográfico)
        with st.expander('💾 Registro Holográfico Completo (JSON)'):
            st.json(data)
    
    elif not isinstance(data, dict) and data is not None and 'error' not in data:
        # Si no es un diccionario (texto plano), mostrar como registro de código
        st.info("🧬 Tipo de Latido No Estándar (Datos en Bruto):")
        st.code(data)
