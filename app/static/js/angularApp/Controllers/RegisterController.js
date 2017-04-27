app.controller('RegisterController', ['$scope', '$http','$location', function($scope, $http,$location){
		
		// $scope.fname = ""
		// $scope.lname = "LastName"
		// $scope.email = "Email"
		// $scope.password = "Password"
	if(localStorage.userID != null){
		$location.url("/wishlist")
	}

	$scope.register = function(){

		console.log($scope.profPic)
		data = {

			'email':$scope.email,
			'name':$scope.name,
			'password':$scope.password,
			'age':$scope.age,
			'gender':$scope.gender

		}

		config = {

				headers:{'Content-Type': "application/json"}

			}
		
		$http.post('/api/users/register', data, config).then(function(response){
			console.log(response.data)
		})


	}
}]);