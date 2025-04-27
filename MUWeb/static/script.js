$(document).ready(function () {
    // Function to load the most liked items dynamically
    function loadPopularItems() {
    	let productsContainer = $("#popular-items");
    	productsContainer.empty();

    	$.getJSON("/api/popular-items", function (data) {
        	data.forEach(item => {
            	    let productCard = `
                	<div class="col-md-4 mb-4">
                    	    <a href="/view/${item.id}" class="card-link text-decoration-none">
                        	<div class="card item-card" data-id="${item.id}">
                            	    <img src="${item.image}" class="card-img-top img-fluid" alt="${item.title}">
                            	    <div class="card-body text-center">
                                	<h5 class="card-title">${item.title}</h5>
                                	<a href="/view/${item.id}" class="btn btn-primary">View Details</a>
                            	    </div>
                        	</div>
                    	    </a>
                	</div>`;
            	    productsContainer.append(productCard);
        	});
    	});
    }


    // Load popular items on page load
    loadPopularItems();

    // Search functionality
    $("#search-form").on("submit", function (e) {
        e.preventDefault();
        let query = $("#search").val().trim();
        if (query === "") {
            $("#search").val("").focus();
            return;
        }
        window.location.href = `/search?q=${encodeURIComponent(query)}`;
    });

    // Like button functionality
    $(document).on("click", ".like-btn", function (e) {
        e.stopPropagation(); // Prevent triggering card click event
        let itemId = $(this).data("id");
        let likesSpan = $(`#likes-${itemId}`);

        $.post(`/like/${itemId}`, function (response) {
            if (response.success) {
                likesSpan.text(response.likes);
            }
        });
    });

    // Viewing items - make the whole card clickable
    $(document).on("click", ".item-card", function () {
        let itemId = $(this).data("id");
        window.location.href = `/view/${itemId}`;
    });

    // Keep "View Details" button functionality
    $(document).on("click", ".view-btn", function (e) {
        e.stopPropagation(); // Prevents event bubbling to the card
        let itemId = $(this).data("id");
        window.location.href = `/view/${itemId}`;
    });
});
