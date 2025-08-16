$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$(document).ready(function()
{
    // increase cart item by 1
    $('.plus-cart').click(function()
    {
        // .toString()
        var id = $(this).attr("pid").toString();
        console.log(id);
        console.log("above");
        // creating a unique id for updating product in the html file
        var text1 = "quantity"
        var quantity = text1.concat(id);
        console.log(id);
        $.ajax({
            type:'GET',
            url:'/cart_quantity',
            data:{
                prod_id: id,
                cart_action:1

            },
            success:function(data)
            {
                document.getElementById(quantity).innerText = data.quantity
                document.getElementById('amount').innerText = data.amount
                document.getElementById('total').innerText = data.total
            }
        })
    })

    // decrease cart item by 1
    $('.minus-cart').click(function(){
        var id = $(this).attr("pid").toString();

        // creating a unique id for updating product in the html file
        var text1 = "quantity"
        var quantity = text1.concat(id);
        $.ajax({
            type:'GET',
            url:'/cart_quantity',
            data:{
                prod_id : id,
                cart_action:2 

            },
            success:function(data)
            {
                document.getElementById(quantity).innerText = data.quantity
                document.getElementById('amount').innerText = data.amount
                document.getElementById('total').innerText = data.total
            }
        })
    })

    // remove item from cart
    $('.remove-cart').click(function(){
        var id = $(this).attr("pid").toString();

        // creating a unique id for updating product in the html file
        var text1 = "remove"
        var quantity = text1.concat(id);
        $.ajax({
            type:'GET',
            url:'/cart_quantity',
            data:{
                prod_id: id,
                cart_action:3

            },
            success:function(data)
            {
                document.getElementById(quantity).remove()
                document.getElementById('amount').innerText = data.amount
                document.getElementById('total').innerText = data.total
            }
        })
    }) 
    
    
})
