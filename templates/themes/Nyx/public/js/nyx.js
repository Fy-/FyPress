$(document).foundation();
jQuery(document).ready(function() {
  jQuery("time.timeago").timeago();

  var bodyHeight = $("body").height();
  var vwptHeight = $(window).height();
  console.log(bodyHeight, vwptHeight)
  if (vwptHeight > bodyHeight) {
    $("footer#footer").css("position","absolute").css("bottom",0);
  }
});