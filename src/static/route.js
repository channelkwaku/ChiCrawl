var map;
var directionsService = new google.maps.DirectionsService();
var directionsDisplay = new google.maps.DirectionsRenderer();
var setDisplay = new google.maps.InfoWindow();

var startLocation = new google.maps.LatLng(startLat, startLon);

function initialize() {
    var mapOptions = {
        zoom: 13,
        center: startLocation,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    directionsDisplay.setMap(map);
    calcRoute();
}

function calcRoute() {
    var start = new google.maps.LatLng(41.788864, -87.604939);
    var end = new google.maps.LatLng(41.878876, -87.635915);
    var request = {
        origin: start,
        destination: end,
        travelMode: google.maps.TravelMode.DRIVING
    };
    directionsService.route(request, function(result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(result);
        }
    });
}

google.maps.event.addDomListener(window, 'load', initialize);
       
