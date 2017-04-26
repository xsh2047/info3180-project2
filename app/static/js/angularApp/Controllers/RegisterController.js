app.controller('RegisterController', ['$scope', '$http','$location', function($scope, $http,$location){
		
		// $scope.fname = ""
		// $scope.lname = "LastName"
		// $scope.email = "Email"
		// $scope.password = "Password"
	if(localStorage.userID != null){
		$location.url("/wishlist")
	}

	$scope.register = function(){

		data = {

			'email':$scope.email,
			'fname':$scope.fname,
			'lname':$scope.lname,
			'password':$scope.password

		}

		config = {

				headers:{'Content-Type': "application/json"}

			}
		
		$http.post('/api/users/register', data, config).then(function(response){
			console.log(response.data)
		})


	}
}]);