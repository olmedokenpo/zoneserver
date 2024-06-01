 
// Iniciar el mapa
var map = L.map('map').setView([40.49820, -3.34714], 14);

// Añadir una capa de tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Función para cargar áreas desde el servidor
function loadAreas() {
    console.log("Cargando áreas desde el servidor...");
    fetch('http://localhost:5002/areas')  // Ajusta la URL según sea necesario
        .then(response => response.json())
        .then(data => {
            console.log(data)
            L.geoJSON(data).addTo(map);
        })
        .catch(error => console.error('Error cargando las áreas:', error));
}

// Llamar a la función para cargar áreas
loadAreas();

// Función para manejar el clic en el mapa
function onMapClick(e) {
    console.log("Clic en el mapa en las coordenadas:", e.latlng);
    // Mostrar un marcador en el mapa en el lugar del clic
    L.marker(e.latlng).addTo(map);
    // Enviar las coordenadas al servidor
    fetch('http://localhost:5002/clic', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            latlng: e.latlng
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta del servidor:', data);
        L.geoJSON(data).addTo(map);
    })
    .catch(error => console.error('Error al enviar las coordenadas al servidor:', error));
}

// Agregar evento de clic al mapa
map.on('click', onMapClick);


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 