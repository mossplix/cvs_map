/**
 * Helper Functions to use with google maps 
 * @Author Mugisha Moses
 * 
 **/
var centerLatitude=2.80000;
var centerLongitude=32.333333333;
var startZoom=9;
var points = [];
var polylines = [];
var markers = [];
var titles = [];
var infopanel;
var start_value;
var end_value;
var bbox;
var current_zoom;
//function to draw simple map
function init() {
	
	

    map = new GMap2(document.getElementById("map"));
    map.addControl(new GLargeMapControl());
    var bounds = new GLatLngBounds; 
	bounds.extend(new GLatLng(parseFloat(minLat), parseFloat(minLon))); 
	bounds.extend(new GLatLng(parseFloat(maxLat), parseFloat(maxLon)));
	map.setCenter(bounds.getCenter(), map.getBoundsZoomLevel(bounds)); 
    //map.setCenter(new GLatLng(centerLatitude, centerLongitude), startZoom);
    var gicons = [];
   
    
    
}
window.onload = init;



function movemap(x,y) {
    if (marker)
    {
        map.removeOverlay(marker);
    }
    var point = new GPoint(parseFloat(x),parseFloat(y));
    map.recenterOrPanToLatLng(point);
    marker = new GMarker(point);
    map.addOverlay(marker);
}

function addGraph(data,x,y,color){
	//map.clearOverlays();
	var d=map.getBounds().toSpan();
	var height=d.lng();
	var width=d.lat();
	var maxsize=0.9;
	var pointpair = [];
	var increment = (parseFloat(height)/10.0)/100;
	
	var volume = parseInt((parseFloat(data)*100)/maxsize);
	pointpair.push(new GPoint(parseFloat(x),parseFloat(y)));
	pointpair.push(new GPoint(parseFloat(x+increment),parseFloat(y+increment)));
	var line = new GPolyline(pointpair,color,volume);
	
	//addmarker(x,y,"test","/Media/img/yellow.png","description");
	map.addOverlay(line);


	
	
	
	
	
}
function addmarker(x,y,title,icon,description) {
	
    var point = new GPoint(parseFloat(x),parseFloat(y));
    points.push(point);
    
	var mIcon  = new GIcon(G_DEFAULT_ICON, icon);
	mIcon.iconSize = new GSize(22,35);
	mIcon.shadowSize=new GSize(0,0);
    var marker = new GMarker(point,mIcon);
    map.addOverlay(marker);
    GEvent.addListener(marker, 'click',
    	    function() {
    	        marker.openInfoWindowHtml('<p class="help">'+title+'</h1>'+'<p>'+description+'</p>'+x+y);
    	    });

    markers.push(marker);
    
    titles.push(title);
    
   
   
}   




$(function(){
	
	
	//demo 3
	$('select#start, select#end').selectToUISlider({
		labels: 12,
		sliderOptions: { 
		change:function(e, ui) { 
		 start_value=$('select#start option').eq(ui.values[0]).text();
		 end_value=$('select#end option').eq(ui.values[1]).text();
		 
		addToMap();
		
	}}
	});
	
	//fix color 
	fixToolTipColor();
});
//purely for theme-switching demo... ignore this unless you're using a theme switcher
//quick function for tooltip color match
function fixToolTipColor(){
	//grab the bg color from the tooltip content - set top border of pointer to same
	$('.ui-tooltip-pointer-down-inner').each(function(){
		var bWidth = $('.ui-tooltip-pointer-down-inner').css('borderTopWidth');
		var bColor = $(this).parents('.ui-slider-tooltip').css('backgroundColor')
		$(this).css('border-top', bWidth+' solid '+bColor);
	});	
}






