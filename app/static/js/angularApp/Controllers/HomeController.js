app.controller('HomeController', ['$scope', '$http','$location', function($scope, $http,$location){
	if(localStorage.userID != null){
		$location.url("/wishlist")
	}

	
}]);