app.controller('LogoutController', ['$location', function($location){

	localStorage.removeItem("name")
	localStorage.removeItem("userID")
	localStorage.removeItem("username")
	localStorage.removeItem("token")

	$location.url('/')
}])