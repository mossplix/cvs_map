
var tl;
var start;
var end;
function init()
{
	map = new GMap2(document.getElementById("map"));
	map.addControl(new GLargeMapControl());
    map.addControl(new GMapTypeControl());
    
    map.removeMapType(G_HYBRID_MAP);
    map.enableDoubleClickZoom();
    map.enableScrollWheelZoom();
    map.enableContinuousZoom();
    

	
    var bounds = new GLatLngBounds; 
	bounds.extend(new GLatLng(parseFloat(minLat), parseFloat(minLon))); 
	bounds.extend(new GLatLng(parseFloat(maxLat), parseFloat(maxLon)));
	map.setCenter(bounds.getCenter(), map.getBoundsZoomLevel(bounds)); 
	GEvent.addListener(map, 'tilesloaded', function(){
		start=tl.getBand(0).getMinDate();
		end=tl.getBand(0).getMaxDate();
        updateTimeline(start,end);
    });
	
//	// hijack popup window callback to open info window
//    Timeline.DurationEventPainter.prototype._showBubble = function(x, y, evt) {
//        evt.item.openInfoWindow();
//    }
//    
    
	 Timeline.DurationEventPainter.prototype._showBubble = function(x, y, evt) {
	        mapWindow(evt._obj);
	    }; 
	    
	    function mapWindow(markerObj) {
	        var win = new google.maps.InfoWindow({
	            content:  createInfoWindow(markerObj),
	            maxWidth: 400
	        });
	        var m = getMapMarker(markerObj.key);
	        win.open(map, m);
	    };
	    
	    function getMapIcon(e) {
	        switch (e.type.toLowerCase()) {
	            case 'hcii':
	                o = 'HCII.png'
	            break;
	            case 'hospital':
	                o = 'Hospital.png';
	            break;
	            case 'hiii':
	                o = 'HIII.png';
	            break;
	            case 'hiv':
	                o = 'HIV.png';
	            break;
	            default:
	            
	            break;
	        }
	        return o;
	    };
    
    var eventSource = new Timeline.DefaultEventSource();

	var bandInfos = [
Timeline.createBandInfo({
	 eventSource: eventSource,
	 date: new Date(),
    width:          "90%", 
    intervalUnit:   Timeline.DateTime.HOUR, 
    intervalPixels: 100,
    timeZone:       -6


                        }),
    
                        
                  
                        
                        
Timeline.createBandInfo({
	eventSource: eventSource,
    date: new Date(),
    width:          "10%", 
    intervalUnit:   Timeline.DateTime.MONTH, 
    intervalPixels: 200,
    showEventText: false,
    magnify:  5


                       })
	               ];
	 bandInfos[1].syncWith = 0;
	   bandInfos[1].highlight = true;

	tl = Timeline.create(document.getElementById("timeline"), bandInfos);
//	tl.loadJSON("/getmessages", function(json, url) {eventSource.loadJSON(json,
//			url);});


tl.getBand(0).addOnScrollListener( function(){
	mindate=tl.getBand(0).getMinDate();
	maxdate=tl.getBand(0).getMaxDate();
	 if (!wd.isSameDate(wd.timeline._currentMinDate, minDate)) {
         wd.timeline._currentMinDate = minDate;
         changed = true;
     }

     if (isSameDate(tl.end, maxdate)) {
         end = maxdate;
         changed = true;
     }
     if (changed) {
        eventSource.clear();
        updateTimeline(mindate, maxdate);
     }
	
});

function formatDate(dt) {
    var m = dt.getMonth() + 1;
    var d = dt.getDate();
    var y = dt.getFullYear();
    if (m < 10) { m = '0'+ m; }
    return [y, m, d].join('-');
}

function isSameDate (d1, d2) {
    return (!(d1>d2 || d2>d1));
}


function updateTimeline(start, end){
	var url="/getmessages"
	alert(start);
	if (start){
        url = url +'&start='+formatDate(start); 
    }
    if (end){
        url = url +'&end='+formatDate(end);
    }
    tl.loadJSON(url, function(json, url) { 
    	
    	
    	map.clearOverlays();
    	for (var x=0;x<json.events.length;x++) {
            var ev = json.events[x];
            var point=new GPoint(parseFloat(ev['lat']),parseFloat(ev['lng']));
            var marker = new GMarker(point);
            GEvent.addListener(marker, 'click',
            	    function() {
            	mapWindow(ev);
            	eventSource.loadJSON(json, url); 
            	
            	    });
    	
    	
    }
    	start=start;
    	end=end;
	
});
}
}
