app.controller('WishlistController', ['$scope','$http','$location', function($scope,$http,$location){
	if(localStorage.userID == null){
		$location.url("/")
	}

	config = {

			headers:{'Accept': "json",
			"Authorization":"Basic " +localStorage.token

			}
	}

	$http.get('/api/users/'+localStorage.userID+'/wishlist', config).then(function(response){
		
			if(response.data.message =="Success"){
				$scope.wishlist = response.data.data.items
				console.log($scope.wishlist)
			}else{
				console.log(response.data.message)
			}
			
	
	})

	$scope.addNew = function(){
		$location.url('/wishlist/new')
	}

	$scope.deleteItem = function(x){
		url = '/api/users/'+localStorage.userID+'/wishlist/'+$scope.wishlist[x].id
		config = {

			headers:{'Accept': "json",
			"Authorization":"Basic " +localStorage.token

			}
		}
		$http.delete(url, config).then(function(response){
			console.log(response.data.message)
			$location.url('/wishlist')
		})
	}

	$scope.share = function(){
		$location.url('/wishlist/share')
	}




}])