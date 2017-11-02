$(document).ready( function() {
  $("#loader_growth").on("click", function() {
      $("#container").load( "{% url 'dashboard:growth' %}" );
  });
});
