app.controller('LoginController', ['$scope', '$http', '$location',function($scope, $http, $location){
	
	if(localStorage.userID != null){
		$location.url('/wishlist')
	}

	$scope.login = function(){
		data = {
			'email':$scope.email,
			'password':$scope.password
		}

		config = {

			headers:{'Content-Type': "application/json"}

		}

		$http.post('/api/users/login', data, config).then(function(response){
			console.log(response.data)
			if(response.data.status =="success"){
				localStorage.setItem("user", response.data.user.username)
				localStorage.setItem("userID", response.data.user.id)
				console.log(localStorage)
				$location.url('/wishlist')
			}
			else{
				console.log(response.data.status)
			}
			
		})
	}
}])