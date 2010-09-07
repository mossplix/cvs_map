/**
 * Helper Functions to use with google maps
 * 
 * @Author Mugisha Moses
 * 
 */

var points = {}; // hash to store layers with their description for each marker
var markers = {};
var infopanel;
var start_value;
var end_value;
var bbox;
var current_zoom;
var layers = {};
var urls = {};
var colors = [];
//make description global
var description = "";

var hf;

//	function to draw simple map
	function init() {
//initialise the map object
	map = new GMap2(document.getElementById("map"));
//bind the map zoomed litsener ..
	GEvent.addListener(map, 'zoomend',
			function() {

		addToMap();
	});
	//add map controls
	map.addControl(new GLargeMapControl());
	map.addControl(new GMapTypeControl());

	//make sure the zoom fits all the points
	var bounds = new GLatLngBounds; 
	bounds.extend(new GLatLng(parseFloat(minLat), parseFloat(minLon))); 
	bounds.extend(new GLatLng(parseFloat(maxLat), parseFloat(maxLon)));
	map.setCenter(bounds.getCenter(), map.getBoundsZoomLevel(bounds)); 
	var gicons = [];


}

//recenter to the point that has been clicked
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

//add graph to point
function addGraph(data,x,y,color,url,desc){
	//get map width and height in lat lon
	var d=map.getBounds().toSpan();
	var height=d.lng();
	var width=d.lat();
	var maxsize=0.9;
	var pointpair = [];
	var increment = (parseFloat(height)/10.0)/100;
	var start=new GPoint(parseFloat(x),parseFloat(y));
	var volume = parseInt((parseFloat(data)*100)/maxsize);

//store the graph in a hash for easy lookup of the description
	if(points[start])
	{

		points[start][String(color)]=desc;
	}
	else{

		points[start]={};
		points[start][String(color)]=desc;



	}

	pointpair.push(start);
	//draw the graph as an overlay
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

/*
 * remove all the overlay identified by its data url
 */
function removeOverlays(url){
	//make sure its not the base layer (match the begginning of base layer)
	if (url.match(hf.split("/")[1].split("?" )[0])==null)
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

/*
 * given a url, draw an overlay
 */
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

/*
 * add a marker given the lat,lon,title icon and the data url
 * 
 * the data urls is to identify markers belonging to a particular overlay
 */
function addmarker(x,y,title,icon,url) {
	if (icon.match("Media"))
	{

		var point = new GPoint(parseFloat(x),parseFloat(y));
		var mIcon  = new GIcon(G_DEFAULT_ICON, icon);

		mIcon.iconSize = new GSize(20,20);
		mIcon.shadowSize=new GSize(0,0);	
		mIcon.iconAnchor = new GPoint(10, 10);
		var marker = new GMarker(point,mIcon);
		map.addOverlay(marker);
		var desc=[];
		
		//check if marker has any url associated with it
		if (points[point])
		{
			//check to see if the marker has some description already and add to it
			$.each(colors, function(key,value){
				if(points[point][value]){

					desc.push(points[point][value]);
				}

			});
			

		}


		var ev=GEvent.addListener(marker, 'click',
				function() {
					//convert the disc list to a string and display in window
			marker.openInfoWindowHtml('<p class="help">'+title+'</h1>'+'<p>'+String(desc).replace(",","")+'</p>');
		});


	} 

}   

/*
 * add a marker that has no click lisener
 */
function addMarkerSimple(x,y,icon) {
	
	var point = new GPoint(parseFloat(x),parseFloat(y));
	var mIcon  = new GIcon(G_DEFAULT_ICON, icon);

	mIcon.iconSize = new GSize(57,32);
	mIcon.shadowSize=new GSize(0,0);
	mIcon.iconAnchor = new GPoint(58, 0);


	var marker = new GMarker(point,mIcon);
	map.addOverlay(marker); 
}   

/*
 * initialise the time slider
 */
$(function(){

    //initialise ui slider
	$('select#start, select#end').selectToUISlider({
		labels: 12,
		sliderOptions: { 
		change:function(e, ui) { 
		start_value=$('select#start option').eq(ui.values[0]).text();
		end_value=$('select#end option').eq(ui.values[1]).text();

		addToMap();

	}}
	});

	// fix color
	fixToolTipColor();
});

function fixToolTipColor(){
	// grab the bg color from the tooltip content - set top border of pointer to
	// same
	$('.ui-tooltip-pointer-down-inner').each(function(){
		var bWidth = $('.ui-tooltip-pointer-down-inner').css('borderTopWidth');
		var bColor = $(this).parents('.ui-slider-tooltip').css('backgroundColor')
		$(this).css('border-top', bWidth+' solid '+bColor);
	});	
}


/*
 * function to get color given a map_url each slug maps to an icon and color in
 * a map_types
 */

function getColor(url){

    var z = url.split("/")
    var slug = z[z.length - 1]
    try {
        var color = map_types[slug][1]
    } 
    catch (err) {
    
    }
    
    
    return color
    
}

function getType(url){

	var z=url.split("/")
	var slug=z[z.length-1]


	           return slug

}

/*
 * function to fetch content and map it given a url
 * 
 * 
 */

function fetchContent(url){
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function(data){
            $.each(data, function(key, value){
            
                if ((value['lon'] != "undefined") && (value['lat'] != "undefined") && (value['icon'] != undefined) && (value['lon'] != "None") && (value['lat'] != "None")) {
                    
                    if (url.match('health_facilities')) {
                        if (value['icon'].match('chart.apis.google.com')) {
                            addMarkerSimple(value['lon'], value['lat'], value['icon']);
                            
                        }
                        addmarker(value['lon'], value['lat'], value['title'], value['icon'], url, value['color']);
                        
                        
                    }
                    else {
                        addGraph(value['heat'], parseFloat(value['lon']), parseFloat(value['lat']), value['color'], url, value['desc']);
                        
                        
                    }
                }
                
                
            });
            
            
            
        }
        
    });
    
}

/*
 * function to add layers to the map. it checks all the layers for any wih a
 * checkbox clicked and
 * 
 * does a corresponding get request for the associated data from the server
 * 
 */ 

function addToMap(){

	map.clearOverlays();

	var url;
	var key;
	colors=[];
	layerContainer.find('input:checked').each(function (){
		key=$(this).attr('name');
		url=map_urls[key][1] + "?start="+start_value+"&end="+end_value+"&maxLat="+ maxLat + "&maxLon=" +maxLon +"&minLat="+ minLat + "&minLon=" + minLon+"&zoom="+zoom;
		if (key && map_urls[key][1] ){
			colors.push(getColor(map_urls[key][1]))
			maxLat= map.getBounds().getNorthEast().lat();
			maxLon=map.getBounds().getNorthEast().lng();
			minLat=map.getBounds().getSouthWest().lat();
			minLon=map.getBounds().getSouthWest().lng();
			zoom=map.getZoom();
			if (zoom>10)
			{	
				
				fetchContent('/health_facilities?start=undefined&end=undefined&maxLat=3.88875&maxLon=33.80176&type=1&minLat=2.1444&minLon=31.198&zoom='+zoom);
				fetchContent(hf);
			}
			addOverlays(hf);

			if (markers[url]==undefined || layers[url]==undefined)
			{
				fetchContent(url);

			}
			else{
				addOverlays(url);

			}

		}

	}

	);
}
