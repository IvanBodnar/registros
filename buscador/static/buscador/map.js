var map = L.map('map', {
    zoom: 12,
    center: [-34.615715, -58.451204],
    maxZoom: 19
})//.setView([-34.615715, -58.451204], 12);

//
// Levanta y parsea la var geojson de tabla_buscador.html,
// la cual tiene el geojson con los siniestros que vienen en
// el contexto.
var gj = JSON.parse(geojson);

// 'map.invalidateState()': Hack para que renderice bien el mapa base.
// shown.bs.tab es un evento del pugin tab de bootstrap,
// que se dispara despues de que la tab se muestra.
$("#mapa_tab").on('shown.bs.tab', function() {
    map.invalidateSize();
});

// Mapa de MapBox
//$(function() {
//L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
//    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
//    maxZoom: 19,
//    id: 'ivangbodnar.p7n41boc',
//    accessToken: 'pk.eyJ1IjoiaXZhbmdib2RuYXIiLCJhIjoiY2lnaXR0YzVvMDAwNXVha3JsZnFlZzBjbyJ9.X17WT4iMx_powofqtqKkDg'
//}).addTo(map);
//})

// Mapa de OSM
//L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
//    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
//    maxZoom: 19
//}).addTo(map);

// Mapa CARTO
L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
    maxZoom: 19, attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy;' +
    '<a href="https://carto.com/attribution"> CARTO</a>'
  }).addTo(map);

// Agrega un popup con algunas propiedades
// a cada feature de geojson
function agregar_popup(feature, layer) {
    if (feature.properties) {
        var ft = feature.properties;
        // Reemplazar null por 'Sin Datos'
        for (var key in ft) {
            if (!ft[key]) {
                ft[key] = 'Sin Datos';
            }
        }
        layer.bindPopup(ft.causa.bold().fontcolor('red').fontsize(3).toUpperCase() + '<br>'
                        + 'Lugar: ' + ft.direccion_normalizada + '<br>'
                        + 'Fecha: ' + moment(ft.fecha).format('DD-MM-YYYY') + '<br>'
                        + 'Participantes: ' + ft.participantes.replace(/\[|\]|\"/g, '') + '<br>');
    }
};


// Icono para los casos de homicidio
var homicidio_icon = L.icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41]
})


// Retorna un L.marker con el icono homicidio_icono
// para los casos de causa === 'homicidio'. Se aplica
// cuando se crean las capas de geojson (var geojson_layer = L.geoJson())
function agregar_color(feature, lat_long) {
    if (feature.properties.causa === 'homicidio') {
        return L.marker(lat_long, {icon: homicidio_icon});
        //Se puede cambiar el tipo de marker tambien:
        //return L.circleMarker(lat_long, {color: '#ff6347'});
    }
    else {
        return L.marker(lat_long);
    }
}


// Crea instancia de markerClusterGroup y la agrega al mapa
var mcg = L.markerClusterGroup();
mcg.addTo(map);
// Crear objeto para contener las capas
var overlays = {};

// Iterar sobre el json, crear las capas de L.geoJSON, agregarles
// los popups, agregar las capas a los subGroups y a overlays
for (var key in gj) {
    var año = JSON.parse(gj[key]);
    var geojson_layer = L.geoJSON(año, {
                                  pointToLayer: agregar_color,
                                  onEachFeature: agregar_popup
                                 })
    var subgroup = L.featureGroup.subGroup(mcg);
    geojson_layer.addTo(subgroup);
    overlays[key] = subgroup;
}

// Agregar las capas al control de capas
L.control.layers(null, overlays).addTo(map);

// Agregar cada capa al mapa
for (var key in overlays) {
    overlays[key].addTo(map);
}


// Mapa de OSM
//L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
//    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
//}).addTo(map);

//L.marker([51.5, -0.09]).addTo(map)
//    .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
//    .openPopup();