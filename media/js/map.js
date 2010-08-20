/**
 * Helper Functions to use with google maps 
 * @Author Mugisha Moses
 * 
 **/
var centerLatitude=2.80000;
var centerLongitude=32.333333333;
var startZoom=9;
var points = {};
var polylines = [];
var markers= {};
var infopanel;
var start_value;
var end_value;
var bbox;
var current_zoom;
var layers={}; 
var urls={};
var colors=[];
//make description global
var description="";
var hf="/health_facilities?start=undefined&end=undefined&maxLat=3.88875&maxLon=33.80176&minLat=2.1444&minLon=31.198&zoom=8"

//function to draw simple map
function init() {
	
	map = new GMap2(document.getElementById("map"));
	GEvent.addListener(map, 'zoomend',
    	    function() {
    	
    	addToMap();
    	    });
	 map.addControl(new GLargeMapControl());
     map.addControl(new GMapTypeControl());

	
    var bounds = new GLatLngBounds; 
	bounds.extend(new GLatLng(parseFloat(minLat), parseFloat(minLon))); 
	bounds.extend(new GLatLng(parseFloat(maxLat), parseFloat(maxLon)));
	map.setCenter(bounds.getCenter(), map.getBoundsZoomLevel(bounds)); 
    var gicons = [];
    
    
}
//window.onload = init;
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

function addGraph(data,x,y,color,url,desc){
	//map.clearOverlays();
	var d=map.getBounds().toSpan();
	var height=d.lng();
	var width=d.lat();
	var maxsize=0.9;
	var pointpair = [];
	var increment = (parseFloat(height)/10.0)/100;
	var start=new GPoint(parseFloat(x),parseFloat(y));
	var volume = parseInt((parseFloat(data)*100)/maxsize);
	
	if(points[start])
	{
	
	points[start][String(color)]=desc;
	}
	else{
		
		points[start]={};
		points[start][String(color)]=desc;
		
		
		
	}
		
	pointpair.push(start);
	
	pointpair.push(new GPoint(parseFloat(x+increment),parseFloat(y+increment)));
	var line = new GPolyline(pointpair,color,volume);
	
	if(layers[url])
    {
    layers[url].push(line);
    }
    else{
    	layers[url]=[]
    	layers[url].push(line);
    	  	
    }
	
	
	map.addOverlay(line);
}
function removeOverlays(url){
	if (url.match("health_facilities")==null)
	{
	m_list=markers[url];
	l_list=layers[url];
	if (m_list != undefined)
	{
	$.each(m_list, function(key,value){map.removeOverlay(value);});
	}
	
	if (l_list != undefined)
	{
	
	$.each(l_list, function(key,value){map.removeOverlay(value);});
	}
	
	}
	
}

function addOverlays(url){
	
	m_list=markers[url];
	l_list=layers[url];
	if (m_list != undefined)
	{
	$.each(m_list, function(key,value){map.addOverlay(value);});
	}
	if (l_list != undefined)
	{
	$.each(l_list, function(key,value){map.addOverlay(value);});
	}	
}


function addmarker(x,y,title,icon,url) {
	if (icon.match("Media"))
	{
	
    var point = new GPoint(parseFloat(x),parseFloat(y));
	var mIcon  = new GIcon(G_DEFAULT_ICON, icon);
	
	mIcon.iconSize = new GSize(20,20);
	mIcon.shadowSize=new GSize(0,0);	
	mIcon.iconAnchor = new GPoint(0, 0);
    var marker = new GMarker(point,mIcon);
    map.addOverlay(marker);
    var desc=[];
    if (points[point])
    {
    	
    	$.each(colors, function(key,value){
    		desc.push(points[point][value]);	
    	
    	});
    	
    	
    }
    
    
    var ev=GEvent.addListener(marker, 'click',
    	    function() {
    	        marker.openInfoWindowHtml('<p class="help">'+title+'</h1>'+'<p>'+String(desc).replace(",","")+'</p>');
    	    });
    
   
	} 
      
}   

function addMarkerSimple(x,y,icon) {
    var point = new GPoint(parseFloat(x),parseFloat(y));
	var mIcon  = new GIcon(G_DEFAULT_ICON, icon);
	
	mIcon.iconSize = new GSize(50,32);
	mIcon.shadowSize=new GSize(0,0);
	mIcon.iconAnchor = new GPoint(51, 0);

	
    var marker = new GMarker(point,mIcon);
    map.addOverlay(marker); 
}   

$(function(){
	
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
