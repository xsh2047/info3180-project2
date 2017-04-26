app.controller('LogoutController', ['$location', function($location){
	localStorage.removeItem("userID")
	localStorage.removeItem("user")
	console.log("hereeee")
	$location.url('/')
}])