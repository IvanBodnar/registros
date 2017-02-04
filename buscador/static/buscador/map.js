var map = L.map('map').setView([-34.615715, -58.451204], 12);

// Levanta y parsea la var geojson de tabla_buscador.html,
// la cual tiene el geojson con los siniestros que vienen en
// el contexto.
var gj = JSON.parse(geojson);

// 'map.invalidateState()': 'Hack para que renderice bien el mapa base.
// shown.bs.tab es un evento del pugin tab de bootstrap,
// que se dispara despues de que la tab se muestra.
$("#mapa_tab").on('shown.bs.tab', function() {
    map.invalidateSize();
});


// Mapa de MapBox
$(function() {
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'ivangbodnar.p7n41boc',
    accessToken: 'pk.eyJ1IjoiaXZhbmdib2RuYXIiLCJhIjoiY2lnaXR0YzVvMDAwNXVha3JsZnFlZzBjbyJ9.X17WT4iMx_powofqtqKkDg'
}).addTo(map);
})

// Agregar el geojson como capa al mapa
L.geoJSON(gj).addTo(map);


// Mapa de OSM
//L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
//    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
//}).addTo(map);

//L.marker([51.5, -0.09]).addTo(map)
//    .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
//    .openPopup();