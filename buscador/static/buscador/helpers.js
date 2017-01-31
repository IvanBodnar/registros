
$(function() {
  $('td').each(function() {
    if($(this).text() == 'Homicidio') {
        $(this).parent().css('background', '#ff5252')
    }
  })
})
