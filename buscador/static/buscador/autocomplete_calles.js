
var lista_calles;

// Recupera un array de nombres de calles
// y lo almacena en var lista_calles
$.ajax({
    type: 'GET',
    url: '/buscador/calles/',
    datatype: 'json',
    async: false,
    success: function (data) {
        lista_calles = data;
    }
})

// Autocomplete para campos calle1 y calle2
$(function () {
  $('#calle1').autocomplete({
    source: JSON.parse(lista_calles),
    minLength: 3,
    autoFocus: true,
  });
});

$(function () {
  $('#calle2').autocomplete({
    source: JSON.parse(lista_calles),
    minLength: 3,
    autoFocus: true,
  });
});

