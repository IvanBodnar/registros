
var list = $('#calles').val();

$(function () {
  $('input').autocomplete({
    source: JSON.parse(list),
    minLength: 3,
    autoFocus: true,
  });
});