
var lista_calles;

// Retrieves array of street names
// and stores it in var lista_calles
$.ajax({
    type: 'GET',
    url: '/buscador/calles/',
    datatype: 'json',
    async: false,
    success: function (data) {
        lista_calles = data;
    }
})

// Autocomplete for calle1 and calle2 fields
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

