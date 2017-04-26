app.controller('HomeController', ['$scope', '$http','$location', function($scope, $http,$location){
	console.log(localStorage)
	if(localStorage.userID != null){
		$location.url("/wishlist")
	}

	
}]);