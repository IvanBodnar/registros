
// Crear los mapas en distintas variables para despues agregarlas
// el el atributo layers de la definicion de L.map
// Mapa de OSM
var mapa_osm = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
                    maxZoom: 19
                });

// Mapa CARTO
var mapa_carto = L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
                    maxZoom: 19, attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy;' +
                    '<a href="https://carto.com/attribution"> CARTO</a>'
                  });

var map = L.map('map', {
    zoom: 12,
    center: [-34.615715, -58.451204],
    maxZoom: 19,
    layers: [mapa_osm, mapa_carto]
})//.setView([-34.615715, -58.451204], 12);


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


// Icono para los casos de homicidio usando
// la libreria de leaflet leaflet-color-markers: https://github.com/pointhi/leaflet-color-markers
var homicidio_icon = L.icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
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

// Crear objeto para contener las capas de mapa base
var base_maps = {
    'Mapa OSM': mapa_osm,
    'Mapa Carto': mapa_carto

}

// Crear objeto para contener las capas de overlay
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

// Agregar las capas de mapas base y overlays al control de capas
L.control.layers(base_maps, overlays).addTo(map);

// Agregar cada capa al mapa
for (var key in overlays) {
    overlays[key].addTo(map);
}